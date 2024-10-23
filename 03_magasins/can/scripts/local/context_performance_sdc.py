import configparser
import pandas as pd

#Fetch the sql files 
path_sql_files = 'scripts/'

#Obtenir les paramètres de connexion pour psycopg2
config = configparser.ConfigParser()
config.read(r'../../../../00_config/config.ini')

DATA_PATH = config.get('entrepot_local', 'data_path') 


# Charger les DataFrames depuis les fichiers CSV (enlever "entrepot" des noms de fichiers)
liaison_sdc_reseau = pd.read_csv(DATA_PATH+'liaison_sdc_reseau.csv')
reseau = pd.read_csv(DATA_PATH+'reseau.csv')
liaison_reseaux = pd.read_csv(DATA_PATH+'liaison_reseaux.csv')
sdc = pd.read_csv(DATA_PATH+'sdc.csv')
dispositif = pd.read_csv(DATA_PATH+'dispositif.csv')
domaine = pd.read_csv(DATA_PATH+'domaine.csv')

# Étape 1 : Construction de la table temporaire "reseaux_agg"
# Agréger les données pour obtenir les colonnes 'nom_reseau_it' et 'nom_reseau_ir'
reseaux_agg = (
    liaison_sdc_reseau
    .merge(reseau, left_on='reseau_id', right_on='id', suffixes=('', '_r'))  # Jointure avec la table 'reseau'
    .merge(liaison_reseaux, left_on='reseau_id', right_on='reseau_id', suffixes=('', '_lr'))  # Jointure avec 'liaison_reseaux'
    .merge(reseau, left_on='reseau_parent_id', right_on='id', suffixes=('', '_parent'))  # Jointure avec 'reseau' pour obtenir 'reseau_parent_id'
    .groupby('sdc_id', as_index=False)
    .agg({
        'nom': lambda x: ', '.join(x.unique()),  # Pour 'nom_reseau_ir'
        'nom_parent': lambda x: ', '.join(x.unique())  # Pour 'nom_reseau_it'
    })
    .rename(columns={'nom': 'nom_reseau_ir', 'nom_parent': 'nom_reseau_it'})
)

# Étape 2 : Réaliser les jointures pour créer le DataFrame final
# Jointure avec 'sdc', 'dispositif', et 'domaine'
df_final = (
    sdc
    .merge(reseaux_agg, left_on='id', right_on='sdc_id', how='left')  # Jointure avec 'reseaux_agg'
    .merge(dispositif, left_on='dispositif_id', right_on='id', suffixes=('', '_dispo'))  # Jointure avec 'dispositif'
    .merge(domaine, left_on='domaine_id', right_on='id', suffixes=('', '_domaine'))  # Jointure avec 'domaine'
)

print(df_final.columns)

# Étape 3 : Sélectionner les colonnes finales
df_final = df_final[[
    'nom_domaine', 
    'id_domaine', 
    'campagne_domaine', 
    'type_ferme_domaine', 
    'departement_domaine', 
    'nom_reseau_it', 
    'nom_reseau_ir', 
    'id_dispositif', 
    'type_dispositif', 
    'id',  # 'sdc_id'
    'filiere', 
    'nom',  # 'sdc_nom'
    'code_dephy',  # 'sdc_num_dephy'
    'type_agriculture',  # 'sdc_type_conduite'
    'validite',  # 'sdc_valide'
    'modalite_suivi_dephy'  # 'sdc_modalite_suivi_dephy'
]]

# Afficher ou sauvegarder le résultat final
df_final.to_csv(DATA_PATH+'context_performance_sdc.csv', index=False)
print(df_final.head())