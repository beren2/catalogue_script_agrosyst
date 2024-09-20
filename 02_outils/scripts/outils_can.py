"""
	Regroupe les fonctions permettant de générer les outils utiles lors de la génération du magasin "CAN".
"""
import pandas as pd
import numpy as np


# FONCTIONS GÉNÉRALES 

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

def get_composant_culture_outils_can(donnees, info_variete=True):
    """ permet d'obtenir toutes les informations sur le composant culture, dans le format attendu par la CAN"""
    # Ajout des informations sur le composant de culture
    df_composant_culture = donnees['composant_culture'].set_index('id')
    df_espece = donnees['espece'].set_index('id')
    df_variete = donnees['variete'].set_index('id')

    left = df_composant_culture
    right = df_espece[
        ['libelle_espece_botanique', 'libelle_qualifiant_aee', 
         'libelle_type_saisonnier_aee', 'libelle_destination_aee']
    ]
    df_composant_culture_extanded = pd.merge(left, right, left_on='espece_id', right_index=True, how='left')

    left = df_composant_culture_extanded
    right = df_variete[
        ['denomination']
    ]
    df_composant_culture_extanded = pd.merge(left, right, left_on='variete_id', right_index=True, how='left')

    # On fill les NaN avec ''
    df_composant_culture_extanded= df_composant_culture_extanded.fillna('')

    # On créé la chaîne correspondant à la description complète du composant de culture
    df_composant_culture_extanded['esp_var'] = df_composant_culture_extanded[[
        'libelle_espece_botanique', 
        'libelle_qualifiant_aee', 
        'libelle_type_saisonnier_aee', 
        'libelle_destination_aee'
    ]].agg(' '.join, axis=1).str.split().str.join(' ')

    if(info_variete):
        # On ajoute l'information de la variété
        df_composant_culture_extanded.loc[
            df_composant_culture_extanded['denomination'] !=  '', 'denomination'
        ] = ' - '+ df_composant_culture_extanded.loc[df_composant_culture_extanded['denomination'] !=  '']['denomination']
        df_composant_culture_extanded['denomination'] = df_composant_culture_extanded['denomination'].fillna('')
        df_composant_culture_extanded['esp_var'] = df_composant_culture_extanded['esp_var'] + \
            df_composant_culture_extanded['denomination']

    # On supprime les dupplications pour ne pas avoir plusieurs fois la même information
    df_composant_culture_extanded = df_composant_culture_extanded[
        ['culture_id', 'esp_var']
    ].drop_duplicates(subset=['esp_var', 'culture_id'], keep='first')

    return df_composant_culture_extanded

# FONCTIONS POUR LES FILTRES (ACTIF + DEPHY)
def dispositif_filtres_outils_can(
        donnees
):
    """
        permet d'obtenir tous les domaine_id qui doivent être conservés selon la CAN :
        c'est à dire ceux qui sont actifs, ceux qui ne contiennent que des dispositifs et des sdc actifs,
        ceux qui sont post 2020 et ceux qui n'appartiennent pas à  'NOT_DEPHY'.
    """

    # dans l'entrepôt, les filtrations sur les actifs sont déjà réalisés
    df_dispositif = donnees['dispositif'].set_index('id')
    df_domaine = donnees['domaine'].set_index('id')

    left = df_dispositif
    right = df_domaine[['campagne']].rename(columns={'campagne' : 'domaine_campagne'})
    df_dispositif = pd.merge(left, right, left_on='domaine_id', right_index=True)

    df_dispositif = df_dispositif.loc[
        (df_dispositif['domaine_campagne'] > 1999) & (df_dispositif['domaine_campagne'] < 2026) & 
        (df_dispositif['type'] != 'NOT_DEPHY')
    ]

    return  df_dispositif.reset_index()[['id']]

def domaine_filtres_outils_can(
        donnees
):
    """
        permet d'obtenir tous les domaine_id qui doivent être conservés selon la CAN :
        c'est à dire ceux qui sont actifs, ceux qui ne contiennent que des dispositifs et des sdc actifs,
        ceux qui sont post 2020 et ceux qui n'appartiennent pas à  'NOT_DEPHY'.
    """

    # dans l'entrepôt, les filtrations sur les actifs sont déjà réalisés
    df_dispositif = donnees['dispositif'].set_index('id')
    df_domaine = donnees['domaine'].set_index('id')

    left = df_dispositif
    right = df_domaine[['campagne']].rename(columns={'campagne' : 'domaine_campagne'})
    df_dispositif = pd.merge(left, right, left_on='domaine_id', right_index=True)

    df_dispositif = df_dispositif.loc[
        (df_dispositif['domaine_campagne'] > 1999) & (df_dispositif['domaine_campagne'] < 2026) & 
        (df_dispositif['type'] != 'NOT_DEPHY')
    ]

    df_domaine = df_domaine.loc[
        df_domaine.index.isin(list(df_dispositif['domaine_id']))
    ]

    return  df_domaine.reset_index()[['id']]


# FONCTIONS POUR LES INTERVENTIONS EN RÉALISÉS
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

    # À ce stade, on a encore des dupplication d'intervention_id : on doit grouper par intervention_id en joignant le nom des actions, mais en gardant
    # à chaque fois la valeur non nulle pour les colonnes
    intervention_actions_indicateurs = merge[[
        'intervention_realise_id', 'interventions_actions', 'proportion_surface_traitee_phyto', 'psci_phyto', 
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
    right = get_intervention_realise_action_outils_can(donnees).rename(columns={'intervention_realise_id': 'id'} )
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
    right = df_materiel[['nom', 'materiel_caracteristique1']].rename(
        columns={'nom' : 'nom_tracteur', 'materiel_caracteristique1' : 'tracteur_ou_automoteur'}
    )
    df_combinaison_outil_extanded = pd.merge(left, right, left_on='tracteur_materiel_id', right_index=True, how='left')

    # Ajout des inforations sur le materiel à la combinaison d'outils
    left = df_combinaison_outil_materiel
    right = df_materiel[['nom', 'type_materiel', 'materiel_caracteristique1']].rename(
        columns={'nom' : 'combinaison_outils_nom', 'materiel_caracteristique1' : 'outils'}
    )
    df_combinaison_outil_materiel= pd.merge(left, right, left_on='materiel_id', right_index=True, how='left')

    # On considère que si plusieurs matériels ont les mêmes caractéristiques (outils)
    # Alors il n'y a pas besoin de remonter plusieurs fois l'information dans l'agrégation 
    # (Correction par rapport aux exports en masse historiques)
    df_combinaison_outil_materiel = df_combinaison_outil_materiel.drop_duplicates(
        subset=['combinaison_outil_id', 'outils']
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

def get_intervention_realise_culture_outils_can(
    donnees
):
    """
        Permet d'obtenir le dataframe avec les informations sur les cultures précédentes
        retourne un dataframe avec pour index culture_id et pour colonne esp_var contenant 
        l'agrégation des informations
        sur la culture
    """
    df_intervention_realise = donnees['intervention_realise'].set_index('id')
    df_noeuds_realise = donnees['noeuds_realise'].set_index('id')
    df_plantation_perenne_phases_realise = donnees['plantation_perenne_phases_realise'].set_index('id')
    df_plantation_perenne_realise = donnees['plantation_perenne_realise'].set_index('id')
    df_composant_culture_concerne_intervention_realise = donnees[
        'composant_culture_concerne_intervention_realise'
    ].set_index('id')
    df_connection_realise = donnees['connection_realise'].set_index('id')

    # informations sur le composants cultures, dans le format attendu
    df_composant_culture_extanded = get_composant_culture_outils_can(donnees)

    # on ajoute aussi l'information de la culture intermédiaire si il y en a une
    left = df_noeuds_realise.reset_index()
    right = df_connection_realise.reset_index().rename(columns={'id' : 'connection_realise_id'})
    df_noeuds_realise_extanded = pd.merge(left, right, left_on='id', right_on='cible_noeuds_realise_id', how='left').set_index('id')

    left = df_noeuds_realise_extanded.reset_index()
    right = df_composant_culture_extanded.reset_index().rename(columns={'id' : 'composant_culture_id'})
    df_noeuds_realise_extanded_ci = pd.merge(left, right, left_on='culture_intermediaire_id', right_on='culture_id', how='left').set_index(
        ['id', 'composant_culture_id']
    )

    # informations assolée
    left = df_noeuds_realise_extanded.reset_index()
    right = df_composant_culture_extanded.reset_index().rename(columns={'id' : 'composant_culture_id'})
    df_noeuds_realise_extanded = pd.merge(left, right, left_on='culture_id', right_on='culture_id', how='left').set_index(
        ['id', 'composant_culture_id']
    )

    # informations perennes
    left = df_plantation_perenne_realise.reset_index()
    right = df_composant_culture_extanded.reset_index().rename(columns={'id' : 'composant_culture_id'})
    df_plantation_perenne_realise_extanded = pd.merge(
        left, right, left_on='culture_id', right_on='culture_id', how='left').set_index(
        ['id', 'composant_culture_id']
    )

    left = df_plantation_perenne_phases_realise.reset_index()
    right = df_plantation_perenne_realise_extanded.reset_index().rename(columns={'id' : 'plantation_perenne_realise_id'})
    df_plantation_perenne_phases_realise_extanded = pd.merge(
        left, right, on='plantation_perenne_realise_id', how='left').set_index('id')

    # on ajoute l'information du noeuds où porte l'intervention
    left = df_composant_culture_concerne_intervention_realise
    right = df_intervention_realise[['noeuds_realise_id', 'plantation_perenne_phases_realise_id']]
    df_composant_culture_concerne_intervention_extanded = pd.merge(
        left, right, left_on='intervention_realise_id', right_index=True, how='left')

    # maintenant qu'on a tout, pour l'assolée :
    left = df_composant_culture_concerne_intervention_extanded
    right = df_noeuds_realise_extanded
    df_composant_culture_concerne_intervention_extanded_assolee = pd.merge(left, right, 
        left_on=['noeuds_realise_id', 'composant_culture_id'],
        right_index=True,
        how='inner'
    )

    left = df_composant_culture_concerne_intervention_extanded
    right = df_noeuds_realise_extanded_ci
    df_composant_culture_concerne_intervention_extanded_assolee_ci = pd.merge(left, right, 
        left_on=['noeuds_realise_id', 'composant_culture_id'],
        right_index=True,
        how='inner'
    )

    df_composant_culture_concerne_intervention_extanded_assolee = pd.concat([
        df_composant_culture_concerne_intervention_extanded_assolee,
        df_composant_culture_concerne_intervention_extanded_assolee_ci
    ])

    # pour le perenne :
    left = df_composant_culture_concerne_intervention_extanded.reset_index()
    right = df_plantation_perenne_phases_realise_extanded.reset_index().rename(columns={'id' : 'plantation_perenne_phases_realise_id'})
    df_composant_culture_concerne_intervention_extanded_perenne = pd.merge(left, right,
        on=['plantation_perenne_phases_realise_id', 'composant_culture_id'],
        how='inner'
    )


    df_final_perenne = df_composant_culture_concerne_intervention_extanded_perenne.groupby([
        'intervention_realise_id'
    ]).agg({
        'esp_var' : ' ; '.join
    })
    df_final_assolee = df_composant_culture_concerne_intervention_extanded_assolee.groupby([
        'intervention_realise_id'
    ]).agg({
        'esp_var' : ' ; '.join
    })

    df_intervention_realise_final = pd.concat([df_final_assolee, df_final_perenne])

    return df_intervention_realise_final.reset_index().rename(columns={'intervention_realise_id' : 'id'})

def get_intervention_realise_culture_prec_outils_can(
        donnees
):
    """Permet d'obtenir le dataframe des informations sur les cultures précédentes pour les interventions pour la CAN"""
    
    df_intervention_realise = donnees['intervention_realise'].set_index('id')
    df_noeuds_realise = donnees['noeuds_realise'].set_index('id')
    df_connection_realise = donnees['connection_realise'].set_index('id')
    df_culture = donnees['culture'].set_index('id')

    # Obtention des informations sur le composant culture, dans le format attendu par la CAN
    df_composant_culture_extanded = get_composant_culture_outils_can(donnees, info_variete=False)

    df_culture_grouped = df_composant_culture_extanded.groupby('culture_id').agg({
        'esp_var' : ' ; '.join
    })

    left = df_culture
    right = df_culture_grouped
    df_culture_extanded = pd.merge(left, right, left_index=True, right_index=True, how='left')

    left = df_noeuds_realise
    right = df_culture_extanded[['nom', 'esp_var']]
    df_noeuds_realise_extanded = pd.merge(
        left, right, left_on='culture_id', right_index=True, how='left'
    )

    left = df_connection_realise
    right = df_noeuds_realise_extanded.rename(
        columns={
            'culture_id' : 'precedent_id', 
            'esp_var' : 'precedent_especes_edi', 
            'nom': 'precedent_nom'
        }
    )
    df_connection_realise_extanded = pd.merge(
        left, right, left_on='source_noeuds_realise_id', right_index=True, how='left'
    )

    left = df_intervention_realise.reset_index()
    right = df_connection_realise_extanded
    df_intervention_realise_extanded = pd.merge(
        left, right, left_on='noeuds_realise_id', right_on='cible_noeuds_realise_id', how='inner'
    ).set_index('id')

    final = df_intervention_realise_extanded[
        ['precedent_id', 'precedent_nom', 'precedent_especes_edi']
    ]
    return final.reset_index()

def get_intervention_realise_outils_can(
    donnees
):
    """
        Permet d'obtenir le dataframe final des interventions réalisés pour la CAN
    """
    # ajout des informations de contexte sur l'intervention
    left = get_intervention_realise_outils_can_context(donnees).rename(
        columns={'id' : 'intervention_realise_id'}
    )
    right = get_intervention_realise_combinaison_outils_can(donnees).rename(
        columns={'id' : 'intervention_realise_id'}
    )
    merge = pd.merge(left, right, on='intervention_realise_id', how='left')

    # ajout des informations sur la culture concernée par l'intervention
    left = merge
    right = get_intervention_realise_culture_outils_can(donnees).rename(
        columns={'id' : 'intervention_realise_id'}
    )
    merge = pd.merge(left, right, on='intervention_realise_id', how='left')


    # ajout des informations sur la culture précédente
    left = merge
    right = get_intervention_realise_culture_prec_outils_can(donnees).rename(
        columns={'id' : 'intervention_realise_id'}
    )
    merge = pd.merge(left, right, on='intervention_realise_id', how='left')

    return merge

# FONCTIONS POUR LES INTERVENTIONS EN SYNTHÉTISÉ

def get_intervention_synthetise_culture_outils_can(
      donnees  
):
    """
        Permet d'obtenir le dataframe avec les informations sur les cultures 
        
        esp_var contenant l'agrégation des informations sur la culture
    """
    # on obtient un dataframe où composant_culture_id x intervention_synthetise_id est unique
    # chaque ligne correspond à l'affectation d'un composant de culture à une intervention_synthetise

    # dans un autre temps, 

    df_intervention_synthetise = donnees['intervention_synthetise'].set_index('id')
    df_noeuds_synthetise = donnees['noeuds_synthetise'].set_index('id')
    df_connection_synthetise = donnees['connection_synthetise'].set_index('id')
    df_plantation_perenne_phases_synthetise = donnees['plantation_perenne_phases_synthetise'].set_index('id')
    df_plantation_perenne_synthetise = donnees['plantation_perenne_synthetise'].set_index('id')
    df_composant_culture_concerne_intervention_synthetise = donnees[
        'composant_culture_concerne_intervention_synthetise'
    ].set_index('id')
    df_noeuds_synthetise_restructure = donnees['noeuds_synthetise_restructure'].set_index('id')
    df_plantation_perenne_synthetise_restructure = donnees['plantation_perenne_synthetise_restructure'].set_index('id')
    df_composant_culture_concerne_intervention_synthetise_restructure = donnees[
        'ccc_intervention_synthetise_restructure'
    ].set_index('id')
    df_connection_synthetise_restructure = donnees['connection_synthetise_restructure'].set_index('id')

    left = df_connection_synthetise
    right = df_connection_synthetise_restructure
    df_connection_synthetise_extanded_prim = pd.merge(left, right, left_index=True, right_index=True, how='left')

    # informations sur les composants cultures, dans le format attendu par la CAN
    df_composant_culture_extanded = get_composant_culture_outils_can(donnees)

    # reconstitution du culture_id pour le synthétisé
    left = df_noeuds_synthetise
    right = df_noeuds_synthetise_restructure
    df_noeuds_synthetise_extanded = pd.merge(left, right, left_index=True, right_index=True, how='left')

    # informations assolée
    left = df_noeuds_synthetise_extanded.reset_index()
    right = df_composant_culture_extanded.reset_index().rename(columns={'id' : 'composant_culture_id'})
    df_noeuds_synthetise_extanded = pd.merge(left, right, left_on='culture_id', right_on='culture_id', how='left')

    left = df_connection_synthetise_extanded_prim.reset_index()
    right = df_noeuds_synthetise_extanded.rename(columns={'id' : 'noeuds_synthetise_id'})
    df_connection_synthetise_extanded = pd.merge(
        left, right, left_on='cible_noeuds_synthetise_id', right_on='noeuds_synthetise_id', how='left'
    ).set_index(
        ['id', 'composant_culture_id']
    )

    left = df_plantation_perenne_synthetise
    right = df_plantation_perenne_synthetise_restructure
    df_plantation_perenne_synthetise_extanded = pd.merge(left, right, left_index=True, right_index=True, how='left')

    # informations perennes
    left = df_plantation_perenne_synthetise_extanded.reset_index()
    right = df_composant_culture_extanded.reset_index().rename(columns={'id' : 'composant_culture_id'})
    df_plantation_perenne_synthetise_extanded = pd.merge(
        left, right, left_on='culture_id', right_on='culture_id', how='left').set_index(
        ['id', 'composant_culture_id']
    )

    left = df_plantation_perenne_phases_synthetise.reset_index()
    right = df_plantation_perenne_synthetise_extanded.reset_index().rename(columns={'id' : 'plantation_perenne_synthetise_id'})
    df_plantation_perenne_phases_synthetise_extanded = pd.merge(
        left, right, on='plantation_perenne_synthetise_id', how='left'
    ).set_index('id')


    # on ajoute l'information de la connection où porte l'intervention
    left = df_composant_culture_concerne_intervention_synthetise
    right = df_composant_culture_concerne_intervention_synthetise_restructure
    df_composant_culture_intervention_synthetise_restructure = pd.merge(
        left, right, left_index=True, right_index=True, how='left'
    )

    left = df_composant_culture_intervention_synthetise_restructure
    right = df_intervention_synthetise[['connection_synthetise_id', 'plantation_perenne_phases_synthetise_id']]
    df_composant_culture_concerne_intervention_extanded = pd.merge(
        left, right, left_on='intervention_synthetise_id', right_index=True, how='left')

    # pour les cultures intermédiaires, on est obligé de faire un traitement spécifique : 
    left = df_connection_synthetise_extanded_prim.reset_index()
    right = df_composant_culture_extanded[['culture_id', 'esp_var']].reset_index().rename(columns={'id': 'composant_culture_id'})
    df_connection_synthetise_extanded_ci = pd.merge(
        left, right, left_on='culture_intermediaire_id', right_on='culture_id', how='inner'
    ).set_index(['id', 'composant_culture_id'])

    
    # maintenant qu'on a tout, pour l'assolée :
    left = df_composant_culture_concerne_intervention_extanded
    right = df_connection_synthetise_extanded
    df_composant_culture_concerne_intervention_extanded_assolee = pd.merge(left, right, 
        left_on=['connection_synthetise_id', 'composant_culture_id'],
        right_index=True,
        how='inner'
    )

    left = df_composant_culture_concerne_intervention_extanded
    right = df_connection_synthetise_extanded_ci
    df_composant_culture_concerne_intervention_extanded_assolee_ci = pd.merge(left, right, 
        left_on=['connection_synthetise_id', 'composant_culture_id'],
        right_index=True,
        how='inner'
    )

    df_composant_culture_concerne_intervention_extanded_assolee = pd.concat([
        df_composant_culture_concerne_intervention_extanded_assolee,
        df_composant_culture_concerne_intervention_extanded_assolee_ci
    ])

    # pour le perenne :
    left = df_composant_culture_concerne_intervention_extanded.reset_index()
    right = df_plantation_perenne_phases_synthetise_extanded.reset_index().rename(columns={'id' : 'plantation_perenne_phases_synthetise_id'})
    df_composant_culture_concerne_intervention_extanded_perenne = pd.merge(left, right,
        on=['plantation_perenne_phases_synthetise_id', 'composant_culture_id'],
        how='inner'
    )

    df_final_perenne = df_composant_culture_concerne_intervention_extanded_perenne.groupby([
        'intervention_synthetise_id'
    ]).agg({
        'esp_var' : ' ; '.join
    })
    df_final_assolee = df_composant_culture_concerne_intervention_extanded_assolee.groupby([
        'intervention_synthetise_id'
    ]).agg({
        'esp_var' : ' ; '.join
    })

    df_intervention_synthetise_final = pd.concat([df_final_assolee, df_final_perenne])

    return df_intervention_synthetise_final.reset_index().rename(
        columns={'intervention_synthetise_id' : 'id'}
    )

def get_intervention_synthetise_culture_prec_outils_can(
        donnees
):
    """Permet d'obtenir le dataframe des informations sur les cultures précédentes pour les interventions synthétisé pour la CAN"""
    
    df_intervention_synthetise = donnees['intervention_synthetise'].set_index('id')
    df_noeuds_synthetise = donnees['noeuds_synthetise'].set_index('id')
    df_connection_synthetise = donnees['connection_synthetise'].set_index('id')
    df_culture = donnees['culture'].set_index('id')
    df_noeuds_synthetise_restructure = donnees['noeuds_synthetise_restructure'].set_index('id')

    # Obtention des informations sur le composant culture, dans le format attendu par la CAN
    df_composant_culture_extanded = get_composant_culture_outils_can(donnees, info_variete=False)

    df_culture_grouped = df_composant_culture_extanded.groupby('culture_id').agg({
        'esp_var' : ' ; '.join
    })

    # ajout des infos sur la culture
    left = df_culture
    right = df_culture_grouped
    df_culture_extanded = pd.merge(left, right, left_index=True, right_index=True, how='left')

    # ajout du composant_culture_id pour ne pas avoir à travailler avec le composant_culture_code
    left = df_noeuds_synthetise
    right = df_noeuds_synthetise_restructure
    df_noeuds_synthetise = pd.merge(left, right, left_index=True, right_index=True, how='left')

    # ajout des informations de la culture au noeud
    left = df_noeuds_synthetise
    right = df_culture_extanded[['nom', 'esp_var']]
    df_noeuds_synthetise_extanded = pd.merge(
        left, right, left_on='culture_id', right_index=True, how='left'
    )

    # ajout des informations du noeud précédent à la connexion
    left = df_connection_synthetise
    right = df_noeuds_synthetise_extanded.rename(
        columns={
            'culture_code' : 'precedent_code', 
            'esp_var' : 'precedent_especes_edi', 
            'nom': 'precedent_nom'
        }
    )
    df_connection_synthetise_extanded = pd.merge(
        left, right, left_on='source_noeuds_synthetise_id', right_index=True, how='left'
    )

    # ajout des informations de la connexion sur laquelle porte l'intervention
    left = df_intervention_synthetise.reset_index()
    right = df_connection_synthetise_extanded
    df_intervention_synthetise_extanded = pd.merge(
        left, right, left_on='connection_synthetise_id', right_index=True, how='inner'
    ).set_index('id')

    final = df_intervention_synthetise_extanded[
        ['precedent_code', 'precedent_nom', 'precedent_especes_edi']
    ]
    return final.reset_index()

def get_intervention_synthetise_action_outils_can(
        donnees
):
    """
        Permet d'obtenir le dataframe des informations sur les actions pour les interventions synthétisé pour la CAN
        (colonnes : )
    """
    df_action_synthetise = donnees['action_synthetise']
    df_intervention_synthetise = donnees['intervention_synthetise']

    left =  df_action_synthetise
    right = df_intervention_synthetise[['id', 'freq_spatiale', 'freq_temporelle', 'psci_intervention']].rename(columns={'id' : 'intervention_synthetise_id'})
    df_action_synthetise_extanded = pd.merge(left, right, on='intervention_synthetise_id', how='left')

    # Pour les applications de produits phytosanitaires :
    df_action_produit_phyto = df_action_synthetise_extanded.loc[df_action_synthetise_extanded['type'] == 'APPLICATION_DE_PRODUITS_PHYTOSANITAIRES']
    df_action_produit_phyto.loc[: , 'proportion_surface_traitee_phyto'] = df_action_produit_phyto['proportion_surface_traitee']
    df_action_produit_phyto.loc[: ,'psci_phyto'] = df_action_produit_phyto['proportion_surface_traitee'] * \
          df_action_produit_phyto['freq_spatiale'] * df_action_produit_phyto['freq_temporelle']

    # Pour la lutte biologique :
    df_action_lutte_bio = df_action_synthetise_extanded.loc[df_action_synthetise_extanded['type'] == 'LUTTE_BIOLOGIQUE']
    df_action_lutte_bio.loc[: ,'proportion_surface_traitee_lutte_bio'] = df_action_lutte_bio['proportion_surface_traitee']
    df_action_lutte_bio.loc[: ,'psci_lutte_bio'] = df_action_lutte_bio['proportion_surface_traitee'] * \
          df_action_lutte_bio['freq_spatiale'] * df_action_lutte_bio['freq_temporelle']

    # Pour l'irrigation :
    df_action_irrigation = df_action_synthetise_extanded.loc[df_action_synthetise_extanded['type'] == 'IRRIGATION']
    df_action_irrigation.loc[: ,'quantite_eau_mm'] = df_action_irrigation['eau_qte_moy_mm'] 

    # Pour les autres :
    df_action_autres = df_action_synthetise_extanded.loc[
        (df_action_synthetise_extanded['type'] != 'APPLICATION_DE_PRODUITS_PHYTOSANITAIRES') &
        (df_action_synthetise_extanded['type'] != 'LUTTE_BIOLOGIQUE') &
        (df_action_synthetise_extanded['type'] != 'IRRIGATION')
    ].groupby(['intervention_synthetise_id']).agg({
        'label' : ' ; '.join
    }).reset_index()
    
    keeped_column_produit_phyto = ['proportion_surface_traitee_phyto', 'psci_phyto']
    keeped_column_lutte_bio = ['proportion_surface_traitee_lutte_bio', 'psci_lutte_bio']
    keeped_column_irrigation = ['quantite_eau_mm']
    merge = pd.merge(df_action_produit_phyto[keeped_column_produit_phyto+['intervention_synthetise_id', 'label']],
    df_action_lutte_bio[keeped_column_lutte_bio+['intervention_synthetise_id', 'label']],
    on='intervention_synthetise_id', how='outer', suffixes = ('', '_lutte_bio'))

    merge = pd.merge(merge.set_index('intervention_synthetise_id'),
                     df_action_autres[['intervention_synthetise_id', 'label']],
                     left_index=True, suffixes = ('', '_autre'),
                     right_on='intervention_synthetise_id', how='outer').drop_duplicates(subset=['intervention_synthetise_id'])
    
    merge = pd.merge(merge.set_index('intervention_synthetise_id'), 
                     df_action_irrigation[keeped_column_irrigation+['intervention_synthetise_id', 'label']],
                     left_index=True, suffixes = ('', '_irrigation'),
                     right_on='intervention_synthetise_id', how='outer').drop_duplicates(subset=['intervention_synthetise_id'])

    merge['interventions_actions'] = merge[['label', 'label_lutte_bio', 'label_autre', 'label_irrigation']].apply(
        lambda x: x.str.cat(sep=' ; '), axis=1
    )

    # À ce stade, on a encore des dupplication d'intervention_id : on doit grouper par intervention_id en joignant le nom des actions, mais en gardant
    # à chaque fois la valeur non nulle pour les colonnes
    intervention_actions_indicateurs = merge[[
        'interventions_actions', 'proportion_surface_traitee_phyto', 'psci_phyto', 
        'proportion_surface_traitee_lutte_bio', 'psci_lutte_bio', 'quantite_eau_mm',
        'intervention_synthetise_id'
    ]].rename(columns={'intervention_synthetise_id' : 'id'})

    return intervention_actions_indicateurs

def get_intervention_synthetise_semence_outils_can(
        donnees
    ):
    """
        permet d'obtenir les informations sur les interventions de type "SEMIS" en synthétisé.
    """
    df_semence = donnees['semence']
    df_composant_culture = donnees['composant_culture']
    df_espece = donnees['espece']
    df_utilisation_intrant_synthetise = donnees['utilisation_intrant_synthetise']

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

    # ajout des informations des semences sur les utilisations d'intrants
    left = df_utilisation_intrant_synthetise[['intervention_synthetise_id', 'intrant_id', 'dose', 'unite', 'semence_id']]
    right = df_semence_extanded.rename(columns={'id' : 'semence_id'})
    df_utilisation_intrant_synthetise_extanded = pd.merge(left, right, on='semence_id', how='inner')

    df_utilisation_intrant_synthetise_extanded['dose'] = df_utilisation_intrant_synthetise_extanded['dose'].astype('str')

    # on groupe par intervention
    df_intervention_semence = df_utilisation_intrant_synthetise_extanded.fillna('').groupby([
        'intervention_synthetise_id'
    ]).agg({
        'description' :  ' ; '.join,
        'type_semence' :  ', '.join,
        'dose' : ', '.join,
        'unite' : ', '.join, 
        'inoculation_biologique' : lambda x: map_boolean(x, sep=', '),
        'traitement_chimique' : lambda x: map_boolean(x, sep=', ')
    })

    df_intervention_semence['dose'] = df_intervention_semence[['dose']].applymap(convert_to_int)

    return df_intervention_semence.reset_index().rename(columns={
        'intervention_synthetise_id' : 'id',
        'description' : 'especes_semees', 
        'dose' : 'densite_semis', 
        'unite' : 'unite_semis', 
        'traitement_chimique' : 'traitement_chimique_semis',
        'inoculation_biologique' : 'inoculation_biologique_semis'
    })

def get_intervention_synthetise_outils_can_context(
    donnees
):
    """
        Permet d'obtenir un dataframe intermédiaire des interventions pour la CAN
    """
    df_intervention_synthetise = donnees['intervention_synthetise']

    # ajout des informations sur les différents indicateurs
    left = df_intervention_synthetise
    right = get_intervention_synthetise_action_outils_can(donnees)
    print(right.columns, right.index)
    merge = pd.merge(left, right, on='id', how='left')
    
    # ajout des informations sur la table semis
    left = merge
    right = get_intervention_synthetise_semence_outils_can(donnees).reset_index()
    merge = pd.merge(left, right, on='id', how='left')



    columns = ['id', 'interventions_actions', 'especes_semees', 'densite_semis', 'unite_semis', 'traitement_chimique_semis', 
               'inoculation_biologique_semis', 'type_semence', 'proportion_surface_traitee_phyto', 'psci_phyto', 
               'proportion_surface_traitee_lutte_bio', 'psci_lutte_bio', 'quantite_eau_mm']
    # ajout des informations sur les espèces concernées
    return merge[columns]

def get_intervention_synthetise_combinaison_outils_can(
    donnees
):
    """
        Permet d'obtenir le dataframe avec les informations sur les combinaisons d'outils
    """
    df_intervention_synthetise = donnees['intervention_synthetise'].set_index('id')
    df_combinaison_outil = donnees['combinaison_outil'].set_index('id')
    df_materiel = donnees['materiel'].set_index('id')
    df_combinaison_outil_materiel = donnees['combinaison_outil_materiel']
    df_intervention_synthetise_restructure = donnees['intervention_synthetise_restructure'].set_index('id')

    # Ajout du combinaison_outil_id pour ne pas avoir à travailler avec combinaison_outil_code
    left = df_intervention_synthetise
    right = df_intervention_synthetise_restructure
    df_intervention_synthetise_extanded = pd.merge(left, right, left_index=True, right_index=True, how='left')

    # Ajout des informations sur le tracteur à la combinaison d'outils 
    left = df_combinaison_outil[['nom', 'tracteur_materiel_id']]
    right = df_materiel[['nom', 'materiel_caracteristique1']].rename(
        columns={'nom' : 'nom_tracteur', 'materiel_caracteristique1' : 'tracteur_ou_automoteur'}
    )
    df_combinaison_outil_extanded = pd.merge(left, right, left_on='tracteur_materiel_id', right_index=True, how='left')

    # Ajout des informations sur le materiel à la combinaison d'outils
    left = df_combinaison_outil_materiel
    right = df_materiel[['nom', 'type_materiel', 'materiel_caracteristique1']].rename(
        columns={'nom' : 'combinaison_outils_nom', 'materiel_caracteristique1' : 'outils'}
    )
    df_combinaison_outil_materiel= pd.merge(left, right, left_on='materiel_id', right_index=True, how='left')

    # On considère que si plusieurs matériels ont les mêmes caractéristiques (outils)
    # Alors il n'y a pas besoin de remonter plusieurs fois l'information dans l'agrégation 
    # (Correction par rapport aux exports en masse historiques)
    df_combinaison_outil_materiel = df_combinaison_outil_materiel.drop_duplicates(
        subset=['combinaison_outil_id', 'outils']
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
    left = df_intervention_synthetise_extanded[['combinaison_outil_id']]
    right = df_combinaison_outil_extanded.rename(columns={'nom' : 'combinaison_outils_nom'})[
        ['combinaison_outils_nom', 'tracteur_ou_automoteur', 'outils']
    ]

    merge = pd.merge(left, right, left_on='combinaison_outil_id', right_index=True, how='left')

    return merge.reset_index()

def get_intervention_synthetise_outils_can(
    donnees
):
    """
        Permet d'obtenir le dataframe final des interventions synthétisés pour la CAN
    """
    # ajout des informations de contexte sur l'intervention
    left = get_intervention_synthetise_outils_can_context(donnees).rename(
        columns={'id' : 'intervention_synthetise_id'}
    )
    right = get_intervention_synthetise_combinaison_outils_can(donnees).rename(
        columns={'id' : 'intervention_synthetise_id'}
    )
    merge = pd.merge(left, right, on='intervention_synthetise_id', how='left')

    # ajout des informations sur la culture concernée par l'intervention
    left = merge
    right = get_intervention_synthetise_culture_outils_can(donnees).rename(
        columns={'id' : 'intervention_synthetise_id'}
    )
    merge = pd.merge(left, right, on='intervention_synthetise_id', how='left')


    # ajout des informations sur la culture précédente
    left = merge
    right = get_intervention_synthetise_culture_prec_outils_can(donnees).rename(
        columns={'id' : 'intervention_synthetise_id'}
    )
    merge = pd.merge(left, right, on='intervention_synthetise_id', how='left')

    return merge




# FONCTIONS POUR LES PARCELLES NON-RATTACHÉES

def get_parcelles_non_rattachees_outils_can(
    donnees
):
    """
        Permet d'obtenir des informations sur les parcelles non-rattachées
        On agrège toutes les informations au niveau du domaine auquel elles appartiennent.
        On ne considère : 
            - que les parcelles qui contiennent des interventions
            - que les parcelles qui ont une surface > 0
    """
    df_parcelle = donnees['parcelle'].set_index('id')
    df_reseau = donnees['reseau'].set_index('id')
    df_liaison_reseaux = donnees['liaison_reseaux']
    df_liaison_sdc_reseau = donnees['liaison_sdc_reseau']
    df_sdc = donnees['sdc'].set_index('id')
    df_dispositif = donnees['dispositif'].set_index('id')
    df_intervention_realise_agrege = donnees['intervention_realise_agrege'].set_index('id')


    # on ne garde que les parcelles non rattachées
    df_parcelles_non_rattachees = df_parcelle.loc[
        (df_parcelle['sdc_id'].isna()) &
        (df_parcelle.index.isin(df_intervention_realise_agrege['parcelle_id'])) &
        (df_parcelle['surface'] > 0)
    ]

    # pour chaque liaison de réseau, on obtient l'information complète
    left = df_liaison_sdc_reseau
    right = df_sdc[['dispositif_id']]
    merge = pd.merge(left, right, left_on='sdc_id', right_index=True, how='left')

    # pour chaque laison, on ajoute les informations sur le réseau
    left = merge 
    right = df_reseau[['nom', 'code_convention_dephy']]
    merge = pd.merge(left, right, left_on='reseau_id', right_index=True, how='left')

    # on obtient le domaine associé au sdc
    left = merge
    right = df_dispositif[['domaine_id']]
    merge = pd.merge(left, right, left_on='dispositif_id', right_index=True, how='left')

    # on obtient aussi le lien vers le parent du réseau
    left = merge
    right = df_liaison_reseaux
    merge = pd.merge(left, right, on='reseau_id', how='left')

    # on ajoute les informations sur le réseau parent
    left = merge
    right = df_reseau.rename(columns={'nom' : 'nom_reseau_parent', 'code_convention_dephy' : 'code_convention_dephy_reseau_parent'})
    merge = pd.merge(left, right, left_on='reseau_parent_id', right_index=True).dropna(subset=['nom', 'nom_reseau_parent']).fillna('')

    res_reseaux_domaine = merge.groupby('domaine_id').agg({
        'nom' : lambda x: '|'.join(x.unique()),
        'nom_reseau_parent' : lambda x: '|'.join(x.unique()),
        'code_convention_dephy' : lambda x: '|'.join(x.unique())
    }).rename(columns={
        'nom' : 'reseaux_ir',
        'nom_reseau_parent' : 'reseaux_it',
        'code_convention_dephy' : 'codes_convention_dephy'
    })

    df_parcelles_non_rattachees = df_parcelles_non_rattachees.reset_index().groupby('domaine_id').agg({
        'id' : 'count', 
        'edaplos_utilisateur_id' : 'count'
    }).reset_index().rename(columns={
        'id' : 'nb_parcelles_sans_sdc', 
        'edaplos_utilisateur_id':'nb_parcelles_avec_id_edaplos',
        'domaine_id' : 'id'
    }).set_index('id')

    left = df_parcelles_non_rattachees
    right = res_reseaux_domaine
    final = pd.merge(left, right, left_index=True, right_index=True, how='left')

    return final.reset_index()


# FONCTIONS POUR LES CULTURES
def get_culture_outils_can(
    donnees
):
    """
        Permet d'obtenir des informations agrégées sur les cultures (sous le format désiré par la CAN)
    """
    df_composant_culture = donnees['composant_culture'].set_index('id')
    df_espece = donnees['espece'].set_index('id')

    df_espece = df_espece.fillna('')
    df_espece['complet_espece_edi'] = (
        df_espece['libelle_espece_botanique']
        +' '
        +df_espece['libelle_qualifiant_aee']
        +' '
        +df_espece['libelle_type_saisonnier_aee']
        +' '
        +df_espece['libelle_destination_aee']
    ).str.replace('\n', '<br>').str.replace('  ', ' ').str.strip()

    # ajout des informations utiles sur la variété et sur l'espèce au composant de culture
    left = df_composant_culture
    right = df_espece['complet_espece_edi']
    df_composant_culture_extanded = pd.merge(left, right, left_on='espece_id', right_index=True, how='left')

    res = df_composant_culture_extanded.groupby('culture_id').agg({
        'complet_espece_edi' : ' ; '.join
    })

    return res.reset_index().rename(columns={'culture_id' : 'id'})


def get_recolte_realise_outils_can(
        donnees
):
    """ permet d'obtenir les informations sur les récoltes en réalisé (cf get_recolte_outils_can)"""
    df = donnees.copy()
    df['composant_culture'] = df['composant_culture'].set_index('id')
    df['culture'] = df['culture'].set_index('id')
    df['composant_culture_concerne_intervention_realise'] = df['composant_culture_concerne_intervention_realise'].set_index('id')
    df['recolte_rendement_prix'] = df['recolte_rendement_prix'].set_index('id')
    df['recolte_rendement_prix_restructure'] = df['recolte_rendement_prix_restructure'].set_index('id')
    df['action_realise'] = df['action_realise'].set_index('id')

    # on veut savoir pour chaque composant culture si celui-ci appartient à une culture "melange espece" / "melange variété"
    left = df['composant_culture']
    right = df['culture'][['melange_especes', 'melange_varietes']]
    df['composant_culture_extanded'] = pd.merge(left, right, left_on='culture_id', right_index=True, how='left')

    left = df['composant_culture_concerne_intervention_realise']
    right = df['composant_culture_extanded'][['surface_relative', 'melange_especes', 'melange_varietes']]
    merge = pd.merge(left, right, left_on='composant_culture_id', right_index=True)

    # on commence par compter le nombre de composants de culture concernés par l'intervention
    nombre_composant_culture_concerne_intervention = pd.DataFrame(merge.groupby('intervention_realise_id').size()).rename(columns={0:'nombre'})

    # on fusionne ce résultat avec notre merge
    left = merge
    right = nombre_composant_culture_concerne_intervention
    merge = pd.merge(left, right, left_on='intervention_realise_id', right_index=True )

    # Attention, pour tout ceux qui ont déjà une surface relative, on doit recalculer la VRAIE surface relative...
    surface_totale = merge.loc[~merge['surface_relative'].isna()].groupby('intervention_realise_id')['surface_relative'].sum()

    left = merge
    right = surface_totale.rename('surface_relative_totale')
    merge = pd.merge(left, right, left_on='intervention_realise_id', right_index=True, how='left')


    # calcul de la surface relative corrigée dans les cas historiques qui posent problème
    merge.loc[merge['surface_relative_totale']>100, 'surface_relative_corrigee'] = (
        merge.loc[merge['surface_relative_totale']>100]['surface_relative'] / merge.loc[merge['surface_relative_totale']>100]['surface_relative_totale']
    )*100

    # affectation de la surface relative pour les cas qui ne posent pas problème 
    merge.loc[merge['surface_relative_totale']<=100, 'surface_relative_corrigee'] = merge.loc[merge['surface_relative_totale']<=100]['surface_relative']

    # affectation des surfaces relatives pour ceux qui ne sont pas saisis du tout
    merge.loc[merge['surface_relative_corrigee'].isna(), 'surface_relative_corrigee'] = (100 / merge.loc[merge['surface_relative_corrigee'].isna()]['nombre'])

    # on rajoute toutes les informations qu'on doit avoir pour fusionner avec le dataframe merge qu'on vient d'obtenir
    left = df['recolte_rendement_prix']
    right = df['recolte_rendement_prix_restructure']
    df['recolte_rendement_prix_extanded'] = pd.merge(left, right, left_index=True, right_index=True, how='left')

    left = df['recolte_rendement_prix_extanded']
    right = df['action_realise'][['intervention_realise_id']]
    df['recolte_rendement_prix_extanded'] = pd.merge(left, right, left_on='action_id', right_index=True, how='inner')

    left = df['recolte_rendement_prix_extanded'].reset_index()
    right = merge
    df['recolte_rendement_prix_extanded'] = pd.merge(left, right, on = ['composant_culture_id', 'intervention_realise_id'], how='left').set_index('id')

    # on remplace les données manquantes
    df['recolte_rendement_prix_extanded'].loc[:, ['melange_especes']] = df['recolte_rendement_prix_extanded'].loc[:, ['melange_especes']].fillna('t')
    df['recolte_rendement_prix_extanded'].loc[:, ['melange_varietes']] = df['recolte_rendement_prix_extanded'].loc[:, ['melange_varietes']].fillna('t')


    left = df['recolte_rendement_prix_extanded']
    right = merge.groupby('intervention_realise_id')['surface_relative_corrigee'].sum().rename('surface_relative_corrigee_totale')
    final_realise = pd.merge(left, right, left_on='intervention_realise_id', right_index=True, how='left')

    # Attention, on ne doit corriger que si ce n'est pas un mélange de variété / ou d'espèce !
    final_realise_1 = final_realise.loc[(final_realise['melange_especes']=='f') & (final_realise['melange_varietes'] == 'f')]
    final_realise_2 = final_realise.loc[(final_realise['melange_especes']=='t') | (final_realise['melange_varietes'] == 't')]

    # pour ceux qui ne sont pas des mélanges d'espèces : 
    final_realise.loc[final_realise_1.index, 'rendement_moy_corr'] = final_realise_1['rendement_moy'] * (final_realise_1['surface_relative_corrigee']) / final_realise_1['surface_relative_corrigee_totale']
    final_realise.loc[final_realise_1.index, 'rendement_median_corr'] = final_realise_1['rendement_median'] * (final_realise_1['surface_relative_corrigee']) / final_realise_1['surface_relative_corrigee_totale']
    final_realise.loc[final_realise_1.index, 'rendement_max_corr'] = final_realise_1['rendement_max'] * (final_realise_1['surface_relative_corrigee']) / final_realise_1['surface_relative_corrigee_totale']
    final_realise.loc[final_realise_1.index,'rendement_min_corr'] = final_realise_1['rendement_min'] * (final_realise_1['surface_relative_corrigee']) / final_realise_1['surface_relative_corrigee_totale']
    final_realise.loc[final_realise_1.index, 'commercialisation_pct_corr'] = final_realise_1['commercialisation_pct'] * (final_realise_1['surface_relative_corrigee']) / final_realise_1['surface_relative_corrigee_totale']
    final_realise.loc[final_realise_1.index, 'autoconsommation_pct_corr'] = final_realise_1['autoconsommation_pct'] * (final_realise_1['surface_relative_corrigee']) / final_realise_1['surface_relative_corrigee_totale']
    final_realise.loc[final_realise_1.index, 'nonvalorisation_pct_corr'] = final_realise_1['nonvalorisation_pct'] * (final_realise_1['surface_relative_corrigee']) / final_realise_1['surface_relative_corrigee_totale']

    # pour ceux qui sont des mélanges d'espèces : 
    final_realise.loc[final_realise_2.index, 'rendement_moy_corr'] = final_realise_2['rendement_moy']
    final_realise.loc[final_realise_2.index, 'rendement_median_corr'] = final_realise_2['rendement_median']
    final_realise.loc[final_realise_2.index, 'rendement_max_corr'] = final_realise_2['rendement_max']
    final_realise.loc[final_realise_2.index,'rendement_min_corr'] = final_realise_2['rendement_min']
    final_realise.loc[final_realise_2.index, 'commercialisation_pct_corr'] = final_realise_2['commercialisation_pct']
    final_realise.loc[final_realise_2.index, 'autoconsommation_pct_corr'] = final_realise_2['autoconsommation_pct']
    final_realise.loc[final_realise_2.index, 'nonvalorisation_pct_corr'] = final_realise_2['nonvalorisation_pct']

    # on groupe pour obtenir un seul résultat par action / destination / rendement unite
    final_realise = final_realise.groupby(['destination_id', 'rendement_unite', 'action_id']).agg({
        'rendement_moy_corr' : 'sum',
        'rendement_median_corr' : 'sum',
        'rendement_max_corr' : 'sum',
        'rendement_min_corr' : 'sum', 
        'commercialisation_pct_corr' : 'sum',
        'autoconsommation_pct_corr' :'sum',
        'nonvalorisation_pct_corr' : 'sum'
    }).reset_index().replace(0, np.NaN).round(2)

    return final_realise

def get_recolte_synthetise_outils_can(
        donnees
):
    """ permet d'obtenir les informations sur les recoltes en synthétisé (cf get_recolte_outils_can)"""
    df = donnees.copy()
    df['composant_culture'] = df['composant_culture'].set_index('id')
    df['culture'] = df['culture'].set_index('id')
    df['composant_culture_concerne_intervention_synthetise'] = df['composant_culture_concerne_intervention_synthetise'].set_index('id')
    df['ccc_intervention_synthetise_restructure'] = df['ccc_intervention_synthetise_restructure'].set_index('id')
    df['recolte_rendement_prix'] = df['recolte_rendement_prix'].set_index('id')
    df['recolte_rendement_prix_restructure'] = df['recolte_rendement_prix_restructure'].set_index('id')
    df['action_synthetise'] = df['action_synthetise'].set_index('id')

    # on veut savoir pour chaque composant culture si celui-ci appartient à une culture "melange espece" / "melange variété"
    left = df['composant_culture']
    right = df['culture'][['melange_especes', 'melange_varietes']]
    df['composant_culture_extanded'] = pd.merge(left, right, left_on='culture_id', right_index=True, how='left')

    left = df['composant_culture_concerne_intervention_synthetise']
    right = df['ccc_intervention_synthetise_restructure']
    df['composant_culture_concerne_intervention_synthetise_extanded'] = pd.merge(left, right, left_index=True, right_index=True, how='left')

    left = df['composant_culture_concerne_intervention_synthetise_extanded'] 
    right = df['composant_culture_extanded'][['surface_relative', 'melange_especes', 'melange_varietes']]
    merge = pd.merge(left, right, left_on='composant_culture_id', right_index=True)

    # on commence par compter le nombre de composants de culture concernés par l'intervention
    nombre_composant_culture_concerne_intervention = pd.DataFrame(merge.groupby('intervention_synthetise_id').size()).rename(columns={0:'nombre'})

    # on fusionne ce résultat avec notre merge
    left = merge
    right = nombre_composant_culture_concerne_intervention
    merge = pd.merge(left, right, left_on='intervention_synthetise_id', right_index=True )

    # Attention, pour tout ceux qui ont déjà une surface relative, on doit recalculer la VRAIE surface relative...
    surface_totale = merge.loc[~merge['surface_relative'].isna()].groupby('intervention_synthetise_id')['surface_relative'].sum()

    left = merge
    right = surface_totale.rename('surface_relative_totale')
    merge = pd.merge(left, right, left_on='intervention_synthetise_id', right_index=True, how='left')


    # calcul de la surface relative corrigée dans les cas historiques qui posent problème
    merge.loc[merge['surface_relative_totale']>100, 'surface_relative_corrigee'] = (
        merge.loc[merge['surface_relative_totale']>100]['surface_relative'] / merge.loc[merge['surface_relative_totale']>100]['surface_relative_totale']
    )*100

    # affectation de la surface relative pour les cas qui ne posent pas problème 
    merge.loc[merge['surface_relative_totale']<=100, 'surface_relative_corrigee'] = merge.loc[merge['surface_relative_totale']<=100]['surface_relative']

    # affectation des surfaces relatives pour ceux qui ne sont pas saisis du tout
    merge.loc[merge['surface_relative_corrigee'].isna(), 'surface_relative_corrigee'] = (100 / merge.loc[merge['surface_relative_corrigee'].isna()]['nombre'])

    # on rajoute toutes les informations qu'on doit avoir pour fusionner avec le dataframe merge qu'on vient d'obtenir
    left = df['recolte_rendement_prix']
    right = df['recolte_rendement_prix_restructure']
    df['recolte_rendement_prix_extanded'] = pd.merge(left, right, left_index=True, right_index=True, how='left')

    left = df['recolte_rendement_prix_extanded']
    right = df['action_synthetise'][['intervention_synthetise_id']]
    df['recolte_rendement_prix_extanded'] = pd.merge(left, right, left_on='action_id', right_index=True, how='inner')


    left = df['recolte_rendement_prix_extanded'].reset_index()
    right = merge
    df['recolte_rendement_prix_extanded'] = pd.merge(left, right, on = ['composant_culture_id', 'intervention_synthetise_id'], how='left').set_index('id')

    # on remplace les données manquantes
    df['recolte_rendement_prix_extanded'].loc[:, ['melange_especes']] = df['recolte_rendement_prix_extanded'].loc[:, ['melange_especes']].fillna('t')
    df['recolte_rendement_prix_extanded'].loc[:, ['melange_varietes']] = df['recolte_rendement_prix_extanded'].loc[:, ['melange_varietes']].fillna('t')


    left = df['recolte_rendement_prix_extanded']
    right = merge.groupby('intervention_synthetise_id')['surface_relative_corrigee'].sum().rename('surface_relative_corrigee_totale')
    final_synthetise = pd.merge(left, right, left_on='intervention_synthetise_id', right_index=True, how='left')

    # attention, il y a un problème dans les données historique (juste 2 actions qui posent problème...)
    final_synthetise = final_synthetise.reset_index().drop_duplicates(subset='id').set_index('id')

    # Attention, on ne doit corriger que si ce n'est pas un mélange de variété / ou d'espèce !
    final_synthetise_1 = final_synthetise.loc[(final_synthetise['melange_especes']=='f') & (final_synthetise['melange_varietes'] == 'f')]
    final_synthetise_2 = final_synthetise.loc[(final_synthetise['melange_especes']=='t') | (final_synthetise['melange_varietes'] == 't')]

    final_synthetise.loc[final_synthetise_1.index, 'rendement_moy_corr'] = final_synthetise_1['rendement_moy'] * (final_synthetise_1['surface_relative_corrigee']) / final_synthetise_1['surface_relative_corrigee_totale']
    final_synthetise.loc[final_synthetise_1.index, 'rendement_median_corr'] = final_synthetise_1['rendement_median'] * (final_synthetise_1['surface_relative_corrigee']) / final_synthetise_1['surface_relative_corrigee_totale']
    final_synthetise.loc[final_synthetise_1.index, 'rendement_max_corr'] = final_synthetise_1['rendement_max'] * (final_synthetise_1['surface_relative_corrigee']) / final_synthetise_1['surface_relative_corrigee_totale']
    final_synthetise.loc[final_synthetise_1.index,'rendement_min_corr'] = final_synthetise_1['rendement_min'] * (final_synthetise_1['surface_relative_corrigee']) / final_synthetise_1['surface_relative_corrigee_totale']
    final_synthetise.loc[final_synthetise_1.index, 'commercialisation_pct_corr'] = final_synthetise_1['commercialisation_pct'] * (final_synthetise_1['surface_relative_corrigee']) / final_synthetise_1['surface_relative_corrigee_totale']
    final_synthetise.loc[final_synthetise_1.index, 'autoconsommation_pct_corr'] = final_synthetise_1['autoconsommation_pct'] * (final_synthetise_1['surface_relative_corrigee']) / final_synthetise_1['surface_relative_corrigee_totale']
    final_synthetise.loc[final_synthetise_1.index, 'nonvalorisation_pct_corr'] = final_synthetise_1['nonvalorisation_pct'] * (final_synthetise_1['surface_relative_corrigee']) / final_synthetise_1['surface_relative_corrigee_totale']

    final_synthetise.loc[final_synthetise_2.index, 'rendement_moy_corr'] = final_synthetise_2['rendement_moy']
    final_synthetise.loc[final_synthetise_2.index, 'rendement_median_corr'] = final_synthetise_2['rendement_median']
    final_synthetise.loc[final_synthetise_2.index, 'rendement_max_corr'] = final_synthetise_2['rendement_max']
    final_synthetise.loc[final_synthetise_2.index,'rendement_min_corr'] = final_synthetise_2['rendement_min']
    final_synthetise.loc[final_synthetise_2.index, 'commercialisation_pct_corr'] = final_synthetise_2['commercialisation_pct']
    final_synthetise.loc[final_synthetise_2.index, 'autoconsommation_pct_corr'] = final_synthetise_2['autoconsommation_pct']
    final_synthetise.loc[final_synthetise_2.index, 'nonvalorisation_pct_corr'] = final_synthetise_2['nonvalorisation_pct']

    final_synthetise = final_synthetise.groupby(['destination_id', 'rendement_unite', 'action_id']).agg({
        'rendement_moy_corr' : 'sum',
        'rendement_median_corr' : 'sum',
        'rendement_max_corr' : 'sum',
        'rendement_min_corr' : 'sum', 
        'commercialisation_pct_corr' : 'sum',
        'autoconsommation_pct_corr' :'sum',
        'nonvalorisation_pct_corr' : 'sum'
    }).reset_index().replace(0, np.NaN).round(2)

    return final_synthetise

# FONCTION POUR LES RECOLTES
def get_recolte_outils_can(
    donnees
):
    """ 
        permet d'obtenir les informations sur les récoltes en réalisé
        Attention : 
        - on veut un seul résultat par action de récolte (pas par action de valorisation)
        - le résultat diffère en fonction de s'il s'agit d'un mélange d'espèce ou non (soit on fait la moyenne pondérée, soit on fait la somme)
        - il y a plusieurs problèmes historiques sur les données (répartition des espèces absentes, mélanges d'especes non renseigné...)

        à la fin, la clé unique est : 
            - 'destination_id', 'rendement_unite', 'action_id'
    """
    resultat_realise = get_recolte_realise_outils_can(donnees)
    resultat_synthetise = get_recolte_synthetise_outils_can(donnees)
    final = pd.concat([resultat_realise, resultat_synthetise])

    return final

# FONCTION POUR ASSOLEES_SYNTHETISE 
def get_culture_indicateur_branche(
    donnees
):
    """
        Permet d'obtenir L'information (d'après moi inexploitable) de culture_indicateur_branche telle
        qu'on la trouve dans les exports en masse
    """
    df_noeuds_synthetise = donnees['noeuds_synthetise'].set_index('id')
    

    return 0