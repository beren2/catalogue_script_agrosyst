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
        > Attention, en base de données,on est obligé de nommer la table "entrepot_stc_sdc_realise_outils_tableau_de_bord_can", sinon trop de caractères.
        
        Tables nécessaires :
        - noeuds_realise
        - itk_realise_agrege
        - zone
        - typologie_can_culture
    
    """
    df = donnees.copy()

    #--------------#
    #    COMMUN    #
    #--------------#
    # On créé une nouvelle colonne "typocan_culture_corrige" qui réaffecte les culture porte graine à une typologie dédiée (volonté Cellule Ref)
    df['typologie_can_culture']['typocan_culture_sans_compagne_corrige'] = df['typologie_can_culture']['typocan_culture']
    df['typologie_can_culture'].loc[
        df['typologie_can_culture']['typo_cpg'].isin(
            ['Cultures porte graines', 'Cultures porte graines et autres destinations']
        ), 'typocan_culture_sans_compagne_corrige'
    ] = 'Porte graine'


    #--------------#
    #    ASSOLE    #
    #--------------#
    left = df['noeuds_realise']
    right = df['itk_realise_agrege'][['itk_id',  'sdc_id']]
    df['noeuds_realise_extanded'] = pd.merge(left, right, left_on='id', right_on='itk_id', how='left').set_index('id')

    # ajout du poids du noeud, c'est à dire la surface en réalisé
    left = df['noeuds_realise_extanded']
    right = df['zone'].set_index('id')[['surface']]
    df['noeuds_realise_extanded'] = pd.merge(left, right, left_on='zone_id', right_index=True, how='left')
    
    left = df['noeuds_realise_extanded']
    right = df['typologie_can_culture'].set_index('culture_id')[['typocan_culture_sans_compagne_corrige']]
    df['noeuds_realise_extanded'] = pd.merge(left, right, left_on='culture_id', right_index=True, how='left')

    result_assole = df['noeuds_realise_extanded'].groupby('sdc_id').apply(
        lambda g: get_percent_each_typo_culture(g, freq_column='surface', normalize=False)
    )

    #--------------#
    #   PERENNE    #
    #--------------#
    left = df['plantation_perenne_phases_realise'].set_index('id')
    right = df['plantation_perenne_realise'].set_index('id')[['culture_id', 'zone_id']]
    df['plantation_perenne_phases_realise_extanded'] = pd.merge(left, right, left_on='plantation_perenne_realise_id', right_index=True, how='left')

    left = df['plantation_perenne_phases_realise_extanded']
    right = df['typologie_can_culture'].set_index('culture_id')[['typocan_culture_sans_compagne_corrige']]
    df['plantation_perenne_phases_realise_extanded'] = pd.merge(left, right, left_on='culture_id', right_index=True, how='left')

    # ajout des identifiants des échelles supérieures
    left = df['plantation_perenne_phases_realise_extanded']
    right = df['itk_realise_agrege'].set_index('itk_id')[['sdc_id']]
    df['plantation_perenne_phases_realise_extanded'] = pd.merge(left, right, left_index=True, right_index=True, how='inner')  
    

    # ajout des identifiants des échelles supérieures
    left = df['plantation_perenne_phases_realise_extanded']
    right = df['zone'].set_index('id')[['surface']].rename(columns={'surface' : 'surface_zone'})
    df['plantation_perenne_phases_realise_extanded'] = pd.merge(left, right, left_on='zone_id', right_index=True, how='inner')  

    # en réalisé, on suppose l'équi-répartition entre les différentes soles au sein d'une même zone.
    left = df['plantation_perenne_phases_realise_extanded']
    right = df['plantation_perenne_phases_realise_extanded'].reset_index().groupby('zone_id').agg({'index' : 'count'}).rename(columns={'index' : 'nb_soles_dans_zone'})
    df['plantation_perenne_phases_realise_extanded'] = pd.merge(left, right, left_on='zone_id', right_index=True, how='left')  

    # recalcul de la surface de la phase en prenant en compte la sau totale, la part de sau du domaine et le pct d'occupation du sol
    df['plantation_perenne_phases_realise_extanded'].loc[
        :, 'plantation_perenne_phases_realise_surface'
    ] = np.round(df['plantation_perenne_phases_realise_extanded']['surface_zone'] / \
        df['plantation_perenne_phases_realise_extanded']['nb_soles_dans_zone']
    )

    result_perenne = df['plantation_perenne_phases_realise_extanded'].groupby('sdc_id').apply(
        lambda g: get_percent_each_typo_culture(g, freq_column='plantation_perenne_phases_realise_surface', normalize=False)
    )

    # pour l'instant, on exclu de l'analyse les systèmes qui présentent à la fois un pérenne et un assolé.
    result_assole = result_assole.loc[
        ~result_assole.index.isin(result_perenne.index)
    ]

    df['result_realise'] = pd.concat([result_assole, result_perenne])

    result_df = df['result_realise'].apply(pd.Series).fillna(0).rename(columns={
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
        'Citronnier' : 'surface_citronnier',
        'Châtaignier' : 'surface_chataigner'
    })

    return result_df.reset_index().rename(columns={'sdc_id' : 'id'})




def get_surface_typo_culture_synthetise_outils_tableau_de_bord_can(donnees):
    """
        Retourne pour chaque système synthétisé, la surface par typologie de culture (une colonne par typologie de culture)
        La fonction retourne un dataframe avec en index le synthetise_id et une colonne par typologie de culture (exemple : surface_abricotier).
        
        Les cultures assolées ET perennes sont bien prises en comptes. 

        > Attention, toutes les culture déclarées "porte-graines" ne doivent pas être décomptées dans les autres typologies de culture. 
        > Attention, en base de données,on est obligé de nommer la table "entrepot_stc_synth_outils_tableau_de_bord_can", 
        sinon trop de caractères.
        > Attention, il y a, au 08/07/2026, 36 synthétisé au moins avec des cultures pérennes et des cultures assolées. Pour l'instant, 
        on les exclus de l'analyse.
        
        Tables nécessaires :
        - noeuds_synthetise
        - connection_synthetise
        - noeuds_synthetise_restructure
        - itk_synthetise_agrege
        - typologie_can_culture
        - poids_connexions_synthetise_rotation
        - sdc
        - domaine 
        - plantation_perenne_phases_synthetise
        - plantation_perenne_synthetise
        - plantation_perenne_synthetise_restructure
    
    """
    #--------------#
    #    COMMUN    #
    #--------------#

    df = donnees.copy()

    # On créé une nouvelle colonne "typocan_culture_corrige" qui réaffecte les culture porte graine à une typologie dédiée (volonté Cellule Ref)
    df['typologie_can_culture']['typocan_culture_sans_compagne_corrige'] = df['typologie_can_culture']['typocan_culture']
    df['typologie_can_culture'].loc[
        df['typologie_can_culture']['typo_cpg'].isin(
            ['Cultures porte graines', 'Cultures porte graines et autres destinations']
        ), 'typocan_culture_sans_compagne_corrige'
    ] = 'Porte graine'

    #--------------#
    #    ASSOLE    #
    #--------------#

    left = df['connection_synthetise']
    right = df['itk_synthetise_agrege'][['itk_id',  'synthetise_id']]
    df['connection_synthetise_extanded'] = pd.merge(left, right, left_on='id', right_on='itk_id', how='left').set_index('id')

    # ajout du poids de connexion, c'est à dire la colonne poids_conx_agregation en synthétisé
    left = df['connection_synthetise_extanded']
    right = df['poids_connexions_synthetise_rotation'].set_index('connexion_id')[['poids_conx_agregation']]
    df['connection_synthetise_extanded'] = pd.merge(left, right, left_index=True, right_index=True, how='left')

    left = df['connection_synthetise_extanded']
    right = df['noeuds_synthetise_restructure'].set_index('id')
    df['connection_synthetise_extanded'] = pd.merge(left, right, left_on='cible_noeuds_synthetise_id', right_index=True, how='left')

    left = df['connection_synthetise_extanded']
    right = df['noeuds_synthetise_restructure'].set_index('id').rename(columns={'culture_id': 'source_culture_id'})
    df['connection_synthetise_extanded'] = pd.merge(left, right, left_on='source_noeuds_synthetise_id', right_index=True, how='left')

    left = df['connection_synthetise_extanded']
    right = df['typologie_can_culture'].set_index('culture_id')[['typocan_culture_sans_compagne_corrige']]
    df['connection_synthetise_extanded'] = pd.merge(left, right, left_on='culture_id', right_index=True, how='left')

    # ajout du nom du noeud préc pour debug
    left = df['connection_synthetise_extanded']
    right = df['typologie_can_culture'].set_index('culture_id')[['typocan_culture_sans_compagne_corrige']].rename(columns={'typocan_culture_sans_compagne_corrige' : 'typocan_prec'})
    df['connection_synthetise_extanded'] = pd.merge(left, right, left_on='source_culture_id', right_index=True, how='left')

    # on considère que toutes les cultures absentes ont un poids de 0.
    df['connection_synthetise_extanded'].loc[:, 'poids_conx_agregation'] = df['connection_synthetise_extanded']['poids_conx_agregation'].fillna(0)

    #--------------#
    #   PERENNE    #
    #--------------#

    left = df['plantation_perenne_phases_synthetise'].set_index('id')
    right = df['plantation_perenne_synthetise'].set_index('id')[['synthetise_id', 'pct_occupation_sol']]
    df['plantation_perenne_phases_synthetise_extanded'] = pd.merge(left, right, left_on='plantation_perenne_synthetise_id', right_index=True, how='left')

    left = df['plantation_perenne_phases_synthetise_extanded']
    right = df['plantation_perenne_synthetise_restructure'].set_index('id')[['culture_id']]
    df['plantation_perenne_phases_synthetise_extanded'] = pd.merge(left, right, left_on='plantation_perenne_synthetise_id', right_index=True, how='left')

    left = df['plantation_perenne_phases_synthetise_extanded']
    right = df['typologie_can_culture'].set_index('culture_id')[['typocan_culture_sans_compagne_corrige']]
    df['plantation_perenne_phases_synthetise_extanded'] = pd.merge(left, right, left_on='culture_id', right_index=True, how='left')

    # ajout des identifiants des échelles supérieures
    left = df['plantation_perenne_phases_synthetise_extanded']
    right = df['itk_synthetise_agrege'].set_index('itk_id')[['sdc_id', 'domaine_id']]
    df['plantation_perenne_phases_synthetise_extanded'] = pd.merge(left, right, left_index=True, right_index=True, how='inner')  

    # ajout des informations nécessaires au calcul des surfaces pondérées
    left = df['plantation_perenne_phases_synthetise_extanded']
    right = df['sdc'].set_index('id')['part_sau_domaine']
    df['plantation_perenne_phases_synthetise_extanded'] = pd.merge(left, right, left_on='sdc_id', right_index=True, how='left')

    left = df['plantation_perenne_phases_synthetise_extanded']
    right = df['domaine'].set_index('id')['sau_totale']
    df['plantation_perenne_phases_synthetise_extanded'] = pd.merge(left, right, left_on='domaine_id', right_index=True, how='left')

    # pour les parts de sau non complétées, on met 100
    df['plantation_perenne_phases_synthetise_extanded'].loc[
        df['plantation_perenne_phases_synthetise_extanded']['part_sau_domaine'].isna(), 'part_sau_domaine'
    ] = 100

    # recalcul de la surface de la phase en prenant en compte la sau totale, la part de sau du domaine et le pct d'occupation du sol
    df['plantation_perenne_phases_synthetise_extanded'].loc[
        :, 'plantation_perenne_phases_synthetise_surface'
    ] = np.round(df['plantation_perenne_phases_synthetise_extanded']['sau_totale'] * \
        df['plantation_perenne_phases_synthetise_extanded']['part_sau_domaine'] / 100 * \
        df['plantation_perenne_phases_synthetise_extanded']['pct_occupation_sol'] / 100, 3)

    #--------------#
    #    COMMUN    #
    #--------------#

    result_assole = df['connection_synthetise_extanded'].groupby('synthetise_id').apply(
        lambda g: get_percent_each_typo_culture(g, freq_column='poids_conx_agregation', normalize=False)
    )
    result_perenne = df['plantation_perenne_phases_synthetise_extanded'].groupby('synthetise_id').apply(
        lambda g: get_percent_each_typo_culture(g, freq_column='plantation_perenne_phases_synthetise_surface', normalize=False)
    )

    # on a que 36 synthétisés qui contiennent à la fois des cultures pérennes et des cultures annuelles
    # pour l'instant, on les exclus de l'analyse.
    result_assole = result_assole.loc[
        ~result_assole.index.isin(result_perenne.index)
    ]


    df['result_synthetise'] = pd.concat([result_assole, result_perenne])

    result= df['result_synthetise'].apply(pd.Series).fillna(0).rename(columns={
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
        'Arbres fruitiers' : 'surface_arbres_fruitiers',
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
        'Citronnier' : 'surface_citronnier',
        'Myrtille et airelles' : 'surface_myrtille_et_airelles',
        'Amandier' : 'surface_amandier',
        'Sorossi' : 'surface_sorossi',
        'Olivier' : 'surface_olivier',
        'Clémentinier' : 'surface_clementiner',
        'Abricotier' : 'surface_abricotier',
        'Kiwi' : 'surface_kiwi'
    })
    return result.reset_index().rename(columns={'synthetise_id' : 'id'})