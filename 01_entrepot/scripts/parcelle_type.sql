CREATE TABLE entrepot_parcelle_type AS
select
pp.topiaid id,
pp.name nom,
pp.area surface,
pp.pacilotnumber num_ilot_pac,
pp.latitude,
pp.longitude,
pp.comment commentaire,
pp.maxslope pente_max,
pp.waterflowdistance distance_cours_eau,
pp.bufferstrip bande_enherbee,
pp.activityendcomment motif_fin_utilisation,
------ Informations sur le zonage de la parcelle
pp.outofzoning hors_zonage, 
pp.zoningcomment commentaire_zonage,
------ onglet equipements
pp.equipmentcomment equipement_commentaire, 
pp.irrigationsystem systeme_irrigation,
pp.irrigationsystemtype systeme_irrigation_type,
pp.pompenginetype pompe_type,
pp.hosespositionning positionnement_tuyaux_arrosage,
pp.waterorigin eau_origine,
pp.fertigationsystem systeme_fertirrigation,
pp.drainage drainage,
pp.drainageyear drainage_annee_realisation,
pp.frostprotection protection_antigel,
pp.frostprotectiontype protection_antigel_type,
pp.hailprotection protection_antigrele,
pp.pestprotection protection_antiinsecte,
pp.rainproofprotection protection_antipluie,
pp.otherequipment equipement_autre,
------ Onglet sol
pp.solcomment commentaire_sol,
pp.surfacetexture as texture_surface_id,
pp.subsoiltexture as texture_sous_sol_id,
pp.solstoniness pierrosite_moyenne,
refsolprof.libelle_classe sol_profondeur_max_enracinement_classe,
pp.solmaxdepth sol_profondeur_max_enracinement,
pp.solorganicmaterialpercent teneur_MO_pct,
pp.solbattance battance,
pp.solwaterph ph,
pp.solhydromorphisms hydromorphie,
pp.sollimestone calcaire,
pp.soltotallimestone proportion_calcaire_total,
pp.solactivelimestone proportion_calcaire_actif,
pp.location commune_id
from practicedplot pp 
left join refsolprofondeurindigo refsolprof on refsolprof.topiaid = pp.soldepth
where pp.active is true;

alter table entrepot_parcelle_type
add constraint parcelle_type_PK
PRIMARY KEY (id);

alter table entrepot_parcelle_type
ADD FOREIGN KEY (commune_id) REFERENCES entrepot_commune(id);

-- Zonage de la parcelle
drop table if exists entrepot_parcelle_type_zonage;

CREATE TABLE entrepot_parcelle_type_zonage AS
select
bp.basicplot parcelle_type_id,
r.libelle_engagement_parcelle as libelle_zonage
from basicplot_plotzonings bp
join entrepot_parcelle_type ept on ept.id = bp.basicplot 
join refparcellezonageedi r on r.topiaid = bp.plotzonings ;

alter table entrepot_parcelle_type_zonage
ADD FOREIGN KEY (parcelle_type_id) REFERENCES entrepot_parcelle_type(id);

alter table entrepot_parcelle_type_zonage
add constraint parcelle_type_zonage_PK
PRIMARY KEY (parcelle_type_id,libelle_zonage);

-- Voisinage de la parcelle
drop table if exists entrepot_parcelle_type_voisinage;

CREATE TABLE entrepot_parcelle_type_voisinage AS
select
ab.basicplot parcelle_type_id,
r.iae_nom as libelle_voisinage
from adjacentelements_basicplot ab 
join entrepot_parcelle_type ept on ept.id = ab.basicplot 
join refelementvoisinage r on r.topiaid = ab.adjacentelements ;

alter table entrepot_parcelle_type_voisinage
ADD FOREIGN KEY (parcelle_type_id) REFERENCES entrepot_parcelle_type(id);

alter table entrepot_parcelle_type_voisinage
add constraint parcelle_type_voisinage_PK
PRIMARY KEY (parcelle_type_id,libelle_voisinage);
