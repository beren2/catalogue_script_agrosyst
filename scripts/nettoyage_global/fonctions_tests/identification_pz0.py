"""
    Fichier pour l'identification des pz0
    Permet d attribuer 1 : si c'est un pz0 ou 0 si ca n'en est pas un pour :
    - chaque ligne de entrepot_zone
    - chaque ligne de entrepot_synthetise
    Selon le mode de saisie mis en argument : c'est une seule et meme fonction pour les deux modes de saisie
    puisque identifie simultanement et conjointement synthetise et realise 
"""
import pandas as pd
import numpy as np
from scripts.utils import fonctions_utiles 

def save_pz0_OK(df_pz0_vf,df_pz0_v1,codes_dephy_ok,status_post_pz0 = False):
    """ 
        Sauvegarde les lignes de zones ou synthetises identifiés comme valides
        
        Parametres : 
            df_pz0_vf : version finale du dataframe zone ou synthetise d'identification de pz0
            df_pz0_v1 : version 1 du dataframe zone ou synthetise d'identification de pz0 : identification zones et synthetise separees
            codes_dephy_ok : list de code dephy identifiés comme valide
            status_post_pz0 : bool. True : le status pz0 = 0 

        Return : Les deux data frames modifies
            df_pz0_vf : version finale du dataframe zone ou synthetise d'identification de pz0 
            df_pz0_v1 : version 1 du dataframe zone ou synthetise d'identification de pz0 : identification zones et synthetise separees
            
    """
    if status_post_pz0 is False :
        df_pz0_vf = pd.concat([df_pz0_vf,
                               df_pz0_v1.query('code_dephy == @codes_dephy_ok')])

    if status_post_pz0 is True :
        df_pz0_vf = pd.concat([df_pz0_vf,
                               df_pz0_v1.query('code_dephy == @codes_dephy_ok').assign(pz0 = 0)])

    # retirer les zones qui ont un status deja attribué
    df_pz0_v1 = df_pz0_v1.query('code_dephy != @codes_dephy_ok')
       
    return(df_pz0_vf,df_pz0_v1)

def identification_pz0(donnees,saisie):
    """
        série binaire avec en index l'id de l'entite indiquant si elle est un pz0
        La ligne i de cette série contient 1 si la ligne est identifié comme pz0, 
            0 si c'est un post-pz0 ou bien si la ligne n'a pas été prise en compte dans l'analyse.

                Paramètres:
                    donnees (dict) : dictionnaire de dataframe
                    saisie (chr) : "realise" ou "synthetise" qui conditionne le df retourne

                Retourne:
                    pz0 (Serie) : série binaire avec en index l'id de l'entite indiquant si elle est un pz0
                                    si saisie = "realise" : renvoie le df des zones
                                    si saisie = "synthetise" : renvoie les df des synthetises
    """
    # Initialisation des dataframes d'identification pz0 version finale que l'on va remplir au fur et a mesure
    synthetise_pz0_vf = pd.DataFrame()
    zone_pz0_vf = pd.DataFrame()

    # Les deux data frames principaux
    e_zone = donnees['zone'].copy()
    e_synthetise = donnees['synthetise'].copy()
    
    # Data frame recapitulatif des attributions des pz0
    df_pz0_recap = pd.DataFrame({'Etape':[],
                                    'cumul_reali_status_attribues':[],
                                    'cumul_synthe_status_attribues':[]})
    df_pz0_recap.loc[len(df_pz0_recap)] = ["0.1 : nombre de realise et synthetise totaux",len(e_zone),len(e_synthetise)]
    

    #### 1. Nettoyage des données 
    # pour l indentification, ne garder que itk sur lesquels il a au moins une culture
    id_zone_with_crops = fonctions_utiles.get_itk_with_crops(e_zone,donnees)
    zone = e_zone.query('id == @id_zone_with_crops') 

    id_synthe_with_crops = fonctions_utiles.get_itk_with_crops(e_synthetise,donnees)
    synthetise = e_synthetise.query('id == @id_synthe_with_crops')

    zone_sansculture = e_zone.query('id != @id_zone_with_crops')
    synthetise_sansculture = e_synthetise.query('id != @id_synthe_with_crops')

    df_pz0_recap.loc[len(df_pz0_recap)] = ["0.2 : nombre de realise et synthetise ayant au moins une culture",len(zone),len(synthetise)]

    # pour l indentification, ne garder que les itk qui ont un numero dephy
    zone = fonctions_utiles.get_num_dephy(zone,donnees)
    synthetise = fonctions_utiles.get_num_dephy(synthetise,donnees)

    zone_sanscodedephy = zone.query('code_dephy.isnull()')
    synthetise_sanscodedephy = synthetise.query('code_dephy.isnull()')

    zone = zone.query('code_dephy.notnull()')
    synthetise = synthetise.query('code_dephy.notnull()')

    df_pz0_recap.loc[len(df_pz0_recap)] = ["0.3 : nombre de realise et synthetise avec numero dephy",len(zone),len(synthetise)]

    #### 2. 1ere identification des pz0 réalisés et synthetise séparement

    # campagne minimale par code dephy
    min_campagne_z = fonctions_utiles.get_min_year_bydephy(zone)
    min_campagne_s = fonctions_utiles.get_min_year_bydephy(synthetise)

    # series de campagnes d'arrivee : 
    # en valeur les campagnes minimales possibles
    # en clé le nb d'années a ajouter pour avoir la fin du pz0 , selon les campagnes minimales
    #serie_campagne = {3 : [2008,2013,2018], 
    #                2 : [2009,2014,2019], 
    #                1 : [2010,2015,2020], 
    #                0 : [2011,2016,2021], 
    #                4 : [2012,2017,2022]}
    serie_campagne = {4 : [2008,2013,2018], 
                    3 : [2009,2014,2019], 
                    2 : [2010,2015,2020], 
                    1 : [2011,2016,2021], 
                    0 : [2012,2017,2022]}

    def get_key(val_search,_dict):
        for key,value in _dict.items():
            if val_search in value:
                return key

    # Creation de la colonne fin_pz0 : attribue le nb de annee a ajouter pour avoir la fin du pz0, selon le dictionnaire serie_campagne
    min_campagne_z['fin_pz0'] = [get_key(x,serie_campagne) for x in min_campagne_z['min_codedephy']]
    
    # pour les synthetises, cette regle par serie de campagnes d arrivees ne s'applique que dans les cas d'une campagne minimale monoannuelle. si c'est pluriannuel, fin_pz0 = 0
    min_campagne_s['fin_pz0'] = [get_key(min_campagne_s.iloc[x]['min_codedephy'],serie_campagne) 
                                if bool(min_campagne_s.iloc[x]['min_pluriannuel']) is False else 0 
                                for x in range(0,len(min_campagne_s))]
    
    print('nombre de codes dephy dans zone qui ont une campagne min 2012 ou 2017 ou 2022')
    print(min_campagne_z.loc[min_campagne_z['fin_pz0'] == 4.0])
    print('nombre de codes dephy dans synthetise qui ont une campagne min 2012 ou 2017 ou 2022')
    print(min_campagne_z.loc[min_campagne_z['fin_pz0'] == 4.0])
    
    # Attribution des pz0 : jointure du df de l'ensemble zone/synthetise + la table min code dephy / fin pz0
    # realise : pz0 = 1 : quand la campagne de la zone between ['min_codedephy', 'min_codedephy'+'fin_pz0']
    # => seront pz0 tous les monoannuels compris dans la vague de campagne
    zone_pz0_v1 = pd.merge(zone,min_campagne_z,on='code_dephy')
    zone_pz0_v1['pz0'] = (np.where(zone_pz0_v1['campagne']
                                        .between(zone_pz0_v1['min_codedephy'],zone_pz0_v1['min_codedephy'] + zone_pz0_v1['fin_pz0']),
                                        1, 0))
    # synthetise : pz0 = 1 : quand la campagne du synthetise between ['min_codedephy', 'min_codedephy'+'fin_pz0']
    synthetise_pz0_v1 = pd.merge(synthetise,min_campagne_s,on='code_dephy')
    synthetise_pz0_v1['pz0'] = (np.where(synthetise_pz0_v1['min_serie_campagne']
                                                .between(synthetise_pz0_v1['min_codedephy'],synthetise_pz0_v1['min_codedephy'] + synthetise_pz0_v1['fin_pz0']),
                                                1, 0))
    # suppression de la colonne fin_pz0
    zone_pz0_v1 = zone_pz0_v1.drop('fin_pz0',axis=1)
    synthetise_pz0_v1 = synthetise_pz0_v1.drop('fin_pz0',axis=1)

    #### 3. Croisement des identifications pz0 realises et synthetise
    # La consigne de saisie des pz0 est de saisir le point initial sur un synthétisé pluriannuel. 
    # Lorsque pour un numero dephy il y a un pz0 en synthétise et realise, on ne garde que le pz0 en synthétise, qu'il soit pluri ou monoannuel 

    df_cross = pd.concat([zone_pz0_v1[['code_dephy','id','campagne_sdc','pz0']].rename(columns = {'id':'zone_id'}), 
                   synthetise_pz0_v1[['code_dephy','id','campagnes','pz0']].rename(columns = {'id':'synthetise_id'})])
    
    df_cross['itk_mode'] = np.where(pd.notnull(df_cross['zone_id']), 'realise', 'synthetise')
    df_cross['pluriannuel'] = np.where((df_cross['campagnes'].str.len() > 1), True, False)

    summary = df_cross.groupby(['code_dephy','pz0','itk_mode','pluriannuel']
        )['code_dephy'].agg(['count']).reset_index()
    
    ###-----------------------------###
    ### 3.1 Les codes dephy qui n ont qu un seul mode de saisie
    ###-----------------------------###
    only_one_itk_mode = (summary
                        .filter(['code_dephy','itk_mode'])
                        .drop_duplicates()
                        .groupby(['code_dephy'])['code_dephy'].agg(['count'])
                        .reset_index()
                        .query('count == 1')['code_dephy']
                        .to_list()
    )

    ### Realises
    # selection puis sauvegarde dans le data frame zone_pz0_vf des zones qui n'ont pas de saisie en synthetise
    codedephy_realise_ok = summary.query('code_dephy == @only_one_itk_mode and itk_mode == "realise"')['code_dephy'].to_list()
    zone_pz0_vf,zone_pz0_v1 = save_pz0_OK(zone_pz0_vf,zone_pz0_v1,codedephy_realise_ok)

    # Remplissage du tableau recap
    df_pz0_recap.loc[len(df_pz0_recap)] = ["1.1 : realises ayant un mode de saisie uniquement en realise",len(zone_pz0_vf),0]

    ### Synthetise avec pz0 pluriannuel
    # selection puis sauvegarde dans le data frame synth_pz0_vf des synthetises qui n'ont pas de realises
    codedephy_synthetise_ok = summary.query('code_dephy == @only_one_itk_mode and itk_mode == "synthetise" and pluriannuel == True')['code_dephy'].to_list()
    synthetise_pz0_vf,synthetise_pz0_v1 = save_pz0_OK(synthetise_pz0_vf,synthetise_pz0_v1,codedephy_synthetise_ok)

    # Remplissage du tableau recap 
    df_pz0_recap.loc[len(df_pz0_recap)] = ["1.2 : synthetise ayant un mode de saisie uniquement en synthetise et un point zero identifie pluriannuel",0,len(synthetise_pz0_vf)]

    ### Synthetise avec pz0 monoannuel
    # selection puis sauvegarde dans le data frame synth_pz0_vf des synthetises qui n'ont pas de realises
    codedephy_synthetise_ok = summary.query('code_dephy == @only_one_itk_mode and itk_mode == "synthetise" and pluriannuel == False')['code_dephy'].to_list()
    synthetise_pz0_vf,synthetise_pz0_v1 = save_pz0_OK(synthetise_pz0_vf,synthetise_pz0_v1,codedephy_synthetise_ok)

    # Remplissage du tableau recap 
    df_pz0_recap.loc[len(df_pz0_recap)] = ["1.3 : synthetise ayant un mode de saisie uniquement en synthetise et un point zero identifie monoannuel",0,len(synthetise_pz0_vf)]
    
    ###-----------------------------###
    ### 3.2 Les codes dephy avec un pz0 synthetise pluriannuel puis saisie en realise.
    ###-----------------------------###
    
    # union par le code dephy des campagnes minimum en realise et synthetise
    union_r_s_min_campagne = (pd.merge(min_campagne_z.assign(type = 'realise'),
                min_campagne_s.assign(type = 'synthetise'),
                on = 'code_dephy',suffixes= ['_r','_s'],
                how = 'outer'))

    code_dephy_pz0_ok = (union_r_s_min_campagne.query('min_codedephy_r >= min_codedephy_s and min_pluriannuel == True')
                            ['code_dephy'].to_list())
    
    # Sauvegarde des realises en changeant le status à post-pz0 pour tous 
    zone_pz0_vf,zone_pz0_v1 = save_pz0_OK(zone_pz0_vf,zone_pz0_v1,code_dephy_pz0_ok,status_post_pz0=True)

    # Sauvegarde des synthetises
    synthetise_pz0_vf,synthetise_pz0_v1 = save_pz0_OK(synthetise_pz0_vf,synthetise_pz0_v1,code_dephy_pz0_ok)

    # Remplissage du tableau recap 
    df_pz0_recap.loc[len(df_pz0_recap)] = ["2 : synthetise pluri annuel detectes comme pz0 anterieur aux realises du meme code dephy",
                                        len(zone_pz0_vf),len(synthetise_pz0_vf)]

    ###-----------------------------###
    ### 3.3 Les codes dephy avec un pz0 synthetise monoannuel puis saisie en realise.
    ###-----------------------------###
    code_dephy_pz0_ok = (union_r_s_min_campagne.query('min_codedephy_r >= min_codedephy_s and min_pluriannuel == False')
                            ['code_dephy'].to_list())

    # Sauvegarde des realises en changeant le status à post-pz0 pour tous 
    zone_pz0_vf,zone_pz0_v1 = save_pz0_OK(zone_pz0_vf,zone_pz0_v1,code_dephy_pz0_ok,status_post_pz0=True)

    # Sauvegarde des synthetises
    synthetise_pz0_vf,synthetise_pz0_v1 = save_pz0_OK(synthetise_pz0_vf,synthetise_pz0_v1,code_dephy_pz0_ok)

    # Remplissage du tableau recap 
    df_pz0_recap.loc[len(df_pz0_recap)] = ["3 : synthetise mono annuel detectes comme pz0 anterieur aux realises du meme code dephy",
                                        len(zone_pz0_vf),len(synthetise_pz0_vf)]

    ###-----------------------------###
    ### 4. Que fait t ont du reste , où il ya des realises pz0 avant des synthetises ? 
    ###-----------------------------###

    code_dephy_pz0_inclassable = (union_r_s_min_campagne.query('min_codedephy_r < min_codedephy_s')['code_dephy'].to_list())

    # Sauvegarde des realises en changeant le status à post-pz0 pour tous 
    zone_pz0_vf,zone_pz0_v1 = save_pz0_OK(zone_pz0_vf,zone_pz0_v1,code_dephy_pz0_inclassable,status_post_pz0=True)

    # Sauvegarde des synthetises
    synthetise_pz0_vf,synthetise_pz0_v1 = save_pz0_OK(synthetise_pz0_vf,synthetise_pz0_v1,code_dephy_pz0_inclassable,status_post_pz0=True)

    # Remplissage du tableau recap 
    df_pz0_recap.loc[len(df_pz0_recap)] = ["4 : realises avant synthetises",len(zone_pz0_vf),len(synthetise_pz0_vf)]


    ###-----------------------------###
    ### 5. attribution pz0 False pour les zones et synthetises sans code dephy, et sur lesquels il n'y a pas de culture
    ###-----------------------------###

    # sans cultures 
    zone_pz0_vf = pd.concat([zone_pz0_vf,
                            zone_sansculture.assign(pz0 = 0),
                            zone_sanscodedephy.assign(pz0 = 0)])

    synthetise_pz0_vf = pd.concat([synthetise_pz0_vf,
                            synthetise_sansculture.assign(pz0 = 0),
                            synthetise_sanscodedephy.assign(pz0 = 0)])


    df_pz0_recap.loc[len(df_pz0_recap)] = ["5 : attribution pz0 False pour les zones et synthetises sans code dephy, et sur lesquels il n'y a pas de culture",
                                        len(zone_pz0_vf),len(synthetise_pz0_vf)]

    print(df_pz0_recap)

    zone_pz0_vf.set_index('id',inplace = True)
    synthetise_pz0_vf.set_index('id',inplace = True)

    zone.to_csv('~/zone_with_codedephy.csv', sep =';')  
    zone_pz0_vf.to_csv('~/zone_pz0_vf.csv', sep =';')  
    synthetise_pz0_vf.to_csv('~/synthetise_pz0_vf.csv', sep =';')  

    if saisie == "realise" :
        return zone_pz0_vf['pz0']
    
    if saisie == "synthetise" :
        return synthetise_pz0_vf['pz0']
