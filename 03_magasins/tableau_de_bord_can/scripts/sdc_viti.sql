SELECT
    COALESCE(sdc.code_dephy, 'CODE_DEPHY_ABSENT_') || '_' || sdc.campagne
        AS id_code_dephy_campagne,
    sdc.code_dephy as sdc_code_dephy,
    sdc.campagne as campagne_donnees,
    dispo."type" as dispositif_type,
    --reseaux_ir,
    --reseaux_it,
    dom.id as domaine_id,
    dom.nom as domaine_nom,
    dom.departement as departement,
    'réalisé' as approche_de_calcul,
   
FROM entrepot_sdc sdc
LEFT JOIN entrepot_dispositif  dispo ON dispo.id = sdc.dispositif_id
LEFT JOIN entrepot_domaine     dom   ON dom.id   = dispo.domaine_id
LEFT JOIN entrepot_commune    comm   ON dom.commune_id = comm.id
join entrepot_entite_unique_par_sdc_nettoyage eeupsn on sdc.id = eeupsn.sdc_id
WHERE sdc.filiere = 'VITICULTURE'
and eeupsn.entite_retenue = 'realise_retenu';


SELECT
    COALESCE(sdc.code_dephy, 'CODE_DEPHY_ABSENT_') || '_' || sdc.campagne
        AS id_code_dephy_campagne,
    sdc.code_dephy as sdc_code_dephy,
    sdc.campagne as campagne_donnees,
    dispo."type" as dispositif_type,
    --reseaux_ir,
    --reseaux_it,
    dom.id as domaine_id,
    dom.nom as domaine_nom,
    dom.departement as departement,
    dom.sau_totale as sau_domaine,
    dom.campagne as domaine_campagne,
    'synthétisé' as approche_de_calcul,
    sdc.id as sdc_id,
    sdc.nom as sdc_nom, 
    sdc.part_sau_domaine as sdc_part_sau_domaine,
    
FROM entrepot_sdc sdc
LEFT JOIN entrepot_dispositif  dispo ON dispo.id = sdc.dispositif_id
LEFT JOIN entrepot_domaine     dom   ON dom.id   = dispo.domaine_id
LEFT JOIN entrepot_commune    comm   ON dom.commune_id = comm.id
join entrepot_entite_unique_par_sdc_nettoyage eeupsn on sdc.id = eeupsn.sdc_id
WHERE sdc.filiere = 'VITICULTURE'
and eeupsn.entite_retenue != 'realise_retenu';
