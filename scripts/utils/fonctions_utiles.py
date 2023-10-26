"""
    Ce script contient les fonctions utiles dans les scripts principaux
"""
import pandas as pd


def get_infos_traitement(df_utilisation_intrant, df_intrant):
    """
        Retourne un dataframe où les utilisations d'intrants sont complétées par des méta-informations utiles.
        Paramètres :
                utilisation_intrant_id (df) : Dataframe contenant les colonnes suivantes : 
                    'id' : identifiant de l'utilisation de l'intrant
                    'intrant_id': identifiant de l'intrant utilisé
                intrant (df) : Dataframe contenant les colonnes suivantes :
                    'id' : identifiant de l'intrant
                    'ref_id' : identifiant de l'intrant dans le référentiel intrant
        Retourne :
                res (df) : Dataframe contenant les valeurs suivantes : 
                    id_produit
                    code_amm_produit
                    id_traitement
                    code_amm_traitement_maa
        
        ATTENTION : 
            Pour l'instant, cette fonction ne permet pas d'obtenir le code amm d'un traitement de semence et retournera : null
    """
    # Déclaration des chemins des données 
    path_ref_acta_traitement_produit = 'data/referentiels/ref_acta_traitement_produit.csv'

    # Import des données utiles
    df_ref_acta_traitement_produit = pd.read_csv(path_ref_acta_traitement_produit)

    # Nettoyage des référentiels
    df_ref_acta_traitement_produit = df_ref_acta_traitement_produit.loc[df_ref_acta_traitement_produit['active']]

    # Obtention de l'identifiant de l'intrant de référence
    left = df_utilisation_intrant
    right = df_intrant[['id', 'ref_id']].rename(columns={'id' : 'intrant_id'})
    merge = pd.merge(left, right, on = 'intrant_id', how='left')

    # Obtention des informations de l'intrant de référence 
    left = merge
    right = df_ref_acta_traitement_produit[['topiaid', 'id_produit', 'id_traitement', 'code_amm', 'code_traitement_maa']].rename(columns={'topiaid' : 'ref_id'})
    df_utilisation_intrant = pd.merge(left, right, on = 'ref_id', how='left')

    return df_utilisation_intrant

def get_infos_culture_realise(
        df_utilisation_intrant_realise, 
        df_intervention_realise, 
        df_noeuds_realise,
        df_plantation_perenne_realise,
        df_plantation_perenne_phase_realise,
        df_composant_culture
    ):
    """
        Retourne un dataframe qui contient une ligne pour la clé (utilisation_id * code_culture_maa * espece_id)
        En effet, pour les mélanges d'espèces, il n'est pas possible d'obtenir une seule ligne.
        Attention, cette fusion ne s'applique que pour les intrants réalisés .
        Paramètres :
                utilisation_intrant_id (df) : Dataframe contenant les valeurs suivantes : 
                    'id' : identifiant de l'utilisation de l'intrant
                    'intrant_id': identifiant de l'intrant utilisé
        Retourne :
                res (df) : Dataframe contenant les valeurs suivantes : 
                    'id' : identifiant de l'utilisation de l'intrant (attention : non unique)
                    'espece_id' : identifiant de l'espèce contenue dans la culture où est appliquée l'intervention
                    'code_culture_maa' :  code culture de l'espèce en question
    """
    # Déclaration des chemins des données 
    path_culture_maa = 'data/referentiels/ref_culture_maa.csv'

    # Import des données utiles
    df_ref_culture_maa = pd.read_csv(path_culture_maa)

    # Nettoyage des référentiels
    df_ref_culture_maa = df_ref_culture_maa.loc[df_ref_culture_maa['active']]
    
    #----------------------------------#
    # TRAVAIL POUR LES CYCLES ASSOLÉES |
    #----------------------------------#
    df_intervention_realise_assolee = df_intervention_realise[~df_intervention_realise['noeuds_realise_id'].isna()]

    # obtention de l'intervention
    left = df_utilisation_intrant_realise
    right = df_intervention_realise_assolee[['id', 'noeuds_realise_id']].rename(columns={
        'id' : 'intervention_realise_id'
    }) 
    df_utilisation_intrant_realise_assolee = pd.merge(left, right, on = 'intervention_realise_id')

    # obtention du noeuds
    left = df_utilisation_intrant_realise_assolee
    right = df_noeuds_realise[['id', 'culture_id']].rename(columns={
        'id' : 'noeuds_realise_id'
    }) 
    df_utilisation_intrant_realise_assolee = pd.merge(left, right, on = 'noeuds_realise_id')

    #---------------------------------------#
    # TRAVAIL POUR LES PLANTATIONS PERENNES |
    #---------------------------------------#
    df_intervention_realise_perenne = df_intervention_realise.loc[~df_intervention_realise['plantation_perenne_phases_realise_id'].isna()]

    # obtention de l'intervention
    left = df_utilisation_intrant_realise
    right = df_intervention_realise_perenne[['id', 'plantation_perenne_phases_realise_id']].rename(columns={
        'id' : 'intervention_realise_id'
    }) 
    df_utilisation_intrant_realise_perenne = pd.merge(left, right, on = 'intervention_realise_id')

    # obtention de la phase de la plantation perenne
    left = df_utilisation_intrant_realise_perenne
    right = df_plantation_perenne_phase_realise[['id', 'plantation_perenne_realise_id']].rename(columns={
        'id' : 'plantation_perenne_phases_realise_id'
    }) 
    df_utilisation_intrant_realise_perenne = pd.merge(left, right, on = 'plantation_perenne_phases_realise_id')

    # obtention de la plantation perenne
    left = df_utilisation_intrant_realise_perenne
    right = df_plantation_perenne_realise[['id', 'culture_id']].rename(columns={
        'id' : 'plantation_perenne_realise_id'
    }) 
    df_utilisation_intrant_realise_perenne = pd.merge(left, right, on = 'plantation_perenne_realise_id')

    #--------#
    # FUSION |
    #--------#

    df_utilisation_intrant_realise_complet = pd.concat([df_utilisation_intrant_realise_assolee, df_utilisation_intrant_realise_perenne])[['id', 'culture_id']]
    
    #-----------------------------------------#
    # OBTENTION DES ESPECES DANS LES CULTURES |
    #-----------------------------------------#

    # obtention des composants de culture  (dupplications car il peut y avoir plusieurs espèces dans une même culture)
    left = df_utilisation_intrant_realise_complet
    right = df_composant_culture[['culture_id', 'espece_id']].drop_duplicates() # on retire les mélanges de variété 
    merge = pd.merge(left, right, on = 'culture_id')

    # obtention du code culture maa (dupplications car il peut y avoir plusieurs code_culture_maa pour une même espece)
    left = merge
    right = df_ref_culture_maa[['espece', 'code_culture_maa']].rename(
        columns={
            'espece' : 'espece_id'
        }
    )
    df_utilisation_intrant_realise = pd.merge(left, right, on = 'espece_id')

    df_utilisation_intrant_realise = df_utilisation_intrant_realise[['id', 'code_culture_maa']].drop_duplicates()

    # On obtient donc un dataframe df_utilisation_intrant_realise dans lequel : 
    # la clé unique est : 'id', 'code_espece_maa'.
    # on ne peut pas retirer espece_id --> car mélange d'especes avec même code_culture_maa 
    #   ex : (fr.inra.agrosyst.api.entities.action.SeedSpeciesInputUsage_8e2de7cf-b60c-49b0-aefc-4f58a98f2626)
    # on ne peut pas retirer code_espece_maa --> car mélange d'espèces avec code_culture_maa différents 
    #   ex : (fr.inra.agrosyst.api.entities.action.OrganicProductInputUsage_4d679917-ee0e-4801-b8d1-21ff8b1687f2)

    return df_utilisation_intrant_realise


def get_infos_culture_synthetise(
        df_utilisation_intrant_synthetise, 
        df_intervention_synthetise, 
        df_connection_synthetise,
        df_noeuds_synthetise,
        df_plantation_perenne_synthetise,
        df_plantation_perenne_phase_synthetise,
        df_composant_culture, 
        df_culture
    ):
    """
        Retourne un dataframe qui contient une ligne pour la clé (utilisation_id * code_culture_maa * espece_id)
        En effet, pour les mélanges d'espèces, il n'est pas possible d'obtenir une seule ligne.
        Attention, cette fusion ne s'applique que pour les intrants réalisés .
        Paramètres :
                utilisation_intrant_id (df) : Dataframe contenant les valeurs suivantes : 
                    'id' : identifiant de l'utilisation de l'intrant
                    'intrant_id': identifiant de l'intrant utilisé
        Retourne :
                res (df) : Dataframe contenant les valeurs suivantes : 
                    'id' : identifiant de l'utilisation de l'intrant (attention : non unique)
                    'espece_id' : identifiant de l'espèce contenue dans la culture où est appliquée l'intervention
                    'code_culture_maa' :  code culture de l'espèce en question
    """
    # Déclaration des chemins des données 
    path_culture_maa = 'data/referentiels/ref_culture_maa.csv'

    # Import des données utiles
    df_ref_culture_maa = pd.read_csv(path_culture_maa)

    # Nettoyage des référentiels
    df_ref_culture_maa = df_ref_culture_maa.loc[df_ref_culture_maa['active']]

    #----------------------------------#
    # TRAVAIL POUR LES CYCLES ASSOLÉES |
    #----------------------------------#
    df_intervention_synthetise_assolee = df_intervention_synthetise[~df_intervention_synthetise['connection_synthetise_id'].isna()]

    # obtention de l'intervention
    left = df_utilisation_intrant_synthetise
    right = df_intervention_synthetise_assolee[['id', 'connection_synthetise_id']].rename(columns={
        'id' : 'intervention_synthetise_id'
    }) 
    df_utilisation_intrant_synthetise_assolee = pd.merge(left, right, on = 'intervention_synthetise_id')

    # obtention du noeuds synthétisé sur lequel a lieu l'intervention
    left = df_utilisation_intrant_synthetise_assolee
    right = df_connection_synthetise[['id', 'cible_noeuds_synthetise_id']].rename(columns={
        'id' : 'connection_synthetise_id'
    })
    merge = pd.merge(left, right, on = 'connection_synthetise_id')

    # obtention du culture_code pour lequel a lieu l'intervention 
    left = merge
    right = df_noeuds_synthetise[['id', 'culture_code']].rename(columns={
        'id' : 'cible_noeuds_synthetise_id'
    })
    df_utilisation_intrant_synthetise_assolee = pd.merge(left, right, on = 'cible_noeuds_synthetise_id')

    #---------------------------------------#
    # TRAVAIL POUR LES PLANTATIONS PERENNES |
    #---------------------------------------#
    df_intervention_synthetise_perenne = df_intervention_synthetise.loc[~df_intervention_synthetise['plantation_perenne_phases_synthetise_id'].isna()]

    # obtention de l'intervention
    left = df_utilisation_intrant_synthetise
    right = df_intervention_synthetise_perenne[['id', 'plantation_perenne_phases_synthetise_id']].rename(columns={
        'id' : 'intervention_synthetise_id'
    }) 
    df_utilisation_intrant_synthetise_perenne = pd.merge(left, right, on = 'intervention_synthetise_id')

    # obtention de la phase de la plantation perenne
    left = df_utilisation_intrant_synthetise_perenne
    right = df_plantation_perenne_phase_synthetise[['id', 'plantation_perenne_synthetise_id']].rename(columns={
        'id' : 'plantation_perenne_phases_synthetise_id'
    }) 
    df_utilisation_intrant_synthetise_perenne = pd.merge(left, right, on = 'plantation_perenne_phases_synthetise_id')

    # obtention de la plantation perenne
    left = df_utilisation_intrant_synthetise_perenne
    right = df_plantation_perenne_synthetise[['id', 'culture_code']].rename(columns={
        'id' : 'plantation_perenne_synthetise_id'
    }) 
    df_utilisation_intrant_synthetise_perenne = pd.merge(left, right, on = 'plantation_perenne_synthetise_id')

    #--------#
    # FUSION |
    #--------#

    df_utilisation_intrant_synthetise_complet = pd.concat([df_utilisation_intrant_synthetise_assolee, df_utilisation_intrant_synthetise_perenne])[['id', 'culture_code']]

    #-----------------------------------------#
    # OBTENTION DES ESPECES DANS LES CULTURES |
    #-----------------------------------------#

    # obtention des culture_id à partir des culture_code
    left = df_utilisation_intrant_synthetise_complet
    right = df_culture[['id', 'code']].rename(columns={
        'code' : 'culture_code',
        'id' : 'culture_id'
    })
    df_utilisation_intrant_synthetise_complet = pd.merge(left, right, on = 'culture_code')

    # obtention des composants de culture  (dupplications car il peut y avoir plusieurs espèces dans une même culture)
    left = df_utilisation_intrant_synthetise_complet
    right = df_composant_culture[['culture_id', 'espece_id']].drop_duplicates() # on retire les mélanges de variété 
    merge = pd.merge(left, right, on = 'culture_id')

    # obtention du code culture maa (dupplications car il peut y avoir plusieurs code_culture_maa pour une même espece)
    left = merge
    right = df_ref_culture_maa[['espece', 'code_culture_maa']].rename(
        columns={
            'espece' : 'espece_id'
        }
    )
    df_utilisation_intrant_synthetise = pd.merge(left, right, on = 'espece_id')

    df_utilisation_intrant_synthetise = df_utilisation_intrant_synthetise[['id', 'code_culture_maa']].drop_duplicates()

    # On obtient donc un dataframe df_utilisation_intrant_realise dans lequel : 
    # la clé unique est : 'id', 'code_espece_maa'.
    # on ne peut pas retirer espece_id --> car mélange d'especes avec même code_culture_maa 
    #   ex : (fr.inra.agrosyst.api.entities.action.SeedSpeciesInputUsage_8e2de7cf-b60c-49b0-aefc-4f58a98f2626)
    # on ne peut pas retirer code_espece_maa --> car mélange d'espèces avec code_culture_maa différents 
    #   ex : (fr.inra.agrosyst.api.entities.action.OrganicProductInputUsage_4d679917-ee0e-4801-b8d1-21ff8b1687f2)

    return df_utilisation_intrant_synthetise



def get_infos_cible(
        df_utilisation_intrant_cible
    ):
    """
        Retourne un dataframe qui contient une ligne pour la clé (utilisation_id * code_culture_maa * espece_id)
        En effet, pour les mélanges d'espèces, il n'est pas possible d'obtenir une seule ligne.
        Attention, cette fusion ne s'applique que pour les intrants réalisés .
        Paramètres :
                utilisation_intrant_id (df) : Dataframe contenant les valeurs suivantes : 
                    'id' : identifiant de l'utilisation de l'intrant
                    'intrant_id': identifiant de l'intrant utilisé
        Retourne :
                res (df) : Dataframe contenant les valeurs suivantes : 
                    'id' : identifiant de l'utilisation de l'intrant (attention : non unique)
                    'espece_id' : identifiant de l'espèce contenue dans la culture où est appliquée l'intervention
                    'code_culture_maa' :  code culture de l'espèce en question
    """
    # Déclaration des chemins des données 
    path_ref_nuisible_edi = 'data/referentiels/ref_nuisible_edi.csv'
    path_ref_correspondance_groupe_cible = 'data/referentiels/ref_correspondance_groupe_cible.csv'
    path_ref_adventice = 'data/referentiels/ref_adventice.csv'

    # Import des données utiles
    df_ref_nuisible_edi = pd.read_csv(path_ref_nuisible_edi, sep=',')
    df_ref_correspondance_groupe_cible = pd.read_csv(path_ref_correspondance_groupe_cible, sep=',')
    df_ref_adventice = pd.read_csv(path_ref_adventice, sep=',')

    # Nettoyage des référentiels
    df_ref_adventice = df_ref_adventice.loc[df_ref_adventice['active']]
    df_ref_nuisible_edi = df_ref_nuisible_edi.loc[df_ref_nuisible_edi['active']]

    # Obtention des cibles liées à des utilisations d'intrants
    df_utilisation_intrant_cible = df_utilisation_intrant_cible.loc[~df_utilisation_intrant_cible['utilisation_intrant_id'].isna()]
    
    # ajout des identifiants des adventices
    left = df_utilisation_intrant_cible[['id', 'utilisation_intrant_id', 'ref_cible_id', 'categorie', 'code_groupe_cible_maa']]
    right = df_ref_adventice[['topiaid', 'identifiant']].rename(columns={
        'topiaid' : 'ref_cible_id',
        'identifiant' : 'cible_edi_ref_id'
    })
    df_utilisation_intrant_cible_adventice = pd.merge(left, right, on = 'ref_cible_id')

    # Ajout des identifiants des nuisibles
    left = df_utilisation_intrant_cible[['id', 'utilisation_intrant_id', 'ref_cible_id', 'categorie', 'code_groupe_cible_maa']]
    right = df_ref_nuisible_edi[['topiaid', 'reference_id']].rename(columns={
        'topiaid' : 'ref_cible_id',
        'reference_id' : 'cible_edi_ref_id'
    })
    df_utilisation_intrant_cible_nuisible = pd.merge(left, right, on = 'ref_cible_id')

    df_utilisation_intrant_cible = pd.concat([df_utilisation_intrant_cible_adventice, df_utilisation_intrant_cible_nuisible], axis=0)

    df_utilisation_intrant_cible['cible_edi_ref_id'] = df_utilisation_intrant_cible['cible_edi_ref_id'].astype('str')

    # Certaines des cibles ont déjà un code_groupe_cible (identifié dès la saisie)
    df_utilisation_intrant_cible_with_code_groupe = df_utilisation_intrant_cible.loc[
        ~df_utilisation_intrant_cible['code_groupe_cible_maa'].isna()
    ]

    df_utilisation_intrant_cible_with_code_groupe = df_utilisation_intrant_cible_with_code_groupe.loc[
        df_utilisation_intrant_cible_with_code_groupe['code_groupe_cible_maa'] !=  '#N/D'
    ]

    df_utilisation_intrant_cible_with_code_groupe['code_groupe_cible_maa'] = df_utilisation_intrant_cible_with_code_groupe[
        'code_groupe_cible_maa'
    ].astype('int')

    # Pour d'autres, il faut les trouver manuellement
    df_utilisation_intrant_cible_without_code_groupe = df_utilisation_intrant_cible.loc[
        df_utilisation_intrant_cible['code_groupe_cible_maa'].isna()
    ]
    # Certaines des cibles ont déjà une catégorie (identifiée dès la saisie)
    df_with_categorie = df_utilisation_intrant_cible_without_code_groupe.loc[
        ~df_utilisation_intrant_cible_without_code_groupe['categorie'].isna()
    ] 
    # Pour d'autres, il faut les trouver manuellement
    df_without_categorie = df_utilisation_intrant_cible_without_code_groupe.loc[
        df_utilisation_intrant_cible_without_code_groupe['categorie'].isna()
    ]
    
    # Pour ceux qui ont une catégorie, on va chercher l'ensemble des code_groupe_cible_maa de cette catégorie
    left = df_with_categorie[['id', 'utilisation_intrant_id', 'ref_cible_id', 'categorie', 'cible_edi_ref_id']]
    right = df_ref_correspondance_groupe_cible[['cible_edi_ref_id', 'code_groupe_cible_maa', 'reference_param']].rename(
        columns={
            'reference_param' : 'categorie'
        }
    )
    df_with_categorie = pd.merge(left, right, on = ['cible_edi_ref_id', 'categorie'], how='left')

    # Pour ceux qui n'ont pas de catégories, on va chercher l'ensemble total
    left = df_without_categorie[['id', 'utilisation_intrant_id', 'ref_cible_id', 'categorie', 'cible_edi_ref_id']]
    right = df_ref_correspondance_groupe_cible[['cible_edi_ref_id', 'code_groupe_cible_maa']]
    df_without_categorie = pd.merge(left, right, on = 'cible_edi_ref_id', how='left')

    # Reconstruction du dataframe final d'utilisation intrant_cible 
    df_utilisation_intrant_cible_without_code_groupe = pd.concat([df_with_categorie, df_without_categorie], axis=0)
    df_utilisation_intrant_cible = pd.concat([
            df_utilisation_intrant_cible_without_code_groupe, 
            df_utilisation_intrant_cible_with_code_groupe
        ], axis=0)[['utilisation_intrant_id', 'code_groupe_cible_maa']]
    
    df_utilisation_intrant_cible = df_utilisation_intrant_cible.rename(columns={
        'utilisation_intrant_id' : 'id'
    })
    # Attention, à ce stade, il y a certains problèmes dans les référentiels (ex : 000000AEE021 impossible d'associer un code_maa)
    # ainsi, certains code_groupe_cible_maa restent nuls

    return df_utilisation_intrant_cible

def get_dose_ref(
        df_utilisation_intrant_complet
    ):
    """
        Retourne un dataframe qui contient les doses de références pour chaque utilisation d'intrants
        Paramètres :
                df_utilisation_intrant_complet (df) : Dataframe contenant les valeurs suivantes : 
                    'id' : identifiant de l'utilisation de l'intrant
                    'code_amm': code_amm du produit
                    'code_traitement_maa' : code du traitement du produit 
                    'code_culture_maa' : code maa de la culture sur laquelle le produit est utilisé
                    
        Retourne :
                final_result (df) : Dataframe contenant les valeurs suivantes : 
                    'id' : identifiant de l'utilisation de l'intrant (attention : non unique)
                    'dose_ref_maa' : dose de référence à la cible non millésimé de l'utilisation d'intrant
                    'unit_dose_ref_maa' :  unité de la dose de référence de l'utilisation d'intrant
    """
    # Déclaration des chemins des données 
    path_dose_ref_cible = 'data/referentiels/dose_ref_cible.csv'

    # Import des données utiles
    df_dose_ref_cible = pd.read_csv(path_dose_ref_cible, sep=',')

    # Nettoyage des référentiels
    df_dose_ref_cible = df_dose_ref_cible.loc[df_dose_ref_cible['active']]

    # Obtention des utilisations d'intrants dans lesquelles on a au moins un code amm de déclaré
    df_utilisation_intrant_complet = df_utilisation_intrant_complet.loc[~df_utilisation_intrant_complet['code_amm'].isna()]
    df_utilisation_intrant_complet['code_amm'] = df_utilisation_intrant_complet['code_amm'].astype('int')

    # Séparation entres les utilisations où on a un groupe cible de retrouvé et les autres
    total_merge_3_without_cible = df_utilisation_intrant_complet.loc[df_utilisation_intrant_complet['code_groupe_cible_maa'].isna()]
    total_merge_3_with_cible = df_utilisation_intrant_complet.loc[~df_utilisation_intrant_complet['code_groupe_cible_maa'].isna()]

    # Séparation
    total_merge_3_with_cible = total_merge_3_with_cible.loc[total_merge_3_with_cible['code_groupe_cible_maa'] !=  '#N/D']
    total_merge_3_with_cible['code_groupe_cible_maa'] = total_merge_3_with_cible['code_groupe_cible_maa'].astype('int')

    # fusion pour celles qui n'ont pas de cibles trouvées :
    left = total_merge_3_without_cible
    right = df_dose_ref_cible[['code_amm', 'code_culture_maa', 'code_traitement_maa', 'dose_ref_maa', 'unit_dose_ref_maa']].drop_duplicates()
    total_merge_without_cible = pd.merge(left, right, on = ['code_amm', 'code_traitement_maa', 'code_culture_maa'], how='left')
    total_merge_without_cible = total_merge_without_cible.loc[~total_merge_without_cible['dose_ref_maa'].isna()]

    # fusion pour celles qui ont une cible 
    left = total_merge_3_with_cible
    right = df_dose_ref_cible[['code_amm', 'code_culture_maa', 'code_traitement_maa', 'dose_ref_maa', 'unit_dose_ref_maa', 'code_groupe_cible_maa']]
    total_merge_with_cible = pd.merge(left, right, on = ['code_amm', 'code_traitement_maa', 'code_groupe_cible_maa', 'code_culture_maa'], how='left')
    total_merge_with_cible = total_merge_with_cible.loc[~total_merge_with_cible['dose_ref_maa'].isna()]

    # On garde les doses minimales trouvées pour chaque utilisation d'intrants
    final_result_with_cible = total_merge_with_cible.loc[total_merge_with_cible.groupby('id')['dose_ref_maa'].idxmax()]
    final_result_without_cible = total_merge_without_cible.loc[total_merge_without_cible.groupby('id')['dose_ref_maa'].idxmin()]

    # On créé le dataframe final
    final_result = pd.concat([final_result_with_cible, final_result_without_cible], axis=0)

    # On a certaines dupplications (ex : fr.inra.agrosyst.api.entities.action.PesticideProductInputUsage_ed7545bf-ad2c-4953-97fd-47ede7233cc0)
    # --> correspond à des données historiques de saisie, on drop. 

    final_result = final_result.drop_duplicates(subset=['id'])

    return final_result