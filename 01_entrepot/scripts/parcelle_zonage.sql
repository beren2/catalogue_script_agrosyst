-- Zonage de la parcelle
drop table if exists entrepot_parcelle_zonage;

CREATE TABLE entrepot_parcelle_zonage AS
select
bp.basicplot parcelle_id,
r.libelle_engagement_parcelle as libelle_zonage
from basicplot_plotzonings bp
join entrepot_parcelle ep on ep.id = bp.basicplot 
join refparcellezonageedi r on r.topiaid = bp.plotzonings ;

alter table entrepot_parcelle_zonage
ADD FOREIGN KEY (parcelle_id) REFERENCES entrepot_parcelle(id);
