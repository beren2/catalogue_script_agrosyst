"""
	Regroupe les fonctions permettant de générer le magasin DEPHYGraph.
"""
import pandas as pd
# import numpy as np

def clean_list(lst):
    """
    Permet de nettoyer une liste en enlevant les valeurs 'nan' (str) et en retournant None si la liste est vide. Si la liste ne contient qu'un seul élément, retourne cet élément directement.
    """
    cleaned = [x for x in lst if str(x) != 'nan']
    if len(cleaned) == 1:
        cleaned = cleaned[0]
    return cleaned if cleaned else None

def get_all_species_and_variety_from_sdc_or_synth(donnees) :
    """
    Permet de récupérer pour chaque SDC ou chaque synthétisé, la liste des espèces et variétés cultivées, ainsi que le nombre d'espèces et variétés différentes cultivées. Ce sont les libellés qui sont récupérés ou les dénominations. Lorsqu'il est préciser 'util' cela signifie que pour l'arboriculture, on ne garde que les espèces importantes (liste définie dans le code). En viticulture, on garde tout. A chaque fois on récupère une liste des libellés uniques.
    """
    # Chargement des données nécessaires
    sdc = donnees["sdc"]['id','code_dephy','filiere'].copy()
    synthetise = donnees["synthetise"]['id', 'nom', 'campagnes', 'sdc_id'].copy()
    
    parcelle = donnees["parcelle"]['id','sdc_id'].copy()
    zone = donnees["zone"]['id','parcelle_id'].copy()

    plantation_perenne_synthetise = donnees["plantation_perenne_synthetise"]['id','synthetise_id'].copy()
    plantation_perenne_realise = donnees["plantation_perenne_realise"]['id','culture_id','zone_id'].copy()
    noeuds_synthetise = donnees["noeuds_synthetise"]['id','synthetise_id'].copy()
    noeuds_realise = donnees["noeuds_realise"]['id','culture_id','zone_id'].copy()

    composant_culture = donnees["composant_culture"].copy()
    espece = donnees["espece"]['id','code_espece_botanique','libelle_espece_botanique','typocan_espece','typocan_espece_maraich'].copy()
    variete = donnees["variete"]['id','denomination'].copy()

    plantation_perenne_synthetise_restructure = donnees['plantation_perenne_synthetise_restructure'].copy()
    noeuds_synthetise_restructure = donnees['noeuds_synthetise_restructure'].copy()

    # merge utiles
    plantation_perenne_synthetise = plantation_perenne_synthetise.merge(plantation_perenne_synthetise_restructure, on='id', how='left')
    del(plantation_perenne_synthetise_restructure)

    noeuds_synthetise = noeuds_synthetise.merge(noeuds_synthetise_restructure, on='id', how='left')
    del(noeuds_synthetise_restructure)

    composant_culture = composant_culture.merge(espece.rename(columns={'id': 'espece_id'}), on='espece_id', how='left').merge(variete.rename(columns={'id': 'variete_id'}), on='variete_id', how='left')
    del(espece, variete)

    noeuds_realise = noeuds_realise.merge(zone.rename(columns={'id': 'zone_id'}), on='zone_id', how='left').merge(parcelle.rename(columns={'id': 'parcelle_id'}), on='parcelle_id', how='left')
    plantation_perenne_realise = plantation_perenne_realise.merge(zone.rename(columns={'id': 'zone_id'}), on='zone_id', how='left').merge(parcelle.rename(columns={'id': 'parcelle_id'}), on='parcelle_id', how='left')
    del(zone, parcelle)

    # Concaténation des entités liées aux cultures ==> df principal
    all_nodes= pd.concat([
        noeuds_realise[['id','culture_id','sdc_id']].assign(type='assole'),
        noeuds_synthetise[['id','culture_id','synthetise_id']].assign(type='assole'),
        plantation_perenne_realise[['id','culture_id','sdc_id']].assign(type='peren'),
        plantation_perenne_synthetise[['id','culture_id','synthetise_id']].assign(type='peren')
    ])
    del(noeuds_realise, noeuds_synthetise, plantation_perenne_realise, plantation_perenne_synthetise)


    def get_unique_list_analyses_especes_variete_sdc_synthe(row, column, filiere_col='filiere'):
        """
        Pour ARBO on filtre sur les espèces importantes. pas pour la VITI
        A UTILISER POUR LA FONCTION analyses_especes_variete_sdc_synthe
        """
        if row[filiere_col] == 'ARBORICULTURE':
            return clean_list(row['filtered_culture_util'][column].unique().tolist())
        return clean_list(row['filtered_culture'][column].unique().tolist())
    

    def analyses_especes_variete_sdc_synthe(df, groupby_col, lib_sp_arbo):
        """
        Crée des groupes par sdc_id ou synthetise_id (dépend de réalisé ou synthétisé). Pour chaque groupe, on récupère TOUTES les espèces présentes, on garde que les libellés uniques, on fait de même mais en filtrant sur la liste des epèces importantes en arbo (ou pas si VITI). On compte le nombre d'espèces différentes utiles. On fait la même pcédure pour les variétés.
        
        df: all_node
        groupby_col: variable concat de sdc_id et synthetise_id
        code_sp_arbo: défini ce qui est 'utile' soit la liste des epsece ARBO, filtré sur filiere

        Return:
        DataFrame avec pour chaque sdc_id ou synthetise_id:
            - filiere
            - code_dephy
            - unique_species: liste des libellés espèces uniques
            - unique_variete: liste des dénominations variétés uniques
            - unique_species_util: liste des libellés espèces uniques (filtrées sur les utiles pour arbo)
            - unique_variete_util: liste des dénominations variétés uniques (filtrées sur les utiles pour arbo)
            - size_unique_sp: nombre d'espèces différentes (filtrées sur les utiles pour arbo)
            - size_unique_var: nombre de variétés différentes (filtrées sur les utiles pour arbo)
        """

        # Besoin absolu de l'sdc_id ou du synthetise_id
        df_filtered = df[df[groupby_col].notna()]

        result = df_filtered.groupby(groupby_col).apply(
            lambda cgrp: pd.Series({
                'filiere': cgrp['filiere'].iloc[0],
                'code_dephy': cgrp['code_dephy'].iloc[0],
                'filtered_culture': composant_culture[composant_culture['culture_id'].isin(cgrp['culture_id'])],
                'filtered_culture_util': composant_culture[
                    (composant_culture['culture_id'].isin(cgrp['culture_id'])) &
                    (composant_culture['libelle_espece_botanique'].isin(lib_sp_arbo))
                ],
            }),
            include_groups=False
        )

        # Analyse des espèces et variété par groupe (liste des libellés uniques, des libellés uniques utiles, compte des uniques)
        result['unique_species'] = result['filtered_culture'].apply(
            lambda x: clean_list(x['libelle_espece_botanique'].unique().tolist())
        )
        result['unique_variete'] = result['filtered_culture'].apply(
            lambda x: clean_list(x['denomination'].unique().tolist())
        )
        result['unique_species_util'] = result.apply(lambda row: get_unique_list_analyses_especes_variete_sdc_synthe(row, 'libelle_espece_botanique'), axis=1)
        result['unique_variete_util'] = result.apply(lambda row: get_unique_list_analyses_especes_variete_sdc_synthe(row, 'denomination'), axis=1)
        result['size_unique_sp'] = result['unique_species_util'].apply(
            lambda x: len(x) if isinstance(x, list) else 1 if x is not None else 0
        )
        result['size_unique_var'] = result['unique_variete_util'].apply(
            lambda x: len(x) if isinstance(x, list) else 1 if x is not None else 0
        )

        result = result.drop(columns=['filtered_culture', 'filtered_culture_util'])

        return result

    # Liste des libellés espèce que l'on souhaite gardé en Arbo
    lib_sp_arbo = ["Pommier", "Poirier", "Pêcher", "Abricotier", "Prunier", "Clémentinier", "Noyer", "Olivier", "Cerisier"] #["G21", "G20", "G07", "E01", "G28", "E85", "F84", "F86", "E67"]

    # On ajoute les infos filiere et codedephy 
    all_nodes['group_id'] = all_nodes['sdc_id'].fillna(all_nodes['synthetise_id'])
    all_nodes = all_nodes.merge(synthetise[['id', 'sdc_id']].rename(columns={'id': 'synthetise_id', 'sdc_id': 'sdc_id_fromsynth'}), on='synthetise_id', how='left')
    all_nodes['sdc_id'] = all_nodes['sdc_id'].fillna(all_nodes['sdc_id_fromsynth'])
    all_nodes = all_nodes.merge(sdc[['id', 'code_dephy', 'filiere']].rename(columns={'id': 'sdc_id'}), on='sdc_id', how='left').drop(columns=['sdc_id_fromsynth'], errors='ignore')

    # Utilisation de la fonction
    df_final = analyses_especes_variete_sdc_synthe(all_nodes.loc[all_nodes['filiere'].isin(['ARBORICULTURE','VITICULTURE'])], 'group_id', lib_sp_arbo)

    return df_final


def all_steps_for_maj_dephygraph(donnees):
    """
    Regroupe toutes les étapes nécessaires pour la mise à jour du magasin DEPHYGraph.
    """
    # Chargement des données nécessaires
    sdc = donnees["sdc"]['id','code_dephy','filiere']
    synthetise = donnees["synthetise"]['id', 'nom', 'campagnes', 'sdc_id']
    
    parcelle = donnees["parcelle"]['id','sdc_id']
    zone = donnees["zone"]['id','parcelle_id']

    plantation_perenne_synthetise = donnees["plantation_perenne_synthetise"]['id','synthetise_id']
    plantation_perenne_realise = donnees["plantation_perenne_realise"]['id','culture_id','zone_id']
    noeuds_synthetise = donnees["noeuds_synthetise"]['id','synthetise_id']
    noeuds_realise = donnees["noeuds_realise"]['id','culture_id','zone_id']

    composant_culture = donnees["composant_culture"]
    espece = donnees["espece"]['id','code_espece_botanique','libelle_espece_botanique','typocan_espece','typocan_espece_maraich']
    variete = donnees["variete"]['id','denomination']

    plantation_perenne_synthetise_restructure = donnees['plantation_perenne_synthetise_restructure']
    noeuds_synthetise_restructure = donnees['noeuds_synthetise_restructure']


    # Récupération des espèces et variétés pour chaque SDC et synthétisé
    species_variety_info = get_all_species_and_variety_from_sdc_or_synth(donnees)
    

    mag_dg = 'a'
    return mag_dg