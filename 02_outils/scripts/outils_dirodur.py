"""
	Regroupe les fonctions permettant de générer les outils utiles lors de la génération du magasin "DiRoDur".
"""
import pandas as pd
import numpy as np

from scripts.utils.dirodur_utiles import filtered_entities_sdc_level

# ----------------------------------------- #
# CRÉATION DU RÉFÉRENTIEL DE MATCH D'UNITÉS #
# ----------------------------------------- #
UNITES_RENDEMENT = {
    'q/ha (humidité ramenée à la norme)' : 'Q_HA_TO_STANDARD_HUMIDITY',
    't MS/ha' : 'TONNE_MS_HA',
    't sucre/ha' : 'TONNE_SUGAR_HA',
    't/ha' : 'TONNE_HA',
    'tonne_racines_ha_16_pourc' : 'TONNE_RACINES_HA_16_POURC', 
    'q/ha' : 'Q_HA',
    'kg/m²' : 'KG_M2',
    'unité/ha' : 'UNITE_HA',
    'hl/ha' : 'HL_HA'
}

def get_rendement_filtre_realise_outils_dirodur(donnees):
    """ wraper de get_rendement_filtre_outils_dirodur pour réaliser les tests plus facilement"""
    res = get_rendement_filtre_outils_dirodur(donnees, mode_saisie='realise')
    return res

def get_rendement_filtre_synthetise_outils_dirodur(donnees):
    """ wraper de get_rendement_filtre_outils_dirodur pour réaliser les tests plus facilement"""
    res = get_rendement_filtre_outils_dirodur(donnees, mode_saisie='synthetise')
    return res


def get_rendement_filtre_outils_dirodur(
        donnees,
        mode_saisie = 'realise'
    ):
    """
        Permet d'obtenir les informations sur la qualité des rendements en synthétisé. 
        Le paramètre type_rendement peut valoir "realise" ou "synthetise", selon que l'on souhaite obtenir les informations pour les rendements en réalisé ou en synthétisé.
        Retourne 3 booléens :
            - destination_have_match_in_ref_dirodur : indique si la destination de récolte est parmis celles retenues pour le magasin DiRoDur
            - unite_problematic : indique si l'unité de rendement (fonction de la destination) est différente de celle attendue --> cas historiques
            - espece_is_na : indique si l'espèce de la culture est nulle
        Pour le magasin DiRodur, on s'attend à avoir, pour ces booléens : 
            - destination_have_match_in_ref_dirodur : True
            - unite_problematic : False
            - espece_is_na : False
    """

    df = donnees.copy()
    df['composant_culture'] = df['composant_culture'].set_index('id')
    df['destination_valorisation'] = df['destination_valorisation'].set_index('id')
    df['recolte_rendement_prix'] = df['recolte_rendement_prix'].set_index('id')
    df['recolte_rendement_prix_restructure'] = df['recolte_rendement_prix_restructure'].set_index('id')
    df['action_'+mode_saisie+'_agrege'] = df['action_'+mode_saisie+'_agrege'].set_index('id')
    df['espece'] = df['espece'].set_index('id')
    df['variete'] = df['variete'].set_index('id')
    
    df['unite_rendement'] = pd.DataFrame.from_dict(UNITES_RENDEMENT, orient='index', columns=['unite_agrosyst']).reset_index().rename(columns={'index':'unite_nl'})

    # complétion du référentiel transmis par les agronomes
    left = df['correspondance_destination_gcpe_dirodur']
    right = df['unite_rendement']
    df['correspondance_destination_gcpe_dirodur'] = pd.merge(left, right, left_on = 'Unité_rendement', right_on = 'unite_nl', how = 'left')


    # compilation d'un composant_culture_extanded
    COLUMNS_ESPECES = ['code_espece_botanique', 'libelle_espece_botanique', 'nom_culture_acta', 'typocan_espece']
    left = df['composant_culture']
    right = df['espece'][COLUMNS_ESPECES]
    df['composant_culture_extanded'] = pd.merge(left, right, left_on = 'espece_id', right_index=True, how='left')
    COLUMNS_VARIETES = ['denomination']
    left = df['composant_culture_extanded']
    right = df['variete'][COLUMNS_VARIETES]
    df['composant_culture_extanded'] = pd.merge(left, right, left_on = 'variete_id', right_index=True, how='left')

    # ajout des informations du référentiel de destination
    left = df['recolte_rendement_prix'][['rendement_moy', 'destination_id', 'rendement_unite', 'action_id']]
    right = df['destination_valorisation'][['code_destination_a', 'libelle']].dropna()
    df['recolte_rendement_prix_extanded'] = pd.merge(left, right, left_on='destination_id', right_index=True, how='left').rename(columns={'code_destination_a' : 'code_destination',  'libelle':'libelle_destination'})

    # ajout des informations du référentiel DiRoDur constitué par les agronomes (join on code destination)
    left = df['recolte_rendement_prix_extanded'].reset_index()
    right = df['correspondance_destination_gcpe_dirodur'][['code_destination_A', 'Dirodur', 'unite_agrosyst']]
    df['recolte_rendement_prix_extanded'] = pd.merge(left, right, left_on='code_destination', right_on='code_destination_A', how='left').set_index('id')

    # ajout des information de l'outil 'recolte_rendement_prix_restructure'
    left = df['recolte_rendement_prix_extanded']
    right = df['recolte_rendement_prix_restructure']
    df['recolte_rendement_prix_extanded'] = pd.merge(left, right, left_index=True, right_index=True, how='left')

    # ajout des informations sur le composant de culture lié
    left = df['recolte_rendement_prix_extanded']
    right = df['composant_culture_extanded']
    df['recolte_rendement_prix_extanded'] = pd.merge(left, right, left_on='composant_culture_id', right_index=True, how='left')

    # Étape 1 : identification des rendements qui ont une destination acceptée dans DiRoDur
    # c'est à dire les rendements dans des destinations pour lesquelles on a pu trouver un match dans le référentiel DiRoDur
    df['recolte_rendement_prix_extanded']['destination_have_match_in_ref_dirodur'] = ~df['recolte_rendement_prix_extanded']['Dirodur'].isna()

    # Étape 2 : identification des unités problématiques 
    # c'est à dire des rendements qui auraient des unités différentes de celles attendues dans DiRoDur pour la destination correspondante
    df['recolte_rendement_prix_extanded']['unite_problematic'] = False
    df['recolte_rendement_prix_extanded'].loc[
        (df['recolte_rendement_prix_extanded']['destination_have_match_in_ref_dirodur']) &
        (df['recolte_rendement_prix_extanded']['unite_agrosyst'] != df['recolte_rendement_prix_extanded']['rendement_unite']),
        'unite_problematic'
    ] = True

    # Étape 3 : identification des rendements qui n'ont pas d'espèce
    df['recolte_rendement_prix_extanded']['espece_is_na'] = df['recolte_rendement_prix_extanded']['code_espece_botanique'].isna()

    # Étape 3 bis (optionnelle) : identification des rendements qui n'ont pas de variété
    df['recolte_rendement_prix_extanded']['variete_is_na'] = df['recolte_rendement_prix_extanded']['denomination'].isna()
    
    res = df['recolte_rendement_prix_extanded'].reset_index()[[
        'id',
        'destination_have_match_in_ref_dirodur',
        'unite_problematic',
        'espece_is_na'
    ]]
    return res

def get_sdc_realise_filtre_outils_dirodur(
        donnees,
    ):
    """
        Permet d'obtenir les informations pour filtrer ou non les sdc en réalisé
        Les colonnes sont à "True" si il faut filtrer les lignes correspondante dans le contexte de DiRoDur.
    """
    # obtention des filtres sur les systèmes de cultures    
    sdc_realise_filtre, _ = filtered_entities_sdc_level(donnees)

    # obtention des filtres à l'échelle itk
    itk_filtre_outils_dirodur = get_itk_filtre_outils_dirodur(donnees)

    # constitution de la colonne "nombre_itk_alerte"
    left = sdc_realise_filtre
    right = itk_filtre_outils_dirodur.groupby('sdc_id').agg({'filtre_alerte':'sum'}).rename(
        columns={'filtre_alerte':'nombre_itk_alerte'}
    ).fillna(0)

    res = pd.merge(left, right, left_on='sdc_id', right_on='sdc_id', how='left').fillna(0)

    return res

def get_synthetise_filtre_outils_dirodur(
        donnees
    ):
    """
        Permet d'obtenir les informations pour filtrer ou non les systèmes synthétisés.
        Les colonnes sont à "True" si il faut filtrer les lignes correspondante dans le contexte de DiRoDur.
    """
    _, synthetises_filtre = filtered_entities_sdc_level(donnees)

    print(synthetises_filtre.columns)

    # obtention des filtres à l'échelle itk
    itk_filtre_outils_dirodur = get_itk_filtre_outils_dirodur(donnees)
    print(itk_filtre_outils_dirodur.columns)


    # constitution de la colonne "nombre_itk_alerte"
    left = synthetises_filtre
    right = itk_filtre_outils_dirodur.groupby('synthetise_id').agg({'filtre_alerte':'sum'}).rename(
        columns={'filtre_alerte':'nombre_itk_alerte'}
    ).fillna(0)

    res = pd.merge(left, right, left_on='synthetise_id', right_on='synthetise_id', how='left').fillna(0)

    return res

def get_itk_filtre_outils_dirodur(
        donnees,
    ):
    """
        
        Permet d'obtenir les informations permettant de filtrer ou non les itinéraires techniques.
        Les colonnes sont à "True" si il faut filtrer les lignes correspondante dans le contexte de DiRoDur.
    
        Attention, le dataframe de sortie ne contient pas tous les ITK d'Agrosyst (uniquement les assolées), 
        On exclue aussi les parcelles non rattachées.
    """
    df = donnees.copy()
    df['sdc'] = df['sdc'].set_index('id')
    df['synthetise'] = df['synthetise'].set_index('id')
    df['connection_synthetise'] = df['connection_synthetise'].set_index('id')
    df['noeuds_synthetise'] = df['noeuds_synthetise'].set_index('id')
    df['noeuds_realise'] = df['noeuds_realise'].set_index('id')
    df['parcelle'] = df['parcelle'].set_index('id')
    df['zone'] = df['zone'].set_index('id')
    df['noeuds_synthetise_restructure'] = df['noeuds_synthetise_restructure'].set_index('id')


    # définition des filières retenues pour le magasin DiRoDur
    
    # définition des filières retenues pour le magasin DiRoDur
    FILIERES = [
        'POLYCULTURE_ELEVAGE',
        'GRANDES_CULTURES'
    ] 

    # définition des champs pouvant signifier que l'alerte n'est pas levée 
    ALERTE_IS_NO_STRINGS = [
        "Pas d'alerte",
        "Cette alerte n'existe pas dans cette filière",
        "Cette alerte n'existe pas encore dans cette filière",
        np.nan
    ]

    # définition des colonnes d'alertes consultées
    ALERTE_COLUMNS = [
        'alerte_co_semis_std_mil',
        'alerte_ift_cible_mil_chim_tot_hts',
        'alerte_ift_cible_mil_f',
        'alerte_ift_cible_mil_h',
        'alerte_ift_cible_mil_i',
        'alerte_ift_cible_mil_biocontrole',
        'alerte_co_irrigation_std_mil',
        'alerte_msn_std_mil_avec_autoconso',
        'alerte_pb_std_mil_avec_autoconso',
        'alerte_rendement',
        'alerte_cm_std_mil',
        'alerte_co_semis_std_mil',
        'alertes_charges'
    ]

    # création de la colonne de filtre sur la filière
    df['itk_synthetise_performance']['filtre_filiere'] = True
    df['itk_realise_performance']['filtre_filiere'] = True

    # en synthétisé 
    # on exclue les plantations perennes
    left = df['itk_synthetise_performance']
    right = df['connection_synthetise']
    df['itk_synthetise_performance_extanded'] = pd.merge(left, right, left_on='connection_synthetise_id', right_index=True, how = 'inner')

    left = df['itk_synthetise_performance_extanded']
    right = df['connection_synthetise'][['cible_noeuds_synthetise_id']]
    df['synthetise_synthetise_performance_extanded'] = pd.merge(left, right, left_on='connection_synthetise_id', right_index=True, how='left')


    left = df['itk_synthetise_performance_extanded']
    right = df['noeuds_synthetise'][['synthetise_id']]
    df['itk_synthetise_performance_extanded'] = pd.merge(left, right, left_on='cible_noeuds_synthetise_id', right_index=True, how='left')

    left = df['itk_synthetise_performance_extanded']
    right = df['noeuds_synthetise_restructure'][['culture_id']]
    df['itk_synthetise_performance_extanded'] = pd.merge(left, right, left_on='cible_noeuds_synthetise_id', right_index=True, how='left')

    left = df['itk_synthetise_performance_extanded']
    right = df['synthetise'][['sdc_id']]
    df['itk_synthetise_performance_extanded'] = pd.merge(left, right, left_on='synthetise_id', right_index=True, how='left')

    left = df['itk_synthetise_performance_extanded']
    right = df['sdc'][['filiere']]
    df['itk_synthetise_performance_extanded'] = pd.merge(left, right, left_on='sdc_id', right_index=True, how='left')

    left = df['itk_synthetise_performance_extanded']
    right = df['typologie_can_culture']
    df['itk_synthetise_performance_extanded'] = pd.merge(left, right, left_on='culture_id', right_on='culture_id', how='left')


    # en réalisé 
    # on exclue le perenne
    left = df['itk_realise_performance']
    right = df['noeuds_realise'][['rang']]
    df['itk_realise_performance_extanded'] = pd.merge(left, right, left_on='noeuds_realise_id', right_index=True, how='inner')

    left = df['itk_realise_performance_extanded']
    right = df['zone'][['parcelle_id']]
    df['itk_realise_performance_extanded'] = pd.merge(left, right, left_on='zone_id', right_index=True, how='left')

    left = df['itk_realise_performance_extanded']
    right = df['parcelle'][['sdc_id']]
    df['itk_realise_performance_extanded'] = pd.merge(left, right, left_on='parcelle_id', right_index=True, how='left')

    # on exclue les parcelles non rattachées
    left = df['itk_realise_performance_extanded']
    right = df['sdc'][['filiere']]
    df['itk_realise_performance_extanded'] = pd.merge(left, right, left_on="sdc_id", right_index=True, how='inner')

    left = df['itk_realise_performance_extanded']
    right = df['typologie_can_culture']
    df['itk_realise_performance_extanded'] = pd.merge(left, right, left_on='culture_id', right_on='culture_id', how='left')



    for performance_df in ('itk_realise_performance_extanded', 'itk_synthetise_performance_extanded'):
        # création de la colonne de filtre sur les alertes
        df[performance_df]['filtre_alerte'] = True

        # on regarde si l'alerte est négative

        # si toutes les colonnes contiennent uniquement des "ALERTE_IS_NO_STRINGS" alors on considère que l'itk est en alerte.
        # cas classique
        df[performance_df].loc[
            (df[performance_df][ALERTE_COLUMNS].isin(ALERTE_IS_NO_STRINGS).all(axis=1)) |
            (df[performance_df][ALERTE_COLUMNS].isna().all(axis=1)) |
            ((df[performance_df]['alerte_cm_std_mil'].str.contains('<', na=False)) & ((df[performance_df]['typocan_culture'] == "Prairie temporaire") | (df[performance_df]['typocan_culture'] == "Prairie permanente"))),
            'filtre_alerte'
        ] = False
        


        # création de la colonne de filtre sur la filière
        df[performance_df]['filtre_filiere'] = ~df[performance_df]['filiere'].isin(FILIERES)


    res = pd.concat([
        df['itk_realise_performance_extanded'][['noeuds_realise_id', 'culture_id', 'filtre_filiere', 'filtre_alerte', 'sdc_id']],
        df['itk_synthetise_performance_extanded'][['connection_synthetise_id', 'filtre_filiere', 'filtre_alerte', 'sdc_id', 'synthetise_id']],
    ])

    res.to_csv('~/Bureau/utils/data/test_dirodur_itk_filtre.csv')

    return res[[
        'noeuds_realise_id', 'connection_synthetise_id', 'filtre_filiere', 'filtre_alerte', 'sdc_id', 'synthetise_id'
    ]]

def get_temporal_status_for_each_sdc_dirodur(donnees):
    """
    Cette fonction permet de définir l'état temporel de chaque sdc_id pour un même numéro DEPHY.
    D'abord on filtre les sdc grace à la fonction filtered_entities_sdc_level : on prend les df de réalisé et de synthétisé séparement 
    et on les filtre par la colonne 'in_dirodur'. On y merge quelques données provenant de la table sdc.
    On ajoute les infos des pz0 grâce à l'outil indentification pz0 (particularité: pour liés aux réalisés, on passe par la zone). 
    Sachant que cet outil filtre également sur les dispositif DEPHY DETAILLE, et sur les sdc avec au moins une intervention.
    On redéfini les label des pz0.
    Puis on cherche à détecter les point B : On regarde toutes les années d'un numéro dephy. On prend pour chaque numéro DEPHY, 
    les X années CONSECUTIVES les plus récentes (3 ou 2 selon la première séquence que l'on trouve, 
    avec une préférence pour les plus récente, et aussi pour une séquence de 3 années, dans cet ordre). 
    Cela nous donne les X années qui crée un point_B. On ne les cherches que parmis les sdc non-tagué pz0 !
    Si un sdc autre qu'un pz0 a une campagne (ou une année parmis la liste de campagne, pour les synthétisé) comprise dans 
    les X dernières années consécutives, elle est tagué 'point_B'.
    
    On tague ensuite en point_A tout les sdc avant les points B s'il n'y a pas de pz0. 
    S'il y a des points B et des pz0, on taguera ceux entre les deux comme point I.
    S'il y a des sdc arpès les points B, on les taguera comme point C (sdc non consécutifs).

    On crée aussi derie_temporel, qui indique si l'ensemble des sdc d'un numéro DEPHY contiennent un pz0 ou non, un points_B ou non.
    On fait une distinction entre les pz0 non présents et ceux qui ont été filtrés par la fonction util de filtration.
    Les point_I (intermédiaires) sont les sdc entre les pz0 et les point_B

    Entree de la fonction util de filtration:
        'synthetise',
        'sdc',
        'typologie_assol_can_realise',
        'typologie_can_rotation_synthetise',
        'entite_unique_par_sdc_nettoyage',
        'sdc_realise_performance',
        'synthetise_synthetise_performance',
        'intervention_synthetise_agrege',
        'intervention_realise_agrege'
        ==> Utilise les outils indicateurs, nettoyages et agregations !
    Entree de la fonction d'état temporel:
        'synthetise',
        'sdc',
        'identification_pz0',
        'zone',
        'parcelle'
        ==> Utilise un outil d'indicateur !

    Retourne:
        Dataframe avec les colonnes suivantes :
        ['sdc_id', 'sdc_code', 'code_dephy', 'campagne', 'synthetise_id', 'campagnes', 'etat_temporel']
        Le sdc_id étant l'identifiant de base et l'etat_temporel la colonne importante
    """

    # On importe les données
    sdc = donnees['sdc'][['id','code','campagne','modalite_suivi_dephy','code_dephy','type_agriculture']].rename(columns={'id':'sdc_id','code':'sdc_code'})
    synthetise = donnees['synthetise'][['id','campagnes','sdc_id']].rename(columns={'id':'synthetise_id'})
    zone = donnees['zone'][['id','parcelle_id']].rename(columns={'id':'entite_id'})
    parcelle = donnees['parcelle'][['id','sdc_id']].rename(columns={'id':'parcelle_id'})
    outil_pz0 = donnees['identification_pz0']

    # On importe la fonction de filtration des dataframe SDC en réal et en synth
    sdc_realise_filt, synthetises_filt = filtered_entities_sdc_level(donnees)

    # On crée les df, et on les filtre pour qu'ils soient dans dirodur
    df_R = sdc_realise_filt.loc[sdc_realise_filt['in_dirodur']]\
    .merge(sdc, on='sdc_id', how='left')\
        .drop(columns=['in_dirodur'])

    df_S = synthetises_filt.loc[synthetises_filt['in_dirodur']]\
        .merge(synthetise, on='synthetise_id', how='left')\
            .merge(outil_pz0.rename(columns={'entite_id':'synthetise_id'}), on='synthetise_id', how='left')\
                .merge(sdc, on='sdc_id', how='left')\
                    .drop(columns=['in_dirodur'])

    # L'outil d'identification des pz0 a la particularité d'etre au niveau de la zone, on fait en sorte d'avoir les infos niveau SDC
    def list_to_scalar(serie):
        unique_values = list(serie.dropna().unique())
        if len(unique_values) == 0:
            return None
        if len(unique_values) == 1:
            return unique_values[0]
        return unique_values
        
    zones_w_pz0 = zone.merge(parcelle, on='parcelle_id', how='left').merge(outil_pz0, on='entite_id', how='left')
    zones_w_pz0 = zones_w_pz0.groupby('sdc_id')['pz0'].apply(list_to_scalar, include_groups=False).reset_index()

    if len(zones_w_pz0.loc[zones_w_pz0['pz0'].apply(lambda x: isinstance(x, list))] ) > 0 :
        raise ValueError("Il y a des sdc réalisé avec plusieurs identification différentes selon leur zones")

    df_R = df_R.merge(zones_w_pz0, on='sdc_id', how='left')

    # On crée le df principal en concaténant réalisé et synthétisé
    df_R['pz0'] = np.where(df_R['modalite_suivi_dephy']=='DETAILLE',
                        df_R['pz0'], 
                        np.where(df_R['modalite_suivi_dephy'].isna(),'non_DEPHY', 'non_suivi'))
    df_S['pz0'] = np.where(df_S['modalite_suivi_dephy']=='DETAILLE',
                        df_S['pz0'], 
                        np.where(df_S['modalite_suivi_dephy'].isna(),'non_DEPHY', 'non_suivi'))
    df = pd.concat([
        df_S[['sdc_id', 'sdc_code', 'code_dephy', 'type_agriculture', 'campagne', 'pz0', 'synthetise_id', 'campagnes']],
        df_R[['sdc_id', 'sdc_code', 'code_dephy', 'type_agriculture', 'campagne', 'pz0']]
        ])

    df.pz0 = df.pz0.fillna('non_DEPHY') # ceux dont la modalité de suivi est NA

    # On modifie les modalités incorrectes de pz0 pour qu'elles soient regroupées sous la modalité 'post'. Seulement pour celles qui ne détecte pas de pz0 fiable.
    df['pz0'] = np.where(df['pz0'].isin([
        'incorrect : saisie pz0 non acceptable',
        'incorrect : aucun pz0 saisi',
        'incorrect : chevauchement pz0',
        'incorrect : saisie de plusieurs pz0']), 'post', df['pz0'])
    # Les modalités incorrects de camapgne non attendue ou de code dephy inconnue sont enlevé car même les points_B peuvent être faux. Par exemple le cas de GCF10181 qui a des points_B avant les pz0 si on laisse passer ces incorrects !
    df = df.loc[~df['pz0'].isin([
        "incorrect : campagne non-attendue",
        "incorrect : code dephy inconnu"
    ])]



    ### CREATION DES FONCTIONS PERMETTANT L'IDENTIFICATION DES ETATS TEMPORELS ###
    
    # On crée les fonction permettant l'identification des etats temporels
    def extract_years(row):
        """ Extrait les années sous forme de liste d'int de la colonne campagnes pour les synthétisés et de la colonne campagne pour les réalisés """
        years = set()
        if pd.notna(row['campagne']):
            years.add(int(row['campagne']))
        if pd.notna(row['campagnes']):
            years.update(int(y) for y in row['campagnes'].split(', '))
        return sorted(years)

    def label_pz0_status(df):
        """ 
        On modifie un peu les label de l'outil d'identification des pz0 pour crée le début de 'état_temporel'. 
        Typiquement on check s'il y a bien au moins 2 pz0 tagué pour un numéro DEPHY, si ce n'est pas le cas on regarde si ils ont été filtré par la fonction util ou si l'outil était déjà sans pz0 pour ce code DEPHY.
        """
        df_pz0 = df[df['pz0'] == 'pz0'].copy()
        df_pz0

        df_pz0['all_years'] = df_pz0.apply(extract_years, axis=1)
        grouped = df_pz0.groupby('code_dephy')['all_years'].agg(lambda x: set().union(*x))
        valid_groups = grouped[grouped.apply(len) >= 2].index.tolist()
        not_incorrect_cd = df.loc[df['pz0'].isin(['pz0','post']),'code_dephy'].tolist()

        df['serie_tempo'] = df.apply(
            lambda row:
                'sans_pz0' if row['code_dephy'] not in not_incorrect_cd and row['code_dephy'] not in valid_groups
                else 'pz0_filtres' if row['code_dephy'] in not_incorrect_cd and row['code_dephy'] not in valid_groups
                else 'pz0' if row['pz0'] == 'pz0' and row['code_dephy'] in valid_groups
                else row['pz0'],
            axis=1
        )

        return df

    def find_last_n_year(years, n):
        """ recheche la dernière séquence des n années les plus récentes et consécutives"""
        for i in range(len(years) - n, -1, -1):
            window = years[i:i+n]
            if all(window[j+1] - window[j] == 1 for j in range(len(window)-1)):
                return window
        return None
        
    def find_last_consecutive_year_sequence(years):
        """ 
        Utilise find_last_n_year() pour repéré les séquences les plus récentes de n années consécutives. 
        Puis fait le choix entre la séquence de 3 années et de 2 année. On privilégie les séquences les plus récentes, 
        puis les séquences les plus grande (3 > 2) 
        """

        if not years:
            return []

        last_3 = find_last_n_year(years, 3) if len(years) >= 3 else None
        last_2 = find_last_n_year(years, 2) if len(years) >= 2 else None

        if last_3 and last_2:
            return last_3 if last_3[-1] >= last_2[-1] else last_2
        return last_3 or last_2 or []

    def update_final_status_for_code_dephy_without_point_B(df, codes_with_consecutive):
        """ 
        Dernière fonction a être appelé. 
        Permet de check s'il y a des points_B parmi chaque code DEPHY. 
        Si ce n'est pas le cas, ajoute un message d'erreur qui correspond au cas. 
        """

        for code in list(df['code_dephy'].unique()):
            if code not in codes_with_consecutive:
                mask = df['code_dephy'] == code
                if (df.loc[mask, 'serie_tempo'] == 'sans_pz0').any():
                    df.loc[mask, 'serie_tempo'] = 'ni_pz0_ni_point_B'
                elif (df.loc[mask, 'serie_tempo'] == 'pz0_filtres').any():
                    df.loc[mask, 'serie_tempo'] = 'pz0_filtres_et_sans_point_B'
                else:
                    df.loc[mask, 'serie_tempo'] = 'sans_point_B'

        return df

    def get_last_consecutive_years(df):
        """ 
        fonction principale qui va extraire pour chaque code DEPHY la séquence des dernières années consécutive parmis un df sans les pz0. 
        Puis va checker dans le df (tout compris cette fois) chaque sdc : s'il est un pz0 ou qu'il fait parti des code dephy sans pz0, 
        on ne modifie pas la ligne et on garde en mémoire que le code DEPHY pourrait contenir des points_B mais n'a pas de pz0 ; 
        s'il est autre chose (post ou incorrect uniquement pour le sdc associé) on va chercher la ou les campagnes du sdc, 
        si au moins une est présente dans la liste des années retenues pour être des point_B on modifie l'état temporel en 'point_B'. 
        Si une ligne a une année supérieur à l'année maximal du point B, on la tague 'point_C' Enfin on utilise la fonction 
        update_final_status_for_code_dephy_without_point_B(). 
        """

        df_non_pz0 = df[df['etat_temporel'] != 'pz0'].copy()
        df_non_pz0['all_years'] = df_non_pz0.apply(extract_years, axis=1)
        grouped = df_non_pz0.groupby('code_dephy')['all_years'].agg(lambda x: sorted(set().union(*x)))
        consecutive_years = grouped.apply(find_last_consecutive_year_sequence)

        df = df.set_index('sdc_id')
        df['all_years'] = df.apply(extract_years, axis=1)
        codes_with_consecutive = set()
        for code, years in consecutive_years.items():
            if years:
                codes_with_consecutive.add(code) # garde en mémoire les code ok pour le update final
                mask = (df['code_dephy'] == code) & \
                        (~df['etat_temporel'].isin(
                            ['pz0',
                            'incorrect : campagne non-attendue',
                            'incorrect : code dephy inconnu', 
                            'non_DEPHY', 
                            'non_suivi']
                            ))
                for idx, row in df[mask].iterrows():
                    if any(y in years for y in row['all_years']):
                        df.loc[idx, 'etat_temporel'] = 'point_B'
                    elif all(y > max(years) for y in row['all_years']):
                        df.loc[idx, 'etat_temporel'] = 'point_C'
        df = df.reset_index()

        df = update_final_status_for_code_dephy_without_point_B(df, codes_with_consecutive)
        return df

    def add_etat_temporel_column(df):
        """ Dernière fonction qui wrap le tout et crée les point_I intermédiaire, et met en forme le df final (drop et sort). """

        # On rajoute une regle avant tout : si le type_agriculture est différent au seins du pz0, on supprime le pz0 !
        # on entend par différent AB != AConv. Information obligatoire et En conversion ne sont pas considéré comme différent de l'un ou de l'autre.
        type_agri_pz0 = (
            df[df["pz0"] == "pz0"].groupby(["code_dephy"])["type_agriculture"]
            .apply(lambda x: {"Agriculture conventionnelle", "Agriculture biologique"}.issubset(set(x.dropna())))
        )
        print(f"Il y a {len(type_agri_pz0.unique())} numéros DEPHY qui ont des entités pz0 ayant des types d'agricultures différentes (AB vs AConv, les autres types n'étant ni considérés comme l'un ni comme l'autre)")
        df = df[
            ~((df["pz0"] == "pz0") & (df["code_dephy"].isin(type_agri_pz0)))
        ]

        df['serie_tempo'] = pd.NA
        df['etat_temporel'] = df['pz0']

        df = label_pz0_status(df)
        df = get_last_consecutive_years(df)

        code_pz0 = df.loc[df["etat_temporel"] == "pz0", "code_dephy"]
        code_pb = df.loc[df["etat_temporel"] == "point_B", "code_dephy"]
        codes_complete_serie = df.loc[(df["code_dephy"].isin(code_pz0)) & (df["code_dephy"].isin(code_pb)), "code_dephy"]
        df.loc[(df["code_dephy"].isin(codes_complete_serie)) & (df['etat_temporel'] == 'post'), "etat_temporel"] = "point_I"
        df.loc[(~df["code_dephy"].isin(codes_complete_serie)) & (df['etat_temporel'] == 'post'), "etat_temporel"] = "point_A"


        df['etat_temporel'] = np.where(df['etat_temporel'] == 'post', 'point_I', df['etat_temporel'])
        df['serie_tempo'] = np.where(df['serie_tempo'].isin(['post','pz0']), 'serie_complete', df['serie_tempo'])


        df.drop(columns=['pz0','all_years'], inplace=True)

        return df.sort_values(['code_dephy','campagne'])

    
    return add_etat_temporel_column(df)