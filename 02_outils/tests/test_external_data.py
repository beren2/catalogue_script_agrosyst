"""
    Contient tous les tests effectués sur les données externes. 
    Ces fonctions permettent de s'assurer que les données externes dont dépend le processus 
    de génération sont conformes à ce qui est attendu en entrée.
"""
import pandas as pd

def check_BDD_donnees_attendues_CAN(donnees):
    """ 
        permet de checker la table BDD_donnees_attendues_CAN, 
        ie de s'assurer qu'elle correspond au format attendu :
        TODO 
    """
    message_error = ""

    df = donnees['BDD_donnees_attendues_CAN']
    cols_to_keep = [col for col in df.columns if '20' in col]
    cols_to_keep.append('codes_SdC')

    df_melt = pd.melt(df[cols_to_keep], id_vars=['codes_SdC'],var_name='campagne',value_name='donnee_attendue')
    df_melt['campagne'] = df_melt['campagne'].astype('int64')

    # Check des modalités attendues
    values_count = df_melt['donnee_attendue'].value_counts().to_dict()
    data_expected = ['Pas de donnees attendues','PZ0 attendu','donnees annuelles attendues']

    data_unexpected = [value for value in values_count.keys() if value not in data_expected]

    if len(data_unexpected) != 0:
        message_error = message_error + "\n" + "\t" + "Attention il y a une modalité de donnée attendue inconnue : " + str(data_unexpected)

    # Check de la cohérence des frises chronologiques : 
    # - nb de PZ0 == 3
    # - pz0 consécutifs : que la difference entre la campagne min et max soit de 2 (cas avec 3 pz0)
    
    df_pz0 = df_melt.loc[df_melt['donnee_attendue'] == "PZ0 attendu",:]
    
    pd.options.mode.copy_on_write = True
    df_pz0.loc[:,'diff_campagne_pz0'] = df_pz0.loc[:,'campagne']
   

    error_ref = df_pz0.groupby(['codes_SdC'], dropna=False).agg({
        'donnee_attendue' : 'size',
        'diff_campagne_pz0' : lambda x : x.max() - x.min(),
        'campagne' : lambda x: ', '.join(x.astype('str'))
        }).rename(columns={'donnee_attendue' : 'nb_pz0', 'campagne':'campagnes_pz0'}).reset_index()
    
    error_ref['nb_pz0'] = error_ref['nb_pz0'].astype('int64')
    
    error_ref = error_ref.loc[(error_ref.loc[:,'nb_pz0'] != 3) | (error_ref.loc[:,'diff_campagne_pz0'] != 2),:]

    if error_ref.shape[0] != 0:
        message_error = message_error + "\n" + "\t" + "Attention il y a des incohérences dans le référentiel : \n"
        message_error = message_error + str(error_ref)
    return [message_error]

def typo_especes_typo_culture(donnees):
    """
        permet de checker la table typo_especes_typo_culture,
        ie de s'assurer qu'elle correspond au format attendu :
        TODO
    """
    return []
