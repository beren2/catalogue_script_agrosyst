"""
    Fichier de test pour l'identification des pz0
    Permet d attribuer 1 : si c'est un pz0 ou 0 si ca n'en est pas un pour :
    - chaque ligne de entrepot_zone
    - chaque ligne de entrepot_synthetise
"""

import os
import pandas as pd
import numpy as np
#from scripts.utils import fonctions_utiles
import fonctions_utiles

def identification_pz0_realise(donnees):
    """
        Retourne une série binaire de taille n. 
        La ligne i de cette série contient 1 si le test est passé pour la ligne, 0 sinon.

                Paramètres:
                    donnees (df) : dataframe contenant les données d'intrants
                    metadata_seuils (df) : dataframe contenant les metadonnées sur les seuils 
                        du test

                Retourne:
                    code_test (Serie) : série binaire de taille n indiquant si le test est passé
    """
    # copie des données en local
    donnees_local = donnees.copy()

    return donnees_local['code_test']

os.chdir("C:/Users/lubaude/Documents/Datagrosyst/catalogue_script/catalogue_script_agrosyst/scripts/pz0/")

e_zone = pd.read_csv("./data/zone.csv", delimiter=',')
e_synthetise = pd.read_csv("./data/synthetise.csv", delimiter=',')

# Data frame recapitulatif des attributions des pz0
df_pz0_recap = pd.DataFrame({'Etape':[],
                                 'cumul_reali_status_attribues':[],
                                 'cumul_synthe_status_attribues':[]})
df_pz0_recap.loc[len(df_pz0_recap)] = ["0.1 : nombre de realise et synthetise totaux",len(e_zone),len(e_synthetise)]

# Initialisation
synthetise_pz0_vf = pd.DataFrame()
zone_pz0_vf = pd.DataFrame()

#### 1. Nettoyage des données 
# ne garder que itk sur lesquels il a au moins une culture pour l indentification
id_zone_with_crops = fonctions_utiles.get_itk_with_crops(e_zone)
zone = e_zone.query('id == @id_zone_with_crops')

id_synthe_with_crops = fonctions_utiles.get_itk_with_crops(e_synthetise)
synthetise = e_synthetise.query('id == @id_synthe_with_crops')

zone_sansculture = e_zone.query('id != @id_zone_with_crops')
synthetise_sansculture = e_synthetise.query('id != @id_synthe_with_crops')

df_pz0_recap.loc[len(df_pz0_recap)] = ["0.2 : nombre de realise et synthetise ayant au moins une culture",len(zone),len(synthetise)]

# codes dephy, ne garder que les itk qui ont un numero dephy pour l indentification
zone = fonctions_utiles.get_num_dephy(zone)
synthetise = fonctions_utiles.get_num_dephy(synthetise)

zone_sanscodedephy = zone.query('code_dephy.isnull()')
synthetise_sanscodedephy = synthetise.query('code_dephy.isnull()')

zone = zone.query('code_dephy.notnull()')
synthetise = synthetise.query('code_dephy.notnull()')

df_pz0_recap.loc[len(df_pz0_recap)] = ["0.3 : nombre de realise et synthetise avec numero dephy",len(zone),len(synthetise)]

#### 2. 1ere identification des pz0 zones et réalisés séparement

# campagne minimale par code dephy
min_campagne_z = fonctions_utiles.get_min_year_bydephy(zone)
min_campagne_s = fonctions_utiles.get_min_year_bydephy(synthetise)

# series de campagnes d'arrivee : 
# en valeur les campagnes minimales possibles
# en clé le nb d'années a ajouter pour avoir la fin du pz0 , selon les campagnes minimales
serie_campagne = {3 : [2008,2013,2018], 
                  2 : [2009,2014,2019], 
                  1 : [2010,2015,2020], 
                  0 : [2011,2016,2021], 
                  4 : [2012,2017,2022]}

def get_key(val_search,dict):
    for key,value in dict.items():
        if val_search in value:
            return key
        
min_campagne_z['fin_pz0'] = [get_key(x,serie_campagne) for x in min_campagne_z['min_codedephy']]
# pour les synthetises, cette regle par serie de campagnes d arrivees ne s'applique que dans les cas d'une campagne minimale monoannuelle

min_campagne_s['fin_pz0'] = [get_key(min_campagne_s.iloc[x]['min_codedephy'],serie_campagne) 
                             if bool(min_campagne_s.iloc[x]['min_pluriannuel']) is False else 0 
                             for x in range(0,len(min_campagne_s))]

zone_pz0_v1 = pd.merge(zone,min_campagne_z,on='code_dephy')
zone_pz0_v1['pz0'] = (np.where(zone_pz0_v1['campagne']
                                      .between(zone_pz0_v1['min_codedephy'],zone_pz0_v1['min_codedephy'] + zone_pz0_v1['fin_pz0']),
                                       1, 0))

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

summary = fonctions_utiles.cross_realise_synthetise(zone_pz0_v1,synthetise_pz0_v1)

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
# selection puis sauvegarde dans le data frame zone_pz0_vf des zones identifiées comme pz0 à l'étape 1 qui sont correctes puisque pas de saisie en synthetise
codedephy_realise_ok = summary.query('code_dephy == @only_one_itk_mode and itk_mode == "realise"')['code_dephy'].to_list()

zone_pz0_vf,zone_pz0_v1 = fonctions_utiles.save_pz0_OK(zone_pz0_vf,zone_pz0_v1,codedephy_realise_ok)

# Remplissage du tableau recap
df_pz0_recap.loc[len(df_pz0_recap)] = ["1.1 : realises ayant un mode de saisie uniquement en realise",len(zone_pz0_vf),0]

### Synthetise avec pz0 pluriannuel
# selection puis sauvegarde dans le data frame synth_pz0_vf des synthetises identifiées comme pz0 , et qui n'ont pas de realises
codedephy_synthetise_ok = summary.query('code_dephy == @only_one_itk_mode and itk_mode == "synthetise" and pluriannuel == True')['code_dephy'].to_list()

synthetise_pz0_vf,synthetise_pz0_v1 = fonctions_utiles.save_pz0_OK(synthetise_pz0_vf,synthetise_pz0_v1,codedephy_synthetise_ok)

# Remplissage du tableau recap 
df_pz0_recap.loc[len(df_pz0_recap)] = ["1.2 : synthetise ayant un mode de saisie uniquement en synthetise et un point zero identifie pluriannuel",0,len(synthetise_pz0_vf)]

### Synthetise avec pz0 monoannuel
# selection puis sauvegarde dans le data frame synth_pz0_vf des synthetises identifiées comme pz0, et qui n'ont pas de realises
codedephy_synthetise_ok = summary.query('code_dephy == @only_one_itk_mode and itk_mode == "synthetise" and pluriannuel == False')['code_dephy'].to_list()

synthetise_pz0_vf,synthetise_pz0_v1 = fonctions_utiles.save_pz0_OK(synthetise_pz0_vf,synthetise_pz0_v1,codedephy_synthetise_ok)

# Remplissage du tableau recap 
df_pz0_recap.loc[len(df_pz0_recap)] = ["1.3 : synthetise ayant un mode de saisie uniquement en synthetise et un point zero identifie monoannuel",0,len(synthetise_pz0_vf)]


###-----------------------------###
### 3.2 Les codes dephy avec un pz0 synthetise pluriannuel puis saisie en realise.
###-----------------------------###

union_r_s_min_campagne = (pd.merge(min_campagne_z.assign(type = 'realise'),
              min_campagne_s.assign(type = 'synthetise'),
              on = 'code_dephy',suffixes= ['_r','_s'],
              how = 'outer'))

code_dephy_pz0_ok = (union_r_s_min_campagne.query('min_codedephy_r >= min_codedephy_s and min_pluriannuel == True')
                         ['code_dephy'].to_list())

# Sauvegarde des realises en changeant le status à post-pz0 pour tous 
zone_pz0_vf,zone_pz0_v1 = fonctions_utiles.save_pz0_OK(zone_pz0_vf,zone_pz0_v1,code_dephy_pz0_ok,status_post_pz0=True)

# Sauvegarde des synthetises
synthetise_pz0_vf,synthetise_pz0_v1 = fonctions_utiles.save_pz0_OK(synthetise_pz0_vf,synthetise_pz0_v1,code_dephy_pz0_ok)

# Remplissage du tableau recap 
df_pz0_recap.loc[len(df_pz0_recap)] = ["2 : synthetise pluri annuel detectes comme pz0 anterieur aux realises du meme code dephy",
                                       len(zone_pz0_vf),len(synthetise_pz0_vf)]

###-----------------------------###
### 3.3 Les codes dephy avec un pz0 synthetise monoannuel puis saisie en realise.
###-----------------------------###
code_dephy_pz0_ok = (union_r_s_min_campagne.query('min_codedephy_r >= min_codedephy_s and min_pluriannuel == False')
                         ['code_dephy'].to_list())

# Sauvegarde des realises en changeant le status à post-pz0 pour tous 
zone_pz0_vf,zone_pz0_v1 = fonctions_utiles.save_pz0_OK(zone_pz0_vf,zone_pz0_v1,code_dephy_pz0_ok,status_post_pz0=True)

# Sauvegarde des synthetises
synthetise_pz0_vf,synthetise_pz0_v1 = fonctions_utiles.save_pz0_OK(synthetise_pz0_vf,synthetise_pz0_v1,code_dephy_pz0_ok)

# Remplissage du tableau recap 
df_pz0_recap.loc[len(df_pz0_recap)] = ["3 : synthetise mono annuel detectes comme pz0 anterieur aux realises du meme code dephy",
                                       len(zone_pz0_vf),len(synthetise_pz0_vf)]

###-----------------------------###
### 4. Que fait t ont du reste , où il ya des realises pz0 avant des synthetises ? 
###-----------------------------###

code_dephy_pz0_inclassable = (union_r_s_min_campagne.query('min_codedephy_r < min_codedephy_s')['code_dephy'].to_list())

# Sauvegarde des realises en changeant le status à post-pz0 pour tous 
zone_pz0_vf,zone_pz0_v1 = fonctions_utiles.save_pz0_OK(zone_pz0_vf,zone_pz0_v1,code_dephy_pz0_inclassable,status_post_pz0=True)

# Sauvegarde des synthetises
synthetise_pz0_vf,synthetise_pz0_v1 = fonctions_utiles.save_pz0_OK(synthetise_pz0_vf,synthetise_pz0_v1,code_dephy_pz0_inclassable,status_post_pz0=True)

# Remplissage du tableau recap 
df_pz0_recap.loc[len(df_pz0_recap)] = ["4 : realises avant synthetises que fait ont d eux ?",len(zone_pz0_vf),len(synthetise_pz0_vf)]


###-----------------------------###
### 5. attribution pz0 False pour les zones et synthetises sans code dephy, et sur lesquels il n'y a pas de culture
###-----------------------------###

# sans cultures 
zone_pz0_vf = pd.concat([zone_pz0_vf,
                        zone_sansculture.assign(pz0 = 2),
                        zone_sanscodedephy.assign(pz0 = 3)])

synthetise_pz0_vf = pd.concat([synthetise_pz0_vf,
                          synthetise_sansculture.assign(pz0 = 2),
                          synthetise_sanscodedephy.assign(pz0 = 3)])


df_pz0_recap.loc[len(df_pz0_recap)] = ["5 : attribution pz0 False pour les zones et synthetises sans code dephy, et sur lesquels il n'y a pas de culture",
                                       len(zone_pz0_vf),len(synthetise_pz0_vf)]


zone_pz0_vf.to_csv(r"./zone_pz0_vf.csv", index=False)
synthetise_pz0_vf.to_csv(r"./synthetise_pz0_vf.csv", index=False)

print(df_pz0_recap)
