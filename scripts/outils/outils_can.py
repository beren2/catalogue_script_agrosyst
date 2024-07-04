"""
	Regroupe les fonctions permettant de générer les outils utiles lors de la génération du magasin "CAN".
"""
import numpy as np
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
    df_action_realise_extanded.loc[
        df_action_realise_extanded['type'] == 'APPLICATION_DE_PRODUITS_PHYTOSANITAIRES', 'proportion_surface_traitee_phyto'
    ] = df_action_realise_extanded['proportion_surface_traitee']

    df_action_realise_extanded.loc[
        df_action_realise_extanded['type'] == 'APPLICATION_DE_PRODUITS_PHYTOSANITAIRES', 'psci_phyto'
    ] = df_action_realise_extanded['proportion_surface_traitee'] *  df_action_realise_extanded['freq_spatiale'] * df_action_realise_extanded['nombre_de_passage']

    # Pour la lutte biologique :
    df_action_realise_extanded.loc[
        df_action_realise_extanded['type'] == 'LUTTE_BIOLOGIQUE', 'proportion_surface_traitee_lutte_bio'
    ] = df_action_realise_extanded['proportion_surface_traitee']

    df_action_realise_extanded.loc[
        df_action_realise_extanded['type'] == 'LUTTE_BIOLOGIQUE', 'psci_lutte_bio'
    ] = df_action_realise_extanded['proportion_surface_traitee'] *  df_action_realise_extanded['freq_spatiale'] * df_action_realise_extanded['nombre_de_passage']

    # Pour l'irrigation : 
    df_action_realise_extanded.loc[
        df_action_realise_extanded['type'] == 'IRRIGATION', 'quantite_eau_mm'
    ] = df_action_realise_extanded['eau_qte_moy_mm']

    intervention_actions_indicateurs = df_action_realise_extanded.groupby(['label', 'intervention_realise_id']).agg({
        'proportion_surface_traitee_phyto' : np.mean,
        'psci_phyto' : np.mean, 
        'proportion_surface_traitee_lutte_bio' : np.mean, 
        'psci_lutte_bio' : np.mean,
        'quantite_eau_mm' : np.mean
    })

    intervention_actions_indicateurs[
        ['proportion_surface_traitee_phyto', 'psci_phyto', 'proportion_surface_traitee_lutte_bio', 'psci_lutte_bio', 'quantite_eau_mm']
    ] = intervention_actions_indicateurs[
        ['proportion_surface_traitee_phyto', 'psci_phyto', 'proportion_surface_traitee_lutte_bio', 'psci_lutte_bio', 'quantite_eau_mm']
    ].applymap(convert_to_int)

    return intervention_actions_indicateurs

def get_intervention_realise_semence_outils_can(
        donnees
    ):
    """
        TODO
    """
    #df_action_realise = donnees['action_realise']
    #df_intervention_realise = donnees['intervention_realise']
    #df_composant_action_semis = donnees['composant_action_semis']
    df_semence = donnees['semence']
    df_composant_culture = donnees['composant_culture']
    df_espece = donnees['espece']
    #df_variete = donnees['variete']
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
    right = get_intervention_realise_action_outils_can(donnees).reset_index().rename(columns={'intervention_realise_id': 'id', 'label' : 'interventions_actions'} )
    merge = pd.merge(left, right, on='id', how='left')

    # ajout des informations sur la table semis
    left = merge 
    right = get_intervention_realise_semence_outils_can(donnees).reset_index().rename(columns={'intervention_realise_id': 'id'})
    merge = pd.merge(left, right, on='id', how='left')


    columns = ['id', 'interventions_actions', 'especes_semees', 'densite_semis', 'unite_semis', 'traitement_chimique_semis', 
               'inoculation_biologique_semis', 'type_semence', 'proportion_surface_traitee_phyto', 'psci_phyto', 
               'proportion_surface_traitee_lutte_bio', 'psci_lutte_bio', 'quantite_eau_mm']
    # ajout des informations sur les espèces concernées
    #get_intervention_realise_especes_concernes_outils_can 
    return merge[columns]


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
    return merge