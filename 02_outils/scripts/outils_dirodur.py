"""
	Regroupe les fonctions permettant de générer les outils utiles lors de la génération du magasin "DiRoDur".
"""
import pandas as pd
import numpy as np
from scripts.utils import dirodur_utiles

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

def get_itk_filtre_outils_dirodur(
        donnees,
    ):
    """
        Permet d'obtenir les informations permettant de filtrer ou non les itinéraires techniques.
        Les colonnes sont à "True" si il faut filtrer les lignes correspondante dans le contexte de DiRoDur.
        
        Attention, l'échelle itk sur Datagrosyst (itk_realise_performance et itk_synthetise_performance)
        peut présenter + d'une ligne pour un même itk (cas des cultures intermédiaires qui font l'objet d'un ikt à part)
        La clé unique en réalisé est donc (noeuds_realise_id, culture_id) et en synthétisé (connection_synthetise_id).

        Attention, le dataframe de sortie ne contient pas tous les ITK d'Agrosyst (uniquement les assolées), 
        On exclue aussi les parcelles non rattachées.
    """
    df = donnees.copy()
    df['sdc'] = df['sdc'].set_index('id')
    df['dispositif'] = df['dispositif'].set_index('id')
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
        "Cette alerte n'existe pas encore dans cette filière"
    ]

    # définition des colonnes d'alertes consultées
    ALERTE_COLUMNS = [
        'alerte_co_semis_std_mil',
        'alerte_ift_cible_non_mil_chim_tot_hts',
        'alerte_ift_cible_non_mil_f',
        'alerte_ift_cible_non_mil_h',
        'alerte_ift_cible_non_mil_i',
        'alerte_ift_cible_non_mil_biocontrole',
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



    for performance_df in ['itk_realise_performance_extanded', 'itk_synthetise_performance_extanded']:
        # création de la colonne de filtre sur les alertes
        df[performance_df]['filtre_alerte'] = True

        # on regarde si l'alerte est négative

        # cas classique
        df[performance_df].loc[
            (df[performance_df][ALERTE_COLUMNS].isin(ALERTE_IS_NO_STRINGS).any(axis=1)) |
            (df[performance_df][ALERTE_COLUMNS].isna().any(axis=1)) |
            ((df[performance_df]['alerte_cm_std_mil'].str.contains('<', na=False)) & ((df[performance_df]['typocan_culture'] == "Prairie temporaire") | (df[performance_df]['typocan_culture'] == "Prairie permanente"))),
            'filtre_alerte'
        ] = False
        


        # création de la colonne de filtre sur la filière
        df[performance_df]['filtre_filiere'] = ~df[performance_df]['filiere'].isin(FILIERES)


    res = pd.concat([
        df['itk_realise_performance_extanded'][['noeuds_realise_id', 'culture_id', 'filtre_filiere', 'filtre_alerte', 'sdc_id']],
        df['itk_synthetise_performance_extanded'][['connection_synthetise_id', 'filtre_filiere', 'filtre_alerte', 'sdc_id']],
    ])

    return res[[
        'noeuds_realise_id', 'culture_id', 'connection_synthetise_id', 'filtre_filiere', 'filtre_alerte', 'sdc_id'
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
    sdc_realise_filt, synthetises_filt = dirodur_utiles.filtered_entities_sdc_level(donnees)

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
        elif len(unique_values) == 1:
            return unique_values[0]
        else:
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




def get_typologie_culture_CAN(donnees):
    ''' 
    Le but est d'obtenir les typologies d'espece et de culture utilisées par la Cellule référence.

    Echelle :
        culture_id

    Args:
        donnees (dict):
            Données d'entrepot
            - 'composant_culture'
            - 'culture'
            - 'espece'
            - 'recolte_rendement_prix'
            - 'recolte_rendement_prix_restructure'
            Données externe (référentiel CAN):
            - 'typo_especes_typo_culture.csv'
            - 'typo_especes_typo_culture_marai.csv'

    Returns:
        pd.DataFrame() contenant la culture_id et la typologie de culture de la CAN
    '''
    # Donnes de bases
    cropsp = donnees['composant_culture'][['espece_id','culture_id','compagne']].copy()
    crop = donnees['culture'][['id','nom','type']].rename(columns={'id':'culture_id'}).copy()
    sp = donnees['espece'][['id','typocan_espece','typocan_espece_maraich']].rename(columns={'id':'espece_id'}).copy()
    
    # Donnees d'intervention pour les dates de semis
    intv_S = donnees['intervention_synthetise'][['id','type','date_debut','date_fin','concerne_ci','connection_synthetise_id']].copy()
    intv_R = donnees['intervention_synthetise'][['id','type','date_debut','date_fin','concerne_ci','noeud_realise_id']].copy()
    conx_S = donnees['connection_synthetise'][['id','cible_noeuds_synthetise_id']].rename(columns={'id':'connection_synthetise_id', 'cible_noeuds_synthetise_id':'noeud_synthetise_id'}).copy()
    noeud_w_culture_id_S = donnees['noeuds_synthetise_restructure'][['id','culture_id']].rename(columns={'id':'noeud_synthetise_id'}).copy()
    noeuds_w_culture_id_R = donnees['noeuds_realise'][['id','culture_id']].rename(columns={'id':'noeud_realise_id'}).copy()

    intv_S = intv_S.merge(conx_S, on='connection_synthetise_id', how='left')
    intv_S = intv_S.merge(noeud_w_culture_id_S, on='noeud_synthetise_id', how='left')
    intv_R = intv_R.merge(noeuds_w_culture_id_R, on='noeud_realise_id', how='left')

    intv = pd.concat([intv_S, intv_R], ignore_index=True)

    intv.groupby('culture_id').apply(
        lambda clt: pd.Series({
            'typo_cpg' : 'Cultures porte graines' if all(clt['nom'].str.contains('porte+.graine|semence', case=False)) |\
                                              all(clt['destination'] == 'Production semences') \
                    else 'Cultures porte graines et autres destinations' if any(clt['destination'] == 'Production semences') \
                    else None
        }), include_groups = False).reset_index()


    # Donnees de typologie d'espece et de culture
    typo1 = donnees['typo_especes_typo_culture'].copy()
    typo1 = typo1.rename(columns={'TYPO_ESPECES':'typocan_espece',
                                  'Typo_Culture':'typocan_culture'})
    typo2 = donnees['typo_especes_typo_culture_marai'].copy()
    typo2 = typo2.rename(columns={'TYPO_ESPECES_BIS':'typocan_espece_maraich',
                                  'Typo_Culture_bis':'typocan_culture_maraich'})

    df = cropsp.merge(sp, how = 'left', on = 'espece_id')
        # On change directement dans le dataframe les typologies d'espèces de la Betterave si elle est fourragère. Cela impactera la typologie de culture car elle ne reconnaitra pas 'Betterave fourragere' comme un 'Betterave' (la betterave industrielle). => Donc a ajouter dans le referentiel de passage typo_sp <=> typo_culture
    df.loc[df['composant_culture_id'].isin( list_cpc_bett_fourr ),'typocan_espece'] = 'Betterave fourragère'
    df.loc[df['composant_culture_id'].isin( list_cpc_bett_fourr ),'typocan_espece_maraich'] = 'Betterave fourragère'

    # Liste des cultures qui contiennent des cultures compagnes
    list_culture_with_compagne = list(set(df.loc[df['compagne'].notnull(), 'culture_id']))

    df['nb_composant_culture'] = 1
    df['nb_typocan_esp'] = df['typocan_espece'].copy()
    df['nb_typocan_esp_maraich'] = df['typocan_espece_maraich'].copy()

    def concat_unique_sorted(series):
        cleaned = series.dropna().unique()
        if len(cleaned) == 0:
            return np.nan
        return '_'.join(sorted(cleaned))
    def get_nb_unique_typo(series):
        cleaned = series.dropna().unique()
        return len(cleaned)
    agg_dict = {
        'typocan_espece': concat_unique_sorted,
        'typocan_espece_maraich': concat_unique_sorted,
        'nb_composant_culture': 'sum',
        'nb_typocan_esp': get_nb_unique_typo,
        'nb_typocan_esp_maraich': get_nb_unique_typo
    }

    #  On crée les typologie can culture et les autre variable utiles grace a agg_dict
    df_base = df[['culture_id','typocan_espece','typocan_espece_maraich',
                'nb_composant_culture','nb_typocan_esp','nb_typocan_esp_maraich']].groupby('culture_id').agg(agg_dict).reset_index()
    #  On crée une typologie can culture mais sans les cpc qui sont des plantes compagnes
    df_comp = df.loc[df['compagne'].isna()].copy()
    df_comp['typocan_esp_sans_compagne'] = df_comp['typocan_espece'].copy()
    df_comp = df_comp[['culture_id','typocan_esp_sans_compagne']].groupby('culture_id').agg(concat_unique_sorted).reset_index()

    # On repart sur un pd.Df qui est le merge de df_base et df_comp (donc le meme groupby mais sur un version filtré de df_base)
    del(df)
    df = df_base.merge(df_comp[['culture_id','typocan_esp_sans_compagne']], on = 'culture_id', how = 'left')

    # On ajoute les culture_id qui n'ont pas de composant de culture et on leur attribue aucune espece renseigné
    df = df.merge(crop, how='left', on='culture_id')

    # Détection des cultures qui contiennent des cultures compagnes
    df['is_any_compagne'] = np.where(df['culture_id'].isin(list_culture_with_compagne), True, False)

    crop_only = crop.loc[~crop['culture_id'].isin(df['culture_id']),:]
    # ATTENTION_DIFF_CAN_a ::: 2 Lignes
    crop_only.loc[:,['nb_composant_culture','nb_typocan_esp','nb_typocan_esp_maraich']] = 0
    crop_only.loc[:,['typocan_espece','typocan_espece_maraich','typocan_esp_sans_compagne']] = 'NoInput-sp'
    crop_only['is_any_compagne'] = False

    df = pd.concat([df, crop_only], ignore_index=True)

    df = df.merge(typo1, how='left', on='typocan_espece')

    df = df.merge(typo2, how='left', on='typocan_espece_maraich')

    df = df.merge(typo1.rename(columns={'typocan_espece':'typocan_esp_sans_compagne',
                                        'typocan_culture':'typocan_culture_sans_compagne'}), \
                                            how='left', on='typocan_esp_sans_compagne')
    
    # ATTENTION_DIFF_CAN_a_bis ::: 1 Lignes
    # le premier c'était pour les composant de culture, ici c'est pour la typo de culture
    df.loc[df['nb_composant_culture'] == 0,['typocan_culture','typocan_culture_maraich','typocan_culture_sans_compagne']] = 'NoInput-sp'

    # Si pas de correspondance espece <-> culture on l'écrit
    df.loc[df['nb_composant_culture'] != 0,['typocan_culture','typocan_culture_maraich','typocan_culture_sans_compagne']] = df.loc[df['nb_composant_culture'] != 0,['typocan_culture','typocan_culture_maraich','typocan_culture_sans_compagne']].fillna('NoLink-sp-crop')


    # ATTENTION_DIFF_CAN_b ::: 2 Lignes
    # df.loc[df.type == 'INTERMEDIATE', ['typocan_culture','typocan_culture_maraich']] = ['Culture intermédiaire', 'Culture intermédiaire']
    # df.loc[df.type == 'INTERMEDIATE', ['typocan_culture','typocan_culture_maraich']] = [np.nan, np.nan]


    df['type'] = df['type'].astype('category')
    df['type'] = df['type'].cat.rename_categories({'MAIN': 'PRINCIPALE', 
                                                   'INTERMEDIATE': 'INTERMEDIAIRE', 
                                                   'CATCH': 'DEROBEE' })
    df['type'] = df['type'].astype('str')
    df[['nb_composant_culture','nb_typocan_esp','nb_typocan_esp_maraich']] = df[['nb_composant_culture','nb_typocan_esp','nb_typocan_esp_maraich']].astype('int64')
    
    # Ajout des tags 'culture porte-graines' dans une colonne à part, voir la détection quelques ligne plus tôt dans cette fonction
    df = df.merge(culture_porteG[['culture_id','typo_cpg']], how='left', on='culture_id')

    return df