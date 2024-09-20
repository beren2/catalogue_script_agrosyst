CREATE TABLE entrepot_acta_dosage_spc AS
SELECT 
r.topiaid as id, 
r.code_amm ,
r.nom_produit ,
r.id_produit ,
r.id_traitement , 
r.code_traitement ,
r.id_culture ,
r.nom_culture ,
r.remarque_culture ,
r.dosage_spc_valeur,
r.dosage_spc_unite ,
r.dosage_spc_commentaire ,
r."source" 
from refactadosagespc r
where active is true
;

alter table entrepot_acta_dosage_spc
add constraint acta_dosage_spc_PK
PRIMARY KEY (id);