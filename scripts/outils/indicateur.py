"""
	Regroupe les fonctions qui consistent en des calculs d'indicateurs 
"""

import pandas as pd
import numpy as np
from scripts.utils import fonctions_utiles

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
    left = res
    right = fonctions_utiles.get_utilisation_intrant_in_unit(donnees)
    merge = pd.merge(left, right, left_on='id', right_on='id', how='left')


    return merge[
        [
            'id', 'dose_ref_maa', 'unit_dose_ref_maa', 
            'code_culture_maa', 'code_groupe_cible_maa', 'code_traitement_maa', 'dose_unite_standardise', 'unite_standardise'
        ]
    ].set_index('id')


def str_replace_code_dephy(df,regex_pattern,pattern_replace):
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
    df_sdc['campagne'] = df_sdc['campagne'].astype('str')

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

    df_sdc = str_replace_code_dephy(df_sdc,'',np.NaN)

    # Merge 'left' entre les donnees saisies sur agrosyst et le referentiel des donnees attendues par la CAN    
    merge = pd.merge(df_sdc, saisies_attendues_melt, left_on=['code_dephy','campagne'],right_on=['code_dephy','campagne'], how = 'left')

    # tag des sdc non dephy ou suivi non detaille
    merge['donnee_attendue'] = merge.apply(
        lambda x: 'inconnue : hors dephy ferme ou suivi non detaille' if (x['donnee_attendue'] != 'inconnue dephy ferme') & (
                                                                        (x['type'] != 'DEPHY_FERME') |
                                                                        (x['modalite_suivi_dephy'] != 'DETAILLE')) else x['donnee_attendue'] , axis=1)
    print("Repartition de l'attribution des donnees attendues")
    print(merge.groupby(by='donnee_attendue').size())
    
    return(merge[['sdc_id','code_dephy','campagne','donnee_attendue']])

