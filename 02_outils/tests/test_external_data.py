"""
    Contient tous les tests effectués sur les données externes. 
    Ces fonctions permettent de s'assurer que les données externes dont dépend le processus 
    de génération sont conformes à ce qui est attendu en entrée.
"""
import pandas as pd

def check_BDD_donnees_attendues_CAN(donnees):
    """ 
    Vérifie la table BDD_donnees_attendues_CAN :
    1. Contrôle des modalités autorisées.
    2. Contrôle des règles PZ0 :
       - 3 PZ0 espacés de 2 ans -> OK
       - 2 PZ0 espacés de 1 ou 2 ans -> OK
       - 1 seul PZ0 -> OK
       - sinon -> incohérence
    
    Retourne :
        - une liste de messages (erreurs/alertes/validations)
    """
    messages = []

    # --- Vérif présence table ---
    if "BDD_donnees_attendues_CAN" not in donnees:
        return ["Table BDD_donnees_attendues_CAN absente des données"]

    df = donnees["BDD_donnees_attendues_CAN"]

    # --- Vérif colonnes attendues ---
    cols_to_keep = [col for col in df.columns if "20" in col]
    if "codes_SdC" not in df.columns or not cols_to_keep:
        return ["Colonnes attendues manquantes dans BDD_donnees_attendues_CAN"]

    # --- Mise en forme longue ---
    df_melt = pd.melt(
        df[cols_to_keep + ["codes_SdC"]],
        id_vars=["codes_SdC"],
        var_name="campagne",
        value_name="donnee_attendue"
    )
    df_melt["campagne"] = df_melt["campagne"].astype("int64")

    # --- 1. Contrôle des modalités ---
    data_expected = {"Pas de donnees attendues", "PZ0 attendu", "donnees annuelles attendues"}
    data_unexpected = set(df_melt["donnee_attendue"].dropna()) - data_expected

    if data_unexpected:
        messages.append(f"⚠ Modalités inattendues trouvées : {sorted(data_unexpected)}")

    # --- 2. Cohérence des PZ0 ---
    df_pz0 = df_melt.loc[df_melt["donnee_attendue"] == "PZ0 attendu"].copy()

    if not df_pz0.empty:
        error_ref = (
            df_pz0.groupby("codes_SdC", dropna=False)
            .agg(
                nb_pz0=("donnee_attendue", "size"),
                diff_campagne_pz0=("campagne", lambda x: x.max() - x.min()),
                campagnes_pz0=("campagne", lambda x: ", ".join(x.astype(str)))
            )
            .reset_index()
        )

        incoherences = error_ref[
            ~(
                (error_ref["nb_pz0"] == 3) & (error_ref["diff_campagne_pz0"] == 2)
                | (error_ref["nb_pz0"] == 2) & (error_ref["diff_campagne_pz0"].isin([1, 2]))
                | (error_ref["nb_pz0"] == 1)
            )
        ]

        if not incoherences.empty:
            messages.append("⚠ Incohérences PZ0 détectées :")
            messages.append(incoherences.to_string(index=False))

    # --- Message de validation si aucun problème ---
    if not messages:
        messages.append("✅ Validation réussie : aucune incohérence détectée")

    return messages

def typo_especes_typo_culture(donnees):
    """
    Vérifie les tables `typo_especes_typo_culture` et `typo_especes_typo_culture_marai`.

    Vérifications :
    - Présence des 2 tables
    - Colonnes exactes attendues :
        * typo_especes_typo_culture : [TYPO_ESPECES, Typo_Culture]
        * typo_especes_typo_culture_marai : [TYPO_ESPECES_BIS, Typo_Culture_bis]
    - Pas de NA
    - Pas de doublons dans la 1ère colonne
    """
    messages = []

    spec_tables = {
        "typo_especes_typo_culture": ["TYPO_ESPECES", "Typo_Culture"],
        "typo_especes_typo_culture_marai": ["TYPO_ESPECES_BIS", "Typo_Culture_bis"]
    }

    for table_name, expected_cols in spec_tables.items():
        # --- Présence table ---
        if table_name not in donnees:
            messages.append(f"❌ Table manquante : {table_name}")
            continue

        df = donnees[table_name]

        # --- Colonnes ---
        if list(df.columns) != expected_cols:
            messages.append(
                f"❌ Colonnes incorrectes dans {table_name}.\n"
                f"   Attendu : {expected_cols}\n"
                f"   Trouvé : {list(df.columns)}"
            )
            continue

        # --- Valeurs manquantes ---
        if df.isna().any().any():
            messages.append(f"⚠️ Valeurs manquantes dans {table_name}")

        # --- Doublons sur la première colonne ---
        col_first = expected_cols[0]
        if df[col_first].duplicated().any():
            messages.append(f"⚠️ Doublons trouvés dans {table_name} sur la colonne {col_first}")

        # --- OK si aucun problème ---
        if not any(msg for msg in messages if table_name in msg):
            messages.append(f"✅ {table_name} conforme")

    return messages

