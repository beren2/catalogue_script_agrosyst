"""
	Regroupe les fonctions permettant de générer le magasin DEPHYGraph.
"""
import pandas as pd
import numpy as np
from datetime import datetime
from ydata_profiling import ProfileReport

GCPE = ['GRANDES_CULTURES','POLYCULTURE_ELEVAGE']

PERFORMANCES_COLS = [
    'approche_de_calcul',
    'ift_cible_non_mil_tx_comp',
    # IFT
    'ift_cible_non_mil_chimique_tot',
    'ift_cible_non_mil_chim_tot_hts',
    'ift_cible_non_mil_h',
    'ift_cible_non_mil_f',
    'ift_cible_non_mil_i',
    'ift_cible_non_mil_ts',
    'ift_cible_non_mil_a',
    'ift_cible_non_mil_hh',
    'ift_cible_non_mil_biocontrole',
    'recours_aux_moyens_biologiques',
    # Temps
    'tps_utilisation_materiel',
    'tps_travail_manuel',
    'tps_travail_total',
    # UTH
    'surface_par_unite_de_travail_humain', # noneed
    'nombre_uth_necessaires', # noneed
    # Travail du sol
    'nbre_de_passages_desherbage_meca',
    'utili_desherbage_meca',
    'type_de_travail_du_sol',
    # Charges
    'co_tot_std_mil',
    'cm_std_mil',
    'c_main_oeuvre_tot_std_mil',
    'c_main_oeuvre_tractoriste_std_mil', # noneed
    'c_main_oeuvre_manuelle_std_mil', # noneed
    # Consommation
    'conso_carburant',
    # Economique
    'pb_std_mil_avec_autoconso',
    'mb_std_mil_avec_autoconso',
    'msn_reelle_avec_autoconso',
    'md_std_mil_avec_autoconso', # noneed
    # Fertilistation
    'ferti_n_tot',
    'ferti_n_mineral',
    'ferti_n_organique',
    'ferti_p2o5_tot',
    'ferti_p2o5_mineral',
    'ferti_p2o5_organique',
    'ferti_k2o_tot',
    'ferti_k2o_mineral',
    'ferti_k2o_organique',
    # HRI1
    'hri1_hts',
    'hri1_g1_hts',
    'hri1_g2_hts',
    'hri1_g3_hts',
    'hri1_g4_hts',
    # QSA
    'qsa_tot_hts',
    'qsa_danger_environnement_hts',
    'qsa_toxique_utilisateur_hts',
    'qsa_cmr_hts',
    'qsa_glyphosate_hts',
    'qsa_cuivre_tot_hts',
    'qsa_soufre_tot_hts'
    ]

DICT_VAR_IMPACTED = {
    'nbre_de_passages_desherbage_meca': 
				[None],
	'tps_travail_total': 
				[None],
	'tps_utilisation_materiel': 
				['tps_travail_total'],
	'tps_travail_manuel': 
				['tps_travail_total'],
	'conso_carburant': 
				[None],
                

	'ferti_n_tot': 
				[None],
	'ferti_n_mineral': 
				['ferti_n_tot'],
	'ferti_n_organique': 
				['ferti_n_tot'],
	'ferti_p2o5_tot': 
				[None],
	'ferti_p2o5_mineral': 
				['ferti_p2o5_tot'],
	'ferti_p2o5_organique': 
				['ferti_p2o5_tot'],
	'ferti_k2o_tot': 
				[None],
	'ferti_k2o_mineral': 
				['ferti_k2o_tot'],
	'ferti_k2o_organique': 
				['ferti_k2o_tot'],
                

	'pb_std_mil_avec_autoconso': 
				['mb_std_mil_avec_autoconso', 'msn_reelle_avec_autoconso', 'md_std_mil_avec_autoconso'],
	'mb_std_mil_avec_autoconso': 
				['msn_reelle_avec_autoconso', 'c504_outLabourTotalExpenses', 'md_std_mil_avec_autoconso'],
	'msn_reelle_avec_autoconso': 
    			[None],
	'c504_outLabourTotalExpenses': 
				['msn_reelle_avec_autoconso','md_std_mil_avec_autoconso'],
	'co_tot_std_mil': 
				['mb_std_mil_avec_autoconso', 'msn_reelle_avec_autoconso', 'c504_outLabourTotalExpenses','md_std_mil_avec_autoconso'],
	'c_main_oeuvre_tot_std_mil': 
				['md_std_mil_avec_autoconso'],
	'cm_std_mil': 
				['msn_reelle_avec_autoconso', 'c504_outLabourTotalExpenses','md_std_mil_avec_autoconso'],
    'md_std_mil_avec_autoconso':
				[None], # si les indicateur éco sont mauvais, on passe la marge directe en NA. L'inverse, on verra plus tard, quand la marge directe sera validée par la CAN                


	'ift_cible_non_mil_chim_tot_hts': 
				['hri1_hts','hri1_g1_hts','hri1_g2_hts','hri1_g3_hts','hri1_g4_hts',
     			'qsa_tot_hts'],
	'c602_IFT_hh_hts': 
				['hri1_hts','hri1_g1_hts','hri1_g2_hts','hri1_g3_hts','hri1_g4_hts',
     			'ift_cible_non_mil_chim_tot_hts', 'qsa_tot_hts'],
	'ift_cible_non_mil_biocontrole': 
				['hri1_hts','hri1_g1_hts','hri1_g2_hts','hri1_g3_hts','hri1_g4_hts',
     			'qsa_tot_hts'],
	'ift_cible_non_mil_h': 
				['hri1_hts','hri1_g1_hts','hri1_g2_hts','hri1_g3_hts','hri1_g4_hts',
     			'ift_cible_non_mil_chim_tot_hts', 'qsa_tot_hts'],
	'ift_cible_non_mil_i': 
				['hri1_hts','hri1_g1_hts','hri1_g2_hts','hri1_g3_hts','hri1_g4_hts',
     			'ift_cible_non_mil_chim_tot_hts', 'c602_IFT_hh_hts', 'qsa_tot_hts'],
	'ift_cible_non_mil_f': 
				['hri1_hts','hri1_g1_hts','hri1_g2_hts','hri1_g3_hts','hri1_g4_hts',
     			'ift_cible_non_mil_chim_tot_hts', 'c602_IFT_hh_hts', 'qsa_tot_hts'],
	'ift_cible_non_mil_a': 
				['hri1_hts','hri1_g1_hts','hri1_g2_hts','hri1_g3_hts','hri1_g4_hts',
     			'ift_cible_non_mil_chim_tot_hts', 'c602_IFT_hh_hts', 'qsa_tot_hts'],
	'recours_aux_moyens_biologiques': 
				[None],
                

	'hri1_hts': 
				['hri1_g1_hts','hri1_g2_hts','hri1_g3_hts','hri1_g4_hts'],
	'hri1_g1_hts': 
				['hri1_hts','hri1_g2_hts','hri1_g3_hts','hri1_g4_hts'],
	'hri1_g2_hts': 
				['hri1_g1_hts','hri1_hts','hri1_g3_hts','hri1_g4_hts'],
	'hri1_g3_hts': 
				['hri1_g1_hts','hri1_g2_hts','hri1_hts','hri1_g4_hts'],
	'hri1_g4_hts': 
				['hri1_g1_hts','hri1_g2_hts','hri1_g3_hts','hri1_hts'],
    

	'qsa_tot_hts': 
				[None],
                # ['hri1_hts', 'ift_cible_non_mil_chim_tot_hts'],
	'qsa_cmr_hts': 
				['qsa_tot_hts'],
	'qsa_toxique_utilisateur_hts': 
				['qsa_tot_hts'],
	'qsa_glyphosate_hts': 
				['qsa_tot_hts'],
	'qsa_danger_environnement_hts': 
				['qsa_tot_hts'],
	'qsa_cuivre_tot_hts': 
				['qsa_tot_hts'],
	'qsa_soufre_tot_hts': 
				['qsa_tot_hts']
}

ALERTES_COLS_VAR = {
    'alerte_ferti_n_tot' : "ferti_n_tot",
    'alerte_ift_cible_non_mil_chim_tot_hts' : "ift_cible_non_mil_chim_tot_hts",
    'alerte_ift_cible_non_mil_f': "ift_cible_non_mil_f",
    'alerte_ift_cible_non_mil_h' : "ift_cible_non_mil_h",
    'alerte_ift_cible_non_mil_i' : "ift_cible_non_mil_i",
    'alerte_ift_cible_non_mil_biocontrole' : "ift_cible_non_mil_biocontrole",
    'alerte_co_irrigation_std_mil' : "co_irrigation_std_mil",
    'alerte_msn_std_mil_avec_autoconso' : "msn_std_mil_avec_autoconso",
    # 'alerte_nombre_interventions_phyto' : ["???"],
    'alerte_pb_std_mil_avec_autoconso' : "pb_std_mil_avec_autoconso",
    # 'alerte_rendement' : ['pb_std_mil_avec_autoconso','mb_std_mil_avec_autoconso', 'msn_reelle_avec_autoconso', 'md_std_mil_avec_autoconso'],
    'alertes_charges' : ["co_tot_std_mil","cm_std_mil"],
    'alerte_cm_std_mil' : "cm_std_mil",
    'alerte_co_semis_std_mil' : "co_semis_std_mil"
}

def list_to_scalar(serie):
    """ 
    Transforme une série pandas contenant des listes en une série où les listes sont remplacées par une valeur scalaire si la liste ne contient qu'une seule valeur distincte; ou par None si la liste est vide; ou par une liste de valeurs uniques. 
    """
    unique_values = list(serie.dropna().unique())
    if len(unique_values) == 0:
        return None
    elif len(unique_values) == 1:
        return unique_values[0]
    else:
        return unique_values

def nettoyage_numero_dephy(data, colonne='code_dephy') :
    """ 
    Permet de nettoyer les numéros DEPHY présents dans la colonne spécifiée du DataFrame.
    On fait un premier nettoyage en ne gardant que les caractères alphanumériques et en supprimant les mentions "PPZ". Ensuite, on extrait le pattern AAAANNNN ou AAAAXNNN s'il est présent dans la chaîne. Les valeurs non conformes sont remplacées par None.
    """
    df = data.copy()
    mask = data[colonne].notna()

    ## On fait un premier nettoyage grossier des numéros DEPHY
    df[colonne] = (
        df[colonne]
        .astype(str)
        .str.upper()
        .str.replace(r'PPZ|[^A-Z0-9]', '', regex=True)
        .where(mask, None)
    )
        
    # Les chaines vides sont remplacés par None
    df[colonne] = np.where(df[colonne]=='', None, df[colonne])

    # On extrait des codes DEPHY le pattern AAAANNNN ou AAAAXNNN s'il est présent
    pattern = r'([A-Z]{3}(?:[0-9]|X)\d{4}(?!\d))'
    df[colonne] = df[colonne].str.extract(pattern, expand=False)

    return df[colonne]

def filtre_1_dispoFermeDetaille_typeAgriNotNull(df):
    """ 
    Filtre les DEPHY FERME DETAILLE et ne gardant que les données avec un type d'agriculture renseigné (AB, Conv, en conversion) 
    """
    a=len(df)

    # On filtre pour ne garder que les DEPHY FERME en détaillés
    df = df.loc[(df['modalite_suivi_dephy']=='DETAILLE') & (df['type']=='DEPHY_FERME')]

    # On enleve toute les données n'ayant pas de type d'agriculture (AB, Conv, en conversion)
    df = df.loc[(df['type_agriculture'].notna()) & (df['type_agriculture'] != 'Information obligatoire')]

    b=len(df)
    print(f"Filtre 1 : -{a-b} lignes")
    return df

def filtre_2_annees(df, annees_trop_vieille=2004, mois_date_butoire_dephy_fin_saisie=4):
    """ 
    Filtre les données en fonction des années de campagne
    On ne gardant que les camapgnes qui sont strictement inférieures à l'année maximale autorisée et supérieures à l'année minimale autorisée (2004 par défaut car 2005 est une année valable pour un pz0 d'un numéro DEPHY). 
    On applique également ce filtrage sur chaque années des synthétisées pluri-annuels. Si toutes les années d'un synthétisé sont filtrées, la ligne correspondante est supprimée.
    Pour l'année maximale autorisée, c'est l'année en cours is on au delà de la date de saisie butoire (le 31 mars habituellement, donc avril=4), sinon c'est l'année qu précède l'année en cours.
    """
    a=len(df)

    # Obtenir l'année maximale autorisée
    if datetime.now().month >= mois_date_butoire_dephy_fin_saisie :
        annees_trop_recente = datetime.now().year
    else : 
        annees_trop_recente = datetime.now().year - 1

    # Créer la fonction qui filtre les années au seins d'un synthétisé pluri-annuel
    def filtrer_annees(annees_str):
        if pd.isna(annees_str):
            return None
        if not isinstance(annees_str, str): annees_str = str(annees_str)
        annees = [int(a.strip()) for a in annees_str.split(",")]
        annees_filtrees = [str(a) for a in annees if (a < annees_trop_recente) & (a > annees_trop_vieille)]
        return ", ".join(annees_filtrees) if annees_filtrees else None

    # Appliquer la fonction de filtrage des années aux campagnes en synthétisé
    df['synthetise_campagne'] = df['synthetise_campagne'].apply(filtrer_annees)

    # Si toutes les années d'un synthétisé ont été filtrées, on supprime la ligne
    # Pareil pour les réalisés dont la campagne est trop récente ou trop vieille
    df = df.loc[(pd.to_numeric(df['campagne'], errors='coerce') < annees_trop_recente) &
                (pd.to_numeric(df['campagne'], errors='coerce') > annees_trop_vieille) &
                (df['synthetise_campagne'].notna())]
    
    b = len(df)
    print(f"Filtre 2 : -{a-b} lignes")
    return df

def identificationDesPz0_et_filtrePz0Detecte(df, itk_realise_agrege, identification_pz0):
    """
    Permet de créer l'identification des pz0 pour les R (passage de zone à sdc) et les S (directement via le synthétisé). On le fait sur des dataframe à part, puis on reconcatène R et S. Enfin on supprime toutes les entités n'étant pas identifié avec un pz0 ou un post de manière fiable.
    Attention cela ne signifie pas que chaque numéro DEPHY ait un pz0 dans ce filtre. Mais cela arrive dans le filtre 3
    """
    a=len(df)

    # Passage des pz0 en R de l'échelle zone à l'échelle sdc
    R_pz0 = itk_realise_agrege.merge(identification_pz0.rename(columns={'entite_id':'zone_id'}), on='zone_id', how='left')[['sdc_id','pz0']].groupby('sdc_id')['pz0'].apply(list_to_scalar, include_groups=False).reset_index() # normalement ils sont tous devenu des scalaires car un sdc ne peut pas avoir plusieurs zones avec des identification de pz0 différentes. On vérifiera quand même.

    R_pz0 = R_pz0.loc[R_pz0['pz0'].notna(), ['sdc_id','pz0']]
        
    if len(R_pz0.loc[R_pz0['pz0'].apply(lambda x: isinstance(x, list))] ) > 0 :
        raise ValueError("Il y a des sdc réalisé avec plusieurs identification différentes selon leur zones")

    # On merge les pz0 identifiés pour les S
    df_S = df.loc[df['synthetise_id'].notna()]
    df_S = df_S.merge(identification_pz0.rename(columns={'entite_id':'synthetise_id'}), on='synthetise_id', how='left')

    # On merge les pz0 identifiés pour les R
    df_R = df.loc[df['synthetise_id'].isna()]
    df_R = df_R.merge(R_pz0.rename(columns={'entite_id':'sdc_id'}), on='sdc_id', how='left')

    # On concatene S + R
    df = pd.concat([df_S, df_R], ignore_index=True)
    
    # On supprime les entités n'ayant pas de pz0 identifié correctement
    df = df.loc[df['pz0'].isin(['pz0','post'])]

    b=len(df)
    print(f"Identification pz0 : {b-a} lignes")
    return df

def explode_campagne(df):
    """ 
    Explose (duplique) les campagnes multi-annuelles en lignes séparées. ("2011, 2012, 2013" -> "2011" + "2012" + "2013")
    Utilise la colonne 'synthetise_campagne' pour créer la nouvelle colonne de campagne explosée.
    Si on est en réalisé, on prend la colonne 'campagne' pour la nouvelle colonne.
    """
    a=len(df)

    df['new_campagne'] = df['synthetise_campagne']
    df['new_campagne'] = df['new_campagne'].fillna(df['campagne'])
    df['new_campagne'] = df['new_campagne'].astype(str).str.split(', ')

    df = df.explode('new_campagne')

    b=len(df)
    print(f"Ajout de {b-a} lignes par explosion des campagnes.")

    return df

def modification_duplicat_codeDephy_newCampagne(df):
    """
    Résout les duplications de code_dephy*new_campagne en suffixant les occurrences non 'pz0'
    et en dupliquant les lignes 'pz0' correspondantes pour chaque code suffixé.
    Les doublons hors 'pz0' sont renommés en ajoutant un suffixe (_0, _1, ...)
    Les lignes 'pz0' associées au code d’origine sont dupliquées pour chaque code suffixé, puis elles même suffixées
    Le code_dephy final remplace code_dephy_nettoyage
    """
    df = df.sort_values(by=['nom','code_dephy','new_campagne'])

    # détection duplicats code_dephy hors pz0
    mask = (
        df.duplicated(subset=['code_dephy_nettoyage','new_campagne'], keep=False)
        & (df["pz0"] != "pz0")
    )

    # ajout des suffixes 
    # Exemple : XXXX en 2011 et 2011 devient XXXX_0 en 2011 et XXXX_1 en 2011
    df.loc[mask, 'code_dephy_nettoyage'] = (
        df.loc[mask, 'code_dephy_nettoyage'] + '_' +
        df.loc[mask].groupby(['code_dephy_nettoyage','new_campagne']).cumcount().astype(str)
    )

    # duplication des pz0 pour les code_dephy qui ont été suffixés
    mapping = (
        df.loc[mask]
        .groupby('code_dephy')['code_dephy_nettoyage']
        .unique()
    )

    rows_to_add = []

    for base_code, new_codes in mapping.items():
        df_pz0 = df[(df['code_dephy'] == base_code) & (df['pz0'] == 'pz0')]
        if df_pz0.empty:
            continue

        # dupliquer le pz0 pour chaque code suffixé
        rows_to_add.append(
            pd.concat([df_pz0.assign(code_dephy_nettoyage=new_code) for new_code in new_codes])
        )

    if rows_to_add:
        df = pd.concat([df] + rows_to_add, ignore_index=True)

    # nettoyage final, on ne garde plus que code_dephy
    df = df.sort_values(by=['code_dephy_nettoyage','new_campagne'])
    df.drop(columns=['code_dephy'], inplace=True)
    df.rename(columns={'code_dephy_nettoyage':'code_dephy'}, inplace=True)

    print(f"Modification de {len(df.loc[df['code_dephy'].str.contains('_'),['code_dephy']])} code_dephy en duplication sur la même campagne. {len(df.loc[df['code_dephy'].str.contains('_')]['code_dephy'].str.extract(r'(.+?)_\d+$', expand=False).unique())} code_dephy différents concernés.")

    return df


def unique_pz0_by_code_dephy(df):
    """
    Ne garde qu'un seul point zéro par numéro dephy. On ne voudrais pas mettre trop de poids à un pz0 par rapport aux données post dans DG 
    On fait attention que les point zéro soit bien tous avant les post
    """
    df = df.copy()
    a=len(df)

    # Vérification que tout les pz0 sont bien avant les post
    grp = df.groupby('code_dephy')

    max_pz0 = grp.apply(lambda x: x.loc[x['pz0'] == 'pz0', 'new_campagne'].max())
    min_post = grp.apply(lambda x: x.loc[x['pz0'] != 'pz0', 'new_campagne'].min())

    incoherent = (max_pz0 >= min_post)
    bad_codes = incoherent[incoherent].index

    if len(bad_codes):
        print(bad_codes)
        raise ValueError("Erreur au moins un pz0 d'un code_dephy est détecté avec une campagne supérieur à celle du post le plus ancien du code_dephy")

    # On ne garde que les pz0 les plus récent (une seule ligne de pz0 par code_dephy)
    mask_pz0 = (df['pz0'] == 'pz0')
    df['rank'] = df[mask_pz0].groupby('code_dephy')['new_campagne'].rank(ascending=False, method='first')

    df = df[
        ((mask_pz0) & (df['rank'] == 1)) |  # 'pz0' les plus récentes
        (~mask_pz0)                         # tous les 'post'
    ].drop(columns=['rank']) 

    b=len(df)
    print(f"Suppression de {b-a} lignes de pz0 pour ne garder que les plus récents")
    return df


def ajout_especes_et_varietes_principales(df):
    """ Permet d'ajouter les espèces et variétés principales pour les cultures pérennes à partir du merge de la table espece_variete_perenne_principale. """
    # On crée d'abord les variables d'espèce et de variété principale pour les culture pérennes
        ## Espèce arboricutulture
    df['c111_species'] = np.where((df['filiere']=='ARBORICULTURE'), 
                                  df['espece_principale'], 
                                  np.nan)
        ## Variété arboricutulture
    df['c112_variety'] = np.where((df['filiere']=='ARBORICULTURE'), 
                                  df['variete_principale'], 
                                  np.nan)
        ## Variété viticulture
    df['c113_grapeVar'] = np.where((df['filiere']=='VITICULTURE'), 
                                   df['variete_principale'], 
                                   np.nan)
    
    return df

def ajout_typologie_simplifiee(df):
    """ Permet d'ajouter les typologies de systèmes simplifiées. """
    # Fonction qui ajoute le type d'agriculture à la typologie
    def add_type_agri(df, col):
        """ permet d'ajouter le type d'agriculture à la typologie, elle même composé d'espèce ou de type de production """
        return np.where(
            (df['type_agriculture'] == 'Agriculture conventionnelle') & (df[col] != np.nan),
            df[col] + ' conventionnels', 
            np.where(
                (df['type_agriculture'].isin(["En conversion vers l'agriculture biologique",'Agriculture biologique'])) & (df[col] != np.nan),
                df[col] + ' biologiques', 
                df[col]))
    # Fonction qui remplace les valeurs 'nan' (str) ou np.nan par None
    def nan_to_none(serie):
        return np.where((serie.isna())|(serie == 'nan'), None, serie)

    # ARBO
    df['c120_arboriculture_typo_sdc'] = np.select(
        [
            df['c111_species'].isna(),
            df['c111_species'].isin(['ERREUR_aucune_des_especes_arbo_majoritaires','melange_egal_espece','ERREUR_aucune_espece']),
            df['c111_species'].isin(['Pommier', 'Poirier']),
            df['c111_species'].isin(['Abricotier', 'Prunier']),
            ~(df['c111_species'].isin(['Pommier', 'Poirier', 'Abricotier', 'Prunier']))
        ],
        [
            np.nan,
            np.nan,
            'Pommiers et Poiriers',
            'Abricotiers et Pruniers',
            df['c111_species'] + 's'
        ],
        default=np.nan)

    df['c120_arboriculture_typo_sdc'] = add_type_agri(df, 'c120_arboriculture_typo_sdc')
    df['c120_arboriculture_typo_sdc'] = np.where(df['filiere']=='ARBORICULTURE',
                                        df['c120_arboriculture_typo_sdc'],
                                        None) # vérification variable que en ARBO
    df['c120_arboriculture_typo_sdc'] = nan_to_none(df['c120_arboriculture_typo_sdc'])

    # MARAICH
    df['c121_maraichage_typo_sdc'] = df['type_production'].str.lower().str.capitalize().str.replace('_', '-')
    df['c121_maraichage_typo_sdc'] = add_type_agri(df, 'c121_maraichage_typo_sdc')
    df['c121_maraichage_typo_sdc'] = np.where(df['filiere']=='MARAICHAGE',
                                        df['c121_maraichage_typo_sdc'],
                                        None) # vérification variable que en MARAICH
    df['c121_maraichage_typo_sdc'] = nan_to_none(df['c121_maraichage_typo_sdc'])


    # HORTICULTURE
    df['c122_horticulture_typo_sdc']  = np.select(
        [
            df['type_production'].isna(),
            df['type_production'] == 'CONTAINER_NURSERY',
            df['type_production'] == 'OPEN_GROUND_NURSERY',
            df['type_production'] == 'MIX',
            df['type_production'] == 'POT_PLANTS'
        ],
        [
            np.nan,
            'Pépinière hors sol, en conteneur',
            'Pépinières pleine terre',
            'Pépinières mixte',
            'Plantes en pot'
        ],
        default=np.nan)
    df['c122_horticulture_typo_sdc'] = np.where(df['filiere']=='HORTICULTURE',
                                        df['c122_horticulture_typo_sdc'],
                                        None) # vérification variable que en HORTI
    df['c122_horticulture_typo_sdc'] = nan_to_none(df['c122_horticulture_typo_sdc'])


    # TROP
    df['c123_cult_tropicales_typo_sdc'] = None # On ajoutera les données des cultures tropicales à la fin avec un Excel envoyé par la CAN mais il nous faut une colonne même vide pour l'instant afin de faire le bind.


    # GCPE
    df['c124_gcpe_typo_sdc'] = df['filiere'].str.lower().str.replace('_e', ' é').str.capitalize().str.replace('_', ' ')
    df['c124_gcpe_typo_sdc'] = add_type_agri(df, 'c124_gcpe_typo_sdc')
    df['c124_gcpe_typo_sdc'] = np.where(
        df['filiere'].isin(['POLYCULTURE_ELEVAGE','GRANDES_CULTURES']),
        df['c124_gcpe_typo_sdc'],
        None) # vérification variable que en GCPE
    df['c124_gcpe_typo_sdc'] = nan_to_none(df['c124_gcpe_typo_sdc'])


    print("c120_arboriculture_typo_sdc :\n",df['c120_arboriculture_typo_sdc'].unique(),"\n")
    print("c121_maraichage_typo_sdc :\n",df['c121_maraichage_typo_sdc'].unique(),"\n")
    print("c122_horticulture_typo_sdc :\n",df['c122_horticulture_typo_sdc'].unique(),"\n")
    print("c123_cult_tropicales_typo_sdc :\n",df['c123_cult_tropicales_typo_sdc'].unique(),"\n")
    print("c124_gcpe_typo_sdc :\n",df['c124_gcpe_typo_sdc'].unique(),"\n")
    return df

def ajout_infos_geo(df, commune, arrond_data, dep_data):
    """
    Permet d'ajouter les informations géographiques (arrondissement, département, région, bassin_viticole, ancienne région) à partir des données de référentiel géographique (json) et des la table commune.
    Par cela on s'assure que les propriétés des json qui sont utilisées par la carto soient bien alignées avec les variables du magasin DEPHYGraph.
    """
    arrond_data['arrondissement_code'] = arrond_data['Arrondissement_code_name'].str.split(' - ', expand=True)[0]
    arrond_data = arrond_data[['arrondissement_code','Arrondissement_code_name']].rename(columns={'Arrondissement_code_name':'arrondissement'})

    dep_data['departement_code'] = dep_data['Department_code_name'].str.split(' - ', expand=True)[0]
    dep_data = dep_data[['departement_code','Department_code_name']].rename(columns={'departement_code':'departement'})

    commune = commune.merge(arrond_data, on='arrondissement_code', how='left')
    commune = (commune.merge(dep_data, on='departement', how='left')
            .drop(columns='departement')
            .rename(columns={'Department_code_name':'departement'}))

    df = df.merge(commune[['commune_id','codeinsee', 'departement', 'region', 'bassin_viticole', 'ancienne_region','latitude', 'longitude','arrondissement']].rename(columns={'id':'commune_id'}), on='commune_id', how='left')

    # Besoin de ce mapping car la colonne region n'est pas la bonne dans le referentiel commune
    mapping = {
        84: "Auvergne-Rhône-Alpes",
        32: "Hauts-de-France",
        93: "Provence-Alpes-Côte d'Azur",
        44: "Grand Est",
        76: "Occitanie",
        28: "Normandie",
        75: "Nouvelle-Aquitaine",
        24: "Centre-Val de Loire",
        27: "Bourgogne-Franche-Comté",
        53: "Bretagne",
        94: "Corse",
        52: "Pays de la Loire",
        11: "Île-de-France",
        1: "Guadeloupe",
        2: "Martinique",
        3: "Guyane",
        4: "La Réunion",
        6: "Mayotte"
    }
    df['region'] = df['region'].map(mapping)

    return df

def filtre_3_coherence(df):
    """
    Attention filtre eds valeur et des lignes !
    Permet de vérifier la cohérence entre espèces principales renseignées et filière.
    Permet aussi de vérfiier la cohérence entre le type de travail du sol Semis Direct et la conduite en Agriculture Biologique, ainsi que la cohérence entre un IFT herbicide très bas et le type de travail du sol en Semis Direct.
    Enfin, on vérifie que les lignes ont bien une longitude, latitude, un sdc_id et une information de réalisé ou synthétisé.
    """
    a=len(df)
    c=df.isna().sum().sum()

    # Filtres des lignes : VITI sans vignes ou ARBO avec vignes
    df = df.loc[~(
        ((df['espece_principale']=='Vigne') & (df['filiere']!='VITICULTURE')) | 
        ((df['espece_principale']!='Vigne') & (df['filiere']=='VITICULTURE'))
        )]

    # Il est fortement peu probable qu’un sdc soit en Semis Direct s’il est en Agriculture Biologique. Lorsque c’est le cas on transforme Semis Direct de type_de_travail_du_sol en NA, car on part du principe que le type de travail du sol est moins fiable que le type de conduite du sdc.
    df.loc[(df['type_de_travail_du_sol'] == 'SEMIS_DIRECT') &
        (df['filiere'].isin(GCPE)) &
        (df['type_agriculture'].isin(["En conversion vers l'agriculture biologique",'Agriculture biologique'])),
        'type_de_travail_du_sol'] = np.nan

    # Si un IFT herbicide (ift_cible_non_mil_h) est strictement inférieur à 0.5 en GCPE alors que son type de travail du sol renseigné est Semis direct alors on transforme en NA les valeurs des variables ift_cible_non_mil_h et ift_cible_non_mil_chim_tot_hts.
    list_var_a_passer_en_na = ['ift_cible_non_mil_h','ift_cible_non_mil_chim_tot_hts']

    df.loc[(df['type_de_travail_du_sol'] == 'SEMIS_DIRECT') &
        (df['filiere'].isin(GCPE)) &
        (df['ift_cible_non_mil_h'] < 0.5),
        list_var_a_passer_en_na] = np.nan

    # On veut absolument une valeur pour longitude/latitude/realized/sdc_id. On filtre les lignes qui n'ont pas une des quatre variables
    df = df.loc[~((df['longitude'].isna()) | 
                  (df['latitude'].isna()) | 
                  (df['realized'].isna()) | 
                  (df['sdc_id'].isna()))]
    
    b=len(df)
    d=df.isna().sum().sum()
    print(f"Filtre 3 : {b-a} lignes ; {(d-c)/df.size*100:.3f}% des valeurs")
    return df

def filtre_4_avecUnPz0_et_auMoinsDeuxCampagnes(df):
    """
    Suppression des code_dephy avec une seule et unique campagne ainsi que ceux n'ayant aucun pz0 !
    """
    a=len(df)

    # On garde les code_dephy ayant au moins 2 campagnes différentes
    df = df.groupby('code_dephy').filter(lambda x: x['new_campagne'].nunique() > 1)

    # On garde les code_dephy ayant au moins un pz0 identifié
    df = df.groupby('code_dephy').filter(lambda x: (x['pz0'] == 'pz0').any())

    b = len(df)
    print(f"Filtre 4 : -{a-b} lignes")
    return df

def filtre_5_disponibilite_par_filiere(df):
    """ 
    Attention ne filtre que des valeurs !
    Filtre les variables qui ne sont pas disponibles pour certaines filières. Par exemple, les variables de performance économique et de travail du sol ne sont disponibles que pour les filières GCPE 
    """
    a=df.isna().sum().sum()

    # Variables économique et travail du sol dispo que pour GCPE
    df.loc[~df['filiere'].isin(GCPE), 
        ['type_de_travail_du_sol', 'utili_desherbage_meca', 'nbre_de_passages_desherbage_meca', 'pb_std_mil_avec_autoconso', 'mb_std_mil_avec_autoconso', 'msn_reelle_avec_autoconso']] = np.nan
    
    # Variable de temps de travail manuel que pour ARBO, VITI, MARAICH et CULTURES_TROP
    df.loc[~df['filiere'].isin(['ARBORICULTURE','VITICULTURE','MARAICHAGE','CULTURES_TROPICALES']), 
        ['tps_travail_manuel']] = np.nan
    
    # Variéble d'espèce principale et variété principale que pour ARBO
    df.loc[df['filiere']!='ARBORICULTURE', 
        ['c111_species','c112_variety']] = np.nan
    
    # Cépage principal que pour VITI
    df.loc[df['filiere']!='VITICULTURE', 
        ['c113_grapeVar']] = np.nan
    
    # Regle du 2021.11.21
    # Enlever les données relatives au fichier “vartohide” du 21/11/2021. Les experts filières, doutant de la qualité de leur données sur certains type de variables, préfèrent cacher les variables problématiques.
    df.loc[~df['filiere'].isin(GCPE + ['VITICULTURE']),  
        ['tps_travail_total']] = np.nan
    
    df.loc[~df['filiere'].isin(GCPE), 
        ['ferti_n_tot', 
         'ferti_n_mineral', 
         'ferti_n_organique',
         'ferti_p2o5_tot', 
         'ferti_p2o5_mineral', 
         'ferti_p2o5_organique', 
         'ferti_k2o_tot',
         'ferti_k2o_mineral',
         'ferti_k2o_organique',
         'tps_utilisation_materiel',
         'c504_outLabourTotalExpenses',
         'co_tot_std_mil',
         'cm_std_mil']] = np.nan

    b=df.isna().sum().sum()
    print(f"Filtre 5 : {(b-a)/df.size*100:.1f}% des valeurs")
    return df

def detect_outliers_via_iqr(df, dict_var_impacted, coef=2):
    """
    Détecte les outliers de chaque colonnes qui sont les keys de DICT_VAR_IMPACTED
    renvoie un dictionnaire des index qui sont détectés outliers
    """
    dict_index_outliers = {}
    for col in dict_var_impacted:
        s = df[col]
        q1, q3 = s.quantile([0.25, 0.75])
        iqr = q3 - q1
        low, high = q1 - coef * iqr, q3 + coef * iqr
        dict_index_outliers[col] = s[(s < low) | (s > high)].index.tolist()
    return dict_index_outliers

def detect_outliers_via_alerte_can(df, alertes_cols_var):
    """
    Détecte les valeurs qui ne correspondent pas aux alertes de la CAN.
    Retourne un dictionnaire d'index pour chaque valeur des colonnes dans ALERTES_COLS_VAR s'il y a une alerte dans la colonne des keys de ALERTES_COLS_VAR.
    """
    dict_idx_alerte_can = {}

    for col_alerte, targets in alertes_cols_var.items():
        # Si pas de colonne dans le df
        if col_alerte not in df.columns:
            print(f"Une alerte n'est pas dans le dataframe : {col_alerte}")
            continue

        # On en garde que les index avec des alertes
        mask = (~df[col_alerte].isin(["Pas d'alerte", "Cette alerte n'existe pas encore dans cette filière"])) | (df[col_alerte].isna())
        idx = set(df.index[mask])

        # Si aucune alerte
        if not idx:
            continue

        # Les targets doivent être sous forme de liste
        if not isinstance(targets, list):
            targets = [targets]

        # Pour chaque target on 
        for t in targets:
            # si la target n'est pas dans le df, ou s'il n'y en a pas
            if t is None or t not in df.columns:
                continue
            
            # si la target n'existe pas dans le dictionnaire final, on le crée
            if t not in dict_idx_alerte_can:
                dict_idx_alerte_can[t] = set()
            dict_idx_alerte_can[t] |= idx

    # conversion en list pour compatibilité avec apply_nan()
    return {k: list(v) for k, v in dict_idx_alerte_can.items()}

def apply_nan(df, dict_var_impacted, dict_index_outliers, name='outlier'):
    """
    Applique des NAN aux valeur qui ont été détectés comme outliers ou comme alertes
    Si une des keys dans dict_index_outliers contient des index, cela implique la colonne qui est la keys de dict_var_impacted qui est égale à la keys de dict_index_outliers, mais aussi les valeurs correspodantes dans dict_var_impacted
    """
    df = df.copy()
    a=df.isna().sum().sum()

    for col, idx in dict_index_outliers.items():
        cols = [col] + [c for c in (dict_var_impacted.get(col) or []) if c in df.columns]
        df.loc[idx, cols] = np.nan

    b=df.isna().sum().sum()
    print(f"Filtre {name} : {(b-a)/df.size*100:.1f}% des valeurs (soit {(b-a)} valeurs)")
    return df

def calcul_evolution_ift(group, col):
    """
    Permet de calculer les évolutions d'IFT et le nombre d'année entre la ligne pz0 et la ligne en question. Pour l'évolution d'IFT : que les ratios soit (post-pz0)/pz0 * 100
    """
    mask_pz0 = group['pz0'] == 'pz0'

    if mask_pz0.sum() > 1:
        raise ValueError("Groupe dephy avec trop de pz0. Ils aurait dû être filtrés pour n'en avoir qu'un seul")
    elif mask_pz0.sum() == 0:
        raise ValueError('Groupe dephy sans pz0')

    if col == 'new_campagne':
        pz0_val = int(group.loc[mask_pz0, col].iloc[0])
        result = np.where(
            mask_pz0 | group[col].isna(),
            np.nan,
            group[col].astype(int) - pz0_val
        )
        result = pd.Series(result, index=group.index)
        result = result.map(lambda x: (
                            np.nan if pd.isna(x)
                            else (f"pz0 + {int(x):02d} an" if int(x) == 1
                                else f"pz0 + {int(x):02d} ans")))
        return result

    else:
        col_values = group[col]
        pz0_val = group.loc[mask_pz0, col].iloc[0]
        conditions = [
            mask_pz0 | col_values.isna(),
            (pz0_val == 0) & (col_values == 0),
            (pz0_val == 0) & (col_values != 0)
        ]
        choices = [np.nan, 
                   0,
                   100]
        result = np.select(conditions, choices, 
            default= (col_values - pz0_val) / pz0_val * 100)
        return pd.Series(result, index=group.index)

def apply_evol(group):
    """
    Permet d'appliquer le calcul des évolutions à chaque colonne
    """
    group = group.copy()

    group['c103_networkYears'] = calcul_evolution_ift(group, 'new_campagne')
    group['c701_totalIFT_evol_ratio'] = calcul_evolution_ift(group, 'ift_cible_non_mil_chim_tot_hts')
    group['c702_IFT_hh_hts_evol_ratio'] = calcul_evolution_ift(group, 'c602_IFT_hh_hts')
    group['c703_biocontrolIFT_evol_ratio'] = calcul_evolution_ift(group, 'ift_cible_non_mil_biocontrole')
    group['c705_herbicideIFT_evol_ratio'] = calcul_evolution_ift(group, 'ift_cible_non_mil_h')
    group['c707_insecticideIFT_evol_ratio'] = calcul_evolution_ift(group, 'ift_cible_non_mil_i')
    group['c708_fungicideIFT_evol_ratio'] = calcul_evolution_ift(group, 'ift_cible_non_mil_f')
    group['c709_otherIFT_evol_ratio'] = calcul_evolution_ift(group, 'ift_cible_non_mil_a')
    group['c710_biologicalWaysSolution_evol_ratio'] = calcul_evolution_ift(group, 'recours_aux_moyens_biologiques')

    return group


def modif_modalite(df):
    """
    Modifie les modalités de toutes les colonnes du df
    """
    df["pz0"] = df["pz0"].replace({
        "pz0": "Systèmes avant l'entrée dans le réseau DEPHY",
        "post": "Systèmes évoluant au sein du réseau DEPHY"
    })

    df["filiere"] = df["filiere"].replace({
        "ARBORICULTURE": "Arboriculture",
        "CULTURES_TROPICALES": "Cultures tropicales",
        "GRANDES_CULTURES": "Grandes cultures Polyculture-élevage",
        "HORTICULTURE": "Horticulture",
        "MARAICHAGE": "Maraîchage",
        "POLYCULTURE_ELEVAGE": "Grandes cultures Polyculture-élevage",
        "VITICULTURE": "Viticulture"
    })

    df["type_de_travail_du_sol"] = df["type_de_travail_du_sol"].replace({
        "LABOUR_SYSTEMATIQUE": "1 - Labour systématique",
        "LABOUR_FREQUENT": "2 - Labour fréquent",
        "LABOUR_OCCASIONNEL": "3 - Labour occasionnel",
        "TCS": "4 - Techniques culturales simplifiées",
        "SEMIS_DIRECT": "5 - Semis direct"
    })

    df["utili_desherbage_meca"] = df["utili_desherbage_meca"].replace({
        "f": "Non",
        "t": "Oui"
    })

    # .str.replace au lieu de .replace car on change les 'pz0' DANS la valeur.
    df['c103_networkYears'] = df['c103_networkYears'].str.replace("pz0", "État initial")

    df['c111_species'] = df['c111_species'].replace({
        "ERREUR_aucune_des_especes_arbo_majoritaires": None,
        "ERREUR_aucune_espece": None,
        "melange_egal_espece": "Mélange équivalent d'espèces"
    })

    df['c112_variety'] = df['c112_variety'].replace({
        "melange_egal_variete": "Mélange équivalent de variétés",
        "ERREUR_aucune_variete": None
    })

    df['c113_grapeVar'] = df['c113_grapeVar'].replace({
        "melange_egal_variete": "Mélange équivalent de cépages",
        "ERREUR_aucune_variete": None
    })

    return df







#####################################################
####### FONCTION MAJEURE QUI RECAP LES ETAPES #######
#####################################################








def all_steps_for_maj_dephygraph(donnees, demande_rapport=False):
    """
    Regroupe toutes les étapes nécessaires pour la mise à jour du magasin DEPHYGraph.
    """
    # Chargement des données nécessaires
        ## Performances
    sdc_realise_performance = donnees["sdc_realise_performance"][['sdc_id'] + PERFORMANCES_COLS + list(ALERTES_COLS_VAR.keys())]
    synthetise_synthetise_performance = donnees["synthetise_synthetise_performance"][['synthetise_id'] + PERFORMANCES_COLS + list(ALERTES_COLS_VAR.keys())]
        ## Entrepot
    synthetise = donnees["synthetise"][['id', 'nom', 'campagnes', 'sdc_id']].rename(columns={'id':'synthetise_id', 'campagnes':'synthetise_campagne'})
    sdc = donnees["sdc"][['id','code','nom','modalite_suivi_dephy','code_dephy','filiere','type_production','type_agriculture','part_sau_domaine','reseaux_ir','reseaux_it','dispositif_id','validite']].rename(columns={"id": "sdc_id"})
    dispositif = donnees["dispositif"][['id','type','domaine_id']].rename(columns={"id": "dispositif_id"})
    domaine = donnees["domaine"][['id','code','nom','campagne','commune_id','sau_totale']].rename(columns={"id": "domaine_id"})
    commune = donnees["commune"][['id','codeinsee', 'departement', 'region', 'bassin_viticole', 'ancienne_region','latitude', 'longitude','arrondissement_code']].rename(columns={"id": "commune_id"})
        ## Referentiel
    arrond_data = donnees['geoVec_arrond']
    dep_data = donnees['geoVec_dep']
        ## Outils
    identification_pz0 = donnees["identification_pz0"]
    espece_variete_perenne_principale = donnees['espece_variete_perenne_principale'][['entite_id','espece_principale','variete_principale']]
    entite_unique_par_sdc_nettoyage = donnees['entite_unique_par_sdc_nettoyage']
    itk_realise_agrege = donnees['itk_realise_agrege'][['sdc_id','zone_id']]

    # Construction du jeu de données de base pour le magasin DEPHYGraph
        ## Création des S à partir de l'outil d'entité unique par SDC
    synth = pd.merge(
        entite_unique_par_sdc_nettoyage.loc[entite_unique_par_sdc_nettoyage["entite_retenue"] != "realise_retenu"].rename(columns={"entite_retenue": "synthetise_id"}), 
        synthetise_synthetise_performance, on="synthetise_id", how="left"
    )
    synth = synth.merge(synthetise.drop(columns='sdc_id').rename(columns={"nom": "nom_synthetise"}), on='synthetise_id', how='left', suffixes=(None,'_synthetise'))
        ## Création des R à partir de l'outil d'entité unique par SDC
    realise = pd.merge(
        entite_unique_par_sdc_nettoyage.loc[entite_unique_par_sdc_nettoyage["entite_retenue"] == "realise_retenu"], sdc_realise_performance, on="sdc_id", how="left"
    )
        ## Concaténation S + R
    df = pd.concat([synth, realise])
        ## Ajout des infos sdc, dispositif et domaine
    df = df.merge(sdc, on='sdc_id', how='left', suffixes=(None,'_sdc'))
    df = df.merge(dispositif, on='dispositif_id', how='left', suffixes=(None,'_dispositif'))
    df = df.merge(domaine, on='domaine_id', how='left', suffixes=(None,'_domaine'))
    df['entite_id'] = np.where(df['synthetise_id'].notna(), df['synthetise_id'], df['sdc_id'])

    # Nettoyage des numéros DEPHY
    df['code_dephy_nettoyage'] = nettoyage_numero_dephy(df, colonne='code_dephy')
    df['code_dephy_nettoyage'] = np.where(df['code_dephy_nettoyage'].isna(), df['code_dephy'], df['code_dephy_nettoyage'])

    # Filtre des dispositifs Ferme Detaille avec un type d'agriculture renseigné
    df = filtre_1_dispoFermeDetaille_typeAgriNotNull(df)

    # Filtre des années trop vieilles ou trop récentes
    df = filtre_2_annees(df)

    # Identification des pz0 et filtrage des entités n'étant pas un état valide (pz0 ou post)
    df = identificationDesPz0_et_filtrePz0Detecte(df, itk_realise_agrege, identification_pz0)

    # On explode les campagnes pluri-annuelles
    df = explode_campagne(df)

    # Modification des duplicats de numéro DEPHY*campagne
    df = modification_duplicat_codeDephy_newCampagne(df)

    # On ne garde que les pz0 les plus récent après l'explosion des campagnes et modif des code_dephy
    df = unique_pz0_by_code_dephy(df)

    # Ajout des infos sur les espèces et variétés principales pour les cultures pérennes
    df = df.merge(espece_variete_perenne_principale, on = 'entite_id', how='left')
    df = ajout_especes_et_varietes_principales(df)

    # Ajout des typologie de systèmes simplifiées
    df = ajout_typologie_simplifiee(df)
    
    # Ajout de variables supplémentaires
        ## IFT hors herbicide et hors TS
    df['c602_IFT_hh_hts'] = df['ift_cible_non_mil_hh'] - df['ift_cible_non_mil_ts']
        ## Charges totales hors main d'oeuvre
    df['c504_outLabourTotalExpenses'] = df['co_tot_std_mil'] + df['cm_std_mil']
        ## Type de saisie
    df['realized'] = np.where(df['synthetise_id'].isna(), 'realise', 'synthetise')

    # Ajout des infos géographiques
    df = ajout_infos_geo(df, commune, arrond_data, dep_data)

    # Filtre de cohérence (Espèces principales en pérennes, Semis direct en AB ou avec IFT faible)
    df = filtre_3_coherence(df)

    # On supprime les code_dephy n'ayant qu'une seule campagne ou n'ayant aucun pz0 identifié
    df = filtre_4_avecUnPz0_et_auMoinsDeuxCampagnes(df)

    # Filtre sur la disponibilité de certaines variables selon les filières
    df = filtre_5_disponibilite_par_filiere(df)

    # On crée un index code_dephy * new_campagne
    if df.duplicated(['code_dephy',"new_campagne"]).any():
        raise ValueError("code_dephy * new_campagne n'est pas unique, pas d'index possible !")

    df["new_campagne_str"] = df["new_campagne"].astype(str)
    df["code_dephy_for_idx"] = df["code_dephy"].astype(str)
    df.set_index(['code_dephy_for_idx',"new_campagne_str"], inplace=True)
    
    # Filtre de valeurs outliers
        ## On garde les index des lignes que l'on va supprimé, et on la save
    dict_idx_iqr = detect_outliers_via_iqr(df, DICT_VAR_IMPACTED, coef=2)
        ## On vire les outliers via les index de dict_idx_iqr
    df = apply_nan(df, DICT_VAR_IMPACTED, dict_idx_iqr)

    # Filtre de valeurs experts
        ## On garde les index des lignes que l'on va supprimé, et on la save
    dict_idx_alerte_can = detect_outliers_via_alerte_can(df, ALERTES_COLS_VAR)
        ## On vire les outliers via les index de dict_idx_iqr
    df = apply_nan(df, DICT_VAR_IMPACTED, dict_idx_alerte_can, name='alerte CAN')

    # Calculer les évolution d'ift (après les filtres de valeurs !)
    df = df.groupby('code_dephy').apply(apply_evol)

    # Modifier les modalités des colonnes
    df = modif_modalite(df)

    # Epurer les colonnes non-indispensable pour ne pas saturer le stockage
    colonnes_to_keep = [
        'code_dephy',
        'realized',
        'sdc_id',
        'synthetise_id',
        'entite_id',
        'dispositif_id',
        'domaine_id',
        'commune_id',

        'new_campagne',
        'pz0',
        'c103_networkYears',

        'codeinsee',
        'departement',
        'region',
        'bassin_viticole',
        'ancienne_region',
        'latitude',
        'longitude',
        'arrondissement',

        'filiere',
        'type_production',
        'type_agriculture',

        'reseaux_ir',
        'reseaux_it',

        'c111_species',
        'c112_variety',
        'c113_grapeVar',

        'c120_arboriculture_typo_sdc',
        'c121_maraichage_typo_sdc',
        'c122_horticulture_typo_sdc',
        'c123_cult_tropicales_typo_sdc',
        'c124_gcpe_typo_sdc',

        'ift_cible_non_mil_chimique_tot',
        'ift_cible_non_mil_chim_tot_hts',
        'ift_cible_non_mil_hh',
        'c602_IFT_hh_hts',
        'ift_cible_non_mil_h',
        'ift_cible_non_mil_f',
        'ift_cible_non_mil_i',
        'ift_cible_non_mil_ts',
        'ift_cible_non_mil_a',
        'ift_cible_non_mil_biocontrole',
        'recours_aux_moyens_biologiques',

        'hri1_hts',
        'hri1_g1_hts',
        'hri1_g2_hts',
        'hri1_g3_hts',
        'hri1_g4_hts',
        
        'qsa_tot_hts',
        'qsa_danger_environnement_hts',
        'qsa_toxique_utilisateur_hts',
        'qsa_cmr_hts',
        'qsa_glyphosate_hts',
        'qsa_cuivre_tot_hts',
        'qsa_soufre_tot_hts',

        'ferti_n_tot',
        'ferti_n_mineral',
        'ferti_n_organique',
        'ferti_p2o5_tot',
        'ferti_p2o5_mineral',
        'ferti_p2o5_organique',
        'ferti_k2o_tot',
        'ferti_k2o_mineral',
        'ferti_k2o_organique',

        'pb_std_mil_avec_autoconso',
        'mb_std_mil_avec_autoconso',
        'msn_reelle_avec_autoconso',
        'md_std_mil_avec_autoconso',

        'c504_outLabourTotalExpenses',
        'co_tot_std_mil',
        'cm_std_mil',
        'c_main_oeuvre_tot_std_mil',
        'c_main_oeuvre_tractoriste_std_mil',
        'c_main_oeuvre_manuelle_std_mil',
        'conso_carburant',

        'tps_utilisation_materiel',
        'tps_travail_manuel',
        'tps_travail_total',

        'surface_par_unite_de_travail_humain',
        'nombre_uth_necessaires',
        'nbre_de_passages_desherbage_meca',
        'utili_desherbage_meca',
        'type_de_travail_du_sol',

        'c701_totalIFT_evol_ratio',
        'c702_IFT_hh_hts_evol_ratio',
        'c703_biocontrolIFT_evol_ratio',
        'c705_herbicideIFT_evol_ratio',
        'c707_insecticideIFT_evol_ratio',
        'c708_fungicideIFT_evol_ratio',
        'c709_otherIFT_evol_ratio',
        'c710_biologicalWaysSolution_evol_ratio'
    ]

    df = df.reset_index(drop=True)
    df['id'] = df['code_dephy'].str.cat(df['new_campagne'], sep='_')
    df = df[['id'] + colonnes_to_keep]

    # Rapport sur le magasin DEPHYGraph
    report = None
    if demande_rapport :
        report = ProfileReport(df[colonnes_to_keep], 
                            title="DEPHYGraph, rapport sur les variables")

    return df, dict_idx_iqr, dict_idx_alerte_can, (report if demande_rapport else None)