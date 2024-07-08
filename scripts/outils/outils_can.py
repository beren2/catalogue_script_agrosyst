"""
	Regroupe les fonctions permettant de générer les outils utiles lors de la génération du magasin "CAN".
"""
import pandas as pd

def get_intervention_realise_especes_concernes_outils_can(
        donnees
):
    """
        Calcule un dataframe qui comprend les infos sur les espèces concernées par les interventions 
        dans le format attendu par la CAN 
    """
    df_composant_culture_concerne_intervention_realise = donnees['composant_culture_concerne_intervention_realise']
    df_espece = donnees['espece']
    df_variete = donnees['variete']
    df_composant_culture = donnees['composant_culture']

    # Ajout des informations "espèces / variétés" au composant de culture
    left = df_composant_culture
    right = df_espece[[
        'id', 'libelle_espece_botanique', 'libelle_qualifiant_aee',
        'libelle_type_saisonnier_aee', 'libelle_destination_aee'
    ]].rename(columns={'id' : 'espece_id'})
    df_composant_culture_extanded = pd.merge(left, right, on='espece_id', how='left')

    left = df_composant_culture_extanded
    right = df_variete[[
        'id', 'denomination'
    ]].rename(columns={'id' : 'variete_id'})
    df_composant_culture_extanded = pd.merge(left, right, on='variete_id', how='left')

    # Ajout des informations dans le dataframe principal 
    left = df_composant_culture_concerne_intervention_realise[
        ['id', 'composant_culture_id', 'intervention_realise_id']
    ]
    right = df_composant_culture_extanded.rename(columns={'id' : 'composant_culture_id'})
    df_studied = pd.merge(left, right, on='composant_culture_id', how='left')

    df_studied = df_studied.fillna('')
    df_studied['description'] = df_studied[[
        'libelle_espece_botanique', 'libelle_qualifiant_aee', 
        'libelle_type_saisonnier_aee', 'libelle_destination_aee', 
    ]].agg(' '.join, axis=1).str.split().str.join(' ')

    df_studied.loc[
        df_studied['denomination'] !=  '', 'denomination'
    ] = ' - '+ df_studied.loc[df_studied['denomination'] !=  '']['denomination']

    df_studied['espece_de_l_intervention'] = (df_studied['description'] +  df_studied['denomination']).str.split().str.join(' ')
    res_especes_concernees = df_studied.groupby('intervention_realise_id')['espece_de_l_intervention'].agg(' ; '.join)
    return res_especes_concernees

def map_boolean(values, sep='; '):
    """ permet de transformer les booléen en string """
    mapping = {'f': 'non', 't': 'oui'}
    return ', '.join(mapping[val] for val in values)
 
def convert_to_int(x):
    """ permet de convertir une colonne en int"""
    try:
        # Convert to float first, then to int
        return str(int(float(x)))
    except (ValueError, TypeError):
        return x

def get_intervention_realise_action_outils_can(
        donnees
):
    """
        TODO
    """
    df_action_realise = donnees['action_realise']
    df_intervention_realise = donnees['intervention_realise']

    left =  df_action_realise
    right = df_intervention_realise[['id', 'freq_spatiale', 'nombre_de_passage', 'psci_intervention']].rename(columns={'id' : 'intervention_realise_id'})
    df_action_realise_extanded = pd.merge(left, right, on='intervention_realise_id', how='left')

    # Pour les applications de produits phytosanitaires :
    df_action_produit_phyto = df_action_realise_extanded.loc[df_action_realise_extanded['type'] == 'APPLICATION_DE_PRODUITS_PHYTOSANITAIRES']
    df_action_produit_phyto.loc[: , 'proportion_surface_traitee_phyto'] = df_action_produit_phyto['proportion_surface_traitee']
    df_action_produit_phyto.loc[: ,'psci_phyto'] = df_action_produit_phyto['proportion_surface_traitee'] * \
          df_action_produit_phyto['freq_spatiale'] * df_action_produit_phyto['nombre_de_passage']

    # Pour la lutte biologique :
    df_action_lutte_bio = df_action_realise_extanded.loc[df_action_realise_extanded['type'] == 'LUTTE_BIOLOGIQUE']
    df_action_lutte_bio.loc[: ,'proportion_surface_traitee_lutte_bio'] = df_action_lutte_bio['proportion_surface_traitee']
    df_action_lutte_bio.loc[: ,'psci_lutte_bio'] = df_action_lutte_bio['proportion_surface_traitee'] * \
          df_action_lutte_bio['freq_spatiale'] * df_action_lutte_bio['nombre_de_passage']

    # Pour l'irrigation :
    df_action_irrigation = df_action_realise_extanded.loc[df_action_realise_extanded['type'] == 'IRRIGATION']
    df_action_irrigation.loc[: ,'quantite_eau_mm'] = df_action_irrigation['eau_qte_moy_mm'] 

    # Pour les autres :
    df_action_autres = df_action_realise_extanded.loc[
        (df_action_realise_extanded['type'] != 'APPLICATION_DE_PRODUITS_PHYTOSANITAIRES') &
        (df_action_realise_extanded['type'] != 'LUTTE_BIOLOGIQUE') &
        (df_action_realise_extanded['type'] != 'IRRIGATION')
    ].groupby(['intervention_realise_id']).agg({
        'label' : ' ; '.join
    }).reset_index()
    
    keeped_column_produit_phyto = ['proportion_surface_traitee_phyto', 'psci_phyto']
    keeped_column_lutte_bio = ['proportion_surface_traitee_lutte_bio', 'psci_lutte_bio']
    keeped_column_irrigation = ['quantite_eau_mm']
    merge = pd.merge(df_action_produit_phyto[keeped_column_produit_phyto+['intervention_realise_id', 'label']], 
                     df_action_lutte_bio[keeped_column_lutte_bio+['intervention_realise_id', 'label']], 
                     on='intervention_realise_id', how='outer', suffixes = ('', '_lutte_bio'))

    merge = pd.merge(merge.set_index('intervention_realise_id'), 
                     df_action_autres[['intervention_realise_id', 'label']], 
                     left_index=True, suffixes = ('', '_autre'),
                     right_on='intervention_realise_id', how='outer').drop_duplicates(subset=['intervention_realise_id'])
    
    merge = pd.merge(merge.set_index('intervention_realise_id'), 
                     df_action_irrigation[keeped_column_irrigation+['intervention_realise_id', 'label']], 
                     left_index=True, suffixes = ('', '_irrigation'),
                     right_on='intervention_realise_id', how='outer').drop_duplicates(subset=['intervention_realise_id'])

    merge['interventions_actions'] = merge[['label', 'label_lutte_bio', 'label_autre', 'label_irrigation']].apply(
        lambda x: x.str.cat(sep=' ; '), axis=1
    )

    merge[
        ['proportion_surface_traitee_phyto', 'psci_phyto', 'proportion_surface_traitee_lutte_bio', 'psci_lutte_bio', 'quantite_eau_mm']
    ] = merge[
        ['proportion_surface_traitee_phyto', 'psci_phyto', 'proportion_surface_traitee_lutte_bio', 'psci_lutte_bio', 'quantite_eau_mm']
    ].applymap(convert_to_int)


    # À ce stade, on a encore des dupplication d'intervention_id : on doit grouper par intervention_id en joignant le nom des actions, mais en gardant
    # à chaque fois la valeur non nulle pour les colonnes
    intervention_actions_indicateurs = merge[[
        'interventions_actions', 'proportion_surface_traitee_phyto', 'psci_phyto', 
        'proportion_surface_traitee_lutte_bio', 'psci_lutte_bio', 'quantite_eau_mm' 
    ]]

    return intervention_actions_indicateurs

def get_intervention_realise_semence_outils_can(
        donnees
    ):
    """
        TODO
    """
    df_semence = donnees['semence']
    df_composant_culture = donnees['composant_culture']
    df_espece = donnees['espece']
    df_utilisation_intrant_realise = donnees['utilisation_intrant_realise']

    # OBTENTION DES INFORMATIONS POUR LES INTERVENTIONS DE TYPE SEMENCES.
    left = df_semence.rename(columns={'espece_id':'composant_culture_id'}) # attention, on est obligé de corriger car il y a une erreur dans le nom de la colonne sur Datagrosyst.
    right = df_composant_culture[['id', 'espece_id', 'variete_id']].rename(columns={'id' : 'composant_culture_id'})
    df_semence_extanded = pd.merge(left, right, on='composant_culture_id', how='left')

    left = df_semence_extanded
    right = df_espece[['id', 'libelle_espece_botanique', 'libelle_qualifiant_aee', 'libelle_type_saisonnier_aee', 'libelle_destination_aee']].rename(columns={'id' : 'espece_id'})
    df_semence_extanded = pd.merge(left, right, on='espece_id', how='left')

    df_semence_extanded = df_semence_extanded.fillna('')

    df_semence_extanded['description'] = df_semence_extanded[[
        'libelle_espece_botanique', 'libelle_qualifiant_aee', 
        'libelle_type_saisonnier_aee', 'libelle_destination_aee', 
    ]].agg(' '.join, axis=1).str.split().str.join(' ')

    # ajout des informations des semences sur les utilsiation d'intrants
    left = df_utilisation_intrant_realise[['intervention_realise_id', 'intrant_id', 'dose', 'unite', 'semence_id']]
    right = df_semence_extanded.rename(columns={'id' : 'semence_id'})
    df_utilisation_intrant_realise_extanded = pd.merge(left, right, on='semence_id', how='inner')

    df_utilisation_intrant_realise_extanded['dose'] = df_utilisation_intrant_realise_extanded['dose'].astype('str')

    # on groupe par intervention
    df_intervention_semence = df_utilisation_intrant_realise_extanded.fillna('').groupby([
        'intervention_realise_id'
    ]).agg({
        'description' :  ' ; '.join,
        'type_semence' :  ', '.join,
        'dose' : ' , '.join,
        'unite' : ', '.join, 
        'inoculation_biologique' : lambda x: map_boolean(x, sep=', '),
        'traitement_chimique' : lambda x: map_boolean(x, sep=', ')
    })

    return df_intervention_semence.rename(columns={
        'description' : 'especes_semees', 
        'dose' : 'densite_semis', 
        'unite' : 'unite_semis', 
        'traitement_chimique' : 'traitement_chimique_semis',
        'inoculation_biologique' : 'inoculation_biologique_semis'
    })



def get_intervention_realise_outils_can_context(
    donnees
):
    """
        Permet d'obtenir un dataframe intermédiaire des interventions pour la CAN
    """
    df_intervention_realise = donnees['intervention_realise']

    # ajout des informations sur les différents indicateurs
    left = df_intervention_realise
    right = get_intervention_realise_action_outils_can(donnees).reset_index().rename(columns={'intervention_realise_id': 'id'} )
    merge = pd.merge(left, right, on='id', how='left')
    
    # ajout des informations sur la table semis
    left = merge 
    right = get_intervention_realise_semence_outils_can(donnees).reset_index().rename(columns={'intervention_realise_id': 'id'})
    merge = pd.merge(left, right, on='id', how='left')

    columns = ['id', 'interventions_actions', 'especes_semees', 'densite_semis', 'unite_semis', 'traitement_chimique_semis', 
               'inoculation_biologique_semis', 'type_semence', 'proportion_surface_traitee_phyto', 'psci_phyto', 
               'proportion_surface_traitee_lutte_bio', 'psci_lutte_bio', 'quantite_eau_mm']
    # ajout des informations sur les espèces concernées
    return merge[columns]

def get_intervention_realise_combinaison_outils_can(
    donnees
):
    """
        Permet d'obtenir le dataframe avec les informations sur les combinaisons d'outils
    """
    df_intervention_realise = donnees['intervention_realise']
    df_combinaison_outil = donnees['combinaison_outil'].set_index('id')
    df_materiel = donnees['materiel'].set_index('id')
    df_combinaison_outil_materiel = donnees['combinaison_outil_materiel']

    # Ajout des informations sur le tracteur à la combinaison d'outils 
    left = df_combinaison_outil[['nom', 'tracteur_materiel_id']]
    right = df_materiel[['nom', 'type_materiel']].rename(
        columns={'nom' : 'nom_tracteur', 'type_materiel' : 'tracteur_ou_automoteur'}
    )
    df_combinaison_outil_extanded = pd.merge(left, right, left_on='tracteur_materiel_id', right_index=True, how='left')

    # Ajout des inforations sur le materiel à la combinaison d'outils
    left = df_combinaison_outil_materiel
    right = df_materiel[['nom', 'type_materiel', 'materiel_caracteristique1']].rename(
        columns={'nom' : 'combinaison_outils_nom', 'type_materiel' : 'outils'}
    )
    df_combinaison_outil_materiel= pd.merge(left, right, left_on='materiel_id', right_index=True, how='left')

    # On considère que si plusieurs matériels ont les mêmes caractéristiques (materiel_caracteristique1)
    # Alors il n'y a pas besoin de remonter plusieurs fois l'information dans l'agrégation 
    # (Correction par rapport aux exports en masse historiques)
    df_combinaison_outil_materiel = df_combinaison_outil_materiel.drop_duplicates(
        subset=['combinaison_outil_id', 'materiel_caracteristique1']
    )

    # On rassemble tous les materiels pour n'avoir qu'une description par combinaison d'outils
    df_combinaison_outil_materiel['outils'] = df_combinaison_outil_materiel['outils'].fillna('')
    df_combinaison_outil_materiel_grouped = df_combinaison_outil_materiel.groupby('combinaison_outil_id').agg({
        'outils' : ' ; '.join, # delete NaN
    })

    # On mets toutes les informations dans le même dataframe
    left = df_combinaison_outil_extanded
    right = df_combinaison_outil_materiel_grouped
    df_combinaison_outil_extanded = pd.merge(left, right, left_index=True, right_index=True, how='left')

    # On agrège les informations au dataframe des interventions
    left = df_intervention_realise[['id', 'combinaison_outil_id']]
    right = df_combinaison_outil_extanded.rename(columns={'nom' : 'combinaison_outils_nom'})[
        ['combinaison_outils_nom', 'tracteur_ou_automoteur', 'outils']
    ]

    merge = pd.merge(left, right, left_on='combinaison_outil_id', right_index=True, how='left')

    return merge

def get_intervention_realise_outils_can(
    donnees
):
    """
        Permet d'obtenir le dataframe final des interventions pour la CAN
    """
    left = get_intervention_realise_outils_can_context(donnees).rename(
        columns={'id' : 'intervention_realise_id'}
    )
    right = get_intervention_realise_especes_concernes_outils_can(donnees).reset_index().rename(
        columns={'id' : 'intervention_realise_id'}
    )
    merge = pd.merge(left, right, on='intervention_realise_id', how='left')

    left = merge
    right = get_intervention_realise_combinaison_outils_can(donnees).rename(
        columns={'id' : 'intervention_realise_id'}
    )

    merge = pd.merge(left, right, on='intervention_realise_id', how='left')

    return merge