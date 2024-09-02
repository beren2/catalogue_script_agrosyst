
-- filtres exigés par le magasin DEPHY
-- CREATE TABLE dispositif_filtre as
--     SELECT
--         d.id domaine_id,
--         ed.id dispositif_id
--     FROM entrepot_dispositif ed
--     JOIN entrepot_domaine d ON ed.domaine_id = d.id
--     AND ed.type !='NOT_DEPHY'
--     AND d.campagne >1999
--     AND d.campagne <2026;

-- drop table if exists domaine_filtre;
-- CREATE TABLE domaine_filtre as 
--     SELECT 
--         distinct domaine_id 
--     FROM dispositif_filtre 

SELECT 
    code as domaine_code, 
    id as domaine_id,
    nom as domaine_nom, 
    siret, 
    campagne as domaine_campagne, 
    type_ferme as type, 
    departement, 
    commune, 
    petite_region_agricole,
    zonage as domaine_zonage,
    pct_sau_zone_vulnerable,
    pct_sau_zone_excedent_structurel,
    pct_sau_zone_actions_complementaires,
    pct_sau_zone_natura_2000,
    pct_sau_zone_erosion,
    pct_sau_perimetre_protection_captage,
    description,
    statut_juridique_nom,
    statut_juridique_commentaire,
    sau_totale as sau,
    cultures_commentaire,
    autres_activites_commentaire,
    mo_commentaire,
    nombre_associes,
    mo_familiale_et_associes,
    mo_permanente,
    mo_temporaire,
    mo_familiale_remuneration,
    charges_salariales,
    mo_conduite_cultures_dans_domaine_expe,
    cotisation_msa,
    fermage_moyen,
    aides_decouplees,
    otex_18_nom,
    otex_70_nom,
    otex_commentaire,
    responsables_domaine
from entrepot_domaine d
join entrepot_domaine_filtres_outils_can edifoc on d.id = edifoc.id
