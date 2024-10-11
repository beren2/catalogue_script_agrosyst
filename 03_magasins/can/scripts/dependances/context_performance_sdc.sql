CREATE TEMPORARY TABLE entrepot_context_performance_sdc AS
with reseaux_agg as (
	select elsr.sdc_id , 
	string_agg(distinct er2.nom, ', ') as nom_reseau_it, 
	string_agg(distinct er.nom,', ') as nom_reseau_ir
	from entrepot_liaison_sdc_reseau elsr 
	join entrepot_reseau er on elsr.reseau_id = er.id
	join entrepot_liaison_reseaux elr on elr.reseau_id = er.id 
	join entrepot_reseau er2 on er2.id = elr.reseau_parent_id
	group by  elsr.sdc_id
)
select 
	ed2.nom as domaine_nom,
	ed2.id as domaine_id, 
	ed2.campagne as domaine_campagne,
	ed2.type_ferme as domaine_type,
	ed2.departement as domaine_departement, 
	r.nom_reseau_it,
	r.nom_reseau_ir,
	ed.id as dispositif_id,
	ed."type" as dispositif_type,
	es.id as sdc_id,
	es.filiere as sdc_filiere, 
	es.nom as sdc_nom,
	es.code_dephy as sdc_num_dephy,
	es.type_agriculture as sdc_type_conduite, 
	es.validite as sdc_valide, 
	es.modalite_suivi_dephy  as sdc_modalite_suivi_dephy
from entrepot_sdc es 
join reseaux_agg r on r.sdc_id = es.id 
join entrepot_dispositif ed on ed.id = es.dispositif_id 
join entrepot_domaine ed2 on ed2.id = ed.domaine_id;