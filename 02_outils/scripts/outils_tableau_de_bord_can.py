"""
	Regroupe les fonctions permettant de générer les outils utiles lors de la génération du magasin "Tableau_de_bord_can".
"""
import pandas as pd
import numpy as np


def get_percent_each_typo_culture(cgrp, freq_column='frequence', normalize=True):
    '''
    Permet de calculer le pourcentage de chaque typologie de culture dans un groupe de données.
    Ce groupe de données est généralement un groupe de données de rotation pour le synthétisé ou un sdc pour le réalisé.

    Args:
        cgrp (pd.DataFrame):
            DataFrame de données de la rotation pour le synthétisé ou du sdc pour le réalisé.
        freq_column (str):
            Nom de la colonne de fréquence à utiliser pour les calculs. Par défaut 'frequence' pour le synthétisé.
            Peut être 'surface_ponderee' ou 'surface' pour le réalisé.
        normalize (bool):
            Si True, retour en pourcentage
            Si False, retour en ha
    Returns:
        dict: Dictionnaire des pourcentages de chaque typologie de culture dans le groupe de données,
        trié par pourcentage décroissant. Clé = typologie, valeur = pourcentage (float).
        Si aucune fréquence renseignée, retourne {'erreur': 'aucune '+freq_column+' renseignée'}
        Si la somme des surfaces est nulle, retourne {'erreur': freq_column+' nulle renseignée'}
        Si la somme des surfaces est inférieure à 0.001, retourne {'erreur': freq_column+' totale < 0.001'}
    '''
    cgrp = cgrp.copy()
    cgrp['typocan_culture_sans_compagne_corrige'] = cgrp['typocan_culture_sans_compagne_corrige'].fillna('NoTypoC')

    if pd.isna(cgrp[freq_column]).all():
        return {'erreur': 'aucune ' + freq_column + ' renseignée'}

    if freq_column in {'surface_ponderee', 'surface'}:
        surf_sum = cgrp[freq_column].sum()
        if surf_sum == 0:
            return {'erreur': freq_column + ' nulle renseignée'}
        if surf_sum < 0.001:
            return {'erreur': freq_column + ' totale < 0.001'}

    percentages = {}
    for x in cgrp['typocan_culture_sans_compagne_corrige'].unique():
        typoc_sum = cgrp.loc[cgrp['typocan_culture_sans_compagne_corrige'] == x, freq_column].sum()
        if freq_column == 'frequence':
            typoc_sum = typoc_sum * 100
        elif freq_column in {'surface_ponderee', 'surface'}:
            if(normalize):
                typoc_sum = (typoc_sum / surf_sum) * 100
            else: 
                typoc_sum = typoc_sum
        percentages[x] = round(typoc_sum, 1)

    # Trier par pourcentage décroissant
    percentages = dict(
        sorted(percentages.items(), key=lambda item: item[1], reverse=True)
    )

    return percentages


def get_reseaux_rattachement_sdc_outils_tableau_de_bord_can(
    donnees
):
    """
    Permet d'obtenir les informations du réseau de rattachement d'un système de culture.

    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames nécessaires pour l'agrégation des informations :
            - 'reseau' : Données des réseaux associés aux dispositifs.
            - 'liaison_reseaux' : Liaison des réseaux et autres données associées.
            - 'liaison_sdc_reseau' : Affectation des systèmes de cultures à un ou plusieurs réseaux.
            - 'sdc' : Données des systèmes de cutlures.
            
    Returns:
        pd.DataFrame:
            Un DataFrame contenant les informations agrégées sur les sdc avec les colonnes suivantes :
            - `id` : Identifiant du sdc.
            - `reseaux_ir` : Concaténation des réseaux associés au domaine (séparés par un pipe `|`).
            - `reseaux_it` : Concaténation des réseaux parents associés au domaine (séparés par une pipe `|`).

    Exemple d'utilisation :
        donnees = {
            'reseau': pd.DataFrame(...),
            'liaison_reseaux': pd.DataFrame(...),
            'liaison_sdc_reseau': pd.DataFrame(...),
            'sdc': pd.DataFrame(...),
        }
        result = get_reseaux_rattachement_sdc(donnees)
    """
    df = donnees.copy()
    df['reseau'] = donnees['reseau'].set_index('id')
    df['liaison_reseaux'] = donnees['liaison_reseaux']
    df['liaison_sdc_reseau'] = donnees['liaison_sdc_reseau']
    df['sdc'] = donnees['sdc'].set_index('id')

    # pour chaque liaison de réseau, on obtient l'information complète
    left = df['liaison_sdc_reseau']
    right = df['sdc'][['dispositif_id']]
    df['liaison_sdc_reseau_extanded'] = pd.merge(left, right, left_on='sdc_id', right_index=True, how='left')

    # pour chaque laison, on ajoute les informations sur le réseau
    left = df['liaison_sdc_reseau_extanded'] 
    right = df['reseau'][['nom', 'code_convention_dephy']]
    df['liaison_sdc_reseau_extanded']  = pd.merge(left, right, left_on='reseau_id', right_index=True, how='left')

    # on obtient aussi le lien vers le parent du réseau
    left = df['liaison_sdc_reseau_extanded']
    right = df['liaison_reseaux']
    df['liaison_sdc_reseau_extanded']  = pd.merge(left, right, on='reseau_id', how='left')

    # on ajoute les informations sur le réseau parent
    left = df['liaison_sdc_reseau_extanded'] 
    right = df['reseau'].rename(columns={
            'nom' : 'nom_reseau_parent', 
            'code_convention_dephy' : 'code_convention_dephy_reseau_parent'
            }
    )
    df['liaison_sdc_reseau_extanded']  = pd.merge(left, right, left_on='reseau_parent_id', right_index=True).dropna(subset=['nom', 'nom_reseau_parent']).fillna('')

    res = df['liaison_sdc_reseau_extanded'] .groupby('sdc_id').agg({
        'nom' : lambda x: '|'.join(x.unique()),
        'nom_reseau_parent' : lambda x: '|'.join(x.unique()),
        'code_convention_dephy' : lambda x: '|'.join(x.unique())
    }).rename(columns={
        'nom' : 'reseaux_ir',
        'nom_reseau_parent' : 'reseaux_it',
        'code_convention_dephy' : 'codes_convention_dephy'
    })
    return res.reset_index().rename(columns={'sdc_id' : 'id'})


def get_surface_sdc_realise_outils_tableau_de_bord_can(
    donnees
):
    """
    Permet d'obtenir la SAU des sdc en réalisé en sommant les surfaces des parcelles contenues dans le sdc
    Args:
        donnees (dict):
            Un dictionnaire contenant les DataFrames nécessaires pour l'agrégation des informations :
            - 'parcelle' : Données des parcelles
            
    Returns:
        pd.DataFrame:
            Un DataFrame contenant les informations agrégées sur les sdc avec les colonnes suivantes :
            - `id` : Identifiant du sdc.
            - `surface_sdc` : Surface du système de culture 

    Exemple d'utilisation :
        donnees = {
            'parcelle': pd.DataFrame(...),
        }
        result = get_surface_sdc_realise_outils_tableau_de_bord_can(donnees)
    """
    df = donnees.copy()
    df['parcelle'] = df['parcelle'].set_index('id')

    # pour chaque parcelle
    res = df['parcelle'].groupby('sdc_id').agg({'surface' : 'sum'}).rename(columns={'surface' : 'surface_sdc'})

    return res.reset_index().rename(columns={'sdc_id' : 'id'})


def get_surface_typo_culture_sdc_realise_outils_tableau_de_bord_can(donnees):
    """
        Retourne pour chaque système de culture en realise, la surface par typologie de culture (une colonne par typologie de culture)

        > Attention, toutes les culture déclarées "porte-graines" ne doivent pas être décomptées dans les autres typologies de culture. 
    
        Tables nécessaires :
        - noeuds_realise
        - itk_realise_agrege
        - zone
        - typologie_can_culture
    
    """
    df = donnees.copy()
    left = df['noeuds_realise']
    right = df['itk_realise_agrege'][['itk_id',  'sdc_id']]
    df['noeuds_realise_extanded'] = pd.merge(left, right, left_on='id', right_on='itk_id', how='left').set_index('id')

    # ajout du poids du noeud, c'est à dire la surface en réalisé
    left = df['noeuds_realise_extanded']
    right = df['zone'].set_index('id')[['surface']]
    df['noeuds_realise_extanded'] = pd.merge(left, right, left_on='zone_id', right_index=True, how='left')

    # On créé une nouvelle colonne "typocan_culture_corrige" qui réaffecte les culture porte graine à une typologie dédiée (volonté Cellule Ref)
    df['typologie_can_culture']['typocan_culture_sans_compagne_corrige'] = df['typologie_can_culture']['typocan_culture']
    df['typologie_can_culture'].loc[
        df['typologie_can_culture']['typo_cpg'].isin(
            ['Cultures porte graines', 'Cultures porte graines et autres destinations']
        ), 'typocan_culture_sans_compagne_corrige'
    ] = 'Porte graine'

    left = df['noeuds_realise_extanded']
    right = df['typologie_can_culture'].set_index('culture_id')[['typocan_culture_sans_compagne_corrige']]
    df['noeuds_realise_extanded'] = pd.merge(left, right, left_on='culture_id', right_index=True, how='left')

    result = df['noeuds_realise_extanded'].groupby('sdc_id').apply(
        lambda g: get_percent_each_typo_culture(g, freq_column='surface', normalize=False)
    )

    result_df = result.apply(pd.Series).fillna(0).rename(columns={
        'Betterave' : 'surface_betterave', 
        'Céréales à paille printemps' : 'surface_cereale_a_paille_printemps',
        'Céréales à paille hiver' : 'surface_cereale_a_paille_hiver',
        'Colza' : 'surface_colza',
        'Légume' : 'surface_legume', # Attention, légume plein champs
        'Lin' : 'surface_lin', # Attention, Lin fibre
        'Maïs' : 'surface_mais', # ATtention, Maïs Sorgho
        'Mélange fourrager' : 'surface_melange_fourrager',
        'Oléagineux (hors Colza et Tournesol)' : 'surface_oleagineux', # Attention, Olea
        'Pomme de terre' : 'surface_pomme_de_terre', 
        'Porte graine': 'surface_porte_graine', 
        'Prairie temporaire' : 'surface_prairie_temporaire',
        'Protéagineux' : 'surface_proteagineux',
        'Tournesol' : 'surface_tournesol',
        'Autre' : 'surface_autre',
        'Pommier' : 'surface_pommier', 
        'Vigne' : 'surface_vigne', 
        'Plante aromatique ou médicinale' : 'surface_plante_aromatique_ou_medicinale', 
        'Fraisier' : 'surface_fraisier', 
        'NoInput-sp' : 'surface_NoInput-sp', 
        'Prunier' : 'surface_prunier',
        'Culture ornementale' : 'surface_culture_ornementale',
        'NoTypoC' : 'surface_NoTypoC',
        'erreur' : 'surface_erreur;', 
        'Pêcher' : 'surface_pecher', 
        'Litchi': 'surface_litchi', 
        'Ananas' : 'surface_ananas',
        'Bananier' : 'surface_bananier', 
        'Attier' : 'surface_attier', 
        'Fruit de la passion' : 'surface_fruit_de_la_passion', 
        'Cerisier' : 'surface_cerisier', 
        'Poirier' : 'surface_poirier',
        'Papayer' : 'surface_papayer', 
        'Cacaoyer' : 'surface_cacaoyer', 
        'Framboisier' : 'surface_framboisier', 
        'Petits fruits' : 'surface_petits_fruits',
        'Arbre à pain' : 'surface_arbre_a_pain',
        'Figuier' : 'surface_figuier',
        'Sapin' : 'surface_sapin', 
        'Canne à sucre' : 'surface_canne_a_sucre',
        'Groseiller' : 'surface_groseiller', 
        'Grenadille' : 'surface_grenadille',
        'Manguier' : 'surface_manguier', 
        'Noyer' : 'surface_noyer', 
        'Cassissier' : 'surface_casssissier',
        'Citronnier' : 'surface_citronnier'
    })

    return result_df.reset_index().rename(columns={'sdc_id' : 'id'})