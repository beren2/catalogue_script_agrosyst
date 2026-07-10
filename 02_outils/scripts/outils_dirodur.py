"""
	Regroupe les fonctions permettant de générer les outils utiles lors de la génération du magasin "DiRoDur".
"""
from datetime import datetime, timedelta
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

    return res[[
        'noeuds_realise_id', 'connection_synthetise_id', 'filtre_filiere', 'filtre_alerte', 'sdc_id', 'synthetise_id'
    ]]

def get_temporal_status_for_each_sdc_dirodur(donnees):
    """
    Cette fonction permet de définir l'état temporel de chaque sdc_id pour un même numéro DEPHY.
    D'abord on filtre les sdc grace à la fonction filtered_entities_sdc_level : on prend les df de réalisé et de synthétisé séparement et on les filtre par la colonne 'in_dirodur'. On y merge quelques données provenant de la table sdc.
    On ajoute les infos des pz0 grâce à l'outil indentification pz0 (particularité: pour liés aux réalisés, on passe par la zone). Sachant que cet outil filtre également sur les dispositif DEPY DETAILLE, et sur les sdc avec au moins une intervention.
    On redéfini les label des pz0.
    Puis on cherche à détecter les point B : 
    on regarde toutes les années d'un numéro dephy. On prend pour chaque numéro DEPHY, les X années CONSECUTIVES les plus récentes (3 ou 2 selon la première séquence que l'on trouve, avec une préférence pour les plus récente, et aussi pour une séquence de 3 années, dans cet ordre). Cela nous donne les X années qui crée un point_B. On ne les cherches que parmis les sdc non-tagué pz0 !
    Si un sdc autre qu'un pz0 a une campagne (ou une année parmis la liste de campagne, pour les synthétisé) comprise dans les X dernières années consécutives, elle est tagué 'point_B'.
    On tague en erreur tous les sdc d'un même numéro DEPHY si celui ci ne comporte pas de pz0 et/ou pas de point_B. On fait une distinction entre les pz0 non présents et ceux qui ont été filtrés par la fonction util de filtration.
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
    sdc = donnees['sdc'][['id','code','campagne','modalite_suivi_dephy','code_dephy']].rename(columns={'id':'sdc_id','code':'sdc_code'})
    synthetise = donnees['synthetise'][['id','campagnes','sdc_id']].rename(columns={'id':'synthetise_id'})
    zone = donnees['zone'][['id','parcelle_id']].rename(columns={'id':'entite_id'})
    parcelle = donnees['parcelle'][['id','sdc_id']].rename(columns={'id':'parcelle_id'})
    pta = donnees['identification_pz0']

    # On importe la fonction de filtration des dataframe SDC en réal et en synth
    sdc_realise_filt, synthetises_filt = filtered_entities_sdc_level(donnees)

    # On crée les df, et on les filtre pour qu'ils soient dans dirodur
    df_R = sdc_realise_filt.loc[sdc_realise_filt['in_dirodur']]\
    .merge(sdc, on='sdc_id', how='left')\
        .drop(columns=['in_dirodur'])

    df_S = synthetises_filt.loc[synthetises_filt['in_dirodur']]\
        .merge(synthetise, on='synthetise_id', how='left')\
            .merge(pta.rename(columns={'entite_id':'synthetise_id'}), on='synthetise_id', how='left')\
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
        
    zones_w_pz0 = zone.merge(parcelle, on='parcelle_id', how='left').merge(pta, on='entite_id', how='left')
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
        df_S[['sdc_id', 'sdc_code', 'code_dephy', 'campagne', 'pz0', 'synthetise_id', 'campagnes']],
        df_R[['sdc_id', 'sdc_code', 'code_dephy', 'campagne', 'pz0']]
        ])
    
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
        """ on modifie un peu les label de l'outil d'identification des pz0 pour crée le début de 'état_temporel'. Typiquement on check s'il y a bien au moins 2 pz0 tagué pour un numéro DEPHY, si ce n'est pas le cas on regarde si ils ont été filtré par la fonction util ou si l'outil était déjà sans pz0 pour ce code DEPHY. """
        df_pz0 = df[df['pz0'] == 'pz0'].copy()
        df_pz0['all_years'] = df_pz0.apply(extract_years, axis=1)
        grouped = df_pz0.groupby('code_dephy')['all_years'].agg(lambda x: set().union(*x))
        valid_groups = grouped[grouped.apply(len) >= 2].index.tolist()
        cd_with_pz0_at_the_begging = df.loc[df['pz0'].isin(['pz0','post']),'code_dephy'].tolist()

        df['etat_temporel'] = df.apply(
            lambda row:
                'sans_pz0' if row['code_dephy'] not in cd_with_pz0_at_the_begging and row['code_dephy'] not in valid_groups
                else 'pz0_filtres' if row['code_dephy'] in cd_with_pz0_at_the_begging and row['code_dephy'] not in valid_groups
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
        """ utilise find_last_n_year() pour repéré les séquences les plus récentes de n années consécutives. Puis fait le choix entre la séquence de 3 années et de 2 année. On privilégie les séquences les plus récentes, puis les séquences les plus grande (3 > 2) """
        if not years:
            return []

        last_3 = find_last_n_year(years, 3) if len(years) >= 3 else None
        last_2 = find_last_n_year(years, 2) if len(years) >= 2 else None

        if last_3 and last_2:
            return last_3 if last_3[-1] >= last_2[-1] else last_2
        return last_3 or last_2 or []

    def update_final_status_for_code_dephy_without_point_B(df, codes_with_consecutive):
        """ Dernière fonction a être appelé. Permet de check s'il y a des points_B parmi chaque code DEPHY. Si ce n'est pas le cas, ajoute un message d'erreur qui correspond au cas. """
        for code in list(df['code_dephy'].unique()):
            if code not in codes_with_consecutive:
                mask = df['code_dephy'] == code
                if (df.loc[mask, 'etat_temporel'] == 'sans_pz0').any():
                    df.loc[mask, 'etat_temporel'] = 'ni_pz0_ni_point_B'
                elif (df.loc[mask, 'etat_temporel'] == 'pz0_filtres').any():
                    df.loc[mask, 'etat_temporel'] = 'pz0_filtres_et_sans_point_B'
                else:
                    df.loc[mask, 'etat_temporel'] = 'sans_point_B'

        return df

    def get_last_consecutive_years(df):
        """ fonction principale qui va extraire pour chaque code DEPHY la séquence des dernières années consécutive parmis un df sans les pz0. Puis va checker dans le df (tout compris cette fois) chaque sdc : s'il est un pz0 ou qu'il fait parti des code dephy sans pz0, on ne modifie pas la ligne et on garde en mémoire que le code DEPHY pourrait contenir des points_B mais n'a pas de pz0 ; s'il est autre chose (post ou incorrect uniquement pour le sdc associé) on va chercher la ou les campagnes du sdc, si au moins une est présente dans la liste des années retenues pour être des point_B on modifie l'état temporel en 'point_B'. Si une ligne a une année supérieur à l'année maximal du point B, on la tague 'point_C' Enfin on utilise la fonction update_final_status_for_code_dephy_without_point_B(). """
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
                        ~(df['etat_temporel'].isin(['sans_pz0','pz0_filtres','pz0']))
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
        df = label_pz0_status(df)
        df = get_last_consecutive_years(df)
        df['etat_temporel'] = np.where(df['etat_temporel'] == 'post', 'point_I', df['etat_temporel'])
        df.drop(columns=['pz0','all_years'], inplace=True)
        return df.sort_values(['code_dephy','campagne'])
    
    return add_etat_temporel_column(df)


def get_date_de_semis_outils_dirodur(donnees):
    """
    Donne, à partir des dates d'interventions, les saisons de semis pour chaque cultures (seulement pour les cultures GCPE).
    Calcule d'abord une date moyenne de semis par culture à partir des interventions date_din et date_début 
    des interventions de semis en réalisées et synthétisées.
    Puis calcul une date de semis moyenne des dates de semis moyennnes par culture.
    On fait bien attention de prendre en compte le passage au nouvel an pour les date en synthétisé (format jj/mm). 
    En réalisé plus simple : (format aaaa-mm-jj).
    Enfin on applique une saison en fonction de cette date !

    Dépendance : 
        - outils.restructuration
    Besoin de ces tables en entrée : 
        'intervention_synthetise',
        'intervention_realise',
        'noeuds_realise',
        'noeuds_synthetise',
        'noeuds_synthetise_restructure',
        'connection_synthetise',
        'zone',
        'parcelle',
        'synthetise',
        'sdc'
    """
    # Chargement des tables utiles nottament les interventions
    intv_S = donnees['intervention_synthetise'][['id','type','date_debut','date_fin','concerne_ci','connection_synthetise_id']].copy()
    intv_R = donnees['intervention_realise'][['id','type','date_debut','date_fin','concerne_ci','noeuds_realise_id']].copy()
    conx_S = donnees['connection_synthetise'][['id','cible_noeuds_synthetise_id']].rename(columns={'id':'connection_synthetise_id', 'cible_noeuds_synthetise_id':'noeuds_synthetise_id'}).copy()
    noeud_w_culture_id_S = donnees['noeuds_synthetise_restructure'][['id','culture_id']].rename(columns={'id':'noeuds_synthetise_id'}).copy()
    noeuds_w_culture_id_R = donnees['noeuds_realise'][['id','culture_id','zone_id']].rename(columns={'id':'noeuds_realise_id'}).copy()

    node_S = donnees['noeuds_synthetise'][['id','synthetise_id']].rename(columns={'id':'noeuds_synthetise_id'}).copy()
    synthe = donnees['synthetise'][['id','sdc_id']].rename(columns={'id':'synthetise_id'}).copy()
    zone = donnees['zone'][['id','parcelle_id']].rename(columns={'id':'zone_id'}).copy()
    parcelle = donnees['parcelle'][['id','sdc_id']].rename(columns={'id':'parcelle_id'}).copy()
    sdc = donnees['sdc'][['id','filiere']].rename(columns={'id':'sdc_id'}).copy()

    # Filtre sur les interventions de semis hors CI
    intv_S = intv_S.loc[(intv_S['type'] == 'SEMIS') & 
                        (intv_S['connection_synthetise_id'].notna()) & 
                        (intv_S['concerne_ci'] == 'f')]
    intv_R = intv_R.loc[(intv_R['type'] == 'SEMIS') & 
                        (intv_R['noeuds_realise_id'].notna()) & 
                        (intv_R['concerne_ci'] == 'f')]

    # Rattachement des cultures
    intv_S = intv_S.merge(conx_S, on='connection_synthetise_id', how='left')
    intv_S = intv_S.merge(noeud_w_culture_id_S, on='noeuds_synthetise_id', how='left')
    intv_R = intv_R.merge(noeuds_w_culture_id_R, on='noeuds_realise_id', how='left')


    def moyenne_dates(start_series, end_series, methode = 'R'):
        """ 
        Calcule la date moyenne entre date_debut et date_fin.
        """

        def parse_S_date(s):
            """ 
            Créer une date au format date. 
            Affecter une année pour avoir une vrai date. 
            On corrige le jour dans le cas des années bissextile et des erreurs de saisie 
            """
            j, m = map(int, s.split('/'))
            try :
                return datetime(2025, m, j)
            except ValueError:
                try : 
                    return datetime(2025, m, j-1)
                except ValueError:
                    return datetime(2025, m, j-2)
                
        def parse_R_date(s):
            """ 
            Créer une date au format date. 
            """
            y, m, j = map(int, s.split('-'))
            return datetime(y, m, j)
        
        # Cas ou les dates de fin sont antérieures aux dates de début
        if methode == 'S':
            start_dates = start_series.apply(parse_S_date)
            end_dates = end_series.apply(parse_S_date)

            mask = end_dates < start_dates
            end_dates.loc[mask] = end_dates.loc[mask].apply(lambda x: datetime(2026, x.month, x.day))

        elif methode == 'R':
            start_dates = start_series.apply(parse_R_date)
            end_dates = end_series.apply(parse_R_date)

        # Moyenne
        moyennes = start_dates + ((end_dates - start_dates) / 2)

        # Retourne la date au format jj/mm
        return moyennes.dt.strftime('%d/%m')

    # Date de semis moyenne par intervention
    intv_R['date_semis'] = moyenne_dates(intv_R['date_debut'], intv_R['date_fin'], methode='R')
    intv_S['date_semis'] = moyenne_dates(intv_S['date_debut'], intv_S['date_fin'], methode='S')

    # Fusion des données réalisées et synthétisées
    intv = pd.concat([intv_S, intv_R], ignore_index=True)

    # Rattachement au SDC puis filtrage sur GCPE
    intv = intv.merge(node_S, on='noeuds_synthetise_id',how='left')
    intv = intv.merge(synthe, on='synthetise_id',how='left')
    intv = intv.merge(zone, on='zone_id',how='left')
    intv = intv.merge(parcelle, on='parcelle_id',how='left')
    intv['sdc_id'] = np.where(intv['sdc_id_x'].notna(), intv['sdc_id_x'], intv['sdc_id_y'])
    intv = intv[['id','culture_id','date_semis','sdc_id']]
    intv = intv.merge(sdc, on='sdc_id',how='left')
    intv = intv.loc[intv['filiere'].isin(['POLYCULTURE_ELEVAGE','GRANDES_CULTURES'])]

    # Conversion en jour de l'année pour calcul circulaire
    # PS : Ajouter une année bissextile (2020) pour parser les dates
    intv['_dayofyear'] = pd.to_datetime(
        intv['date_semis'].astype(str) + '/2020',
        format='%d/%m/%Y'
    ).dt.dayofyear

    def circular_mean_date(group):
        """
        Moyenne de dates moyennes en tenant compte du passage au nouvel an (ex: 30/12, 01/01, 02/01 => date moyenne = 01/01).
        """

        days = group['_dayofyear'].values
        if len(set(days)) == 1:
            return pd.Series({
                'dates_nbjr_triees': days.tolist(),
                'date_moyenne': group['date_semis'].iloc[0]
            })

        # Trouve l'écart maximal entre 2 dates consécutives (en boucle)
        sorted_days = np.sort(days)
        diffs = np.diff(np.r_[sorted_days, sorted_days[0] + 366])  # +366 pour gérer 29/02
        cut = np.argmax(diffs)+1
        # Réordonne en partant après la coupure
        order = np.roll(sorted_days, -cut)

        # Retourne la date moyenne
        asc_list = [y + order[0] if y < order[0] else y for y in order]
        moy = np.mean(asc_list)
        if moy > 366:
            moy -= 366
        date_moy = datetime(2020, 1, 1) + timedelta(days=moy-1)
        date_moy = date_moy.strftime('%d/%m') 

        return pd.Series({
            'dates_nbjr_triees': order.tolist(),
            'date_moyenne': date_moy
        })
    
    # Applique la fonction circular_mean_date et retourner l'objet
    # result = intv.groupby('culture_id', group_keys = True).apply(circular_mean_date, include_groups=False)
    result = intv.groupby('culture_id').apply(circular_mean_date, include_groups=False)

    def transforme_date_en_saison(date_str):
        """ 
        A partir d'une date au format jj/mm, retourne la saison de semis correspondante.
        """
        if pd.isna(date_str):
                return None
        j, m = map(int, date_str.split('/'))
        date = datetime(2024, m, j)
        if datetime(2024, 1, 16) <= date <= datetime(2024, 4, 15):
            return 'printemps'
        elif datetime(2024, 4, 16) <= date <= datetime(2024, 6, 15):
            return 'ete'
        elif datetime(2024, 6, 16) <= date <= datetime(2024, 9, 15):
            return 'automne'
        else:
            return 'hiver'

    result['saison_semis_detect_via_intv'] = result['date_moyenne'].apply(transforme_date_en_saison)

    result = result.reset_index()
    result['dates_nbjr_triees'] = result['dates_nbjr_triees'].apply(str)

    return result[['culture_id', 'dates_nbjr_triees', 'date_moyenne', 'saison_semis_detect_via_intv']]



def get_typologie_culture_outils_dirodur(donnees):
    """
    Besoin de :
        - La matrice de typologie DIRODUR dans les data externes
        - la tables créé par la fonction get_date_de_semis_outils_dirodur() pour récupérer la saison de semis des cultures ==> elle est dans la même catégorie d'outils DIRODUR, suffit de positionner cette fonction avant celle ci dans le code.
        - la table typologie_can_culturecréer par les outils de typologie can culture pour récupérer la variable porte-graine

    Retourne la typologie des cultures selon les critères DIRODUR.
    On utilise la matrice de typologie DIRODUR pour derterminer la typologie de chaque culture en fonction des espèces qui la composent (donc des combinaison de typologies d'espèces). 
    De plus on a des valeurs supplémentaire comme le nombre d'espèce, de famille bota provenant de la combinaison des composants de culture.
    Et des valeurs supplémentaires comme si la culture contient des cultures compagnes, et si la culture est annuelle ou non, ... provenant de la matrice de correspodance entre les typologies d'espèces et de culture.
    Et la variable porte-graine provenant de l'outil de typologie can culture.

    Point à savoir : parfois dans la matrice dirodur la colonne typodirodur_espece_periode_semis est vide, ce qui veut dire que la saison de semis n'est pas déterminante pour la typologie de culture. Dans le cas contraire, elle l'est, on va donc chercher à savoir si la saison de semis est disponible dans le référentiel espece, sinon on va récupérer l'info grace à l'outil get_date_de_semis_outils_dirodur() qui calcule la saison de semis à partir des dates d'interventions. On merge ensuite avec la matrice pour récupérer le typodirodur_culture correspondant, en fonction des typologies d'espece MAIS AUSSI de la saison de semis.
    Pour les autres culture dont la saison de semis n'est pas déterminante, on merge directement avec la matrice pour récupérer le typodirodur_culture correspondant, en fonction des typologies d'espece.
    """
    
    cropsp = donnees['composant_culture'][['id','espece_id','culture_id','compagne']].rename(columns={'id':'composant_culture_id'}).copy()
    crop = donnees['culture'][['id','nom','type']].rename(columns={'id':'culture_id'}).copy()
    sp = donnees['espece'][['id','typodirodur_espece','typodirodur_espece_precise','typodirodur_espece_famille_bota','typodirodur_espece_periode_semis']].rename(columns={'id':'espece_id'}).copy()
    matrice = donnees['matrice_typologie_culture_dirodur'][['typodirodur_espece', 'typodirodur_culture', 'culture_est_avec_compagne', 'culture_est_annuelle_asso', 'culture_est_prairie', 'besoin_saison']].copy()
    date_semis = donnees['date_de_semis_outils_dirodur'][['culture_id','saison_semis_detect_via_intv']].copy()
    typocan = donnees['typologie_can_culture'][['culture_id','typo_cpg']].copy()

    df = cropsp.merge(sp, how = 'left', on = 'espece_id')

    df['nb_composant_culture'] = 1
    df['nb_typodirodur_espece'] = df['typodirodur_espece'].copy()
    df['nb_typodirodur_espece_precise'] = df['typodirodur_espece_precise'].copy()
    df['nb_typodirodur_espece_famille_bota'] = df['typodirodur_espece_famille_bota'].copy()

    def concat_unique_sorted(series):
        cleaned = series.dropna().unique()
        if len(cleaned) == 0:
            return np.nan
        return '_'.join(sorted(cleaned))

    def get_nb_unique_typo(series):
        cleaned = series.dropna().unique()
        return len(cleaned)

    agg_dict = {
        'nb_composant_culture': 'sum',
        'typodirodur_espece': concat_unique_sorted,
        'typodirodur_espece_precise': concat_unique_sorted,
        'typodirodur_espece_famille_bota': concat_unique_sorted,
        'typodirodur_espece_periode_semis': concat_unique_sorted,
        'nb_typodirodur_espece': get_nb_unique_typo,
        'nb_typodirodur_espece_precise': get_nb_unique_typo,
        'nb_typodirodur_espece_famille_bota': get_nb_unique_typo,
    }

    #  On crée les typologie can culture et les autre variable utiles grace a agg_dict
    df = df[['culture_id',
            'nb_composant_culture',
            'typodirodur_espece',
            'typodirodur_espece_precise',
            'typodirodur_espece_famille_bota',
            'typodirodur_espece_periode_semis',
            'nb_typodirodur_espece',
            'nb_typodirodur_espece_precise',
            'nb_typodirodur_espece_famille_bota']].groupby('culture_id').agg(agg_dict).reset_index()

    # On ajoute les type des culture_id
    # On fait un outer pour avoir toutes les cultures meme celles qui n'ont pas de composant_culture
    df = df.merge(crop[['culture_id','nom','type']], how='outer', on='culture_id')

    df.loc[df['nb_composant_culture'].isna(),['nb_composant_culture','nb_typodirodur_espece','nb_typodirodur_espece_precise','nb_typodirodur_espece_famille_bota']] = 0

    # Les culture dont la colonne besoin_saison est vide sont les cultures dont la saion ne défnini pas la typologie de culture.
    # 1. On récupère les date de semis réel (vu via l'intervention) au cas où nous avons besoin de la saison et qu'elle ne soit pas dispo dans le referentiel espece
    df = df.merge(date_semis, how='left', on='culture_id')
    df['typodirodur_espece_periode_semis'] = df['typodirodur_espece_periode_semis'].fillna(df['saison_semis_detect_via_intv'])
    df.drop(columns='saison_semis_detect_via_intv', inplace=True)

    # 2. On regarde les cultures qui ont un besoin de saison pour faire le merge avec la matrice
    # Pour le savoir on regarde si la matrice a une valeur non nulle dans la colonne typodirodur_espece_periode_semis. Si c'est le cas, on merge avec la matrice pour récupérer le typodirodur_culture correspondant.
    # Dans le cas ou l'on a besoin de savoir la saison mais que la saison n'est pas renseigné dans le referentiel espece, on prend la saison détecté via les interventions.
    matrice_saison_needed = matrice.loc[matrice['besoin_saison'].notna()]
    typo_espece_en_pluriannuelle = matrice_saison_needed.loc[matrice_saison_needed['besoin_saison'] == 'pluriannuelle', 'typodirodur_espece'].to_list()

    df_saison_needed = df.copy()
    df_saison_needed['typodirodur_espece_periode_semis'] = np.where(
        (df_saison_needed['typodirodur_espece'].isin(typo_espece_en_pluriannuelle)) & (df_saison_needed['typodirodur_espece_periode_semis'].str.contains('pluriannuelle')),
        'pluriannuelle', 
        df_saison_needed['typodirodur_espece_periode_semis'])
    matrice_saison_needed.rename(columns={'besoin_saison' : 'typodirodur_espece_periode_semis'}, inplace=True)
    df_saison_needed = df_saison_needed.merge(matrice_saison_needed, how='inner', on=['typodirodur_espece', 'typodirodur_espece_periode_semis'])
    df_saison_needed = df_saison_needed.loc[df_saison_needed['typodirodur_culture'].notna()]

    # 3. On regarde les cultures qui n'ont pas de besoin de saison pour faire le merge avec la matrice
    # Ce sont donc les culture_id qui ne sont pas dans df_saison_needed. On les merge avec la matrice pour récupérer le typodirodur_culture correspondant.
    df_no_saison_needed = df.copy()
    df_no_saison_needed = df_no_saison_needed.loc[~df_no_saison_needed['culture_id'].isin(df_saison_needed['culture_id'])]
    df_no_saison_needed = df_no_saison_needed.merge(matrice.loc[matrice['besoin_saison'].isna()], how='left', on=['typodirodur_espece'])
    df_no_saison_needed = df_no_saison_needed.loc[df_no_saison_needed['typodirodur_culture'].notna()]
    df_no_saison_needed.drop(columns = 'besoin_saison', inplace = True)

    # 4. On concat les deux df pour avoir le df final
    df = pd.concat([df_no_saison_needed, df_saison_needed], ignore_index=True)

    # On ajoute les culture porte-graines
    df = df.merge(typocan, how='left', on='culture_id')

    df['type'] = df['type'].astype('category')
        
    df['type'] = df['type'].cat.rename_categories({'MAIN': 'principale', 
                                                    'INTERMEDIATE': 'intermediaire', 
                                                    'CATCH': 'derobee' })
    df['type'] = df['type'].astype('str')

    df[['nb_typodirodur_espece','nb_composant_culture','nb_typodirodur_espece_precise','nb_typodirodur_espece_famille_bota']] = df[['nb_typodirodur_espece','nb_composant_culture','nb_typodirodur_espece_precise','nb_typodirodur_espece_famille_bota']].astype('int64')
    
    return df


def get_poids_noeuds_realise_outils_dirodur(donnees):
    """
    Obtient les poids de chaque itk au seins de son sdc_id. 
    On prend tout les noeud realisé, donc meme ceux au seins d'un sdc_id qui contiennent également des synthétisés. Par contre, le pourcentage n'est calculé que par rapport aux zones en réalisé, le synthétisé n'ont aucun impacte sur les poids ici !
    Mais vu qu'on merge en left sur les noeuds realisé cela veut aussi dire qu'on prend toutes les zones contennant au moins un itk, donc au moins une culture !
    On crée 3 poids différents :

    - poids_surface_ponderee : si X itk sont conduit sur la meme zone durant une année, la surface affecté à chacune est la surface de la zone divisé par X. Et cela divisé par la surface totale du sdc_id qui est la somme des surface de chaque zone (compté chacune 1 seule fois !)

    - poids_surface_developpee_agreg : si X itk sont conduit sur la meme zone durant une année, la surface affecté à chacune est la surface de la zone. Cela fait qu'on développe X fois la surface. Et cela divisé par la surface totale des zones du sdc_id qui est la somme des surface de chaque zone (compté chacune 1 seule fois !). Donc si on prends X fois la surface en numérateur mais que la surface de la zone n'est décompté qu'1 seule fois en dénominateur ==> les valeurs PEUVENT dépasser 100% !

    - poids_surface_developpee_normalisee : si X itk sont conduit sur la meme zone durant une année, la surface affecté à chacune est la surface de la zone. Cela fait qu'on développe X fois la surface. Et cela divisé par la surface totale des zones développées du sdc_id (donc si la somme de toutes les X*surface du sdc_id). ==> les valeurs NE peuvent PAS dépasser 100% !
    """

    nd = donnees['noeuds_realise'][['id','culture_id','zone_id']].rename(columns={'id':'noeuds_realise_id'})
    zone = donnees['zone'][['id','surface','parcelle_id']].rename(columns={'id':'zone_id'})
    parcelle = donnees['parcelle'][['id','surface','sdc_id']].rename(columns={'id':'parcelle_id', 'surface':'surface_parcelle'})

    df = nd.merge(zone, on = 'zone_id', how = 'left').merge(parcelle, on = 'parcelle_id', how = 'left')
    df = df.loc[(df['sdc_id'].notna()) & (df['surface'] != 0)]

    df['nb_itk_mm_zone'] = df.groupby("zone_id")["noeuds_realise_id"].transform("count")
    df['surface_ponderee_zone'] = df['surface'] / df['nb_itk_mm_zone']

    df['surface_ponderee_totale'] = df.groupby("sdc_id")["surface_ponderee_zone"].transform("sum")
    df["surface_developpee_totale"] = df.groupby("sdc_id")["surface"].transform("sum")

    df['poids_surface_ponderee'] = df['surface_ponderee_zone'] / df['surface_ponderee_totale']
    df['poids_surface_developpee_agreg'] = df['surface'] / df['surface_ponderee_totale']
    df['poids_surface_developpee_normalisee'] = df['surface'] / df['surface_developpee_totale']

    df = df[['noeuds_realise_id', 'culture_id', 'sdc_id', 'poids_surface_ponderee', 'poids_surface_developpee_agreg', 'poids_surface_developpee_normalisee']]

    return df


def get_percoutage_chaque_typologie(donnees):
    """ """
    unique_sdc = donnees['entite_unique_par_sdc_nettoyage'].copy()

    sdc = donnees['sdc'].rename(columns={'id':'sdc_id'}).copy()
    sdc = sdc.loc[sdc['sdc_id'].isin(unique_sdc.loc[unique_sdc['synthetise_id'].isnull(),'sdc_id'])]
    synthetise = donnees['synthetise'].rename(columns={'id':'synthetise_id'}).copy()



    cnx_s = donnees['connection_synthetise'].rename(columns={'id':'connection_synthetise_id', 'cible_noeuds_synthetise_id':'noeuds_synthetise_id'}).copy()
    nd_s = donnees['noeuds_synthetise'][['id','synthetise_id']].rename(columns={'id':'noeuds_synthetise_id'}).copy()
    nd_r = donnees['noeuds_realise'].rename(columns={'id':'noeuds_realise_id'}).copy()

    esp = donnees['espece'][['id','libelle_espece_botanique','typodirodur_espece','typodirodur_espece_precise','typodirodur_espece_famille_bota','typodirodur_espece_periode_semis']].rename(columns={'id':'espece_id'}).copy()
    comp_cult = donnees['composant_culture'][['id','espece_id','culture_id','compagne']].rename(columns={'id':'composant_culture_id'}).copy()


    
    return final_df