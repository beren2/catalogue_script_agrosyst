CREATE TABLE entrepot_atelier_elevage AS
  SELECT
  l.topiaid as id,
  l.code,
  d.campagne,
  r.animaltype as type_animaux,
  l.livestockunitsize as taille_elevage,
  r.animalpopulationunits as taille_elevage_unite,
  l.permanentgrasslandarea as prairie_permanente_paturee_ha,
  l.temporarygrasslandarea as prairie_temporaire_paturee_ha,
  l.permanentmowedgrasslandarea as prairie_permanente_fauchee_ration_ha,
  l.temporarymowedgrasslandarea as prairie_temporaire_fauchee_ration_ha,
  l.foragecropsarea as production_fourage_ration_ha,
  l.producingfoodarea as production_alim_concentre_rationa_ha, 
  l.holdingstrawarea as production_paille_valoriseatelier_ha,
  l.massselfsustainingpercent as autonomie_massique_atelier_pct,
  l.averagestrawforbedding as paille_pourlitiere_t_an,
  l.averagemanureproduced as production_fumier_t_an,
  l.averageliquideffluent as effluents_liquides_m3_an,
  l.averagecompostedeffluent as effluents_compostes_t_an,
  l.averagemethanisedeffluent as effluents_methanises_t_an,
  l."comment" commentaire,
  d.id as domaine_id
  FROM livestockunit l
  JOIN entrepot_domaine d on d.id = l."domain" --fusion pour n'obtenir que des domaines actifs
  JOIN refanimaltype r ON l.refanimaltype = r.topiaid;

alter table entrepot_atelier_elevage
add constraint atelier_elevage_PK
PRIMARY KEY (id);

alter table entrepot_atelier_elevage
ADD FOREIGN KEY (domaine_id) REFERENCES entrepot_domaine(id);
