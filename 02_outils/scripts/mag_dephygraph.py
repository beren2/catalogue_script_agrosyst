"""
	Regroupe les fonctions permettant de générer le magasin DEPHYGraph.
"""
import pandas as pd
import numpy as np
from datetime import datetime
# import geopandas as gpd

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

ALERTES_COLS = [
    'alerte_ferti_n_tot',
    'alerte_ift_cible_non_mil_chim_tot_hts',
    'alerte_ift_cible_non_mil_f',
    'alerte_ift_cible_non_mil_h',
    'alerte_ift_cible_non_mil_i',
    'alerte_ift_cible_non_mil_biocontrole',
    'alerte_co_irrigation_std_mil',
    'alerte_msn_std_mil_avec_autoconso',
    'alerte_nombre_interventions_phyto',
    'alerte_pb_std_mil_avec_autoconso',
    'alerte_rendement',
    'alertes_charges',
    'alerte_cm_std_mil',
    'alerte_co_semis_std_mil'
]

# def clean_list(lst):
#     """
#     Permet de nettoyer une liste en enlevant les valeurs 'nan' (str) et en retournant None si la liste est vide. Si la liste ne contient qu'un seul élément, retourne cet élément directement.
#     """
#     cleaned = [x for x in lst if str(x) != 'nan']
#     if len(cleaned) == 1:
#         cleaned = cleaned[0]
#     return cleaned if cleaned else None

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

def nettoyage_numero_dephy(df, colonne='code_dephy') :
    """ 
    Permet de nettoyer les numéros DEPHY présents dans la colonne spécifiée du DataFrame.
    On fait un premier nettoyage en ne gardant que les caractères alphanumériques et en supprimant les mentions "PPZ". Ensuite, on extrait le pattern AAAANNNN ou AAAAXNNN s'il est présent dans la chaîne. Les valeurs non conformes sont remplacées par None.
    """
    mask = df[colonne].notna()

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
    pattern = r'[A-Z]{3}(?:[0-9]|X)\d{4}(?!\d)'
    df[colonne] = df[colonne].str.extract(pattern, expand=False)

    return df[colonne]

def filtre_1_dispoFermeDetaille_typeAgriNotNull(df):
    """ 
    Filtre les DEPHY FERME DETAILLE et ne gardant que les données avec un type d'agriculture renseigné (AB, Conv, en conversion) 
    """
    # On filtre pour ne garder que les DEPHY FERME en détaillés
    df = df.loc[(df['modalite_suivi_dephy']=='DETAILLE') & (df['type']=='DEPHY_FERME')]

    # On enleve toute les données n'ayant pas de type d'agriculture (AB, Conv, en conversion)
    df = df.loc[(df['type_agriculture'].notna()) & (df['type_agriculture'] != 'Information obligatoire')]

    return df

def filtre_2_annees(df, annees_trop_vieille=2004, mois_date_butoire_dephy_fin_saisie=4):
    """ 
    Filtre les données en fonction des années de campagne
    On ne gardant que les camapgnes qui sont strictement inférieures à l'année maximale autorisée et supérieures à l'année minimale autorisée (2004 par défaut car 2005 est une année valable pour un pz0 d'un numéro DEPHY). 
    On applique également ce filtrage sur chaque années des synthétisées pluri-annuels. Si toutes les années d'un synthétisé sont filtrées, la ligne correspondante est supprimée.
    Pour l'année maximale autorisée, c'est l'année en cours is on au delà de la date de saisie butoire (le 31 mars habituellement, donc avril=4), sinon c'est l'année qu précède l'année en cours.
    """
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
    
    return df

def identificationDesPz0_et_filtrePz0Detecte(df, itk_realise_agrege, identification_pz0):
    """
    Permet de créer l'identification des pz0 pour les R (passage de zone à sdc) et les S (directement via le synthétisé). On le fait sur des dataframe à part, puis on reconcatène R et S. Enfin on supprime toutes les entités n'étant pas identifié avec un pz0 valide. 
    """
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

    print(f"Il y a {len(df.loc[~df['pz0'].isin(['pz0','post'])])} synthétisé ou sdc filtrés n'ayant pas de pz0 identifié correctement.")
    
    # On supprime les entités n'ayant pas de pz0 identifié correctement
    df = df.loc[df['pz0'].isin(['pz0','post'])]

    return df

def explode_campagne(df):
    """ 
    Doit contenir les colonnes pz0 + synthetise_campagne + campagne !
    Explose (duplique) les campagnes multi-annuelles en lignes séparées.
    Utilise la colonne 'synthetise_campagne' pour créer la nouvelle colonne de campagne explosée.
    Si on est en réalisé, on prend la colonne 'campagne' pour la nouvelle colonne.
    """
    df['new_campagne'] = df['synthetise_campagne']
    df['new_campagne'] = df['new_campagne'].fillna(df['campagne'])
    df['new_campagne'] = df['new_campagne'].astype(str).str.split(', ')

    # Cas des synthétisé pluri-annuel :
    # Lorsqu'une entité est un pz0, on ne garde que la dernière année du synthétisé pour ne pas donner plus de poids au point zéro qu'il ne le faudrait (on veut qu'une seule ligne, pas 3). On prendra le max des années dans ce cas.
    df['new_campagne'] = np.where(df['pz0']=='pz0', 
                                  df['new_campagne'].apply(lambda x: str(max(int(year) for year in x if year.strip().isdigit())) if isinstance(x, list) else x),
                                  df['new_campagne'])

    df = df.explode('new_campagne')

    # Cas des réalisé ou de synthétisé mono-annuel :
    # On ne garde que les lignes pz0 les plus récentes.
    mask_pz0 = (df['pz0'] == 'pz0')
    df['rank'] = df[mask_pz0].groupby('code_dephy')['new_campagne'].rank(ascending=False, method='first')

    df = df[
        ((mask_pz0) & (df['rank'] == 1)) |  # 'pz0' les plus récentes
        (~mask_pz0)                         # tous les 'post'
    ].drop(columns=['rank']) 

    return df

def modification_duplicat_codeDephy_newCampagne(df):
    # On ordonne le df via le nom du sdc et le code_dephy avant nettoyage
    df = df.sort_values(by=['nom_sdc','code_dephy','new_campagne'])
    # On crée le mask des code_dephy*new_campagne en dupliqués
    mask = df.duplicated(subset=['code_dephy_nettoyage','new_campagne'], keep=False)
    # On ajoute un suffixe _1, _2, etc. aux code_dephy dupliqués pour les différencier
    df.loc[mask, 'code_dephy_nettoyage'] = (
        df.loc[mask, 'code_dephy_nettoyage'] + '_' +
        (df.loc[mask].groupby(['code_dephy_nettoyage','new_campagne']).cumcount()).astype(str)
        )
    
    # On purifie le df
    df = df.sort_values(by=['code_dephy_nettoyage','new_campagne'])
    df.drop(columns=['code_dephy'], inplace=True)
    df.rename(columns={'code_dephy_nettoyage':'code_dephy'}, inplace=True)

    return df


def filtre_3_avecUnPz0_et_auMoinsDeuxCampagnes(df):
    """
    Suppression des code_dephy avec une seule et unique campagne ainsi que ceux n'ayant aucun pz0 !
    """
    # On garde les code_dephy ayant au moins 2 campagnes différentes
    df = df.groupby('code_dephy').filter(lambda x: x['new_campagne'].nunique() > 1)

    # On garde les code_dephy ayant au moins un pz0 identifié
    df = df.groupby('code_dephy').filter(lambda x: (x['pz0'] == 'pz0').any())

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
            df['c111_species'].isin(['Pommier', 'Poirier']),
            df['c111_species'].isin(['Abricotier', 'Prunier']),
            ~(df['c111_species'].isin(['Pommier', 'Poirier', 'Abricotier', 'Prunier']))
        ],
        [
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

    df = df.merge(commune[['id','codeinsee', 'departement', 'region', 'bassin_viticole', 'ancienne_region','latitude', 'longitude','arrondissement']].rename(columns={'id':'commune_id'}), on='commune_id', how='left')

    return df

def filtre_4_coherence(df):
    """
    Permet de vérifier la cohérence entre espèces principales renseignées et filière.
    Permet aussi de vérfiier la cohérence entre le type de travail du sol Semis Direct et la conduite en Agriculture Biologique, ainsi que la cohérence entre un IFT herbicide très bas et le type de travail du sol en Semis Direct.
    Enfin, on vérifie que les lignes ont bien une longitude, latitude, un sdc_id et une information de réalisé ou synthétisé.
    """
    # Filtres des lignes : VITI sans vignes ou ARBO avec vignes
    df = df.loc[~(
        ((df['c111_species']=='Vigne') & (df['c101_sector']!='VITICULTURE')) | 
        ((df['c111_species']!='Vigne') & (df['c101_sector']=='VITICULTURE'))
        )]

    # Il est fortement peu probable qu’un sdc soit en Semis Direct s’il est en Agriculture Biologique. Lorsque c’est le cas on transforme Semis Direct de c201_groundWorkType en NA, car on part du principe que le type de travail du sol est moins fiable que le type de conduite du sdc.
    df.loc[(df['c201_groundWorkType'] == 'SEMIS_DIRECT') &
        (df['c101_sector'].isin(['GRANDES_CULTURES','POLYCULTURE_ELEVAGE'])) &
        (df['c110_managementType'].isin(["En conversion vers l'agriculture biologique",'Agriculture biologique'])),
        'c201_groundWorkType'] = np.nan

    # Si un IFT herbicide (c605_herbicideIFT) est strictement inférieur à 0.5 en GCPE alors que son type de travail du sol renseigné est Semis direct alors on transforme en NA les valeurs des variables c605_herbicideIFT et c601_totalIFT.
    list_var_a_passer_en_na = ['c605_herbicideIFT','c601_totalIFT']

    df.loc[(df['c201_groundWorkType'] == 'SEMIS_DIRECT') &
        (df['c101_sector'].isin(['GRANDES_CULTURES','POLYCULTURE_ELEVAGE'])) &
        (df['c605_herbicideIFT'] < 0.5),
        list_var_a_passer_en_na] = np.nan

    # On veut absolument une valeur pour longitude/latitude/realized/sdc_id. On filtre les lignes qui n'ont pas une des quatre variables
    df = df.loc[~((df['longitude'].isna()) | 
                  (df['latitude'].isna()) | 
                  (df['realized'].isna()) | 
                  (df['sdc_id'].isna()))]
    
    return df

def filtre_5_disponibilite_par_filiere(df):
    """ 
    Filtre les variables qui ne sont pas disponibles pour certaines filières. Par exemple, les variables de performance économique et de travail du sol ne sont disponibles que pour les filières GCPE 
    """
    # Variables économique et travail du sol dispo que pour GCPE
    df.loc[~df['c101_sector'].isin(GCPE), 
        ['c201_groundWorkType', 'c203_mechanicalWeeding', 'c204_mechanicalWeedingInterventionFrequency', 'c501_grossProceeds', 'c502_grossProfit', 'c503_semiNetMargin']] = np.nan
    
    # Variable de temps de travail manuel que pour ARBO, VITI, MARAICH et CULTURES_TROP
    df.loc[~df['c101_sector'].isin(['ARBORICULTURE','VITICULTURE','MARAICHAGE','CULTURES_TROPICALES']), 
        ['c303_labourTime']] = np.nan
    
    # Variéble d'espèce principale et variété principale que pour ARBO
    df.loc[df['c101_sector']!='ARBORICULTURE', 
        ['c111_species','c112_variety']] = np.nan
    
    # Cépage principal que pour VITI
    df.loc[df['c101_sector']!='VITICULTURE', 
        ['c113_grapeVar']] = np.nan
    
    # Regle du 2021.11.21
    # Enlever les données relatives au fichier “vartohide” du 21/11/2021. Les experts filières, doutant de la qualité de leur données sur certains type de variables, préfèrent cacher les variables problématiques.
    df.loc[~df['c101_sector'].isin(GCPE + ['VITICULTURE']),  
        ['c301_workingTime']] = np.nan
    
    df.loc[~df['c101_sector'].isin(GCPE), 
        ['c401_fertilizationUnityN', 'c402_fertilizationMineralUnityN', 'c403_fertilizationOrganicUnityN',
            'c404_fertilizationUnityP', 'c405_fertilizationMineralUnityP', 'c406_fertilizationOrganicUnityP',
            'c407_fertilizationUnityK', 'c408_fertilizationMineralUnityK', 'c409_fertilizationOrganicUnityK',
            'c302_mechanizationTime',
            'c504_outLabourTotalExpenses', 'c505_operatingExpenses','c507_mechanizationExpenses']] = np.nan

    return df

def filtre_6_outliers(df):
    return df

def calcul_evolution_ift(df):
    def get_evol(group, col):
        mask_pz0 = group['c102_pz0'] == 'pz0'

        if mask_pz0.sum() > 1:
            raise ValueError("Groupe dephy avec trop de pz0. Ils aurait dû être filtrés pour n'en avoir qu'un seul")
        elif mask_pz0.sum() == 0:
            raise ValueError('Groupe dephy sans pz0')

        if col == 'c104_campaign_dis':
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
            pz0_val = group.loc[mask_pz0, col].iloc[0]
            result = np.where(
                mask_pz0 | group[col].isna(),
                np.nan,
                group[col] - pz0_val
            )
            return pd.Series(result, index=group.index)

    def apply_evol(group):
        group = group.copy()

        group['c103_networkYears'] = get_evol(group, 'c104_campaign_dis')
        group['c701_totalIFT_evol_diff'] = get_evol(group, 'c601_totalIFT')
        group['c702_IFT_hh_hts_evol_diff'] = get_evol(group, 'c602_IFT_hh_hts')
        group['c703_biocontrolIFT_evol_diff'] = get_evol(group, 'c603_biocontrolIFT')
        group['c705_herbicideIFT_evol_diff'] = get_evol(group, 'c605_herbicideIFT')
        group['c707_insecticideIFT_evol_diff'] = get_evol(group, 'c607_insecticideIFT')
        group['c708_fungicideIFT_evol_diff'] = get_evol(group, 'c608_fungicideIFT')
        group['c709_otherIFT_evol_diff'] = get_evol(group, 'c609_otherIFT')
        group['c710_biologicalWaysSolution_evol_diff'] = get_evol(group, 'c610_biologicalWaysSolution')

        return group

    df = df.groupby('dephyNb').apply(apply_evol).reset_index(drop=True)

    return df












def all_steps_for_maj_dephygraph(donnees):
    """
    Regroupe toutes les étapes nécessaires pour la mise à jour du magasin DEPHYGraph.
    """
    # Chargement des données nécessaires
        ## Performances
    sdc_realise_performance = donnees["sdc_realise_performance"][['sdc_id'] + PERFORMANCES_COLS + ALERTES_COLS]
    synthetise_synthetise_performance = donnees["synthetise_synthetise_performance"][['synthetise_id'] + PERFORMANCES_COLS + ALERTES_COLS]
        ## Entrepot
    synthetise = donnees["synthetise"][['id', 'nom', 'campagnes', 'sdc_id']].rename(columns={'id':'synthetise_id', 'campagnes':'synthetise_campagne'})
    sdc = donnees["sdc"][['id','code','nom','modalite_suivi_dephy','code_dephy','filiere','type_production','type_agriculture','part_sau_domaine','reseaux_ir','reseaux_it','dispositif_id','validite']]
    dispositif = donnees["dispositif"][['id','type','domaine_id']]
    domaine = donnees["domaine"][['id','code','nom','campagne','commune_id','sau_totale']]
    commune = donnees["commune"][['id','codeinsee', 'departement', 'region', 'bassin_viticole', 'ancienne_region','latitude', 'longitude','arrondissement_code']]
        ## Referentiel
    arrond_data = donnees['geoVec_arrond']
    dep_data = donnees['geoVec_dep']
        ## Outils
    identification_pz0 = donnees["identification_pz0"]
    espece_variete_perenne_principale = donnees['espece_variete_perenne_principale'][['entite_id','espece_principale','variete_principale']]
    entite_unique_par_sdc_nettoyage = donnees['entite_unique_par_sdc_nettoyage']
    itk_realise_agrege = donnees['itk_realise_agrege'][['sdc_id','zone_id']]

    # itk_synthetise_agrege = donnees['itk_synthetise_agrege']
    # plantation_perenne_synthetise_restructure = donnees['plantation_perenne_synthetise_restructure']
    # noeuds_synthetise_restructure = donnees['noeuds_synthetise_restructure']
    # poids_connexions_synthetise_rotation = donnees["poids_connexions_synthetise_rotation"]
    # typologie_can_culture = donnees["typologie_can_culture"]
    # typologie_can_rotation_synthetise = donnees["typologie_can_rotation_synthetise"]
    # typologie_assol_can_realise = donnees["typologie_assol_can_realise"]
    # donnees_spatiales_commune_du_domaine = donnees["donnees_spatiales_commune_du_domaine"]

    # Construction du jeu de données de base pour le magasin DEPHYGraph
        ## Création des S à partir de l'outil d'entité unique par SDC
    synth = pd.merge(
        entite_unique_par_sdc_nettoyage.loc[entite_unique_par_sdc_nettoyage["entite_retenue"] != "realise_retenu"].rename(columns={"entite_retenue": "synthetise_id"}), 
        synthetise_synthetise_performance, on="synthetise_id", how="left"
    )
    synth = synth.merge(synthetise, on='synthetise_id', how='left', suffixes=(None,'_synthetise'))
        ## Création des R à partir de l'outil d'entité unique par SDC
    realise = pd.merge(
        entite_unique_par_sdc_nettoyage.loc[entite_unique_par_sdc_nettoyage["entite_retenue"] == "realise_retenu"], sdc_realise_performance, on="sdc_id", how="left"
    )
        ## Concaténation S + R
    df = pd.concat([synth, realise])
        ## Ajout des infos sdc, dispositif et domaine
    df = df.merge(sdc, on='sdc_id', how='left', suffixes=(None,'_sdc'))
    df = df.merge(dispositif, left_on='dispositif_id', right_on='id', how='left', suffixes=(None,'_dispositif'))
    df = df.merge(domaine, left_on='domaine_id', right_on='id', how='left', suffixes=(None,'_domaine'))
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

    # On explode les campagnes pluri-annuelles, sauf les pz0 pour lesquels on ne garde que l'année la plus récente du synthétisé
    df = explode_campagne(df)

    # Modification des duplicats de numéro DEPHY*campagne
    df = modification_duplicat_codeDephy_newCampagne(df)

    # On supprime les code_dephy n'ayant qu'une seule campagne ou n'ayant aucun pz0 identifié
    df = filtre_3_avecUnPz0_et_auMoinsDeuxCampagnes(df)

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

    # Ajout des infos géographiques
    df = ajout_infos_geo(df, commune, arrond_data, dep_data)

    # Filtre de cohérence (Espèces principales en pérennes, Semis direct en AB ou avec IFT faible)
    df = filtre_4_coherence(df)

    # Filtre sur la disponibilité de certaines variables selon les filières
    df = filtre_5_disponibilite_par_filiere(df)





    df = filtre_6_outliers(df)

    df = calcul_evolution_ift(df)

    return df