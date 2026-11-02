# Doc creation/ajout table entrepot

Etapes à suivre lors de la creation d'une nouvelle table entrepot. Les étapes de gestion git ne seront pas suivies.
Prérequis, un clone local du git : catalogue_script_agrosyst

# Table.sql

Generer un code sql de creation de table en sql, executable via DBeaver pour la phase de test.
Exemple type :

```sql
CREATE TABLE table_nom AS
SELECT 
    ex.topiaid as id,
    ex.colonne_1,
    ex2.colonne_2,
FROM table_referente ex
JOIN table_referente_2 ex2 ON ex.topiaid = ex2.topiaid;

ALTER TABLE table_nom
ADD CONSTRAINT table_nom_PK
PRIMARY KEY (id);
```

Ce fichier sql doit se trouver dans le dossier main/01_entrepot/scripts/table_nom.sql

Pour la phase de test, il faut, soit :
    - Generer la table avec le sql sur Dbeaver
    - Generer la table via main.py du dossier 01_entrepot du catalogue local

# Mettre à jour datagrosyst

Sur DBeaver, se connecter à la bonne base de donnée magasin (différent de l'entrepot, ex : datagrosyst_prod_2025XXXX) puis modifier les deux tables :

entrepot_table : 

```sql
INSERT INTO entrepot_table (id, label, explication, category_id, is_active, "order", required_right, generated, sql_request)
VALUES
('table_exemple', 'table_exemple','description exemple', 'categorie', TRUE, XX, 0, FALSE, NULL);
```

et entrepot_column : 

```sql
INSERT INTO entrepot_column (id, label, explication, sensible_column, table_id, is_active, "order", foreign_key_table, reference_column_id)
VALUES
('table_exemple_id', 'id', 'identifiant table_exemple', FALSE, 'table_exemple', TRUE, 0, NULL, NULL),
('table_exemple_colonne_1', 'colonne_1', 'explication colonne_1', FALSE, 'table_exemple', FALSE, 1, NULL, NULL),
('table_exemple_colonne_2', 'colonne_2', 'explication colonne_2', FALSE, 'table_exemple', FALSE, 2, NULL, NULL);
```

# Relancer datagrosyst

Relancer datagrosyst pour appliquer les changements : (Attention, s'assurer que datagrosyst utilise bien l'entrepot modifié, changer la config si nécéssaire : catalogue_script_agrosyst/00_config/config.ini).

```bash
ssh ******@*********

cd /opt/docker/datagrosyst-tests/

docker compose down
docker compose up -d
```
