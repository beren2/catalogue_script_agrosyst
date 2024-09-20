CREATE TABLE entrepot_synthetise AS
select
ps.topiaid id,
ps."name" nom,
ps.campaigns campagnes,
ps."source" source,
ps."comment" commentaire,
ps.practicedplot parcelle_type_id,
ps.growingsystem sdc_id,
ps.validated as valide
from practicedsystem ps
join entrepot_sdc es on es.id = ps.growingsystem 
where ps.active = true;

alter table entrepot_synthetise
add constraint synthetise_PK
PRIMARY KEY (id);

--alter table entrepot_synthetise
--ADD FOREIGN KEY (parcelle_type_id) REFERENCES entrepot_parcelle_type(id);

alter table entrepot_synthetise
ADD FOREIGN KEY (sdc_id) REFERENCES entrepot_sdc(id);


 


