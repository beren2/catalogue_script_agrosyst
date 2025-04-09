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
        code_dephy : pd.serie, serie de code_dephy à traiter
    
    return :
        df : data.frame
        dephy_mono : list, liste des codes dephy ayant un pz0 mono annuel
    '''

    select_df = df.loc[df['code_dephy'].isin(code_dephy_select.to_list())]
    unselect_df = df.loc[~ df['code_dephy'].isin(code_dephy_select.to_list())]

    # Mettre en évidence synthetises pz0 uniquement monoannuels 
    pz0 = select_df.loc[select_df['donnee_attendue'].str.contains("pz0")].reset_index()
    
    pz0.loc[pz0['donnee_attendue'].str.contains(","), 'triannuel'] = "pluri"
    pz0.loc[pz0['triannuel'].isna(), ['triannuel']] = "mono"

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
    select_df.loc[:,'donnee_attendue'] = select_df.apply(lambda x : "post" if (x['code_dephy'] not in (dephy_mono) and x['donnee_attendue'] == 'pz0') 
                                                                            else x['donnee_attendue'], axis = 1)
 
    # sauvegarde les post
    post = select_df.loc[select_df['donnee_attendue'] == "post"]
    select_df = select_df.loc[select_df['donnee_attendue'] != "post"]

    # B) Pour les pz0 pluri annuels pz0, pz0, pz0 : 
    code_dephy_000 = select_df.loc[select_df['donnee_attendue'] == "pz0, pz0, pz0", 'code_dephy'].to_list()
    select_df.loc[select_df['code_dephy'].isin(code_dephy_000),'donnee_attendue'] = select_df.loc[select_df['code_dephy'].isin(code_dephy_000)].apply(
        lambda x : 'pz0' if x['donnee_attendue'] == "pz0, pz0, pz0"
                            else modalite_pz0_chevauchement, axis = 1)

    # C) Pour les pz0 pluri annuels restants : 
    # tag des lignes correctes
    select_df.loc[:,'to_keep'] = select_df.apply(lambda x : True if (x['donnee_attendue'] in (pattern_pz0_correct))
                                                                            else False , axis = 1)
    
    dephy_correct = select_df.loc[select_df['to_keep'], 'code_dephy'].to_list()
    
    select_df.loc[:,'donnee_attendue'] = select_df.apply(lambda x : modalite_pz0_non_acceptable if (x['code_dephy'] not in (dephy_correct))
                                                                            else x['donnee_attendue'] , axis = 1)
    
    select_df.loc[:,'donnee_attendue'] = select_df.apply(lambda x : modalite_pz0_chevauchement if (x['code_dephy'] in (dephy_correct)) & (x['to_keep'] is False)
                                                                            else x['donnee_attendue'] , axis = 1)    
    
    select_df.loc[:,'donnee_attendue'] = select_df.apply(lambda x : "pz0" if (x['code_dephy'] in (dephy_correct)) & (x['to_keep'] is True)
                                                                            else x['donnee_attendue'] , axis = 1)    
    
    select_df = select_df.drop(['to_keep'], axis = 1)

    # Pour les post sauvegardes à part, les taguer incorrect : saisie pz0 non acceptable" pour des codes dephy concernes
    code_dephy_nonacceptable = select_df.loc[select_df['donnee_attendue'] == modalite_pz0_non_acceptable,'code_dephy'].to_list()
    post.loc[post['code_dephy'].isin(code_dephy_nonacceptable), 'donnee_attendue'] = modalite_pz0_non_acceptable

    df = pd.concat([unselect_df,select_df,post])
    return(df,dephy_mono)


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
    saisies_attendues = donnees['BDD_donnees_attendues_CAN']
    
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
    identif_pz0.loc[:,'count_campaign'] = identif_pz0.apply(lambda x : len(x['campagnes'].split(', ')), axis=1)
    identif_pz0.loc[:,'count_unique_campaign'] = identif_pz0.apply(lambda x : len(set(x['campagnes'].split(', '))), axis=1)
    
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
    identif_pz0_non_attendue.loc[:,'donnee_attendue_split'] = identif_pz0_non_attendue.apply(lambda x : ', '.join(set(x['donnee_attendue'].split(', '))) , axis = 1)
    identif_pz0_non_attendue = identif_pz0_non_attendue.loc[identif_pz0_non_attendue['donnee_attendue_split'] == "non-attendu"]
    identif_pz0_non_attendue['donnee_attendue'] = modalite_non_attendu

    identif_pz0_non_attendue = identif_pz0_non_attendue.drop(['donnee_attendue_split'], axis = 1)

    # retirer les non attendue du data aucun pz0
    identif_pz0_aucun = identif_pz0_aucun.drop(identif_pz0_non_attendue.index,errors = 'ignore')

    identif_pz0_with_pz0 = identif_pz0.drop(identif_pz0_aucun.index,errors = 'ignore')
    identif_pz0_with_pz0 = identif_pz0_with_pz0.drop(identif_pz0_non_attendue.index,errors = 'ignore')
    
    ## TRI DES PZ0 NON ACCEPTABLES
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
    # si il reste des codes dephy ayant plusieurs pz0, transformer la frise en incorrect. Vu les cas -> cas de saisie reeelle de plusieurs synthetises pz0
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
    check = [m in modalites for m in ["pz0", "post", modalite_pz0_non_acceptable, modalite_pz0_chevauchement, modalite_pz0_inconnu, modalite_non_attendu, modalite_pz0_plusieurs]]
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
    cropsp = donnees['composant_culture'][['espece_id','culture_id']]
    crop = donnees['culture'][['id','type']].rename(columns={
        'id':'culture_id'})
    sp = donnees['espece_vCAN'][['id','typocan_espece','typocan_espece_maraich']].rename(columns={
        'id':'espece_id'})
    # Tant que le référentiel n'est pas pret (ajout des deux colonnes de la can)
    # sp = donnees['espece'][['id','typocan_espece','typocan_espece_maraich']]
    typo1 = donnees['typo_especes_typo_culture'].rename(columns={
        'TYPO_ESPECES':'typocan_espece', 'Typo_Culture':'typocan_culture'})
    typo2 = donnees['typo_especes_typo_culture_marai'].rename(columns={
        'TYPO_ESPECES_BIS':'typocan_espece_maraich', 'Typo_Culture_bis':'typocan_culture_maraich'})

    df = cropsp.merge(sp, how = 'left', on = 'espece_id')

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


    df = df.merge(crop, how='left', on='culture_id')
    crop_only = crop.loc[~crop['culture_id'].isin(df['culture_id']),:]
    # ATTENTION_DIFF_CAN_a ::: 2 Lignes
    crop_only.loc[:,['nb_espece','nb_typocan_esp','nb_typocan_esp_maraich']] = 0
    crop_only.loc[:,['typocan_espece','typocan_espece_maraich']] = 'Aucune espèce renseignée'

    df = pd.concat([df, crop_only], ignore_index=True)

    df = df.merge(typo1, how='left', on='typocan_espece')

    df = df.merge(typo2, how='left', on='typocan_espece_maraich')

    # ATTENTION_DIFF_CAN_a_bis ::: 1 Lignes
    df.loc[df['nb_espece'] == 0,['typocan_culture','typocan_culture_maraich']] = 'Aucune espèce renseignée'


    # ATTENTION_DIFF_CAN_b ::: 2 Lignes
    # df.loc[df.type == 'INTERMEDIATE', ['typocan_culture','typocan_culture_maraich']] = ['Culture intermédiaire', 'Culture intermédiaire']
    # df.loc[df.type == 'INTERMEDIATE', ['typocan_culture','typocan_culture_maraich']] = [np.nan, np.nan]


    df['type'] = df['type'].astype('category')
    df['type'] = df['type'].cat.rename_categories({'MAIN': 'PRINCIPALE', 
                                                   'INTERMEDIATE': 'INTERMEDIAIRE', 
                                                   'CATCH': 'DEROBEE' })
    df['type'] = df['type'].astype('str')
    df[['nb_espece','nb_typocan_esp','nb_typocan_esp_maraich']] = df[['nb_espece','nb_typocan_esp','nb_typocan_esp_maraich']].astype('int64')
    df = df.set_index('culture_id')

    # Ajout de 'Culture porte-graine' ??
    # Surement un changement de culture au niveau des interventions dans le contexte d'une destination production de semence
    # Du coup utilisation du nom de la culture pour changement non souhaité

    return df



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
        if all(ranks_theo.isin(series)) == False :
            return list(ranks_theo.loc[~(ranks_theo.isin(series))])
    
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
        if list(noeud.loc[(noeud['synth_id']==row['synth_id']) & (noeud['rang'].isin(empty_rank_list)), 'sameyear']=='t') == []:
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
    
    return list_good_synth_rotation, dic_of_bad_synth
            

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


def get_connexion_weight_in_synth_rotation(donnees, parallelization_enabled=True):
    ''' 
    Le but est d'obtenir un Dataframe avec les poids des connexions au sein du stynhétisé. 
    On exporte aussi le dataframe intermédiaire qui est très utile avec les couples connexions-chemins

    Le but est d'avoir tout les couples connexions-chemins. Puis on associe chaque couple à un groupe de culture ayant la même campagne (groupe de 1 culture possible). On identifie les connexion absentes. Le poids des chemins est la multiplication de toutes frequences de connexion présentes dans le chemin. On crée un poids de connexion annualisé soit le poid du chemin divisé par le nombre d'année. Le nombre d'année est le nombre de groupe de même campagne dans le chemin, après avoir filtré les connexions absentes. Puis pour chaque connexion on donne ce poids de connexion annualisé divisé par le nombre de connexions dans le groupe de même camapgne qui n'est pas absente. Puis on passe en NA les poids de connexions pour les connexions absentes. Et au final on fait une somme des poids de connexion pour une meme connexion (car on était jusque là au niveau du couple connexion-chemin)
    Attention, on filtre les synthétisés dont la somme des poids de connexion ne fait pas 1 ! (c'est le cas d'une trentaine de synthétisé qui ont des chemins entierrement composé de culture absentes)

    Note(s):
        Que pour les cultures assolées en synthétisé
        Processus parralélisé à 70% des cores de la machine (4h30 --> 45min)

    Echelle :
        connexion_id
        couple connexion_id-chemin_id

    Args:
        donnees (dict):
            Données d'entrepot
            - 'connection_synthetise'
            - 'noeuds_synthetise'
            Focntions
            - trouver_chemins(graphe, debut, fins)
            - extract_good_rotation_diagram(donnees[['connection_synthetise', 'noeuds_synthetise']])

    Returns:
        1° : pd.Dataframe() des poids de connexion
        2° : pd.Dataframe() des poids des couples connexion-chemin (donc avec connexion, chemins de noeuds, groupe de couples ayant la même campagne, connexion absente, poids du couple)
    '''

    import os
    from concurrent.futures import ProcessPoolExecutor

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

    # Fonction principal en mode fonction pour permettre la parrallélisation
    def process_sy(sy):

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
        df_couples_connexion_chemins = []
        df_chemins = []

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
                    df_couples_connexion_chemins.append({
                        'connexion_id': connexions[(nd_prec, nd_suiv)]['conx_id'],
                        'chemin_id': chemin,
                        'groupe_sameyear': groupes_sameyear[nd_suiv],  # La connexion prend le groupe du noeud suivant
                        'abs': connexions[(nd_prec, nd_suiv)]['abs']
                    })
            # Ajout des connexions des nœuds terminaux vers le premier nœud
            if chemin[-1] in end_nodes and (chemin[-1], chemin[0]) in connexions:
                poid_chemin *= connexions[(chemin[-1], chemin[0])]['freq'] / 100
                df_couples_connexion_chemins.append({
                    'connexion_id': connexions[(chemin[-1], chemin[0])]['conx_id'],
                    'chemin_id': chemin,
                    'groupe_sameyear': groupes_sameyear[chemin[0]],  # La connexion prend le groupe du premier noeud
                    'abs': connexions[(chemin[-1], chemin[0])]['abs']
                })
            
            # Nombre d'année (soit le nombre de groupe sameyear après avoir enlever les connexions absentes)
            nb_annee = len(set([entry['groupe_sameyear'] for entry in df_couples_connexion_chemins if \
                                (entry['abs'] == 'f') & (entry['chemin_id'] == chemin)]))
            if nb_annee == 0 : nb_annee = 1
            # Ajouter les infos des chemins, dont le poids des chemins après recalcul sans conx absente
            df_chemins.append({
                'chemin_id': chemin,
                'pd_chem' : poid_chemin,
                'poid_standard_cnx_wo_abs': poid_chemin / nb_annee,
                'synth_id': sy
            })

        # Convertir en DataFrame
        df_chemins = pd.DataFrame(df_chemins)
        df_chemins['chemin_id'] = df_chemins['chemin_id'].astype(str)
        df_couples_connexion_chemins = pd.DataFrame(df_couples_connexion_chemins)
        df_couples_connexion_chemins['chemin_id'] = df_couples_connexion_chemins['chemin_id'].astype(str)
        # Merge chemin sur les couples cx_ch
        df_couples_connexion_chemins = df_couples_connexion_chemins.merge(df_chemins, on = 'chemin_id', how = 'left')

        # Avoir le compte du nombre de connexions active (abs == 'f') ayant le meme chemin ET le meme groupe_sameyear
        nb_grp_sameyear_overall = df_couples_connexion_chemins[df_couples_connexion_chemins['abs'] == 'f'].\
            groupby(['chemin_id', 'groupe_sameyear']).size().reset_index(name='count_grp_sameyear_overall')
        all_df = df_couples_connexion_chemins.merge(nb_grp_sameyear_overall, on=['chemin_id', 'groupe_sameyear'], how='left')

        # Calculer le vrai poids de connexion final (poid_standard_cnx_wo_abs / count_grp_sameyear_overall)
        all_df['connexion_freq'] = all_df['poid_standard_cnx_wo_abs'] / all_df['count_grp_sameyear_overall']

        # Supprimer le poids de connexion des connexions absentes
        all_df.loc[all_df['abs'] == 't','connexion_freq'] = np.nan

        return all_df


    # Utilisation de ProcessPoolExecutor avec 70% des cœurs
    if(parallelization_enabled):
        # si on est en mode réel, on active la parallélisation
        with ProcessPoolExecutor(max_workers= max(1, int(os.cpu_count() * 0.7)) ) as executor:
            results = list(executor.map(process_sy, list_good_synth))
    else:
        # si on est en mode TU, on désactive la parralélisation
        results = []
        for sy in list(list_good_synth) :
            results.append(process_sy(sy))

    # Concaténation des résultats
    final_data = pd.concat(results)

    test_sum_at_100 = final_data.copy()
    test_sum_at_100 = test_sum_at_100[['connexion_freq','synth_id']].groupby('synth_id').sum('connexion_freq')
    test_sum_at_100 = test_sum_at_100.loc[round(test_sum_at_100['connexion_freq'],2) != 1].index

    # print('Nombre de connexion qui ne somme pas à 100 : ', len(test_sum_at_100).astype('str'))

    final_data = final_data.loc[~(final_data['synth_id'].isin(test_sum_at_100))]
    final_data = final_data[['connexion_id','chemin_id','groupe_sameyear','abs','connexion_freq']]

    # Somme des poids des couples cnx_chem pour aller à l'échelle connexion_id
    final_data_conx_level = final_data[['connexion_id','connexion_freq']].groupby('connexion_id').agg({
        'connexion_freq' : lambda x : np.nan if all(x.isna()) else sum(x.dropna())
    })

    # final_data_conx_level = échelle connexion /// final_data = échelle couples cnx_chem
    return final_data_conx_level, final_data


def get_connexion_weight_in_synth_rotation_for_test(donnees):
    """
        Enveloppe pour tester le premier résultat de la fonction get_connexion_weight_in_synth_rotation_first_for plus facilement.
    """
    final_data_conx_level, _ = get_connexion_weight_in_synth_rotation(donnees, parallelization_enabled=False)
    return final_data_conx_level