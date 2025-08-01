"""
	Regroupe les fonctions qui consistent en des calculs d'indicateurs 
"""

import os
from concurrent.futures import ProcessPoolExecutor
from functools import partial
import pandas as pd
import numpy as np
from tqdm import tqdm
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

    # certains code dephy ont le pz0 qui est inconnu. On supprime ces lignes, c'est comme si le code dephy est inconnu
    df = df.dropna()

    if df.shape[0] == 0:
        print('Attention vérifiez le référentiel à propos des na ! lors de la suppresion des lignes avec nan pour les inconnu toutes les lignes ont été supprimées')

    # FORMATAGE DU DATA SAISIES ATTENDUES : => 1 ligne = code_dephy * campagne * donnee_attendue
    cols_to_keep = [col for col in df.columns if '20' in col]
    cols_to_keep.append('code_dephy')
    df_melt = pd.melt(df[cols_to_keep], id_vars=['code_dephy'],var_name='campagne',value_name='donnee_attendue')
    df_melt['campagne'] = df_melt['campagne'].astype('str')

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

def select_sdc_interet(df_domaine,df_dispositif,df_sdc):
    ''' Selectionne les systemes de culture d'interet : DEPHY_FERME & DETAILLE
        ceux uniquements présents dans le référentiel
    arg : 
        df_domaine,df_dispositif,df_sdc : data.frame

    return : df_sdc : data.frame
    
    '''
    # Recuperation de la campagne du domaine
    df_domaine['campagne'] = df_domaine['campagne'].astype('str')
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
        df_sdc : data.frame, issue de select_sdc_interet()
        df_synthetise : data.frame
        saisies_attendues : data.frame, issu de formatage_referentiel_donnees_attendue()
    
    return :
        identif_pz0 : data.frame, avec index ['sdc_id', 'synthetise_id'] et colonne ['donnee_attendue']
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
    identif_distrib['campagnes_dis'] = identif_distrib['campagnes_dis'].astype("str")
    identif_pz0 = identif_distrib.groupby(['code_dephy','sdc_id','campagne_domaine','synthetise_id'], dropna=False).agg({
        'campagnes_dis' : ', '.join,
        'donnee_attendue' : ', '.join
        }).reset_index().rename(columns = {'campagnes_dis' : 'campagnes'})
    
    # Un realise ne peux pas etre un pz0, on les transforme en pz0
    # si ils chevauchent avec le pz0 ils seront tagues comme "incorrect : chevauchement pz0" 
    identif_pz0.loc[(identif_pz0['synthetise_id'].isna()) & (identif_pz0['donnee_attendue'] == "pz0"),'donnee_attendue'] = "post"

    return(identif_pz0.set_index(['sdc_id','synthetise_id']))
    
def do_tag_pz0_not_correct(df,code_dephy_select,pattern_pz0_correct,modalite_pz0_chevauchement,modalite_pz0_non_acceptable):
    ''' Tague les frises des pz0 non acceptables
    arg :
        df : data.frame : issu de join_saisies_with_ref_donnees_attendues()
        code_dephy_select : pd.serie, serie de code_dephy à traiter
        pattern_pz0_correct : list de chr, valeurs de la colonne "donnee_attendue" que l'on juge acceptable
        modalite_pz0_chevauchement : chr, modalite a attribuer
        modalite_pz0_non_acceptable : chr, modalité a attribuer
    
    return :
        df_res : data.frame, issu de df, où les données ont été taguées
        dephy_mono : list, liste des codes dephy ayant un pz0 mono annuel
    '''

    select_df = df.loc[df['code_dephy'].isin(code_dephy_select.to_list())]
    unselect_df = df.loc[~ df['code_dephy'].isin(code_dephy_select.to_list())]

    # Mettre en évidence synthetises pz0 uniquement monoannuels 
    pz0 = select_df.loc[select_df['donnee_attendue'].str.contains("pz0")].reset_index()
    
    pz0['triannuel'] = pd.Series()
    if (pz0['donnee_attendue'].str.contains(",", na=False)).any() :
        pz0.loc[pz0['donnee_attendue'].str.contains(","), 'triannuel'] = "pluri"
    
    pz0.loc[pz0['triannuel'].isna(), 'triannuel'] = "mono"

    pz0 = pz0.groupby(['code_dephy']).agg({
        'triannuel' : lambda x: ', '.join(x.unique())
        }).reset_index()
    
    dephy_mono = pz0.loc[pz0['triannuel'] == 'mono', 'code_dephy'].to_list()
    
    ## Detecter les pz0 non corrects
    
    # Attention ! parmi les pattern pz0 corrects, on a deux préférences :
    # - A) pluri annuel plutot que monoannuel
    # - B) pz0,pz0,pz0 plutot qu'autres pz0 
    # Sinon ils sont considérés comme correctes, on ne peux pas choisir et le script renvera les deux pz0

    # A) On prefere un pluriannuel plutot que monoannuel si il y a le choix donc :
    # Si le code dephy n'es pas dans dephy_mono, le pz0 mono annuel devient post. on le sauvegarde ensuite dans post
    # (Si il chevauche avec le pz0, il sera traité plus tard)
    select_df.loc[:,'donnee_attendue'] = select_df.apply(lambda x : "post" if (x['code_dephy'] not in (dephy_mono) and x['donnee_attendue'] == 'pz0') else x['donnee_attendue'], axis = 1)
 
    # sauvegarde les "post" (il n'y a plus de post,post)
    post = select_df.loc[select_df['donnee_attendue'] == "post"]
    select_df = select_df.loc[select_df['donnee_attendue'] != "post"]

    # B) Pour les pz0 pluri annuels pz0, pz0, pz0 : 
    code_dephy_000 = select_df.loc[select_df['donnee_attendue'] == "pz0, pz0, pz0", 'code_dephy'].to_list()
    select_df.loc[select_df['code_dephy'].isin(code_dephy_000),'donnee_attendue'] = select_df.loc[select_df['code_dephy'].isin(code_dephy_000)].apply(
        lambda x : 'pz0' if x['donnee_attendue'] == "pz0, pz0, pz0"
                            else modalite_pz0_chevauchement, axis = 1)

    # C) Pour les pz0 pluri annuels restants : 
    # tag des lignes correctes
    select_df.loc[:,'to_keep'] = select_df.apply(lambda x : x['donnee_attendue'] in (pattern_pz0_correct) , axis = 1)
    
    dephy_correct = select_df.loc[select_df['to_keep'], 'code_dephy'].to_list()
    
    # si code dephy n'a aucun pz0 qui est dans la liste pattern_pz0_correct : pz0 non acceptable pour toute la frise
    select_df.loc[:,'donnee_attendue'] = select_df.apply(lambda x : modalite_pz0_non_acceptable if (x['code_dephy'] not in (dephy_correct))
                                                                            else x['donnee_attendue'] , axis = 1)
    
    # si le code dephy est dans dephy_correct, mais que la ligne de select_df to_keep = False => chevauchement pz0, puisqu'il y a mieux
    select_df.loc[:,'donnee_attendue'] = select_df.apply(lambda x : modalite_pz0_chevauchement if (x['code_dephy'] in (dephy_correct)) & (x['to_keep'] is False)
                                                                            else x['donnee_attendue'] , axis = 1)    
    
    # si le code dephy est dans dephy_correct, mais que la ligne de select_df to_keep = True => c'est le pz0 à choisir
    # Attention si la frise a deux saisies de même ''valeur'' , ex : 'NA,pz0,pz0', à ce stade ils sont tagués tous les deux pz0
    # On ne peut pas choisir, ils seront tagués comme non acceptable suite au control_nb_pz0_per_codedephy()
    select_df.loc[:,'donnee_attendue'] = select_df.apply(lambda x : "pz0" if (x['code_dephy'] in (dephy_correct)) & (x['to_keep'] is True)
                                                                            else x['donnee_attendue'] , axis = 1)    
    
    select_df = select_df.drop(['to_keep'], axis = 1)

    # Pour les post sauvegardes à part dont leur code dephy n'a pas de pz0 acceptable, les taguer aussi en pz0 non acceptable"
    code_dephy_nonacceptable = select_df.loc[select_df['donnee_attendue'] == modalite_pz0_non_acceptable,'code_dephy'].to_list()
    post.loc[post['code_dephy'].isin(code_dephy_nonacceptable), 'donnee_attendue'] = modalite_pz0_non_acceptable

    df_res = pd.concat([unselect_df,select_df,post])
    return(df_res,dephy_mono)


def do_correct_overlap(df,modalite_pz0_chevauchement,dephy_monoannuel):
    ''' Tague les saisies qui chevauchent avec le pz0 donc incorrectes 
        ou transforme en post si la saisie est de la derniere campagne pz0 et que le pz0 choisi est decale de 1 
        ex : pz0 = "NA, pz0, pz0" 2013,2014,2015 + monoannuel "pz0" 2016
    arg : 
        df : data.frame,
        modalite_pz0_chevauchement : str, tag a appliquer
        dephy_monoannuel : list, liste des codes dephy ayant un pz0 monoannuel

    return : data.frame modifie
    '''
    # isoler les donnees des codes dephy avec pz0 uniquement monoannuel
    df_monoannuel = df.loc[df['code_dephy'].isin(dephy_monoannuel)]
    df_not_monoannuel = df.loc[~ df['code_dephy'].isin(dephy_monoannuel)]

    # isoler les codes dephy sans pz0
    dephy_with_pz0 = df_not_monoannuel.loc[df_not_monoannuel['donnee_attendue'] == "pz0",'code_dephy'].to_list()
    df_none_pz0 = df_not_monoannuel.loc[~ df['code_dephy'].isin(dephy_with_pz0)]
    
    pz0_choosed = df_not_monoannuel.reset_index()
    pz0_choosed = pz0_choosed.loc[pz0_choosed['donnee_attendue'] == "pz0",['code_dephy','campagnes']].rename(columns = {'campagnes' : 'campagnes_pz0'})
    pz0_choosed.loc[:,'campagnes_pz0'] = pz0_choosed['campagnes_pz0'].str.split(', ')
    
    df_not_monoannuel = pd.merge(df_not_monoannuel.reset_index(),pz0_choosed, on = 'code_dephy')
    df_not_monoannuel.loc[:,'campagnes_split'] = df_not_monoannuel.loc[:,'campagnes'].str.split(', ')

    # si le min de la campagne du synthetise <= au max de la campagne pz0, il y a chevauchement
    # pour le cas de detection de post qui chevauchent
    df_not_monoannuel.loc[:,'donnee_attendue'] = df_not_monoannuel.apply(lambda x : modalite_pz0_chevauchement if ((min(x['campagnes_split']) <= max(x['campagnes_pz0']))
                                                                                                                & (x['donnee_attendue'] != 'pz0') )
                                                                                                    else x['donnee_attendue'], axis=1)
    
    # pour le cas de de plusieurs pz0 à choisir, l'un est devenu chevauchant alors que il doit etre post. ex PYF10511 2009,2010,2011 et 2012,2013,2014,2015
    df_not_monoannuel.loc[:,'donnee_attendue'] = df_not_monoannuel.apply(lambda x : "post" if ((min(x['campagnes_split']) > max(x['campagnes_pz0']))
                                                                                                                & (x['donnee_attendue'] == modalite_pz0_chevauchement) )
                                                                                                    else x['donnee_attendue'], axis=1)

    df_not_monoannuel = df_not_monoannuel.drop('campagnes_pz0', axis = 1)
    df_not_monoannuel = df_not_monoannuel.set_index(['sdc_id','synthetise_id'])

    # les pz0 mono annuels peuvent aussi avoir des chevauchements si il y a un realise de campagne pz0.
    # a ete transformé en post mais doit devenir chevauchement
    pz0_mono = df_monoannuel.reset_index()
    pz0_mono = pz0_mono.loc[pz0_mono['donnee_attendue'] == "pz0",['code_dephy','campagnes']].rename(columns = {'campagnes' : 'campagnes_pz0'})
    pz0_mono = pz0_mono.groupby(by = ['code_dephy'])['campagnes_pz0'].apply(list)

    df_monoannuel = pd.merge(df_monoannuel.reset_index(), pz0_mono, on = 'code_dephy')

    df_monoannuel.loc[:,'donnee_attendue'] = df_monoannuel.apply(
        lambda x : modalite_pz0_chevauchement if ((x['donnee_attendue'] == "post") & (x['campagnes'] <= max(x['campagnes_pz0']))) else x['donnee_attendue'] ,
    axis=1)

    df_monoannuel = df_monoannuel.drop(['campagnes_pz0'], axis=1)
    df_monoannuel = df_monoannuel.set_index(['sdc_id','synthetise_id'])

    df_modified = pd.concat([df_not_monoannuel,df_monoannuel,df_none_pz0])

    return(df_modified)

def control_nb_pz0_per_codedephy(df,dephy_monoannuel):
    ''' Controle si il y a bien 1 pz0 par code dephy
    arg : 
        df, data.frame
        dephy_monoannuel : list, liste des codes dephy ayant un pz0 monoannuel
    
    return : list, dephynb_manypz0 , codes dephy ayant plusieurs pz0
    '''
    # retirer les codes dephy avec pz0 uniquement monoannuel
    count_pz0_by_code = df.reset_index()
    count_pz0_by_code = count_pz0_by_code.loc[~ count_pz0_by_code['code_dephy'].isin(dephy_monoannuel)]

    count_pz0_by_code = count_pz0_by_code.loc[count_pz0_by_code['donnee_attendue'] == 'pz0',['code_dephy','synthetise_id']].groupby(
        by = ['code_dephy']).size().reset_index().rename(columns = {0 : 'count_pz0'})

    dephynb_manypz0 = count_pz0_by_code.loc[count_pz0_by_code['count_pz0'] > 1]['code_dephy'].to_list()

    # les pz0 mono annuels peuvent aussi être mal saisi,
    # - nb pz0 > 3 ex : 2014,2015,2016,2016 = 4 pz0
    # - ou plusieurs fois la meme annee
    count_pz0_mono = df.reset_index()
    count_pz0_mono = count_pz0_mono.loc[count_pz0_mono['code_dephy'].isin(dephy_monoannuel)]
    count_pz0_mono.loc[:,'count'] = count_pz0_mono.loc[:,'campagnes']

    count_pz0_mono = count_pz0_mono.loc[count_pz0_mono['donnee_attendue'] == 'pz0',['code_dephy','synthetise_id','campagnes','count']].groupby(
        by = ['code_dephy']).agg({
        'campagnes' : lambda x :'/ '.join(x.unique()),
        'count' : 'size'
        })
    
    count_pz0_mono.loc[:,'count_unique'] = count_pz0_mono['campagnes'].str.count('/') +1

    dephynb_pz0_notunique = count_pz0_mono.loc[count_pz0_mono['count_unique'] != count_pz0_mono['count']].index.to_list()

    return(dephynb_manypz0 + dephynb_pz0_notunique)

def check_coherence_frise_chronologique(df,modalite_pz0_non_acceptable,modalite_pz0_aucun, modalite_pz0_chevauchement, modalite_pz0_inconnu, modalite_non_attendu, modalite_pz0_plusieurs):
    ''' Controle la coherence des frises chronologiques. Retourne si y a des post avant les pz0 = Pas possible
    arg : 
        df : data.frame
        modalite_pz0_non_acceptable : str

    return bool, False si au moin une frises a un post avant le pz0
    '''
    frises = df.reset_index()

    frises.loc[frises['donnee_attendue'] == modalite_pz0_inconnu, 'donnee_attendue'] = 'inconnu'
    frises.loc[frises['donnee_attendue'] == modalite_non_attendu, 'donnee_attendue'] = 'NA'
    frises.loc[frises['donnee_attendue'] == modalite_pz0_chevauchement, 'donnee_attendue'] = 'C'
    frises.loc[frises['donnee_attendue'] == modalite_pz0_non_acceptable, 'donnee_attendue'] = 'bof'
    frises.loc[frises['donnee_attendue'] == modalite_pz0_aucun, 'donnee_attendue'] = 'X'
    frises.loc[frises['donnee_attendue'] == modalite_pz0_plusieurs, 'donnee_attendue'] = '+1'
    frises.loc[frises['donnee_attendue'] == 'pz0', 'donnee_attendue'] = '0'
    frises.loc[frises['donnee_attendue'] == 'post', 'donnee_attendue'] = 'p'

    # avoir 1 seule ligne par sdc_id si ce sont des zones 
    frises = frises.groupby(by=['code_dephy','sdc_id','synthetise_id'], dropna=False).agg({
        'donnee_attendue' : lambda x : '/ '.join(x.unique()),
        'campagnes' : lambda x :'/ '.join(x.unique())
        }).reset_index()

    frises = frises.sort_values(['code_dephy','campagnes'])
    frises = frises.loc[:,['code_dephy','donnee_attendue','campagnes']].groupby(
        by = ['code_dephy']).agg({
        'donnee_attendue' : '/ '.join,
        'campagnes' : '/ '.join
        }).reset_index()
    
    frises_summary = frises.groupby(['donnee_attendue']).size().reset_index().rename(columns = {0 : 'count'})

    test = frises_summary[frises_summary['donnee_attendue'].str.contains('p/ 0')].shape[0] != 0
    test2 = frises_summary[frises_summary['donnee_attendue'].str.contains('p/ C')].shape[0] != 0
    
    return(test & test2)

def identification_pz0(donnees):
    '''
    Qualifie chaque entité : synthétise OU zone par :
        "pz0", OU "post-pz0", OU
        "incorrect : campagne non attendue",
        "incorrect : chevauchement pz0",
        "incorrect : saisie pz0 non acceptable", -> tague toute la frise chronologique = ne laisse pas post
        "incorrect : aucun pz0 saisi", -> tague toute la frise chronologique
        "incorrect : code dephy inconnu" pour les dispositifs DEPHY_FERME. -> tague toute la frise chronologique
        "incorrect : saisie de plusieurs plusieurs pz0" -> tague toute la frise, deux pz0 acceptables ont été trouvés
    La méthode fait intervenir un référentiel externe , produit par la CAN des données attendues qui peut être partageable si il n'y a que les codes dephy * campagne * donnee_attendue
    
    Ce reférentiel peut contenir des erreurs. La procédure de vérification est externe à la fonction et se fait via le main des outils

    Returns:
        pd.DataFrame:
            `index` : entite_id -> synthetise_id OU zone_id
            `pz0 ` : tag "pz0" OU "post-pz0" ou "incorrect : xxx"

    !!! NE SONT PAS DANS LA SORTIE : 
        - autre que dephy_ferme
        - autre que suivi detaille
        - les zones et synthetises ayant aucune intervention
    '''
    message_error = ''

    # pattern pz0
    modalite_pz0_non_acceptable = "incorrect : saisie pz0 non acceptable"
    modalite_pz0_chevauchement = "incorrect : chevauchement pz0"
    modalite_pz0_inconnu = "incorrect : code dephy inconnu"
    modalite_non_attendu = "incorrect : campagne non-attendue"
    modalite_pz0_plusieurs = "incorrect : saisie de plusieurs plusieurs pz0"
    modalite_pz0_aucun = "incorrect : aucun pz0 saisi"

    df_domaine = donnees['domaine'].set_index('id')
    df_dispositif = donnees['dispositif'].set_index('id')
    df_sdc = donnees['sdc'].set_index('id')
    df_synthetise = donnees['synthetise'].set_index('id')
    df_parcelle = donnees['parcelle'].set_index('id')
    df_zone = donnees['zone'].set_index('id')
    df_intervention_synthetise_agrege = donnees['intervention_synthetise_agrege'].set_index('id')
    df_intervention_realise_agrege = donnees['intervention_realise_agrege'].set_index('id')
    saisies_attendues = donnees['BDD_donnees_attendues_CAN'].copy()
    
    # suppression des colonnes campagne du sdc et dispositif
    df_dispositif = df_dispositif.drop(['campagne'], axis = 1)
    df_sdc = df_sdc.drop(['campagne'], axis = 1)

    # retirer les zones et synthetises sur lesquelles il n'y a aucune intervention (list(set()) puisque il y a plusieurs interventions par synthetises)
    #print('nb zones sans interventions' + str(df_zone.loc[df_zone.index.isin(list(set(df_intervention_realise_agrege['zone_id'])))].shape))
    #print('nb synthetise sans interventions'+ str(df_synthetise.loc[~df_synthetise.index.isin(list(set(df_intervention_synthetise_agrege['synthetise_id'])))].shape))

    df_synthetise = df_synthetise.loc[df_synthetise.index.isin(list(set(df_intervention_synthetise_agrege['synthetise_id'])))]
    df_zone = df_zone.loc[df_zone.index.isin(list(set(df_intervention_realise_agrege['zone_id'])))]

    # puis supprimer les sdc_id qui n'ont pas de zone_id ou synthetise_id
    left = df_zone[['parcelle_id']]
    right = df_parcelle[['sdc_id']]
    df_zone_extanded = pd.merge(left,right, left_on = 'parcelle_id', right_index=True).drop('parcelle_id', axis = 1)

    df_sdc = df_sdc.loc[df_sdc.index.isin(df_zone_extanded['sdc_id'].to_list()) | df_sdc.index.isin(df_synthetise['sdc_id'].to_list())]

    # formatage du tableau des données attendues
    saisies_attendues_melt = formatage_referentiel_donnees_attendue(saisies_attendues)

    # selection des systemes de culture d'interet
    df_sdc = select_sdc_interet(df_domaine, df_dispositif,df_sdc)

    # jointure saisies - referentiel
    identif_pz0 = join_saisies_with_ref_donnees_attendues(df_sdc, df_synthetise, saisies_attendues_melt)
    
    # ETAT DES LIEUX 
    #print(identif_pz0.groupby(by='donnee_attendue').size())

    # les campagnes synthetise pluriannuelles ont elles des doublons ? 
    identif_pz0['count_campaign'] = identif_pz0['campagnes'].apply(lambda x: len(x.split(', ')))

    identif_pz0['count_unique_campaign'] = identif_pz0['campagnes'].apply(lambda x: len(set(x.split(', '))))
    
    if identif_pz0.loc[identif_pz0['count_campaign'] != identif_pz0['count_unique_campaign']].shape[0] != 0:
        message_error = message_error + "!!! Attention !!! Saisies de synthetises incorrects : campagnes en doubles"
        message_error = message_error + str(identif_pz0.loc[identif_pz0['count_campaign'] != identif_pz0['count_unique_campaign']].head(5))

    identif_pz0 = identif_pz0.drop(['count_campaign','count_unique_campaign'], axis = 1)

    # POST PLURIANNUELS , transformer en "post"
    identif_pz0.loc[identif_pz0['donnee_attendue'].str.contains('post') & ~ identif_pz0['donnee_attendue'].str.contains('non-attendu|pz0'),'donnee_attendue'] = "post"

    # Separer les codes dephy selon le nb de synthetise avec campagnes pz0
    count_pz0_by_code = identif_pz0.reset_index()
    count_pz0_by_code = count_pz0_by_code.loc[count_pz0_by_code['donnee_attendue'].str.contains('pz0'),['code_dephy','synthetise_id']].groupby(
        by = ['code_dephy']).size().reset_index().rename(columns = {0 : 'count_pz0'})

    dephy_one_synthetise_pz0 = count_pz0_by_code.loc[count_pz0_by_code['count_pz0'] == 1,'code_dephy']
    dephy_many_synthetise_pz0 = count_pz0_by_code.loc[count_pz0_by_code['count_pz0'] > 1,'code_dephy']
    dephy_none_synthetise_pz0 = identif_pz0.loc[~(identif_pz0['code_dephy'].isin(dephy_one_synthetise_pz0) | 
                                                  identif_pz0['code_dephy'].isin(dephy_many_synthetise_pz0)),'code_dephy']

    # separer les saisies non_attendues et inconnues
    identif_pz0_aucun = identif_pz0.loc[identif_pz0['code_dephy'].isin(dephy_none_synthetise_pz0)]
    identif_pz0_aucun.loc[:, ['donnee_attendue']] = modalite_pz0_inconnu # on attribue d'abord à tous "inconnu"
    identif_pz0_aucun.loc[identif_pz0_aucun['code_dephy'].isin(saisies_attendues_melt['code_dephy']),'donnee_attendue'] = modalite_pz0_aucun # mais ceux qui sont dans le fichier BDD_donnees_attendues_CAN, sont des "saisies non acceptables"

    identif_pz0_non_attendue = identif_pz0.copy()
    identif_pz0_non_attendue['donnee_attendue_split'] = identif_pz0_non_attendue['donnee_attendue'].apply(lambda x: ', '.join(set(x.split(', '))))
    identif_pz0_non_attendue = identif_pz0_non_attendue[identif_pz0_non_attendue['donnee_attendue_split'] == "non-attendu"]
    identif_pz0_non_attendue['donnee_attendue'] = modalite_non_attendu

    identif_pz0_non_attendue = identif_pz0_non_attendue.drop(['donnee_attendue_split'], axis = 1)

    # aucun pz0 = TOUTE la frise pz0 inconnu OU saisie non acceptable
    # SAUF pour les non attendue que l'on garde tague comme tel.
    # On les retire du data aucun pz0 : 
    identif_pz0_aucun = identif_pz0_aucun.drop(identif_pz0_non_attendue.index,errors = 'ignore')

    identif_pz0_with_pz0 = identif_pz0.drop(identif_pz0_aucun.index,errors = 'ignore')
    identif_pz0_with_pz0 = identif_pz0_with_pz0.drop(identif_pz0_non_attendue.index,errors = 'ignore')
    
    ## TRI DES PZ0 ACCEPTABLES
    # Meme si un synthetise contient une campagne pz0, il y en a qui ne sont pas acceptables
    # les pz0 que l'on considere correct sont ceux parfaits : "pz0, pz0, pz0" OU 3 synthetise monoannuels des 3 campagnes pz0 attendues 
    # On accepte les décalages de 1 an avant ou apres donc une mention de non-attendu ou post 1 fois

    pattern_pz0_correct = ["pz0, pz0, pz0", 
                           "non-attendu, pz0, pz0", 
                           "pz0, pz0, post",
                           "pz0"]
    # !! On traite "dephy_one_synthetise_pz0" et "dephy_many_synthetise_pz0" séparement : 
    # Pour les codes dephy avec plusieurs seul pz0
    dephy_mono = []
    identif_pz0_with_pz0,dephy_mono_temp = do_tag_pz0_not_correct(identif_pz0_with_pz0, dephy_many_synthetise_pz0, pattern_pz0_correct,
                                                  modalite_pz0_chevauchement, modalite_pz0_non_acceptable)
    dephy_mono = dephy_mono + dephy_mono_temp

    # Pour les codes dephy avec 1 seul pz0, on accepte en plus les biannuels (pour dephy_many_synthetise_pz0 on a plusieurs pz0, pz0 + pz0, pz0 donc ils ne sont pas acceptables)
    pattern_pz0_correct.append("pz0, pz0")

    identif_pz0_with_pz0,dephy_mono_temp = do_tag_pz0_not_correct(identif_pz0_with_pz0, dephy_one_synthetise_pz0, pattern_pz0_correct,
                                                  modalite_pz0_chevauchement, modalite_pz0_non_acceptable)
    dephy_mono = dephy_mono + dephy_mono_temp
    
    ## CONTROLE DU NB DE PZ0 PAR CODE DEPHY 
    # si il reste des codes dephy ayant plusieurs pz0, transformer la frise en incorrect. Vu les cas -> cas de saisie reelle de plusieurs synthetises pz0
    dephynb_plusieurspz0_restant = control_nb_pz0_per_codedephy(identif_pz0_with_pz0,dephy_mono)
    identif_pz0_with_pz0.loc[identif_pz0_with_pz0['code_dephy'].isin(dephynb_plusieurspz0_restant),'donnee_attendue'] = modalite_pz0_plusieurs

    ## Y A IL DES CHEVAUCHEMENT DES PZ0 ?
    identif_pz0_with_pz0 = do_correct_overlap(identif_pz0_with_pz0, modalite_pz0_chevauchement, dephy_mono)

    ## Re unir les tables
    df_identification_pz0 = pd.concat([identif_pz0_with_pz0,identif_pz0_non_attendue,identif_pz0_aucun]).reset_index()

    ## CAS DES REALISES 
    # ajouter le detail jusque à la zone. Jusqu'a maintenant on s'arretait jusque sdc_id
    left = df_zone[['parcelle_id']]
    right = df_parcelle[['sdc_id']]
    df_zone_extanded = pd.merge(left,right, left_on = 'parcelle_id', right_index=True).drop('parcelle_id', axis = 1)

    left = df_identification_pz0.loc[df_identification_pz0['synthetise_id'].isna()]
    right = df_zone_extanded.reset_index().rename(columns = {'id' : 'zone_id'})
    df_identification_pz0_zones = pd.merge(left,right, on = "sdc_id")

    df_identification_pz0_synthetise = df_identification_pz0.loc[~ df_identification_pz0['synthetise_id'].isna()]
    df_identification_pz0_synthetise.loc[:,['zone_id']] = np.nan

    df_identification_pz0 = pd.concat([df_identification_pz0_synthetise, df_identification_pz0_zones])

    # construction de la colonne 'id' = synthetise_id OU 'zone_id'
    df_identification_pz0.loc[df_identification_pz0['synthetise_id'].isna(),'id'] = df_identification_pz0.loc[df_identification_pz0['synthetise_id'].isna(),'zone_id']
    df_identification_pz0.loc[df_identification_pz0['zone_id'].isna(),'id'] = df_identification_pz0.loc[df_identification_pz0['zone_id'].isna(),'synthetise_id']

    df_identification_pz0 = df_identification_pz0.set_index('id')
    
    ## Derniers CONTROLEs
    dephynb_plusieurspz0_restant = control_nb_pz0_per_codedephy(df_identification_pz0,dephy_mono)
    if len(dephynb_plusieurspz0_restant) != 0: 
        message_error = message_error + "ATTENTION : il reste des codes dephy avec plusieurs pz0 ce qui est impossible !"

    modalites = df_identification_pz0['donnee_attendue'].value_counts().reset_index()['donnee_attendue'].to_list()
    modalites_list_expected = ["pz0", "post", modalite_pz0_non_acceptable, modalite_pz0_chevauchement, modalite_pz0_inconnu, modalite_non_attendu, modalite_pz0_plusieurs,modalite_pz0_aucun]
    check = [m in modalites for m in modalites_list_expected]
    if all(check) is False:
        message_error = message_error + "ATTENTION : Le nombre de modalités ne correspond pas à celles attendues !"

    if df_identification_pz0[df_identification_pz0.index.duplicated()].shape[0] != 0: 
        message_error = message_error + "ATTENTION : Il y a des zones ou synthetise qui sont dupliques"

    post_before_pz0 = check_coherence_frise_chronologique(df_identification_pz0, modalite_pz0_non_acceptable, modalite_pz0_aucun, modalite_pz0_chevauchement, modalite_pz0_inconnu, modalite_non_attendu,modalite_pz0_plusieurs)
    if post_before_pz0: 
        message_error = message_error + "ATTENTION : Il y a frises qui contiennent des post avant les pz0"
    
    if len(message_error) != 0:
        print(message_error)

    df_identification_pz0 = df_identification_pz0[['donnee_attendue']].rename(columns={'donnee_attendue' : 'pz0'})
    df_identification_pz0.index.names = ['entite_id']

    return(df_identification_pz0)



def get_typologie_culture_CAN(donnees):
    ''' 
    Le but est d'obtenir les typologies d'espece et de culture utilisées par la Cellule référence.

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
            - 'espece'
            - 'recolte_rendement_prix'
            - 'recolte_rendement_prix_restructure'
            Données externe (référentiel CAN):
            - 'typo_especes_typo_culture.csv'
            - 'typo_especes_typo_culture_marai.csv'

    Returns:
        pd.DataFrame() contenant la culture_id et la typologie de culture de la CAN

    ATTENTION :
        Modèle de sortie différent de celui de la CAN
        De plus 2 changements de décision par rapport à leurs sorties
        ATTENTION_DIFF_CAN_a :
            Pour les culture qui n'ont pas de composant culture, on les ajoute en renseignant "Aucune espèce renseignée" pour les typologies au lieu de NaN pour les typologie d'espece
            Et on renseigne 0 au lieu de 1 pour le nb d'espece/nb de typologie
        ATTENTION_DIFF_CAN_b :
            Pour les Cultures intermédiaires on laisse la définition de typologie au lieu de passer les typologies en NaN
            Voir si on passe en NaN lors de la création du magasin
            ==> Cela induit que les typologie de culture en NaN sont celles qui nécéssite une MàJ du référentiel !
    '''
    # Donnes de bases
    cropsp = donnees['composant_culture'].copy()
    cropsp = cropsp[['id','espece_id','culture_id','compagne']].rename(columns={'id':'composant_culture_id'}) # besoin de 'composant_culture_id' que pour les cultures porte-graines
    crop = donnees['culture'].copy()
    crop = crop[['id','nom','type']].rename(columns={'id':'culture_id'}) # Besoin de 'nom' que pour les cultures porte-graines
    sp = donnees['espece'].copy()
    sp = sp[['id','typocan_espece','typocan_espece_maraich']].rename(columns={'id':'espece_id'})
    
    # Donnees de recolte pour les portes graines et les betterave fourrageres
    recolte = donnees['recolte_rendement_prix'][['id','destination','action_id']].copy()
    recolte_restr = donnees['recolte_rendement_prix_restructure'].copy()

    recolte = recolte.merge(recolte_restr, on='id', how='left')
    recolte = recolte.merge(cropsp, on='composant_culture_id', how='left')
    recolte = recolte.loc[(recolte['composant_culture_id'].notnull()) & \
                          (recolte['compagne'].isnull()),]
    recolte = recolte.merge(crop, on='culture_id', how='left')

        # Culture portegraine

        # On cherche les culture portes graines par le nom de la culture et par la destination. Si la destination n'est pas entierement faite de 'Production semences' on retourne 'culture porte-graine et autres'
    culture_porteG = recolte.groupby('culture_id').apply(
        lambda clt: pd.Series({
            'typo_cpg' : 'Cultures porte graines' if all(clt['nom'].str.contains('porte+.graine|semence', case=False)) |\
                                              all(clt['destination'] == 'Production semences') \
                    else 'Cultures porte graines et autres destinations' if any(clt['destination'] == 'Production semences') \
                    else None
        }), include_groups = False).reset_index()


        # Culture betterave fourragere

    culture_bett_fourr = recolte.merge(sp[['espece_id','typocan_espece']], on='espece_id', how='left')
    culture_bett_fourr = culture_bett_fourr.groupby('composant_culture_id').apply(
        lambda clt: pd.Series({
            'typo_bett_fourr' : 'betterave fourragere' if all(clt['typocan_espece'] == 'Betterave') & \
                                                all(clt['destination'].str.contains('Fourrage')) \
                                else None
        }), include_groups = False).reset_index()
    
        # On crée la liste des composant de culture qui sont des betteraves fourragères, réutilisé après
    list_cpc_bett_fourr = list(culture_bett_fourr.loc[culture_bett_fourr['typo_bett_fourr'] == 'betterave fourragere','composant_culture_id'])

    crop = crop.drop(columns=['nom'])

    # Donnees de typologie d'espece et de culture
    typo1 = donnees['typo_especes_typo_culture'].copy()
    typo1 = typo1.rename(columns={'TYPO_ESPECES':'typocan_espece',
                                  'Typo_Culture':'typocan_culture'})
    typo2 = donnees['typo_especes_typo_culture_marai'].copy()
    typo2 = typo2.rename(columns={'TYPO_ESPECES_BIS':'typocan_espece_maraich',
                                  'Typo_Culture_bis':'typocan_culture_maraich'})

    df = cropsp.merge(sp, how = 'left', on = 'espece_id')
        # On change directement dans le dataframe les typologies d'espèces de la Betterave si elle est fourragère. Cela impactera la typologie de culture car elle ne reconnaitra pas 'Betterave fourragere' comme un 'Betterave' (la betterave industrielle). => Donc a ajouter dans le referentiel de passage typo_sp <=> typo_culture
    df.loc[df['composant_culture_id'].isin( list_cpc_bett_fourr ),'typocan_espece'] = 'Betterave fourragère'
    df.loc[df['composant_culture_id'].isin( list_cpc_bett_fourr ),'typocan_espece_maraich'] = 'Betterave fourragère'

    # Liste des cultures qui contiennent des cultures compagnes
    list_culture_with_compagne = list(set(df.loc[df['compagne'].notnull(), 'culture_id']))

    df['nb_composant_culture'] = 1
    df['nb_typocan_esp'] = df['typocan_espece'].copy()
    df['nb_typocan_esp_maraich'] = df['typocan_espece_maraich'].copy()

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
        'nb_composant_culture': 'sum',
        'nb_typocan_esp': get_nb_unique_typo,
        'nb_typocan_esp_maraich': get_nb_unique_typo
    }

    #  On crée les typologie can culture et les autre variable utiles grace a agg_dict
    df_base = df[['culture_id','typocan_espece','typocan_espece_maraich',
                'nb_composant_culture','nb_typocan_esp','nb_typocan_esp_maraich']].groupby('culture_id').agg(agg_dict).reset_index()
    #  On crée une typologie can culture mais sans les cpc qui sont des plantes compagnes
    df_comp = df.loc[df['compagne'].isna()].copy()
    df_comp['typocan_esp_sans_compagne'] = df_comp['typocan_espece'].copy()
    df_comp = df_comp[['culture_id','typocan_esp_sans_compagne']].groupby('culture_id').agg(concat_unique_sorted).reset_index()

    # On repart sur un pd.Df qui est le merge de df_base et df_comp (donc le meme groupby mais sur un version filtré de df_base)
    del(df)
    df = df_base.merge(df_comp[['culture_id','typocan_esp_sans_compagne']], on = 'culture_id', how = 'left')

    # On ajoute les culture_id qui n'ont pas de composant de culture et on leur attribue aucune espece renseigné
    df = df.merge(crop, how='left', on='culture_id')

    # Détection des cultures qui contiennent des cultures compagnes
    df['is_any_compagne'] = np.where(df['culture_id'].isin(list_culture_with_compagne), True, False)

    crop_only = crop.loc[~crop['culture_id'].isin(df['culture_id']),:]
    # ATTENTION_DIFF_CAN_a ::: 2 Lignes
    crop_only.loc[:,['nb_composant_culture','nb_typocan_esp','nb_typocan_esp_maraich']] = 0
    crop_only.loc[:,['typocan_espece','typocan_espece_maraich','typocan_esp_sans_compagne']] = 'NoInput-sp'
    crop_only['is_any_compagne'] = False

    df = pd.concat([df, crop_only], ignore_index=True)

    df = df.merge(typo1, how='left', on='typocan_espece')

    df = df.merge(typo2, how='left', on='typocan_espece_maraich')

    df = df.merge(typo1.rename(columns={'typocan_espece':'typocan_esp_sans_compagne',
                                        'typocan_culture':'typocan_culture_sans_compagne'}), \
                                            how='left', on='typocan_esp_sans_compagne')
    
    # ATTENTION_DIFF_CAN_a_bis ::: 1 Lignes
    # le premier c'était pour les composant de culture, ici c'est pour la typo de culture
    df.loc[df['nb_composant_culture'] == 0,['typocan_culture','typocan_culture_maraich','typocan_culture_sans_compagne']] = 'NoInput-sp'

    # Si pas de correspondance espece <-> culture on l'écrit
    df.loc[df['nb_composant_culture'] != 0,['typocan_culture','typocan_culture_maraich','typocan_culture_sans_compagne']] = df.loc[df['nb_composant_culture'] != 0,['typocan_culture','typocan_culture_maraich','typocan_culture_sans_compagne']].fillna('NoLink-sp-crop')


    # ATTENTION_DIFF_CAN_b ::: 2 Lignes
    # df.loc[df.type == 'INTERMEDIATE', ['typocan_culture','typocan_culture_maraich']] = ['Culture intermédiaire', 'Culture intermédiaire']
    # df.loc[df.type == 'INTERMEDIATE', ['typocan_culture','typocan_culture_maraich']] = [np.nan, np.nan]


    df['type'] = df['type'].astype('category')
    df['type'] = df['type'].cat.rename_categories({'MAIN': 'PRINCIPALE', 
                                                   'INTERMEDIATE': 'INTERMEDIAIRE', 
                                                   'CATCH': 'DEROBEE' })
    df['type'] = df['type'].astype('str')
    df[['nb_composant_culture','nb_typocan_esp','nb_typocan_esp_maraich']] = df[['nb_composant_culture','nb_typocan_esp','nb_typocan_esp_maraich']].astype('int64')
    
    # Ajout des tags 'culture porte-graines' dans une colonne à part, voir la détection quelques ligne plus tôt dans cette fonction
    df = df.merge(culture_porteG[['culture_id','typo_cpg']], how='left', on='culture_id')

    return df

def get_rota_typo(cgrp, freq_column='frequence'):
    '''
    Comme la CAN fait, on check à chaque fois une condition, si true on return. Il y a donc un ordre de priorité bien défini
    Sans cet ordre de priorité il y aurait qlq chevauchements
    Pour la CAN il n'y a pas de distinction entre l'absence de fréquence et l'absence de typo de culture
    ils aggregent tout avec un return 'Pas de type rotation calculé'. Nous ferons le distingo avec les 2 premieres conditions

    ATTENTION : 
        - pour le synthétisé, la colonne de fréquence est 'frequence'
        - pour le réalisé, la colonne de fréquence est 'surface_ponderee' ou 'surface'
    ATTENTION :
        - la colonne de typologie de culture est 'typocan_culture_sans_compagne'

    Args:
        cgrp (pd.Series):
            Series de données de la rotation pour le synthétisé ou du sdc pour le réalisé.
        freq_column (str):
            Nom de la colonne de fréquence à utiliser pour les calculs. Par défaut 'frequence' pour le synthétisé. Peut être 'surface_ponderee' ou 'surface' pour le réalisé.
    Returns:
        str: Typologie de culture
            si pas de surface renseignée, retourne 'aucune surface renseignée'
            si surface nulle, retourne 'surface nulle renseignée'
            si surface totale < 0.001 ha, retourne 'surface totale < 0.001 ha'
            si aucune fréquence de rotation calculée, retourne 'aucune fréquence de rotation calculée'
            si aucune typologie de culture détectée, retourne 'aucune typologie de culture détectée'
            Puis les conditions suivantes sont vérifiées dans l'ordre :
                'succession avec betterave ou lin ou légumes (>= 5 %)'
                'successions avec pomme de terre'
                'successions avec cultures porte graine'
                'céréales à paille hiver/colza'
                'céréales à paille hiver+printemps/colza'
                'maïs'
                'céréales à paille/colza/maïs ou protéagineux'
                'céréales à paille/colza/tournesol'
                'céréales à paille/maïs(/tournesol)'
                'céréales à paille/tournesol'
                'prairie temporaire < 50 % assolement'
                'prairie temporaire >= 50 % assolement'
            Si aucune de ces conditions n'est remplie, retourne 'Autre'
    '''
    # Si la colonne de fréquence n'est qu'une surface ou une surface pondérée, on vérifie si cette surface est non nulle et on la normalise afin de pouvoir les comparer par rapport à la totalité de la
    if freq_column in {'surface_ponderee', 'surface'}:
        if all(cgrp[freq_column] == 0):
            return 'aucune '+freq_column+' renseignée'
        if all(cgrp[freq_column] == 0):
            return freq_column+' nulle renseignée'
        if cgrp[freq_column].sum() < 0.001:
            return freq_column+' totale < 0.001 ha'
        cgrp[freq_column] = cgrp[freq_column] / np.nansum(cgrp[freq_column])
    if freq_column == 'frequence':
        if all(cgrp[freq_column].isna()):
            return 'aucune fréquence de rotation calculée'


    conditions = [
        (all(cgrp\
            ['typocan_culture_sans_compagne'].isna()), \
            'aucune typologie de culture détectée'),
        (sum(cgrp.loc[cgrp['typocan_culture_sans_compagne'].isin(\
            ['Betterave', 'Lin', 'Légume']), freq_column]) \
            >= 0.05, \
            'successions avec betterave ou lin ou légumes de plein champ (> 5 % surfaces)'),
        (sum(cgrp.loc[cgrp['typocan_culture_sans_compagne'].isin(\
            ['Pomme de terre']), freq_column]) \
            >= 0.05, \
            'successions avec pomme de terre'),
        (sum(cgrp.loc[cgrp['typo_cpg'].isin(\
            ['Cultures porte graines']), freq_column]) \
            >= 0.05, \
            'successions avec cultures porte graine'), # attention on va ici chercher dans la colonne 'typo_cpg'
        ((sum(cgrp.loc[cgrp['typocan_culture_sans_compagne'].isin(\
            ['Céréales à paille hiver', 'Colza']), freq_column]) \
            >= 0.95) & \
            (sum(cgrp.loc[cgrp['typocan_culture_sans_compagne'].isin(\
            ['Céréales à paille printemps']), freq_column]) \
            == 0), \
            'céréales à paille hiver/colza'),
        (sum(cgrp.loc[cgrp['typocan_culture_sans_compagne'].isin(\
            ['Céréales à paille hiver', 'Céréales à paille printemps', 'Colza']), freq_column]) \
            >= 0.95, \
            'céréales à paille hiver+printemps/colza'),
        # Attention la typo_culture de 'Sorgho' est 'Maïs' lorsque seul, sinon 'Autre'. voir référentiel typocan_culture_sans_compagne
        (sum(cgrp.loc[cgrp['typocan_culture_sans_compagne'].isin(\
            ['Maïs']), freq_column]) \
            >= 0.95, \
            'maïs'),
        (sum(cgrp.loc[cgrp['typocan_culture_sans_compagne'].isin(\
            ['Céréales à paille hiver', 'Céréales à paille printemps', 'Colza', 'Maïs', 'Oléagineux (hors Colza et Tournesol)', 'Protéagineux', 'Mélange fourrager']), freq_column])\
            >= 0.95, \
            'céréales à paille/colza/maïs ou protéagineux'),
        (sum(cgrp.loc[cgrp['typocan_culture_sans_compagne'].isin(\
            ['Céréales à paille hiver', 'Céréales à paille printemps', 'Colza', 'Tournesol', 'Oléagineux (hors Colza et Tournesol)', 'Mélange fourrager']), freq_column]) \
            >= 0.95, \
            'céréales à paille/colza/tournesol'),
        (sum(cgrp.loc[cgrp['typocan_culture_sans_compagne'].isin(\
            ['Céréales à paille hiver', 'Céréales à paille printemps', 'Maïs', 'Tournesol', 'Oléagineux (hors Colza et Tournesol)', 'Mélange fourrager']), freq_column]) \
            >= 0.95, \
            'céréales à paille/maïs (/tournesol)'),
        (sum(cgrp.loc[cgrp['typocan_culture_sans_compagne'].isin(\
            ['Céréales à paille hiver', 'Céréales à paille printemps', 'Tournesol']), freq_column]) \
            >= 0.95, \
            'céréales à paille/tournesol'),
        ((sum(cgrp.loc[cgrp['typocan_culture_sans_compagne'].isin(\
            ['Prairie temporaire']), freq_column]) \
            < 0.5) & \
            (sum(cgrp.loc[cgrp['typocan_culture_sans_compagne'].isin(\
            ['Prairie temporaire']), freq_column]) \
            > 0),
            'prairie temporaire < 50 % assolement'),
        ((sum(cgrp.loc[cgrp['typocan_culture_sans_compagne'].isin(\
            ['Prairie temporaire']), freq_column]) \
            >= 0.5), \
            'prairie temporaire >= 50 % assolement')
    ]
    
    for condition, message in conditions:
        if condition:
            return message

    return 'Autre'

def get_percent_each_typo_culture(cgrp, freq_column='frequence'):
    '''
    Permet de calculer le pourcentage de chaque typologie de culture dans un groupe de données. Ce groupe de données est généralement un groupe de données de rotation pour le synthétisé ou un sdc pour le réalisé.

    Args:
        cgrp (pd.Series):
            Series de données de la rotation pour le synthétisé ou du sdc pour le réalisé.
        freq_column (str):
            Nom de la colonne de fréquence à utiliser pour les calculs. Par défaut 'frequence' pour le synthétisé. Peut être 'surface_ponderee' ou 'surface' pour le réalisé.
    Returns:
        list: Liste des pourcentages de chaque typologie de culture dans le groupe de données.
        Chaque élément de la liste est une chaîne de caractères au format 'typologie: pourcentage'.
        Si aucune fréquence renseignée, retourne ['aucune frequence renseignée']
        Si la somme des surfaces est nulle, retourne ['surface nulle renseignée']
        Si la somme des surfaces est inférieure à 0.001, retourne ['surface totale < 0.001']
    '''

    list_grp = []
    percentages = []
    cgrp['typocan_culture_sans_compagne'] = cgrp['typocan_culture_sans_compagne'].fillna('NoTypoC')

    if pd.isna(cgrp[freq_column]).all() :
        return ['aucune '+freq_column+' renseignée']
    
    if freq_column in {'surface_ponderee', 'surface'}:
        surf_sum = cgrp[freq_column].sum()
        if surf_sum == 0:
            return [freq_column+' nulle renseignée']
        if surf_sum < 0.001:
            return [freq_column+' totale < 0.001']

    for x in list(cgrp['typocan_culture_sans_compagne'].unique()) : 
        typoc_sum = cgrp.loc[cgrp['typocan_culture_sans_compagne'] == x, freq_column].sum()
        if freq_column == 'frequence':
            typoc_sum = typoc_sum * 100
        if freq_column in {'surface_ponderee', 'surface'}:
            typoc_sum = (typoc_sum / surf_sum) * 100
        percentages.append(typoc_sum.round(1))
        list_grp.append(x + ':' + str(typoc_sum.round(1)))

    # Trier les deux listes en fonction des pourcentages
    sorted_lists = sorted(zip(list_grp, percentages), key=lambda pair: pair[1], reverse=True)
    list_grp_sorted = [item[0] for item in sorted_lists]

    return list_grp_sorted


def get_typologie_rotation_CAN_synthetise(donnees):
    ''' 
    Le but est d'obtenir les typologies de rotation utilisées par la Cellule référence.
    Pour le synthetise

    Echelle :
        entite_id : synthetise_id

    Args:
        donnees (dict):
            Données d'entrepot
                'connection_synthetise'
                'noeuds_synthetise'
            Données d'outils (attention dépendence)
                'noeuds_synthetise_restructure'
                'poids_connexions_synthetise_rotation'
                'typologie_can_culture'

    Returns:
        pd.DataFrame() contenant le synthetise_id et la typologie de rotation de la CAN
        On prends le poids de connexion utilisé pour l'aggrégation de la rotation.
    '''
    # OUTILS
    # Attention on utilise ici l'outil passant de noeuds_synth_id à la culture_id (voir outil restructuration et calcul de frequence de connexion)
    noeud_with_culture_id = donnees['noeuds_synthetise_restructure'].copy()
    con_frq = donnees['poids_connexions_synthetise_rotation'][['connexion_id','poids_conx_agregation']].copy()
    typo_culture = donnees['typologie_can_culture'].copy()

    # ENTREPOT
    conn = donnees['connection_synthetise'][['id','cible_noeuds_synthetise_id','culture_absente']].copy()
    conn = conn.loc[conn['culture_absente'] == 'f'].drop('culture_absente', axis=1)
    noeud = donnees['noeuds_synthetise'][['id','synthetise_id']].copy()
    noeud = noeud.merge(noeud_with_culture_id, left_on = 'id', right_on = 'id')

    # Renommer les id pour éviter les doublon id_x, id_y, ...
    noeud = noeud.rename(columns={'id':'cible_noeuds_synthetise_id'})
    conn = conn.rename(columns={'id':'connexion_id'})
    typo_culture = typo_culture.rename(columns={'id':'culture_id'})

    # MERGE
    df = conn.merge(noeud, on = 'cible_noeuds_synthetise_id')
    df = df.merge(con_frq, on = 'connexion_id')
    df = df.merge(typo_culture, on = 'culture_id')

    # ATTENTION on prends la typologie de culture SANS LES COMPAGNES. De plus on ne prend PAS en compte les CULTURE INTERMEDIAIRE (les CI ça se fait automatiquement car on merge sur les culture_id des connexions ; et pas sur les culture_id des culture intermédiaires ; de toute maniere les CI n'ont pas de fréquence de connexion rien qu'à eux)
    df = df[['connexion_id','synthetise_id','typocan_culture_sans_compagne','typo_cpg','poids_conx_agregation']].\
        rename(columns={'poids_conx_agregation' : 'frequence'})

    df = df.drop('connexion_id', axis=1)  

    df = df.groupby('synthetise_id').apply(
         lambda cgrp: pd.Series({
            'typocan_rotation': get_rota_typo(cgrp),
            'frequence_total_rota': round(cgrp['frequence'].sum(),2),
            'list_freq_typoculture': '_'.join(  get_percent_each_typo_culture(cgrp)  )  
        }))
    
    return df


def get_typologie_assol_CAN_realise(donnees):
    ''' 
    Le but est d'obtenir les typologies d'assolement utilisées par la Cellule référence.
    Pour le réalisé
    Attention ici on fait l'assolement en prenant l'ensemble des zones et parcelles d'un sdc_id donné, toutes pondérées par leurs surfaces respectives.

    Echelle :
        entite_id : sdc_id

    Args:
        donnees (dict):
            Données d'entrepot
                'noeuds_realise'
                'intervention_realise'
                'zone'
                'parcelle'
            Données d'outils (attention dépendence)
                'typologie_can_culture'

    Returns:
        pd.DataFrame() contenant 
            'surface_totale_assol_dvlp'
            'surface_totale_assol'
            'typocan_assol_dvlp'
            'typocan_assol'
            'list_freq_typoculture_dvlp'
            'list_freq_typoculture'

        La surface totale de l'assolement est ici la somme de toutes les surfaces des zones des parcelles d'un sdc_id donné, pour cela il faut que les parcelles soit rattachée à un sdc_id (donc aps le sbugs edaplos).
        La différence entre _dvlp et _ est que _dvlp est la surface totale de l'assolement sans pondération par le nombre de connexion dans une même zone_id. Si la même année il y a 2 cultures sur une meme zone de 30ha, alors la surface totale de l'assolement sera de 60ha pour _dvlp et de 30ha pour _ (car 2 connexions dans la meme zone_id).
        ATTENTION il faut enlever toutes les zones qui n'ont aucune interventions. Ces zones sont des zones créé par edaplos et jamais reprises par les utilisateurs.
    '''
    # OUTILS
    typo_culture = donnees['typologie_can_culture'][['culture_id','typocan_culture_sans_compagne','typo_cpg']].copy()

    # ENTREPOT
    noeuds = donnees['noeuds_realise'][['id','culture_id','zone_id']]\
        .rename(columns={'id':'noeuds_realise_id'}).copy()
    set_interventions_real = set(donnees['intervention_realise']['noeuds_realise_id'])
    zone = donnees['zone'][['id','surface','parcelle_id']]\
        .rename(columns={'id':'zone_id'}).copy()
    # ATTENTION LES PARCELLES QUI NE SONT PAS RATTACHES A UN SDC SONT SUPPRIMES
    parcelle = donnees['parcelle'][['id','sdc_id']]\
        .rename(columns={'id':'parcelle_id'}).copy()

    # On supprime les zones sans interventions
    noeuds = noeuds.loc[noeuds['noeuds_realise_id'].isin(set_interventions_real),]

    # MERGE
    df = noeuds.merge(typo_culture, on='culture_id', how='left')
    df = df.merge(zone, on='zone_id', how='left')
    df = df.merge(parcelle, on='parcelle_id', how='left')

    # Ajouter une transformation de la surface pour que ce soit la surface pondérée : diviser par le nombre de connexion dans une même zone_id
    df['surface_ponderee'] = df['surface'] / df.groupby('zone_id')['noeuds_realise_id'].transform('count')

    df_end = df.groupby(['sdc_id','typocan_culture_sans_compagne']).agg({
        'surface_ponderee': 'sum',
        'surface': 'sum',
        'typo_cpg': lambda x: 'Cultures porte graines' if 'Cultures porte graines' in x.values else 'Cultures porte graines et autres destinations' if 'Cultures porte graines et autres destinations' in x.values else None
    }).reset_index()

    df_end['surface'] = df_end['surface'].round(2)
    df_end['surface_ponderee'] = df_end['surface_ponderee'].round(2)

    df_end = df_end.groupby('sdc_id').apply(
        lambda cgrp: pd.Series({
        'surface_totale_assol_dvlp': cgrp['surface'].sum().round(2),
        'surface_totale_assol': cgrp['surface_ponderee'].sum().round(2),
        'typocan_assol_dvlp': get_rota_typo(cgrp, 'surface'),
        'typocan_assol': get_rota_typo(cgrp, 'surface_ponderee'),
        'list_freq_typoculture_dvlp': '_'.join(  get_percent_each_typo_culture(cgrp, freq_column='surface') ),
        'list_freq_typoculture': '_'.join(  get_percent_each_typo_culture(cgrp, freq_column='surface_ponderee') )
    }), include_groups=False).reset_index()

    df_end = df_end.set_index('sdc_id')

    return df_end



def extract_good_rotation_diagram(donnees):
    ''' 
    Le but est d'obtenir une liste de synthetise_id qui ont une bonne structure/ un bon schéma de rotation
    Par exemple il faut une seule culture (=noeud) en premier rang (rang = 0). Ou bien, il faut que les itk (= connexion) en sortie d'une même culture somme à 100%

    Note(s):
        Est réutilisé dans le cadre du calcul des poids de connexion au seins du synthétisé
        Que pour les cultures assolées en synthétisé

    Echelle :
        synthetise_id

    Args:
        donnees (dict):
            Données d'entrepot
            - 'connection_synthetise'
            - 'noeuds_synthetise'

    Returns:
        1° : list() des synthetisés qui sont bons
        2° : dict() des synthetisés mauvais selon leur problèmes
    '''

    conx = donnees['connection_synthetise'].copy()
    noeud = donnees['noeuds_synthetise'].copy()

    conx = conx[['id', 'frequence_source','culture_absente','source_noeuds_synthetise_id','cible_noeuds_synthetise_id']]
    conx = conx.rename(columns={'id' : 'conx_id',
                                'frequence_source' : 'freq',
                                'culture_absente' : 'abs',
                                'source_noeuds_synthetise_id' : 'nd_prec',
                                'cible_noeuds_synthetise_id' : 'nd_suiv'})
    noeud = noeud[['id', 'rang', 'fin_cycle','memecampagne_noeudprecedent', 'synthetise_id']]
    noeud = noeud.rename(columns={'id' : 'nd_id',
                                  'fin_cycle' : 'end',
                                  'rang' : 'rang',
                                  'memecampagne_noeudprecedent' : 'sameyear',
                                  'synthetise_id' : 'synth_id'})

        
    # Nombre de premier rang
    def number_node_rank0(dfgrp):
        return len(dfgrp.loc[dfgrp['rang']==0,'rang'])
    # Nombre de noeud terminaux
    def number_node_end(dfgrp):
        return len(dfgrp.loc[dfgrp['end']=='t','end'])
    # Nombre de noeud en premier rang
    def noeud_end_on_rank0(dfgrp):
        return any(dfgrp.loc[dfgrp['end']=='t','rang']==0)

    noeud_test = noeud.groupby('synth_id').apply(
        lambda dfgrp: pd.Series({
            'nb_noeud_de_rang1': number_node_rank0(dfgrp),
            'nb_noeud_finaux' : number_node_end(dfgrp),
            'noeud_finaux_en_rang1' : noeud_end_on_rank0(dfgrp)
            }), include_groups=False).copy()
    
    # Tague des synthétisé qui (n')ont...
    # ...Aucun noeud en premier rang
    no_first_node = list(noeud_test.loc[noeud_test['nb_noeud_de_rang1']==0].index)
    # ...Plusieurs noeuds en premier rang
    several_first_nodes = list(noeud_test.loc[noeud_test['nb_noeud_de_rang1']>1].index)
    # ...Aucun noeud terminal
    no_end_node = list(noeud_test.loc[noeud_test['nb_noeud_finaux']==0].index)
    # ...Au moins un noeud de premier rang qui est aussi terminal
    first_node_is_end_node = list(noeud_test.loc[noeud_test['noeud_finaux_en_rang1']>0].index)
    
    # Les noeuds qui n'ont pas de précédent OU pas de suivant
    node_wo_prev_or_next = list(noeud.loc[~((noeud['nd_id'].isin(conx['nd_prec'])) & \
                                            (noeud['nd_id'].isin(conx['nd_suiv']))),'synth_id'])

    def get_hole_in_rotation(series):
        ranks_theo = pd.Series(range(min(series)+1, max(series)))
        if all(ranks_theo.isin(series)) is False :
            return list(ranks_theo.loc[~(ranks_theo.isin(series))])
        return None
    
    # Les rangs qui sont entierement vide
    empty_rank = noeud[['rang','synth_id']].groupby('synth_id').agg(get_hole_in_rotation).reset_index()
    empty_rank = list(empty_rank.loc[empty_rank['rang'].notna(), 'synth_id'])

    # Merge de connexion et noeud (suivant et précédent)
    df = conx.merge(noeud[['nd_id','rang','end']].add_suffix('_prec'), left_on='nd_prec', right_on='nd_id_prec')\
        .drop('nd_id_prec', axis=1)
    df = df.merge(noeud.add_suffix('_suiv'), left_on='nd_suiv', right_on='nd_id_suiv').\
        rename(columns={'synth_id_suiv' : 'synth_id'}).drop('nd_id_suiv', axis=1)
    
    # Frequence des connexions égales à 0
        # On augmente un peu le sueil à 0.5% car bizarre d''avoir une connexion avec une fréquence si faible
    freq_cnx_at_0 = list(df.loc[df['freq'] < 0.5, 'synth_id'])

    # Somme de sortie du noeuf ne faisant pas 100%
    def get_unique_txt(series):
        cleaned = series.dropna().unique().copy()
        return cleaned[0]

    exit_cnx_100 = df[['synth_id','freq','nd_prec']].groupby('nd_prec').agg({
        'synth_id' : get_unique_txt,
        'freq' : 'sum'})
    exit_cnx_100 = list(exit_cnx_100.loc[round(exit_cnx_100['freq'],8) != 100, 'synth_id'])

    # Noeud suivant est forcement sur le rang suivant (pas de 'trou') 
        # Attention si le rang qui a un trou dans le chemin n'est fait que de culture dérobée et que le noeud suivant n'est pas une dérobée

    test_hole_in_path = df.loc[(df['rang_prec'] != (df['rang_suiv']-1) ) & (df['end_prec'] == 'f'),].copy()
    test_hole_in_path['empty_rank_are_catch_crop'] = ''

    for idx, row in test_hole_in_path.iterrows() :
        empty_rank_list = list(range(row['rang_prec']+1, row['rang_suiv']))
        # Premier if eventuellement redondant (voir avant avec le rang entierement)
        if not list(noeud.loc[(noeud['synth_id']==row['synth_id']) & (noeud['rang'].isin(empty_rank_list)), 'sameyear']=='t'):
            test_hole_in_path.at[idx,'empty_rank_are_catch_crop'] = 'empty_rank'
        elif (row['sameyear_suiv'] == 'f') & (all(list(noeud.loc[(noeud['synth_id']==row['synth_id']) & (noeud['rang'].isin(empty_rank_list)), 'sameyear'] == 't'))) & (all(list(noeud.loc[(noeud['synth_id']==row['synth_id']) & (noeud['rang']==row['rang_suiv']), 'sameyear'] == 'f'))) \
        | \
        (row['sameyear_suiv'] == 'f') & (all(list(noeud.loc[(noeud['synth_id']==row['synth_id']) & (noeud['rang'].isin(empty_rank_list)), 'sameyear'] == 'f'))) & (all(list(noeud.loc[((noeud['synth_id']==row['synth_id']) & (noeud['rang']==row['rang_suiv'])) & (noeud['nd_id']!=row['nd_suiv']), 'sameyear'] == 't'))) :
            test_hole_in_path.at[idx,'empty_rank_are_catch_crop'] = 'ok'
        else :
            test_hole_in_path.at[idx,'empty_rank_are_catch_crop'] = 'hole_in_path'

    def concat_unique_sorted_txt(series):
        cleaned = series.dropna().unique().copy()
        return '_&_'.join(sorted(cleaned))
    
    test_hole_in_path = test_hole_in_path.groupby('synth_id').agg({'empty_rank_are_catch_crop': concat_unique_sorted_txt}).reset_index()

    hole_in_path = list(test_hole_in_path.loc[test_hole_in_path['empty_rank_are_catch_crop'] != 'ok', 'synth_id'])

    # Noeud terminaux qui ne boucle pas entierement sur un noeud de premier rang
    end_node_continue = list(df.loc[(df['end_prec'] == 't') & df['rang_suiv'] != 0, 'synth_id'])


    # Liste final des BONS synthétisés
    list_good_synth_rotation = tuple(set(noeud['synth_id']) - set(list(
        no_first_node + several_first_nodes + no_end_node + first_node_is_end_node + node_wo_prev_or_next + empty_rank + exit_cnx_100 + freq_cnx_at_0 + hole_in_path + end_node_continue
        )))

    dic_of_bad_synth = {'no_first_node': no_first_node, 
                        'several_first_nodes' : several_first_nodes,
                        'no_end_node' : no_end_node, 
                        'first_node_is_end_node' : first_node_is_end_node, 
                        'node_wo_prev_or_next' : node_wo_prev_or_next, 
                        'empty_rank' : empty_rank, 
                        'exit_cnx_100' : exit_cnx_100, 
                        'freq_cnx_at_0' : freq_cnx_at_0, 
                        'hole_in_path' : hole_in_path, 
                        'end_node_continue' : end_node_continue}
    
    # Obtenir toutes les valeurs uniques
    all_values = list(set(value for values in dic_of_bad_synth.values() for value in values))

    # Créer un DataFrame pour les variables muettes
    csv_of_bad_synth = pd.DataFrame(False, index=all_values, columns=dic_of_bad_synth.keys())

    # Remplir le DataFrame avec True si la valeur est présente dans la liste
    for key, values in dic_of_bad_synth.items():
        csv_of_bad_synth.loc[values, key] = True
    
    return list_good_synth_rotation, csv_of_bad_synth
            

def trouver_chemins(graphe, debut, fins):
    ''' 
    Fonction utile permettant de calculer tout les chemins possibles au seins d'une rotation d'un synthétisé 
    '''
    stack = [(debut, [])]  # (node actuel, chemin parcouru)
    chemins = []

    while stack:
        node, chemin = stack.pop()
        chemin.append(node)

        if node in fins:
            chemins.append(list(chemin))
            continue

        for voisin in graphe.get(node, []):
            if voisin not in chemin:  # Éviter les cycles
                stack.append((voisin, chemin[:]))  # Copie du chemin actuel

    return chemins


def process_sy(sy, cx, nd):
    '''
    Fonction principale utilisée dans la fonction plus globale get_connexion_weight_in_synth_rotation(). Voir son docstring.
    La fonction process_sy() est sortie de la fonction globale pour la parrallelsation  !

    sy = liste des synthétisé à faire tourner
    cx = données des connexions suite a la manipulation dans la fonction gloable
    nd = données des noeuds suite a la manipulation dans la fonction globale
    '''

    # Construire le graphe des connexions sous forme de dictionnaire
    graphe = {}
    connexions = {}

    for idx, row in cx.iterrows():
        nd_prec, nd_suiv, conx_id, abs_value, freq = row['nd_prec'], row['nd_suiv'], idx, row['abs'], row['freq']
        
        if nd_prec not in graphe:
            graphe[nd_prec] = []
        graphe[nd_prec].append(nd_suiv)

        # Stocker les connexions avec leurs IDs et attributs pour un accès rapide
        connexions[(nd_prec, nd_suiv)] = {
            'conx_id': conx_id,
            'abs': abs_value,
            'freq': freq
        }

    # Trouver le premier nœud et les nœuds finaux
    first_node = nd.loc[(nd['rang'] == 0) & (nd['synth_id'] == sy)].index.item()
    end_nodes = set(nd.loc[(nd['end'] == 't') & (nd['synth_id'] == sy)].index)

    # Obtenir tous les chemins
    chemins_possibles = trouver_chemins(graphe, first_node, end_nodes)

    #  Associer chaque connexion aux chemins où elle apparaît, en comptant abs='t', sameyear='t', et calculant le poids du chemin
    lst_couples_connexion_chemins = []
    lst_chemins = []

    for chemin in chemins_possibles:

        poid_chemin = 1
        groupe_id = 0
        groupes_sameyear = {}

        # Déterminer les groupes sameyear chemin par chemin
        for i, node3 in enumerate(chemin):
            if i == 0 or nd.loc[node3, 'sameyear'] == 'f':
                groupe_id += 1  # Nouveau groupe
            groupes_sameyear[node3] = groupe_id  # Associer le nœud à son groupe
        # Si le premier noeud est en sameyear on associe son groupe à toutes les connexions qui ont le meme groupe que le dernier neoud
        if nd.loc[chemin[0], 'sameyear'] == 't':
            list_node_same_grp_as_last = [key for key, value in groupes_sameyear.items() if value == groupes_sameyear[chemin[-1]]]
            for key in list_node_same_grp_as_last: groupes_sameyear[key] = groupes_sameyear[chemin[0]]

        # Calculer le poids du chemin (produit) et Ajouter les infos de couples connexions/chemins
        for i in range(len(chemin) - 1):
            nd_prec, nd_suiv = chemin[i], chemin[i + 1]
            if (nd_prec, nd_suiv) in connexions:
                poid_chemin *= connexions[(nd_prec, nd_suiv)]['freq'] / 100  # Convertir en probabilité
                lst_couples_connexion_chemins.append({
                    'connexion_id': connexions[(nd_prec, nd_suiv)]['conx_id'],
                    'chemin_id': chemin,
                    'groupe_sameyear': groupes_sameyear[nd_suiv],  # La connexion prend le groupe du noeud suivant
                    'abs': connexions[(nd_prec, nd_suiv)]['abs']
                })
        # Ajout des connexions des nœuds terminaux vers le premier nœud
        if chemin[-1] in end_nodes and (chemin[-1], chemin[0]) in connexions:
            poid_chemin *= connexions[(chemin[-1], chemin[0])]['freq'] / 100
            lst_couples_connexion_chemins.append({
                'connexion_id': connexions[(chemin[-1], chemin[0])]['conx_id'],
                'chemin_id': chemin,
                'groupe_sameyear': groupes_sameyear[chemin[0]],  # La connexion prend le groupe du premier noeud
                'abs': connexions[(chemin[-1], chemin[0])]['abs']
            })
        
        # Nombre d'année (soit le nombre de groupe sameyear après avoir enlever les connexions absentes)
        nb_annee = len({entry['groupe_sameyear'] for entry in lst_couples_connexion_chemins if \
                            (entry['abs'] == 'f') & (entry['chemin_id'] == chemin)})
        if nb_annee == 0 : nb_annee = 1
        # Ajouter les infos des chemins, dont le poids des chemins après recalcul sans conx absente
        lst_chemins.append({
            'chemin_id': chemin,
            'pd_chem' : poid_chemin,
            'poids_conx_standard': poid_chemin / nb_annee,
            'synth_id': sy
        })

    # Convertir en DataFrame
    df_chemins = pd.DataFrame.from_records(lst_chemins)
    df_chemins['chemin_id'] = df_chemins['chemin_id'].astype('str')
    df_couples_connexion_chemins = pd.DataFrame.from_records(lst_couples_connexion_chemins)
    df_couples_connexion_chemins['chemin_id'] = df_couples_connexion_chemins['chemin_id'].astype('str')

    # Merge chemin sur les couples cx_ch
    df_couples_connexion_chemins = df_couples_connexion_chemins.merge(df_chemins, on = 'chemin_id', how = 'left')

    # Avoir le facteur de normalisation pour chaque chemin soit la somme des poids de connexions standard présentes dans le chemin divisé par le poids du chemin
    chemin_normalisation = df_couples_connexion_chemins[df_couples_connexion_chemins['abs'] == 'f'].\
        groupby(['chemin_id']).agg(
            facteur_normalisation=('poids_conx_standard', lambda x: x.sum() / df_couples_connexion_chemins.loc[x.index, 'pd_chem'].iloc[0])
            ).reset_index()

    # Avoir le compte du nombre de connexions active (abs == 'f') ayant le meme chemin ET le meme groupe_sameyear
    nb_grp_sameyear_overall = df_couples_connexion_chemins[df_couples_connexion_chemins['abs'] == 'f'].\
        groupby(['chemin_id', 'groupe_sameyear']).size().reset_index(name='count_grp_sameyear_overall')
    
    all_df = df_couples_connexion_chemins.merge(nb_grp_sameyear_overall, on=['chemin_id', 'groupe_sameyear'], how='left')
    all_df = all_df.merge(chemin_normalisation, on=['chemin_id'], how='left')

    # Calculer proba_conx_spatiotemp
    all_df['proba_conx_spatiotemp'] = all_df['poids_conx_standard'] / all_df['count_grp_sameyear_overall']

    # Normalisation des poids de connexions pour l'agrégation, au niveau des chemins
    all_df['poids_conx_agregation_norm_chemin'] = all_df['poids_conx_standard'] / all_df['facteur_normalisation']

    # Supprimer le poids de connexion des connexions absentes
    all_df.loc[all_df['abs'] == 't','poids_conx_agregation_norm_chemin'] = np.nan
    all_df.loc[all_df['abs'] == 't','poids_conx_standard'] = np.nan
    all_df.loc[all_df['abs'] == 't','proba_conx_spatiotemp'] = np.nan

    # On donne directement le poids standard de connexion qui est utilisé pour l'agrégation au niveau du synthétisé dans Agrosyst et par 
    all_df['poids_conx_agregation'] = all_df['poids_conx_standard'].copy()
    # Normalisation des poids de connexions pour l'agrégation au niveau du SDC
    all_df['poids_conx_agregation_norm_synth'] = all_df['poids_conx_standard'] / all_df['poids_conx_standard'].sum()

    all_df.drop(['pd_chem', 'poids_conx_standard', 'facteur_normalisation'], axis=1, inplace=True)

    return all_df


def get_connexion_weight_in_synth_rotation(donnees, parallelization_enabled:bool = True):
    ''' 
    Le but est d'obtenir un Dataframe avec les poids des connexions au sein du stynhétisé.
    Avec le poids des connexions pour l'agrégation (indicateur à l'itk) et la probabilité d'apparition de la connexion (indicateur à l'année, ou proportion spatio-temporelle de la culture). 
    On exporte aussi le dataframe intermédiaire qui est très utile avec les couples connexions-chemins

    Le but est d'avoir tout les couples connexions-chemins. Puis on associe chaque couple à un groupe de culture ayant la même campagne (groupe de 1 culture possible). On identifie les connexion absentes. Le poids des chemins est la multiplication de toutes frequences de connexion présentes dans le chemin. On crée un poids de connexion standard soit le poid du chemin divisé par le nombre d'année. Le nombre d'année est le nombre de groupe de même campagne dans le chemin, après avoir filtré les connexions absentes. 
    Avec toutes ces variable on détermine :
        * le poids de connexion d'aggrégation, utilisé dans agrosyst et la cellref. Qui est égale au poids standard = multiplication de toutes les fréquences de connexion présentes dans le chemin divisé par le nombre d'année. NE SOMME PAS A 100%
        * le poids de connexion d'aggrégation. Qui est le poids de connexion standard nomralisé au niveau du synthétisé (soit diviser par la somme de tout les poids de connexion standard du synthé)
        * la probabilité d'apparittion de la connexion qui est le poids de connexion standard divisé par le nombre de connexion actives au sein de la même campagne (le groupe de connexions de meme campagne)
        * le poids de connexion d'aggrégation normalisé au chemin. Qui est le poids de connexion standard nomralisé au niveau du chemin (soit diviser par la somme de tout les poids de connexion standard du chemin)
    Attention, on filtre les synthétisés dont la somme des probabilités d'apparition de culture ne fait pas 1 ! (c'est le cas d'une trentaine de synthétisé qui ont des chemins entierrement composé de culture absentes)

    Note(s):
        Que pour les cultures assolées en synthétisé
        Processus parralélisé à 50% des cores de la machine (4h30 --> 45min)

    Echelle :
        connexion_id
        couple connexion_id-chemin_id

    Args:
        donnees (dict):
            Données d'entrepot
            - 'connection_synthetise'
            - 'noeuds_synthetise'
            Fonctions
            - trouver_chemins(graphe, debut, fins)
            - extract_good_rotation_diagram(donnees[['connection_synthetise', 'noeuds_synthetise']])
        parallelization_enabled (bool):
            booléen indiquant si la parralélisation est active ou non

    Returns:
        1° : pd.Dataframe() des poids de connexion
        2° : pd.Dataframe() des poids des couples connexion-chemin (donc avec connexion, chemins de noeuds, groupe de couples ayant la même campagne, connexion absente, poids du couple)
    '''
    
    # Importation des données etmise en forme
    conx = donnees['connection_synthetise'].copy()
    noeud = donnees['noeuds_synthetise'].copy()

    conx = conx[['id', 'frequence_source','culture_absente','source_noeuds_synthetise_id','cible_noeuds_synthetise_id']]\
    .rename(columns={'id' : 'conx_id',
                     'frequence_source' : 'freq',
                     'culture_absente' : 'abs',
                     'source_noeuds_synthetise_id' : 'nd_prec',
                     'cible_noeuds_synthetise_id' : 'nd_suiv'})
    noeud = noeud[['id', 'rang', 'fin_cycle','memecampagne_noeudprecedent', 'synthetise_id']]\
        .rename(columns={'id' : 'nd_id',
                        'fin_cycle' : 'end',
                        'rang' : 'rang',
                        'memecampagne_noeudprecedent' : 'sameyear',
                        'synthetise_id' : 'synth_id'})

    df = conx.merge(noeud[['nd_id','rang','end']].add_suffix('_prec'), left_on='nd_prec', right_on='nd_id_prec')\
        .drop('nd_id_prec', axis=1)
    df = df.merge(noeud.add_suffix('_suiv'), left_on='nd_suiv', right_on='nd_id_suiv').\
        rename(columns={'synth_id_suiv' : 'synth_id'})\
            .drop('nd_id_suiv', axis=1)

    list_good_synth, _ = extract_good_rotation_diagram(donnees)

    cx = df.loc[df['synth_id'].isin(list_good_synth)].set_index('conx_id').copy()
    nd = noeud.loc[noeud['synth_id'].isin(list_good_synth)].set_index('nd_id').copy()


    final_data = pd.DataFrame()

    # On parrallelise la fonction principale process_sy() qui fait l'important des calculs.
    # Utilisation de ProcessPoolExecutor avec X% des cœurs
    ratio_cpu_use = 0.5
    if parallelization_enabled:
        print('Parallélisation de la fonction de calcul des poids de connexion :')
        # si on est en mode réel, on active la parallélisation
        partial_process_sy = partial(process_sy, cx=cx, nd=nd)
        with ProcessPoolExecutor(max_workers= max(1, int(os.cpu_count() * ratio_cpu_use)) ) as executor:
            results = list(tqdm(executor.map(partial_process_sy, list_good_synth), total=len(list_good_synth)))
    else:
        # si on est en mode TU, on désactive la parralélisation
        results = [process_sy(sy, cx=cx, nd=nd) for sy in list_good_synth]

    # Concaténation des résultats
    final_data = pd.concat(results)

    # On enleve les données qui ne somme pas à 1 pour les poids de connexion non utilisé pour l'agrégation de base ( soit poids_conx_agregation_norm_synth, proba_conx_spatiotemp, poids_conx_agregation_norm_chemin)
    test_sum_at_100 = final_data.copy()
    test_sum_at_100 = test_sum_at_100[['proba_conx_spatiotemp','poids_conx_agregation_norm_synth','poids_conx_agregation_norm_chemin','synth_id']].groupby('synth_id').agg({
        'poids_conx_agregation_norm_synth' : 'sum',
        'proba_conx_spatiotemp' : 'sum',
        'poids_conx_agregation_norm_chemin' : 'sum'
    })
    test_sum_at_100 = test_sum_at_100.loc[(round(test_sum_at_100['poids_conx_agregation_norm_synth'],2) != 1) | \
                                          (round(test_sum_at_100['proba_conx_spatiotemp'],2) != 1) | \
                                          (round(test_sum_at_100['poids_conx_agregation_norm_chemin'],2) != 1)].index

    # print('Nombre de connexion qui ne somme pas à 100 : ', len(test_sum_at_100).astype('str'))

    final_data = final_data.loc[~(final_data['synth_id'].isin(test_sum_at_100))]
    final_data = final_data[['connexion_id','chemin_id','synth_id','groupe_sameyear','abs','poids_conx_agregation','poids_conx_agregation_norm_synth','proba_conx_spatiotemp','poids_conx_agregation_norm_chemin']].rename(columns={'synth_id' : 'synthetise_id'})

    # Somme des poids des couples cnx_chem pour aller à l'échelle connexion_id
    # On choisit d'arrondir à 5 chiffres après la virgule :
    final_data_conx_level = final_data[['connexion_id','synthetise_id','poids_conx_agregation','poids_conx_agregation_norm_synth','proba_conx_spatiotemp','poids_conx_agregation_norm_chemin']].groupby('connexion_id').agg({
        'synthetise_id' : lambda x : x.iloc[0],
        'poids_conx_agregation' : lambda x : np.nan if all(x.isna()) else round(sum(x.dropna()),5),
        'poids_conx_agregation_norm_synth' : lambda x : np.nan if all(x.isna()) else round(sum(x.dropna()),5),
        'proba_conx_spatiotemp' : lambda x : np.nan if all(x.isna()) else round(sum(x.dropna()),5),
        'poids_conx_agregation_norm_chemin' : lambda x : np.nan if all(x.isna()) else round(sum(x.dropna()),5)
    }).reset_index()

    final_data_conx_level = final_data_conx_level.set_index('connexion_id')
    final_data = final_data.set_index('connexion_id')

    # final_data_conx_level = échelle connexion /// final_data = échelle couples cnx_chem /// liste synthe somme pas à 1
    return final_data_conx_level, final_data, test_sum_at_100


def get_connexion_weight_in_synth_rotation_for_test(donnees):
    """
        Enveloppe pour tester le premier résultat de la fonction get_connexion_weight_in_synth_rotation_first_for plus facilement.
    """
    final_data_conx_level, _, _ = get_connexion_weight_in_synth_rotation(donnees, parallelization_enabled=False)
    return final_data_conx_level
