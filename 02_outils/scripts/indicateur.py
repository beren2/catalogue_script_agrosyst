"""
	Regroupe les fonctions qui consistent en des calculs d'indicateurs 
"""

import pandas as pd
import numpy as np
from scripts.utils import fonctions_utiles
from scripts.utils import get_surfaces_connections_synthetise

def get_surface_connexion_synthetise(
        donnees
):
    """
    Permet d'obtenir un DataFrame où on associe à une connexion en synthétisé la surface imputable à cette connexion.
    Cette fonction utilise notamment un calcul de la répartition du flux dans la description de la rotation.
    Elle se base aussi :
        - sur la surface déclarée dans le domaine
        - sur le pourcentage de surface du domaine alloué au système de culture
        - sur la présence ou non de cultures perennes dans le même système synthétisé
        
    Note(s):
        - Une surface nulle peut signifier : 
            - que certaines connexions ont un poids de 0 dans l'assolement
            - que le graph est "mal formé", c'est à dire qu'il existe des poids absurdes
            - qu'aucune intervention n'a été renseigné pour l'ensemble de l'assolement.

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames suivants :
            - 'synthetise' : Informations sur les systèmes synthétisés
            - 'culture' : Informations sur les cultures
            - 'noeuds_synthetise' : Informations sur les noeuds en synthétisé
            - 'connection_synthetise' : Informations sur les connexion en synthétisé
            - 'intervention_synthetise' : Information sur les interventions en synthétisé
            - 'plantation_perenne_synthetise' : Informations sur les plantations perennes en synthétisés
            - 'sdc' : Informations sur les systèmes de cultures
            - 'dispositif' : Informations sur les dispositifs
            - 'domaine' : Informations sur les domaines

    Returns:
        pd.DataFrame:
            Un DataFrame avec les informations suivantes par connexion synthétisé (`connection_synthetise_id`) :
            - `surface (ha)` : valeur de la surface de la connexion en hectare

    Exemple d'utilisation :
        donnees = {
            'synthetise': pd.DataFrame(...),
            'culture': pd.DataFrame(...),
            'noeuds_synthetise': pd.DataFrame(...),
            ...
        }
        result = get_surfaces_connections_synthetise(donnees)
    """

    res = get_surfaces_connections_synthetise.get_surfaces_connections_synthetise(
        donnees['synthetise'].set_index('id'),
        donnees['culture'].set_index('id'),
        donnees['noeuds_synthetise'].set_index('id'),
        donnees['connection_synthetise'].set_index('id'),
        donnees['intervention_synthetise'].set_index('id'),
        donnees['plantation_perenne_synthetise'].set_index('id'),
        donnees['sdc'].set_index('id'),
        donnees['dispositif'].set_index('id'),
        donnees['domaine'].set_index('id')
    )

    res = res.rename(index={'id' : 'connection_synthetise_id'})
    return res

def indicateur_utilisation_intrant(donnees):
    """ 
        fonction permettant d'obtenir pour chaque utilsation d'intrants, la dose de référence utilisée
    """
    df_utilisation_intrant_realise = fonctions_utiles.get_infos_all_utilisation_intrant(
        donnees, saisie = 'realise'
    )

    df_utilisation_intrant_synthetise = fonctions_utiles.get_infos_all_utilisation_intrant(
        donnees, saisie = 'synthetise'
    )
    
    res = pd.concat([df_utilisation_intrant_realise, df_utilisation_intrant_synthetise], axis=0)

    # obtention des doses toutes dans la même unité (par défaut : KG_HA)
    donnees['utilisation_intrant'] = res
    left = res.dropna(subset=['id'])
    right = fonctions_utiles.get_utilisation_intrant_in_unit(donnees).dropna(subset=['id'])
    right['id'] = right['id'].astype('object')
    merge = pd.merge(left, right, left_on='id', right_on='id', how='left')


    return merge[
        [
            'id', 'dose_ref_maa', 'unit_dose_ref_maa', 
            'code_culture_maa', 'code_groupe_cible_maa', 'code_traitement_maa', 'dose_unite_standardise', 'unite_standardise'
        ]
    ].set_index('id')


def str_replace_code_dephy(df,regex_pattern,pattern_replace):
    ''' Remplace un pattern dans la colonne code_dephy
    '''
    df = df.replace(to_replace={'code_dephy': regex_pattern},value=pattern_replace,regex=True)
    return(df)

def sdc_donnee_attendue(donnees):
    '''
    Qualifie chaque sdc (code dephy * campagne) par "PZ0 attendu" OU "Pas de donnees attendues" OU "donnees annuelles attendues" OU "inconnue dephy ferme" pour les dispositifs DEPHY_FERME.
    Pour les sdc d autres dispositif : "inconnue : hors dephy ferme ou suivi non detaille"
    La méthode fait intervenir un référentiel produit par la CAN des données attendues : NON PARTAGEABLE
    '''
    df_dispositif = donnees['dispositif']
    df_sdc = donnees['sdc']
    
    # Referentiel interne fourni par la CAN, NON PARTAGEABLE : saisies attendues au vu des entrees et sorties des agriculteurs
    # 1 ligne pour chaque sdc
    saisies_attendues = donnees['BDD_donnees_attendues_CAN']
    saisies_attendues = saisies_attendues.rename(columns={'codes_SdC' : 'code_dephy'})

    # formatage du data saisies_attendues : pour [code_dephy,campagne] est ce un pz0 attendu ou une donnee annuelle
    # => 1 ligne pour un sdc*campagne
    cols_to_keep = [col for col in saisies_attendues.columns if '20' in col]
    cols_to_keep.append('code_dephy')
    saisies_attendues_melt = pd.melt(saisies_attendues[cols_to_keep], id_vars=['code_dephy'],var_name='campagne',value_name='donnee_attendue')
    saisies_attendues_melt['campagne'] = saisies_attendues_melt['campagne'].astype('str')
    saisies_attendues_melt['donnee_attendue'].fillna('inconnue dephy ferme', inplace=True)

    # selection des colonnes utiles
    df_dispositif = df_dispositif[['id','type']]
    df_sdc = df_sdc[['id','campagne','code_dephy','dispositif_id','filiere','modalite_suivi_dephy']]
    df_sdc.loc[:, 'campagne'] = df_sdc['campagne'].astype('str')

    # Selection des dephy_ferme
    df_sdc = pd.merge(df_sdc, df_dispositif, left_on = 'dispositif_id', right_on = 'id', how = 'left').rename(columns={'id_x' : 'sdc_id'})

    # Traitement de chaine de caractere
    # mettre tous les codes dephy en majuscules
    df_sdc['code_dephy'] = df_sdc['code_dephy'].str.upper()
    saisies_attendues_melt['code_dephy'] = saisies_attendues_melt['code_dephy'].str.upper()

    str_to_remove = ['^PPZ_',' PZ','NOYER$','AB$','BACHE$','HERBE$','-','_','\\t',' ']
    for s in str_to_remove:
        df_sdc = str_replace_code_dephy(df_sdc,s,'')

    df_sdc = str_replace_code_dephy(df_sdc,'GFC','GCF')
    df_sdc = str_replace_code_dephy(df_sdc,'LEF','LGF')
    df_sdc = str_replace_code_dephy(df_sdc,'lgf','LGF')

    df_sdc = str_replace_code_dephy(df_sdc,'GF35712','GCF35712')
    df_sdc = str_replace_code_dephy(df_sdc,'GC31515','GCF31515')
    df_sdc = str_replace_code_dephy(df_sdc,'GC38922','GCF38922')
    df_sdc = str_replace_code_dephy(df_sdc,'PY10486','PYF10486')
    df_sdc = str_replace_code_dephy(df_sdc,'PY27671','PYF27671')
    df_sdc = str_replace_code_dephy(df_sdc,'VI28987','VIF28987')

    df_sdc = str_replace_code_dephy(df_sdc,'',np.nan)

    # Merge 'left' entre les donnees saisies sur agrosyst et le referentiel des donnees attendues par la CAN    
    merge = pd.merge(df_sdc, saisies_attendues_melt, left_on=['code_dephy','campagne'],right_on=['code_dephy','campagne'], how = 'left')
    merge['donnee_attendue'] = merge['donnee_attendue'].fillna('')
    
    # tag des sdc non dephy ou suivi non detaille
    merge['donnee_attendue'] = merge.apply(
        lambda x: 'inconnue dephy ferme' if (x['donnee_attendue'] == '') & (
                                             (x['type'] == 'DEPHY_FERME') &
                                             (x['modalite_suivi_dephy'] == 'DETAILLE')) else x['donnee_attendue'] , axis=1)
    
    merge['donnee_attendue'] = merge.apply(
        lambda x: 'inconnue : hors dephy ferme ou suivi non detaille' if (x['donnee_attendue'] == '') & (
                                                                        (x['type'] != 'DEPHY_FERME') |
                                                                        (x['modalite_suivi_dephy'] != 'DETAILLE')) else x['donnee_attendue'] , axis=1)
    
    # print("Repartition de l'attribution des donnees attendues")
    # print(merge.groupby(by='donnee_attendue').size())
    
    return(merge[['sdc_id','code_dephy','campagne','donnee_attendue']])



def get_typologie_culture_rotation_CAN(donnees):
    ''' 
    Le but est d'obtenir les typologies de culture et de rotation utilisées par la Cellule référence.

    Note(s):
        Eventuellement à mettre dans Agrosyst directement
        La typologie espece a été directement intégré au référentiel refespece d'Agrosyst

    Echelle :
        culture_id

    Args:
        donnees (dict):
            Données d'entrepot
            - 'composant_culture'
            - 'culture'
            Données externe (référentiel CAN):
            - 'typo_especes_typo_culture.csv'
            - 'typo_especes_typo_culture_marai.csv'

    Returns:
        pd.DataFrame() contenant la culture_id et la typologie de culture de la CAN
    '''
    cropsp = donnees['composant_culture'][['espece_id','culture_id']]
    crop = donnees['culture'][['type']]
    sp = donnees['espece_vCAN'][['typocan_espece','typocan_espece_maraich']]
    # Tant que le référentiel n'est pas pret (ajout des deux colonnes de la can)
    # sp = donnees['espece'][['id','typocan_espece','typocan_espece_maraich']]
    typo1 = donnees['typo_especes_typo_culture'].rename(columns={
        'TYPO_ESPECES':'typocan_espece', 'Typo_Culture':'typocan_culture'})
    typo2 = donnees['typo_especes_typo_culture_marai'].rename(columns={
        'TYPO_ESPECES_BIS':'typocan_espece_maraich', 'Typo_Culture_bis':'typocan_culture_maraich'})

    df = cropsp.merge(sp, how = 'left', left_on = 'espece_id', right_on = 'id')

    df['nb_espece'] = 1
    df['nb_typocan_esp'] = df['typocan_espece']
    df['nb_typocan_esp_maraich'] = df['typocan_espece_maraich']

    def concat_unique_sorted(series):
        cleaned = series.dropna().unique()
        if len(cleaned) == 0:
            return np.nan
        return '_'.join(sorted(cleaned))
    def get_nb_unique_typo(series):
        cleaned = series.dropna().unique()
        return len(cleaned)
    agg_dict = {
        'typocan_espece': concat_unique_sorted,
        'typocan_espece_maraich': concat_unique_sorted,
        'nb_espece': 'sum',
        'nb_typocan_esp': get_nb_unique_typo,
        'nb_typocan_esp_maraich': get_nb_unique_typo
    }
    df = df[['culture_id','typocan_espece','typocan_espece_maraich',
             'nb_espece','nb_typocan_esp','nb_typocan_esp_maraich']].groupby('culture_id').agg(agg_dict).reset_index()

    
    df = df.merge(crop, how='left', left_on='culture_id', right_on='id')
    df = df.merge(typo1, how='left', on='typocan_espece')
    df = df.merge(typo2, how='left', on='typocan_espece_maraich')

    df.loc[df.type == 'INTERMEDIATE', ['typocan_culture','typocan_culture_maraich']] = ['Culture intermédiaire', 'Culture intermédiaire']

    df = df.set_index('culture_id')
    # Ajout de 'Culture porte-graine' ??
    # Surement un changement de culture au niveau des interventions dans le contexte d'une destination production de semence
    # Du coup utilisation du nom de la culture pour changement non souhaité

    return df
