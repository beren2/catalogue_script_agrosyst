--------------------
-- SEMENCES
--------------------

-- Cette table pointe vers la table intrant par l'intermédiaire de lot_semence_id 
-- Elle permet d'avoir l'ensemble des informations sur les données "lots de semences" 
-- Chaque ligne représente les informations pour la semence particulière d'une espèce 
-- C'est à ce niveau là qu'on peut calculer des prix


create table entrepot_semence(
	id character varying(255), 
	inoculation_biologique boolean default false,
	traitement_chimique boolean default false,
	bio boolean default false, 
	traitement_semence_id character varying(255), 
	inoculation_biologique_id character varying(255), 
	composant_culture_id character varying(255), 
	type_semence character varying(255),
	prix_saisi float8,
	prix_saisi_unite character varying(255),
	prix_ref float8,
	prix_ref_unite character varying(255),
	lot_semence_id character varying(255) -- lot de semence auquel appartient cette semence particulière
);

-- on insère d'abord sans les prix
insert into entrepot_semence(id, inoculation_biologique, traitement_chimique, bio, composant_culture_id, type_semence, prix_saisi, prix_saisi_unite, prix_ref, prix_ref_unite, lot_semence_id)
	select
		dssi.topiaid as id,
		dssi.biologicalseedinoculation  as inoculation_biologique,
		dssi.chemicaltreatment  as traitement_chimique,
		dssi.organic  as bio,
		dssi.speciesseed  as composant_culture_id,
		dssi.seedtype as type_semence,
		ip.price as prix_saisi,
		ip.priceunit as prix_saisi_unite,
		null as prix_ref,
		null as prix_ref_unite,
		dssi.domainseedlotinput as lot_semence_id
		--dsli.usageunit as unite_application
	from domainseedspeciesinput dssi
	left join abstractdomaininputstockunit adisu on dssi.topiaid = adisu.topiaid
	left join domain d on adisu.domain = d.topiaid
	left join croppingplanspecies cps on cps.topiaid = dssi.speciesseed
	left join refespece re on re.topiaid = cps.species
	left join domainseedlotinput dsli on dsli.topiaid = dssi.domainseedlotinput 
	left join inputprice ip on dssi.seedprice = ip.topiaid;

-- Ajout des cle etrangere vers le local a intrant pour les traitements et inoculation bio 
update entrepot_semence s SET
traitement_semence_id = (case when refacta.id_traitement <> '166' then dppi.topiaid end),
inoculation_biologique_id = (case when refacta.id_traitement = '166' then dppi.topiaid end)
from domainseedspeciesinput dssi
join domainphytoproductinput dppi on dssi.topiaid = dppi.domainseedspeciesinput 
join refactatraitementsproduit refacta on refacta.topiaid = dppi.refinput 
where dssi.topiaid = s.id ;

-- on créé une table temporaire qui contient tous les doublons en fonction des différentes unités. 
drop table if exists semence_all;
create temporary table semence_all as 
select
	dssi.topiaid as id,
	dssi.biologicalseedinoculation  as inoculation_biologique,
	dssi.chemicaltreatment  as traitement_chimique,
	dssi.organic  as bio,
	dssi.speciesseed  as composant_culture_id,
	dssi.seedtype as type_semence,
	ip.price as prix_saisi,
	ip.priceunit as prix_saisi_unite,
	rpe.price  as prix_ref,
	rpe.unit as prix_ref_unite,
	dssi.domainseedlotinput as lot_semence_id
	--dsli.usageunit as unite_application
from domainseedspeciesinput dssi
left join abstractdomaininputstockunit adisu on dssi.topiaid = adisu.topiaid
left join domain d on adisu.domain = d.topiaid
left join croppingplanspecies cps on cps.topiaid = dssi.speciesseed
left join refespece re on re.topiaid = cps.species
left join domainseedlotinput dsli on dsli.topiaid = dssi.domainseedlotinput 
left join inputprice ip on dssi.seedprice = ip.topiaid
left join refinputunitpriceunitconverter riupuc on riupuc.seedplantunit = dsli.usageunit 
left join refprixespece rpe on (rpe.campaign = d.campaign and
	re.code_espece_botanique = rpe.code_espece_botanique and 
	re.code_qualifiant_aee = rpe.code_qualifiant_aee and 
	riupuc.priceunit = rpe.unit and 
	rpe.active = true and 
	rpe.seedtype = dssi.seedtype and
	rpe.treatment = dssi.chemicaltreatment and 
	rpe.organic = dssi.organic);
	

-- on met à jours les lignes qui ne posent pas de problème (prix de référence bien trouvé, et on en garde qu'un par id.)
update entrepot_semence es
set prix_ref = sc.prix_ref,
	prix_ref_unite = sc.prix_ref_unite
from 
	(select 
		distinct on (id) id, inoculation_biologique, traitement_chimique, bio, composant_culture_id, type_semence, prix_saisi, prix_saisi_unite, prix_ref, prix_ref_unite, lot_semence_id from semence_all
		where prix_ref is not null
	) sc
where es.id = sc.id;
		
