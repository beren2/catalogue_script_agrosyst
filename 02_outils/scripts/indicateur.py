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



def formatage_referentiel_donnees_attendue(df):
    '''Transforme le dataframe du référentiel des données attendues 1 lignes = 1 codedephy
        en un dataframe 1 lignes = codedephy * campagne
    arg : 
        df, dataframe
    return : df, dataframe
    '''
    # Referentiel interne fourni par la CAN, : saisies attendues pour chaque codephy par campagnes au vu des entrees et sorties des agriculteurs
    # "PZ0 attendu" OU "donnees annuelles attendues" OU "Pas de donnees attendues"
    # 1 ligne pour chaque codephy
    df = df.rename(columns={'codes_SdC' : 'code_dephy'})

    # FORMATAGE DU DATA SAISIES ATTENDUES : => 1 ligne = code_dephy * campagne * donnee_attendue
    cols_to_keep = [col for col in df.columns if '20' in col]
    cols_to_keep.append('code_dephy')
    df_melt = pd.melt(df[cols_to_keep], id_vars=['code_dephy'],var_name='campagne',value_name='donnee_attendue')
    df_melt['campagne'] = df_melt['campagne'].astype('str')

    # certains code dephy ont le pz0 qui est inconnu
    df_melt.fillna({'donnee_attendue' : 'inconnu'}, inplace=True)

    # Renommage des modalités 
    df_melt.loc[df_melt['donnee_attendue'] == "PZ0 attendu",'donnee_attendue'] = "pz0"
    df_melt.loc[df_melt['donnee_attendue'] == "donnees annuelles attendues",'donnee_attendue'] = "post"
    df_melt.loc[df_melt['donnee_attendue'] == "Pas de donnees attendues",'donnee_attendue'] = "non-attendu"

    df_melt['code_dephy'] = df_melt['code_dephy'].str.upper()

    return(df_melt)

def str_replace_code_dephy(df,regex_pattern,pattern_replace):
    ''' Remplace un pattern dans la colonne code_dephy
    arg : 
        df : data.frame, avec une colonne 'code_dephy'
        regex_pattern : str, motif recherche
        pattern_replace : str, motif de remplacement
    
    return : data.frame
    '''
    df = df.replace(to_replace={'code_dephy': regex_pattern},value=pattern_replace,regex=True)
    return(df)

def selection_sdc_interet(df_domaine,df_dispositif,df_sdc):
    ''' Selectionne les systemes de culture d'interet : DEPHY_FERME & DETAILLE
        ceux uniquements présents dans le référentiel
    arg : 
        df_domaine,df_dispositif,df_sdc : data.frame

    return : df_sdc : data.frame
    
    '''
    # Recuperation de la campagne du domaine
    df_domaine.loc[:, 'campagne'] = df_domaine['campagne'].astype('str')
    df_dispositif = pd.merge(df_dispositif, df_domaine, left_on='domaine_id', right_index = True, how = 'inner')
    
    # Selection des dephy_ferme uniquement. Les donnees autres ne seront pas dans la sortie
    df_sdc = pd.merge(df_sdc, df_dispositif, left_on = 'dispositif_id', right_index = True, how = 'left').rename(columns={'id_x' : 'sdc_id'})
    df_sdc = df_sdc[df_sdc['type'] == 'DEPHY_FERME']

    # Selection des suivis detailles uniquement, sinon pas de codeDEPHY
    df_sdc = df_sdc[df_sdc['modalite_suivi_dephy'] == 'DETAILLE']

    # TRAITEMENT DE CHAINE DE CHARACTERE DES CODES DEPHY SAISIS
    # mettre tous les codes dephy en majuscules
    df_sdc['code_dephy'] = df_sdc['code_dephy'].str.upper()

    str_to_remove = ['^PPZ_',' PZ','NOYER$','AB$','BACHE$','HERBE$','-','_','\\t',' ']
    for s in str_to_remove:
        df_sdc = str_replace_code_dephy(df_sdc,s,'')

    df_sdc = str_replace_code_dephy(df_sdc,'GFC','GCF')
    df_sdc = str_replace_code_dephy(df_sdc,'LEF','LGF')
    df_sdc = str_replace_code_dephy(df_sdc,'lgf','LGF')

    # remplacement de certains codes (fait par la CAN)
    df_sdc = str_replace_code_dephy(df_sdc,'GC38922','GCF38922')
    df_sdc = str_replace_code_dephy(df_sdc,'PY27671','PYF27671')
    df_sdc = str_replace_code_dephy(df_sdc,'',np.nan)

    df_sdc = df_sdc[['code_dephy','campagne']]
    
    return(df_sdc)

def join_saisies_with_ref_donnees_attendues(df_sdc, df_synthetise, saisies_attendues):
    ''' Fait la jointure entre les saisies et le référentiel des donnnees attendues
    arg : 
        df_sdc : data.frame, issue de selection_sdc_interet()
        df_synthetise : data.frame
        saisies_attendues : data.frame, issu de formatage_referentiel_donnees_attendue()
    
    return :
        identif_pz0 : data.frame, avec ['sdc_id', 'synthetise_id','donnee_attendue']
    '''
    # LA JOINTURE SE FAIT avec LES CAMPAGNES DU SYNTHETISE ou la campagne du domaine pour les realises
    # UN PZ0 = un synthétisé et un tri annuel
    # !!! Un pz0 ne peut donc pas etre un réalisé (une zone) 
    # => mais on integre quand meme les zones pour les taguer "post-pz0" ou bien "incorrect : campagne non attendue"
    
    # On distribue les synthétisés pluriannuels => 1 ligne par campagne du synthetise
    df_synthetise['campagnes'] = df_synthetise['campagnes'].str.split(', ')
    df_synthetise_distrib = df_synthetise.explode('campagnes').rename(columns = {'campagnes' : 'campagnes_dis'}).reset_index()

    # On joint les synthetises sur les sdc pour garder les realises (les zones seront integrees à la fin)
    # si realise, campagne_dis = campagne du domaine
    df_sdc_distrib = pd.merge(df_sdc, df_synthetise_distrib, left_index = True, right_on='sdc_id', how = 'left').rename(columns = {'id' : 'synthetise_id'})

    df_sdc_distrib.loc[df_sdc_distrib['synthetise_id'].isna(),'campagnes_dis'] = df_sdc_distrib.loc[df_sdc_distrib['synthetise_id'].isna(),'campagne']

    # JOINTURE
    left = df_sdc_distrib
    right = saisies_attendues
    identif_distrib = pd.merge(left, right, left_on=['code_dephy','campagnes_dis'],right_on=['code_dephy','campagne'], how = 'left').rename(columns={'campagne_x' : 'campagne_domaine'})
    identif_distrib = identif_distrib.drop(['campagne_y'], axis = 1)

    identif_distrib['donnee_attendue'] = identif_distrib['donnee_attendue'].fillna('inconnu')
    
    # On fait l'inverse de la distribution, on concatene les cas de synthetises pluriannuel pour retrouver 1 ligne par synthetise 
    # On obtiens des donnnees attendues de type "non-attendue,pz0,pz0"
    identif_pz0 = identif_distrib.groupby(['code_dephy','sdc_id','campagne_domaine','synthetise_id'], dropna=False).agg({
        'campagnes_dis' : ', '.join,
        'donnee_attendue' : ', '.join
        }).reset_index()
    
    # Un realise ne peux pas etre un pz0, on les transforme en pz0
    # si ils chevauchent avec le pz0 ils seront tagues comme "incorrect : chevauchement pz0" 
    identif_pz0.loc[identif_pz0['synthetise_id'].isna(),'donnee_attendue'] = "post"

    return(identif_pz0)
    

def identification_pz0(donnees):
    '''
    Qualifie chaque entité : synthétise OU zone par :
        "pz0", OU "post-pz0", OU
        "incorrect : chevauchement pz0",
        "incorrect : saisie pz0 non acceptable", -> tague toute la frise chronologique = ne laisse pas post
        "incorrect : code dephy inconnu" pour les dispositifs DEPHY_FERME. -> tague toute la frise chronologique
    La méthode fait intervenir un référentiel externe , produit par la CAN des données attendues qui peut être partageable si il n'y a que les codes dephy * campagne * donnee_attendue
    
    Ce reférentiel peut contenir des erreurs. La procédure de vérification est externe à la fonction et se fait via le main des outils

    Returns:
        pd.DataFrame:
            `index` : entite_id -> synthetise_id OU zone_id
            `pz0 ` : tag "pz0" OU "post-pz0" ou "incorrect : xxx"

    !!! NE SONT PAS DANS LA SORTIE : 
        - autre que dephy_ferme
        - autre que suivi detaille
    '''
    df_domaine = donnees['domaine'].set_index('id')
    df_dispositif = donnees['dispositif'].set_index('id')
    df_sdc = donnees['sdc'].set_index('id')
    df_synthetise = donnees['synthetise'].set_index('id')
    df_parcelle = donnees['parcelle'].set_index('id')
    df_zone = donnees['zone'].set_index('id')
    saisies_attendues = donnees['BDD_donnees_attendues_CAN']
    
    # formatage du tableau des données attendues
    saisies_attendues_melt = formatage_referentiel_donnees_attendue(saisies_attendues)

    # selection des systemes de culture d'interet
    df_sdc = selection_sdc_interet(df_domaine, df_dispositif,df_sdc)

    identif_pz0 = join_saisies_with_ref_donnees_attendues(df_sdc, df_synthetise, saisies_attendues_melt)
    
    # ETAT DES LIEUX 
    print("ETAT DES LIEUX")
    print(identif_pz0.groupby(by='donnee_attendue').size())

    # les campagnes synthetise pluriannuelles ont elles des doublons ? 

    # code dephy avec 1 seulle saisie de campagne pz0 
    # -> regarder si pz0 non acceptable
    # -> regarder si chevauchement

    # code dephy avec plusieurs saisies de campagne pz0
    # -> choix du pz0 si acceptable
    # -> regarder si chevauchement

    # donnees non attendues 
    
    return()
    # df_identification_pz0 = merge.set_index('id')
    #return(df_identification_pz0)

