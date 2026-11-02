DROP TABLE IF EXISTS entrepot_parcelle CASCADE;

CREATE TABLE entrepot_parcelle AS
  WITH plot_zone AS (
    SELECT z.plot, count(*) nombre_de_zones
    FROM zone z
    where z.active IS TRUE
    GROUP BY z.plot)
  select
  ------ Informations generales
  p.topiaid id,
  p.code code, 
  p.name nom,
  d.campagne,
  p.pacilotnumber,
  p.latitude,
  p.longitude,
  p.comment commentaire,
  pz.nombre_de_zones,
  p.area surface,
  p.maxslope pente,
  p.waterflowdistance distance_cours_eau,
  p.bufferstrip bande_enherbee,
  ------ Informations sur le zonage de la parcelle
  p.inzoning dans_zonage,
  p.zoningcomment commentaire_zonage,
 ------ onglet equipements
  p.equipmentcomment equip_commentaire,
  p.irrigationsystem systeme_irrigation,
  p.irrigationsystemtype systeme_irrigation_type,
  p.pompenginetype pompe_type,
  p.hosespositionning positionnement_tuyaux_arrosage,
  p.fertigationsystem systeme_fertirrigation,
  p.waterorigin eau_origine,
  p.drainage drainage,
  p.drainageyear drainage_annee_realisation,
  p.frostprotection protection_antigel,
  p.frostprotectiontype protection_antigel_type,
  p.hailprotection protection_antigrele,
  p.pestprotection protection_antiinsecte,
  p.rainproofprotection protection_antipluie,
  p.otherequipment equip_autre,
  ------ Onglet sol de la parcelle
  p.solcomment commentaire_sol,
  reftextu.classes_texturales_gepaa as texture_surface,
  reftextu2.classes_texturales_gepaa as texture_sous_sol,
  p.solwaterph sol_ph,
  p.solstoniness sol_pierrosite_moyenne,
  refsolprof.libelle_classe sol_profondeur_max_enracinement_classe,
  p.solmaxdepth sol_profondeur_max_enracinement,
  p.solorganicmaterialpercent teneur_MO_pct,
  p.solhydromorphisms hydromorphie,
  p.sollimestone calcaire,
  p.soltotallimestone proportion_calcaire_total,
  p.solactivelimestone proportion_calcaire_actif,
  p.solbattance battance,
  d.id as domaine_id,
  gs.topiaid sdc_id,
  p."location" commune_id,
  p.ground domaine_sol_id,
  g.name as sol_nom_ref,
  p.edaplosissuerid as edaplos_utilisateur_id
  FROM plot p
  LEFT JOIN growingsystem gs ON p.growingsystem = gs.topiaid -- on garde dans l'entrepot les parcelles qui ne sont pas rattachées à un sdc
  JOIN entrepot_domaine d on p."domain" = d.id -- fusion pour n'obtenir que les domaines actifs
  JOIN plot_zone pz ON pz.plot = p.topiaid
  left join refsolprofondeurindigo refsolprof ON refsolprof.topiaid = p.soldepth 
  left join refsoltexturegeppa reftextu on reftextu.topiaid = p.surfacetexture 
  left join refsoltexturegeppa reftextu2 on reftextu2.topiaid = p.subsoiltexture
  left join ground g on p.ground = g.topiaid
  WHERE (
  	(gs.topiaid in (select distinct id from entrepot_sdc)) -- on vérifie que le sdc associé est actif
  	OR 
  	gs.active is null -- pour garder aussi les parcelles non attachee a un sdc
  )
  AND p.active IS true;

DO $$
BEGIN
    BEGIN
        alter table entrepot_parcelle
        ADD CONSTRAINT parcelle_PK
        primary key (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;

alter table entrepot_parcelle
add FOREIGN KEY (domaine_id) REFERENCES entrepot_domaine(id);

alter table entrepot_parcelle
add FOREIGN KEY (sdc_id) REFERENCES entrepot_sdc(id);

alter table entrepot_parcelle
add FOREIGN KEY (domaine_sol_id) REFERENCES entrepot_domaine_sol(id);

alter table entrepot_parcelle
add FOREIGN KEY (commune_id) REFERENCES entrepot_commune(id);


