"""Module utiles."""
import re
import pandas as pd
import numpy as np
from tqdm import tqdm



def get_surfaces_connections_synthetise(df_synthetise,
                                       df_culture,
                                       df_noeuds_synthetise,
                                       df_connection_synthetise,
                                       df_intervention_synthetise,
                                       df_plantation_perenne_synthetise,
                                       df_sdc,
                                       df_dispositif,
                                       df_domaine):
    """
        Retourne un dataframe où on associe la surface au sol aux connections en synthétisé
        Colonnes du dataframe de sortie : 
            - surface (ha)                      (valeur de la surface en hectare)
        Indice du dataframe de sortie :
            - connection_synthetise_id          (identifiant de la connection en synthétisé)
    """

    ####################################################################################################
    # On augmente quelques dataframes d'infos supplémentaires servant à filtrer les systèmes synthétisés valides et en corriger certains
    ####################################################################################################

    # on ajoute une colonne à la table culture disant si oui ou non on est une culture fictive
    df_culture = add_column_fictif(df_culture=df_culture)

    # on ajoute campagne_sdc à la table synthetise
    df_synthetise = add_column_campagne(df_synthetise=df_synthetise, df_sdc=df_sdc)

    # on ajoute campagne, cultureID et fictif à la table noeuds_synthetise
    df_noeuds_synthetise = add_columns_campagne_cultureID_fictif(df_noeuds_synthetise=df_noeuds_synthetise, df_culture=df_culture, df_synthetise=df_synthetise, df_domaine=df_domaine)

    # on ajoute sau_(Ha) à la table synthetise
    df_synthetise = add_column_sau(df_synthetise=df_synthetise, df_sdc=df_sdc, df_dispositif=df_dispositif, df_domaine=df_domaine)

    # on ajoute synthetise_id à la table connection_synthetise
    df_connection_synthetise = add_column_synthetise_id_to_connection(df_connection_synthetise=df_connection_synthetise, df_noeuds_synthetise=df_noeuds_synthetise)

    # on ajoute synthetise_id à la table intervention_synthetise
    df_intervention_synthetise = add_column_synthetise_id_to_intervention(df_intervention_synthetise=df_intervention_synthetise, df_connection_synthetise=df_connection_synthetise)

    ####################################################################################################
    # On groupe les éléments des graphes de rotations synthetises ensembles
    ####################################################################################################

    df_noeuds_synthetise_grouped = df_noeuds_synthetise.groupby('synthetise_id')
    df_connection_synthetise_grouped = df_connection_synthetise.groupby('synthetise_id')
    df_intervention_synthetise_grouped = df_intervention_synthetise.groupby('synthetise_id')
    df_plantation_perenne_synthetise_grouped = df_plantation_perenne_synthetise.groupby('synthetise_id')

    # la fonction qui filtre et renvoie groupés les graphes de rotation synthétisés
    def filter_rotation_synthetise_(synthetise_id):
        graph_synthetise = filter_rotation_graph(synthetise_id=synthetise_id,
                                                                  df_noeuds_synthetise_grouped=df_noeuds_synthetise_grouped,
                                                                  df_connection_synthetise_grouped=df_connection_synthetise_grouped,
                                                                  df_intervention_synthetise_grouped=df_intervention_synthetise_grouped,
                                                                  delete_empty_arete=False)
        return graph_synthetise

    ret_noeuds, ret_aretes = [], []
    for synthetise_id in tqdm(df_synthetise.index, total=len(df_synthetise)):
        graph_synthetise = filter_rotation_synthetise_(synthetise_id)
        if graph_synthetise['valid']:
            
            # on calcule les surfaces associées aux noeuds et aux aretes
            noeuds, aretes = correct_rang0_and_compute_importances(graph_synthetise['noeuds'], graph_synthetise['aretes'])

            # on récupère les surfaces déjà occupées par les plantations pérennes renseignées en synthétisé
            if synthetise_id in df_plantation_perenne_synthetise_grouped.groups:
                pct_occupation_perennes = sum(df_plantation_perenne_synthetise_grouped.get_group(synthetise_id)['pct_occupation_sol'])
            else:
                pct_occupation_perennes = 0
            # la surface disponible pour l'assolé est donc :
            surface_disponible_synthetise_assole = df_synthetise.loc[synthetise_id, 'sau_(Ha)'] * (100 - pct_occupation_perennes)/100

            ###############################################
            # on récupère le nombre d'années de la rotation
            ###############################################
            n_annees = noeuds['rang'].max() + 1
            
            noeuds_0 = noeuds.loc[noeuds['rang']==0]
            rang_0_removed = False
            # si la rotation débute par un précédent fictif au rang 0, on retire le rang 0 (donc 1) dans le nombre d'année de la rotation
            if len(noeuds_0) == 1 and noeuds_0.iloc[0]['fictif']:
                rang_0_removed = True
                n_annees -= 1

            # si un rang ne contient que des cultures de la même années que les cultures précédentes, on retire ce rang (donc 1) dans le nombre d'année de la rotation
            rang_is_cultures_intermediaires = noeuds.groupby('rang').apply(lambda x: (x['memecampagne_noeudprecedent']=='t').all()).drop(index=0)
            if rang_0_removed:
                # si le rang 1 est décrit comme de la meme campagne que le rang précédent alors que le rang précédent est fictif et a été déjà décompté, on ne décompte pas le rang 1
                rang_is_cultures_intermediaires.loc[1] = False
            n_rangs_de_cultures_intermediaires = rang_is_cultures_intermediaires.sum()
            n_annees -= n_rangs_de_cultures_intermediaires
            ###############################################

            # (noeuds et aretes contiennent d'autres infos que les proportions de terrains associées, mais on les jette ici)
            ret_noeuds.append((noeuds['frequence_totale'] / n_annees) * surface_disponible_synthetise_assole)
            ret_aretes.append((aretes['frequence_totale'] / n_annees) * surface_disponible_synthetise_assole)
        else:
            pass # on ne fait rien, on pourrait ajouter des NaN avec les indices des noeuds et des aretes mais a voir si il faut ou pas

    connections_synthetise_surfaces = pd.DataFrame(pd.concat(ret_aretes)).rename(columns={'frequence_totale' :'surface (ha)'})
    # noeuds_synthetise_surfaces =  pd.concat(ret_noeuds)

    return connections_synthetise_surfaces



######################################################
################## FONCTIONS UTILES ##################
######################################################



def get_culture_id_FROM_culture_code_AND_campagne(df_culture, df_domaine):
    """
    Retourne un dictionnaire dico permettant d'accéder à un "culture_id" depuis un "culture_code" et une "campagne", 
    utilisable comme ceci:
    dico[culture_code][campagne] --> culture_id
    """
    culture_id_FROM_culture_code_AND_campagne = {} # dico[culture_code][campagne] = culture_id

    for culture in df_culture[['code', 'domaine_id']].itertuples():
        
        culture_code = culture.code
        campagne = df_domaine.loc[culture.domaine_id, 'campagne']
        
        if culture_code not in culture_id_FROM_culture_code_AND_campagne:
            # on ajoute le premier culture_id à la liste pour ce code
            culture_id_FROM_culture_code_AND_campagne[culture_code] = {campagne: culture.Index}
        else:
            # on vérifie qu'aucune culture n'était renseigné pour la même campagne
            if campagne in culture_id_FROM_culture_code_AND_campagne[culture_code]:
                raise ValueError('Doublon')
            # on ajoute la culture de la campagne à la liste pour ce code
            culture_id_FROM_culture_code_AND_campagne[culture_code][campagne] = culture.Index

    return culture_id_FROM_culture_code_AND_campagne

def to_regex(mot):
    """
    Rend sous forme d'expression régulière une forme du mot plus générique
    """
    regex_mot = '['+mot[0].upper()+mot[0].lower()+']'+mot[1:] + '|' + mot.upper()
    regex_mot = '(e|é|è)'.join(re.split('e|é|è', regex_mot))
    regex_mot = '(E|É|È)'.join(re.split('E|É|È', regex_mot))
    return regex_mot

def add_column_fictif(df_culture):
    """
    Ajoute une colonne "fictif" à la table df_culture
    """
    # expression reguliere captant les cultures "précédent fictif"
    regex_precedent_fictif = '('+to_regex('Précédent')+')|('+to_regex('fictif')+')' # on cherche soit "precedent" soit "fictif" (1520 cultures)
    # on ajoute une colonne à la table culture disant si oui ou non on est une culture fictive
    df_culture['fictif'] = df_culture['nom'].str.match(regex_precedent_fictif)
    return df_culture

def add_column_campagne(df_synthetise, df_sdc):
    """
    Ajoute une colonne "campagne_sdc" à la table df_synthetise
    """
    # on ajoute campagne_sdc à la table synthetise
    df_synthetise.loc[:, ['campagne_sdc']] = df_synthetise['sdc_id'].apply(lambda x: df_sdc.loc[x, 'campagne'])
    return df_synthetise

def add_column_sau(df_synthetise, df_sdc, df_dispositif, df_domaine):
    """
    Ajoute une colonne "sau_(Ha)" à la table df_synthetise
    """
    # on ajoute l'info de SAU au dispositif
    df_dispositif = df_dispositif.merge(right=df_domaine['sau_totale'], left_on='domaine_id', right_index=True, how='left')
    # on ajoute l'info de SAU au SdC
    df_sdc = df_sdc.merge(right=df_dispositif['sau_totale'], left_on='dispositif_id', right_index=True, how='left')
    # on modifie la colonne en multipliant par la part utilisées dans le SdC
    df_sdc['sau_(Ha)'] = df_sdc['sau_totale'] * df_sdc['part_sau_domaine'].fillna(100) / 100
    # on ajoute sau_(Ha) à la table synthetise
    df_synthetise = df_synthetise.merge(right=df_sdc['sau_(Ha)'], left_on='sdc_id', right_index=True, how='left')
    return df_synthetise

def add_columns_campagne_cultureID_fictif(df_noeuds_synthetise, df_culture, df_synthetise, df_domaine):
    """
    Ajoute les colonnes ("campagne_sdc", "culture_id", "fictif") à la table df_noeuds_synthetise
    """
    # on ajoute campagne_sdc à la table noeuds_synthetise
    df_noeuds_synthetise.loc[:, ['campagne_sdc']] = df_noeuds_synthetise['synthetise_id'].apply(lambda x: df_synthetise.loc[x, 'campagne_sdc'])
    # on ajoute culture_id à la table noeuds_synthetise
    # on load le dictionnaire (culture_code, campagne) --> culture_id
    culture_id_FROM_culture_code_AND_campagne = get_culture_id_FROM_culture_code_AND_campagne(df_culture=df_culture, df_domaine=df_domaine)
    df_noeuds_synthetise.loc[:, ['culture_id']] = df_noeuds_synthetise.apply(lambda x: culture_id_FROM_culture_code_AND_campagne[x['culture_code']].get(x['campagne_sdc'], np.NaN), axis=1)
    invalid_culture_nodes = df_noeuds_synthetise['culture_id'].isna()
    # on ajoute fictif à la table noeuds_synthetise
    df_noeuds_synthetise.loc[:, ['fictif']] = True
    df_noeuds_synthetise.loc[~invalid_culture_nodes, 'fictif'] = df_noeuds_synthetise.loc[~invalid_culture_nodes, 'culture_id'].apply(lambda x: df_culture.loc[x, 'fictif'])
    return df_noeuds_synthetise

def add_column_synthetise_id_to_connection(df_connection_synthetise, df_noeuds_synthetise):
    """
    Ajoute la colonne "synthetise_id" à la table df_connection_synthetise
    """
    # on ajoute une colonne synthetise_id à la table connection_synthetise
    return df_connection_synthetise.merge(right=df_noeuds_synthetise['synthetise_id'], left_on='cible_noeuds_synthetise_id', right_index=True, how='left')

def add_column_synthetise_id_to_intervention(df_intervention_synthetise, df_connection_synthetise):
    """
    Ajoute la colonne "synthetise_id" à la table df_intervention_synthetise
    """
    # on ajoute une colonne synthetise_id à la table intervention_synthetise
    return df_intervention_synthetise.merge(right=df_connection_synthetise['synthetise_id'], left_on='connection_synthetise_id', right_index=True, how='left')



######################################################
### FONCTIONS UTILES POUR LES GRAPHES SYNTHETISES ####
######################################################



def verif_is_coherent(noeuds, aretes):
    """
    Supprime les noeuds isolés,
    Invalide un graphe ayant des flux incohérents (sortie(s) ne sommant pas à 100), 
    Corrige quelques cas de sorties incohérentes
    """
    
    # flux à chaque noeud
    poids_sortants = aretes.groupby('source_noeuds_synthetise_id').apply(lambda x: pd.Series({'somme': np.sum(x['frequence_source']), 'number': len(x)}))
    poids_entrants = aretes.groupby('cible_noeuds_synthetise_id').apply(lambda x: pd.Series({'somme': np.sum(x['frequence_source']), 'number': len(x)})) # (lambda x: np.sum(x['frequence_source']))

    # noeuds isolés
    noeuds_sans_sortie = noeuds.loc[~noeuds.index.isin(poids_sortants.index)]
    noeuds_sans_entree = noeuds.loc[~noeuds.index.isin(poids_entrants.index)]
    noeuds_isoles = noeuds_sans_entree.loc[noeuds_sans_entree.index.isin(noeuds_sans_sortie.index)]

    # on supprime les noeuds isolés
    noeuds = noeuds.loc[~noeuds.index.isin(noeuds_isoles.index)]

    # determine si on conserve le flux (tolérence pour les arrondis)
    is_sortie_bad = abs(poids_sortants['somme']-100) > poids_sortants['number'] # nécessite des corrections de + que 1 point sur chaque arete pour sommer à 100
    
    # pour l'instant on ne corrige pas les poids des aretes acceptées qui ne somment pas exactement à 100 : ne semble pas nécessaire mais a voir
    
    # les noeuds ne conservant pas le flux
    noeuds_avec_sorties_incoherentes = noeuds.loc[poids_sortants.loc[is_sortie_bad].index]

    # si un noeud a des sorties mauvaises mais qu'on voit que c'est une seule sortie et qu'elle est égale à la seule entrée du noeud, alors on consifère que c'est une erreur de mécompréhension lors de la saisie et que la persoone voulait mettre 100 sur la sortie
    noeuds_a_modifier = noeuds_avec_sorties_incoherentes.loc[noeuds_avec_sorties_incoherentes.index.isin((poids_entrants.loc[poids_entrants['number']==1].index.intersection(poids_sortants.loc[poids_sortants['number']==1].index)))].index
    aretes.loc[aretes['source_noeuds_synthetise_id'].isin(noeuds_a_modifier), 'frequence_source'] = 100


    valid = len(noeuds_avec_sorties_incoherentes) == len(noeuds_a_modifier)

    return valid, noeuds, aretes


def filter_rotation_graph(synthetise_id, 
                          df_noeuds_synthetise_grouped, 
                          df_connection_synthetise_grouped, 
                          df_intervention_synthetise_grouped, 
                          delete_empty_arete=False):
    """
    Prend en argument un "synthetise_id"
    Et renvoie un dictionnaire :
        - disant si le graphe de rotation qu'il décrit est valide (non vide et cohérent)
        - contenant les noeuds, et les aretes du graphe si valide
    """

    # les noeuds de la rotation
    noeuds = df_noeuds_synthetise_grouped.get_group(synthetise_id) if synthetise_id in df_noeuds_synthetise_grouped.groups else pd.DataFrame()
    # les aretes de la rotation
    aretes = df_connection_synthetise_grouped.get_group(synthetise_id) if synthetise_id in df_connection_synthetise_grouped.groups else pd.DataFrame()

    if len(noeuds)<=1 or len(aretes)==0:
        return {'synthetise_id': synthetise_id, 'valid': False, 'noeuds': None, 'aretes': None, 'cause': 1}

    # on vérifie la cohérence des flux dans le graphe
    valid, noeuds, aretes = verif_is_coherent(noeuds, aretes)

    # ajout d'une colonne 'absent'
    aretes.loc[:, ['absent']] = aretes['culture_absente']=='t'
    
    # les interventions sur les aretes de la rotation
    interventions = df_intervention_synthetise_grouped.get_group(synthetise_id) if synthetise_id in df_intervention_synthetise_grouped.groups else pd.DataFrame(columns=['connection_synthetise_id'])

    # on marque 'absent' les aretes sans aucune intervention
    aretes.loc[~aretes.index.isin(interventions['connection_synthetise_id']), 'absent'] = True

    # on supprime les noeuds avec des codes de culture n'ayant pas de culture_id associé pour cette campagne...
    #on le met "fictif"
    noeuds.loc[noeuds['culture_id'].isna(), 'fictif'] = True
    # ON AGIT SUR DES COPIES ICI
    # on le supprime
    noeuds_copy = noeuds.loc[~noeuds['culture_id'].isna()].copy()

    # on supprime les aretes marquées absentes (et celles dont une extrémité est maintenant pendante) TODO : on risque de déconnecter des chemins liés à la source...
    aretes_copy = aretes.loc[(~aretes['absent']) & aretes['source_noeuds_synthetise_id'].isin(noeuds_copy.index) & aretes['cible_noeuds_synthetise_id'].isin(noeuds_copy.index)].copy()
    noeuds_copy = noeuds_copy.loc[noeuds_copy.index.isin(aretes_copy['source_noeuds_synthetise_id']) | noeuds_copy.index.isin(aretes_copy['cible_noeuds_synthetise_id'])]
        
    if delete_empty_arete:
        noeuds = noeuds_copy
        aretes = aretes_copy

    # on garde les noeuds (même les fictifs) si ils sont liés à une arete non-absente
    noeuds = noeuds.loc[noeuds.index.isin(aretes['source_noeuds_synthetise_id']) | noeuds.index.isin(aretes['cible_noeuds_synthetise_id'])]
    
    # on invalide les graphes de rotation dont tous les noeuds ou toutes les aretes sont absent(e)s
    if len(aretes_copy)==0 or len(noeuds_copy)==0:
        return {'synthetise_id': synthetise_id, 'valid': False, 'noeuds': None, 'aretes': None, 'cause': 3}

    return {'synthetise_id': synthetise_id, 
            'valid': valid, 
            'noeuds': noeuds, 
            'aretes': aretes}


def correct_rang0_freq_init(noeuds, aretes):
    """
    Vient vérifier/corriger les graphes vis a vis de leurs noeuds au rang 0 et la présence/cohérence de fréquences initiales pour ceux-ci
    """
    
    # les sources
    noeuds_0 = noeuds.loc[noeuds['rang']==0]
    
    # Certains rang0 n'ont pas de fq_init
    if (noeuds.loc[noeuds['rang']==0, 'fq_initial_noeud'].isna()).any():
        # Dans ces cas,
        source_de_fq_init = aretes.groupby('source_noeuds_synthetise_id').apply(lambda x: set(x['cible_noeuds_synthetise_id']) == set(noeuds_0.index))
        noeuds_alimentant_rang0 = source_de_fq_init.loc[source_de_fq_init].index
        # on dit que les fq_init sont définies par les aretes entrantes si existantes
        if len(noeuds_alimentant_rang0) == 1 and (aretes['cible_noeuds_synthetise_id'].value_counts().loc[noeuds_0.index] == 1).all():
            aretes_init = aretes.loc[aretes['source_noeuds_synthetise_id'] == noeuds_alimentant_rang0[0]]
            for arete in aretes_init.itertuples():
                noeuds.loc[arete.cible_noeuds_synthetise_id, 'fq_initial_noeud'] = arete.frequence_source
        # sinon on se distribue uniformément les 100%
        else:
            noeuds.loc[noeuds['rang']==0, 'fq_initial_noeud'] = 100 / len(noeuds_0)
    
    # Certains noeuds avec fq_init ne sont pas de rang 0. on ignore ces veleurs surement reliquats de déplacements depuis le rang 0 vers un autre rang mais les fleches existent forcément et font foi
    noeuds.loc[noeuds['rang']!=0, 'fq_initial_noeud'] = np.NaN
    
    # Maintenant normalement les noeuds de rang 0 sont exactement ceux avec des frequences initiales renseignées
    assert set(noeuds[noeuds['rang']==0].index) == set(noeuds[~noeuds['fq_initial_noeud'].isna()].index)

    # le graphe a bien au moins 1 élément de rang 0
    assert len(noeuds_0) > 0

    noeuds_fin = noeuds.loc[noeuds['fin_cycle']=='t']
    if len(aretes.loc[aretes['source_noeuds_synthetise_id'].isin(noeuds_fin.index) & ~aretes['cible_noeuds_synthetise_id'].isin(noeuds_0.index)]) > 0:
        # certains noeuds sont marqués finaux mais sont tout de même liés à d'autres cultures...
        pass
        # print("pbs_noeuds_finaux")
    # pour le moment on ignore le label "final" des noeuds et on ne considère pas non plus les aretes de retour comme interférant dans la fréquence totale des noeuds de départ

    return noeuds, aretes


def compute_importance(noeuds, aretes):
    """
    Calcule les poids de chaque noeud au sein de l'ensemble de noeuds, 
    et de chaque arete au sein de l'ensemble d'aretes.
    Méthode de propagation des "frequence_source" de proche en proche.
    Renvoie les noeuds et aretes augmetés d'une colonne "frequence_totale" contenant ces poids.
    """
    # on ajoute une colonne aux aretes : frequence_totale (= décrit la proportion de cette succession source->cible)
    aretes.loc[:, ['frequence_totale']] = float(0)
    # on ajoute une colonne aux aretes : frequence_totale_tmp (= décrit temporairement la proportion de cette succession source->cible)
    aretes.loc[:, ['frequence_totale_tmp']] = float(0)
    # on ajoute une colonne aux noeuds : frequence_totale (= décrit la proportion de cette culture afin de calculer la proportion des aretes partant de lui)
    noeuds.loc[:, ['frequence_totale']] = float(0)
    # on ajoute une colonne aux noeuds : frequence_totale_tmp (= décrit temporairement la proportion de cette culture (ce qu'elle vient de recevoir de prédécesseurs à un round de messages envoyés)
    noeuds.loc[:, ['frequence_totale_tmp']] = float(0)

    # on part des noeuds initiaux (= de rang 0)
    noeuds_cibles_id = noeuds.loc[noeuds['rang']==0].index
    # on leur attribut une frequence totale égale à leur frequence initiale
    noeuds.loc[noeuds_cibles_id, 'frequence_totale'] = noeuds.loc[noeuds_cibles_id, 'fq_initial_noeud']/100
    noeuds.loc[noeuds_cibles_id, 'frequence_totale_tmp'] = noeuds.loc[noeuds_cibles_id, 'frequence_totale']
    
    noeuds_DEPARTS = noeuds_cibles_id.copy()

    convergence = "ok"
    c = 0
    while len(noeuds_cibles_id) > 0:
        c += 1
        # aretes en partance
        aretes_tmp_id = aretes.loc[aretes['source_noeuds_synthetise_id'].isin(noeuds_cibles_id)].index
        if len(aretes_tmp_id)==0:
            break
        # on leur attribut une frequence totale en multipliant leur poids par le poids de leur noeud de départ TODO verifier si le calcul marche avec plusieurs noeuds initiaux
        aretes.loc[aretes_tmp_id, 'frequence_totale_tmp'] = aretes.loc[aretes_tmp_id].apply(lambda x: noeuds.loc[x['source_noeuds_synthetise_id'], 'frequence_totale_tmp'] * x['frequence_source']/100, axis=1)
        aretes.loc[aretes_tmp_id, 'frequence_totale'] += aretes.loc[aretes_tmp_id, 'frequence_totale_tmp']
        # noeuds de destiations
        # on leur attribue leur fréquence totale en sommant celles des chemins leur parvenant
        noeuds_cibles_fq_tot_tmp = aretes.loc[aretes_tmp_id].groupby('cible_noeuds_synthetise_id').apply(lambda x: sum(x['frequence_totale_tmp']))
        # on ne modifie pas les noeuds de DEPART
        noeuds_cibles_id = noeuds_cibles_fq_tot_tmp.loc[~noeuds_cibles_fq_tot_tmp.index.isin(noeuds_DEPARTS)].index
        # on ajoute à la valeur déjà présente pour prendre en compte les différences de timings entre les arrivées en un même noeud
        noeuds.loc[noeuds_cibles_id, 'frequence_totale_tmp'] = noeuds_cibles_fq_tot_tmp.loc[noeuds_cibles_id]
        noeuds.loc[noeuds_cibles_id, 'frequence_totale'] += noeuds.loc[noeuds_cibles_id, 'frequence_totale_tmp']
        if c>20:
            convergence = "strange loop in the graph"
            break
    # on supprime les colonnes temporaires aidant à calculer les messages dans le graphe
    aretes = aretes.drop(columns='frequence_totale_tmp')
    noeuds = noeuds.drop(columns='frequence_totale_tmp')
    
    return noeuds, aretes, convergence, c


def correct_rang0_and_compute_importances(noeuds, aretes):
    """
    Appelle les fonctions de mise en conformité du graphe sythetise décrit par noeuds et aretes,
    et de calcul des poids absolus de chaque noeud et arete.
    Renvoie les memes tables augmentées de la colonne "frequence_totale".
    """
    
    # on vient faire le dernier filtrage nécessaire pour le calcul des proprtions de surface associées à chaque noeud/arete
    noeuds, aretes = correct_rang0_freq_init(noeuds, aretes)

    # on attribue les fréquences totales aux noeuds et aretes
    noeuds, aretes, convergence, _ = compute_importance(noeuds=noeuds, aretes=aretes)
    
    assert convergence == "ok"

    # on peut vérifier si la somme des frequences totales de retour aux noeuds de départ est égale à la valeur attribuée en fréquence initiale
    # ca ne sera peutetre pas exactement le cas
    
    return noeuds, aretes

