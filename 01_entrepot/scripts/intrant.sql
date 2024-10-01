
--------------------
-- Export local à intrant
--------------------
create table entrepot_intrant(
	id character varying(255), 
	type character varying(255),
	type_produit character varying(255),
	domaine_id character varying(255),
	ref_id character varying(255),				-- si disponible l'identifiant de l'intrant de référence
	ref_nom character varying(500),				-- si disponible le nom de l'intrant de référence
	nom_utilisateur text,
	semence_id character varying (255), 				-- si il s'agit d'un traitement phyto concernant une semence --> identifiant de la semence que ce produit phyto traite. 
	lot_semence_bio boolean default false,				-- si le lot de semences est en bio
	lot_semence_culture_id character varying(255),		-- culture concernée par le traiteme
	lot_semence_type character varying(255), 			-- type de semences
	code_amm character varying(500),
	biocontrole boolean default false, 
	n float8, 
	p2o5 float8, 
	k2o float8, 
	bore float8, 
	calcium float8, 
	fer float8, 
	manganese float8, 
	molybdene float8, 
	mgo float8, 
	oxyde_de_sodium float8,
	so3 float8, 
	cuivre float8, 
	zinc float8, 
	cao float8, 
	s float8,
	--unite_teneur_fert_orga character varying(255),
	unite_teneur_fert character varying(500),
	unite_application character varying(500),
	effet_sdn character varying(255), --stimulateur des défenses naturelles
	forme_fert_min character varying(255),
	-- substance_active character varying(255),
	caracteristique_1 character varying(500),
	caracteristique_2 character varying(500),
	caracteristique_3 character varying(500),
	type_intrant_autre character varying(255),
	duree_de_vie character varying(255),
	type_produit_sans_amm character varying(255),
	prix_saisi float8, 
	prix_saisi_unite character varying(500), 
	prix_ref float8,
	prix_ref_unite character varying(255),
	prix_ref_bio float8,
	prix_ref_bio_unite character varying(255)
);

-- AJOUT DES SUBSTRATS : 
insert into entrepot_intrant (id, type, domaine_id, ref_id, nom_utilisateur, prix_saisi, prix_saisi_unite, prix_ref, prix_ref_unite, caracteristique_1, caracteristique_2, unite_application)
select 
	distinct on (dsi.topiaid) dsi.topiaid as id,
	adisu.inputtype as type,
	adisu.domain as domaine_id,
	dsi.refinput as ref_id,
	adisu.inputname as nom_utilisateur,
	ip.price as prix_saisi,
	ip.priceunit as prix_saisi_unite,
	rps.price as prix_ref,
	rps.unit as prix_ref_unite,
	rs.caracteristic1 as caracteristique_1, 
	rs.caracteristic2 as caracteristique_2,
	dsi.usageunit as unite_application
	--riupuc.substrateinputunit
	from domainsubstrateinput dsi
	left join abstractdomaininputstockunit adisu on dsi.topiaid = adisu.topiaid
	left join domain d on adisu.domain = d.topiaid
	left join inputprice ip on adisu.inputprice = ip.topiaid
	left join refsubstrate rs on rs.topiaid = dsi.refinput
	left join refprixsubstrate rps on rps.caracteristic1 = rs.caracteristic1 and rps.caracteristic2 = rs.caracteristic2 and d.campaign = rps.campaign and rps.price != 0;
--

-- AJOUT DES CARBURANTS : 
insert into entrepot_intrant (id, type, domaine_id, nom_utilisateur, prix_saisi, prix_saisi_unite, prix_ref, prix_ref_unite)
select 
	dfi.topiaid as id,
	adisu.inputtype as type,
	adisu.domain as domaine_id,
	adisu.inputname as nom_utilisateur,
	ip.price as prix_saisi,
	ip.priceunit as prix_saisi_unite,
	rpc.price as prix_ref,
	rpc.unit as prix_ref_unite
from domainfuelinput dfi
left join abstractdomaininputstockunit adisu on dfi.topiaid = adisu.topiaid
left join domain d on adisu.domain = d.topiaid
left join inputprice ip on adisu.inputprice = ip.topiaid
left join refprixcarbu rpc on rpc.campaign = d.campaign;
--

-- AJOUT DES IRRIGATIONS :
insert into entrepot_intrant (id, type, domaine_id, nom_utilisateur, prix_saisi, prix_saisi_unite, prix_ref, prix_ref_unite)
select 
	dii.topiaid as id,
	adisu.inputtype as type,
	adisu.domain as domain_id,
	adisu.inputname as nom_utilisateur,
	ip.price as prix_saisi,
	ip.priceunit as prix_saisi_unite,
	rpi.price as prix_ref,
	rpi.unit as prix_ref_unite
from domainirrigationinput dii
left join abstractdomaininputstockunit adisu on dii.topiaid = adisu.topiaid
left join domain d on adisu.domain = d.topiaid
left join inputprice ip on adisu.inputprice = ip.topiaid
left join refprixirrig rpi on rpi.campaign = d.campaign;
--


-- AJOUT DES INTRANTS MINERAUX : 
insert into entrepot_intrant (id, type, domaine_id, ref_id, nom_utilisateur,
	n, p2o5, k2o, bore, calcium, fer, manganese, molybdene, mgo, oxyde_de_sodium, so3, cuivre, zinc, 
	prix_saisi, prix_saisi_unite, prix_ref, prix_ref_unite, effet_sdn, unite_teneur_fert, unite_application, forme_fert_min)
select 	
	dmpi.topiaid as id,
	adisu.inputtype as type,
	adisu.domain as domaine_id,
	dmpi.refinput as ref_id,
	adisu.inputname as nom_utilisateur,
	rfmu.n n,
	rfmu.p2o5 p2o5,
	rfmu.k2o k2o,
	rfmu.bore bore, 
	rfmu.calcium calcium,
	rfmu.fer fer,
	rfmu.manganese manganese,
	rfmu.molybdene molybdene,
	rfmu.mgo mgo,
	rfmu.oxyde_de_sodium oxyde_de_sodium,
	rfmu.so3 so3,
	rfmu.cuivre cuivre,
	rfmu.zinc zinc,
	ip.price as prix_saisi,
	ip.priceunit as prix_saisi_unite,
	(rpfm_n.price*rfmu.n + rpfm_p2o5.price*rfmu.p2o5 + rpfm_k2o.price*rfmu.k2o + rpfm_bore.price*rfmu.bore + rpfm_calcium.price*rfmu.calcium + rpfm_fer.price*rfmu.fer + rpfm_manganese.price*rfmu.manganese + rpfm_molybdene.price*rfmu.molybdene + rpfm_mgo.price*rfmu.mgo + rpfm_oxyde_de_sodium.price*rfmu.oxyde_de_sodium + rpfm_so3.price*rfmu.so3 + rpfm_cuivre.price*rfmu.cuivre + rpfm_zinc.price*rfmu.zinc)/100 as prix_ref,
	rpfm_n.unit as prix_ref_unite,
	dmpi.phytoeffect as effet_sdn,
	'Unités fertilisantes/100kg' unite_teneur_fert,
	dmpi.usageunit as unite_application,
	rfmu.forme as forme_fert_min
from domainmineralproductinput dmpi
left join reffertiminunifa rfmu on dmpi.refinput = rfmu.topiaid
left join abstractdomaininputstockunit adisu on adisu.topiaid = dmpi.topiaid
left join inputprice ip on adisu.inputprice = ip.topiaid
left join domain d on adisu.domain = d.topiaid
left join refprixfertimin rpfm_bore on rpfm_bore."element" = 'BORE' and rpfm_bore.categ = rfmu.categ and rpfm_bore.forme = rfmu.forme and rpfm_bore.campaign = d.campaign
left join refprixfertimin rpfm_calcium on rpfm_calcium."element" = 'CALCIUM' and rpfm_calcium.categ = rfmu.categ and rpfm_calcium.forme = rfmu.forme and rpfm_calcium.campaign = d.campaign
left join refprixfertimin rpfm_cuivre on rpfm_cuivre."element" = 'CUIVRE' and rpfm_cuivre.categ = rfmu.categ and rpfm_cuivre.forme = rfmu.forme and rpfm_cuivre.campaign = d.campaign
left join refprixfertimin rpfm_fer on rpfm_fer."element" = 'FER' and rpfm_fer.categ = rfmu.categ and rpfm_fer.forme = rfmu.forme and rpfm_fer.campaign = d.campaign
left join refprixfertimin rpfm_k2o on rpfm_k2o."element" = 'K2_O' and rpfm_k2o.categ = rfmu.categ and rpfm_k2o.forme = rfmu.forme and rpfm_k2o.campaign = d.campaign
left join refprixfertimin rpfm_manganese on rpfm_manganese."element" = 'MANGANESE' and rpfm_manganese.categ = rfmu.categ and rpfm_manganese.forme = rfmu.forme and rpfm_manganese.campaign = d.campaign
left join refprixfertimin rpfm_mgo on rpfm_mgo."element" = 'MG_O' and rpfm_mgo.categ = rfmu.categ and rpfm_mgo.forme = rfmu.forme and rpfm_mgo.campaign = d.campaign
left join refprixfertimin rpfm_molybdene on rpfm_molybdene."element" = 'MOLYBDENE' and rpfm_molybdene.categ = rfmu.categ and rpfm_molybdene.forme = rfmu.forme and rpfm_molybdene.campaign = d.campaign
left join refprixfertimin rpfm_n on rpfm_n."element" = 'N' and rpfm_n.categ = rfmu.categ and rpfm_n.forme = rfmu.forme and rpfm_n.campaign = d.campaign
left join refprixfertimin rpfm_oxyde_de_sodium on rpfm_oxyde_de_sodium."element" = 'OXYDE_DE_SODIUM' and rpfm_oxyde_de_sodium.categ = rfmu.categ and rpfm_oxyde_de_sodium.forme = rfmu.forme and rpfm_oxyde_de_sodium.campaign = d.campaign
left join refprixfertimin rpfm_p2o5 on rpfm_p2o5."element" = 'P2_O5' and rpfm_p2o5.categ = rfmu.categ and rpfm_p2o5.forme = rfmu.forme and rpfm_p2o5.campaign = d.campaign
left join refprixfertimin rpfm_so3 on rpfm_so3."element" = 'S_O3' and rpfm_so3.categ = rfmu.categ and rpfm_so3.forme = rfmu.forme and rpfm_so3.campaign = d.campaign
left join refprixfertimin rpfm_zinc on rpfm_zinc."element" = 'ZINC' and rpfm_zinc.categ = rfmu.categ and rpfm_zinc.forme = rfmu.forme and rpfm_zinc.campaign = d.campaign;


-- AJOUT DES INTRANTS ORGANICS
insert into entrepot_intrant (id, type, domaine_id, ref_id, ref_nom, nom_utilisateur,
biocontrole, n, p2o5, k2o, cao, s, prix_saisi, prix_saisi_unite, prix_ref, prix_ref_unite, prix_ref_bio, prix_ref_bio_unite, unite_application, unite_teneur_fert)
select 
	dopi.topiaid as id,
	adisu.inputtype as type,
	adisu.domain as domain_id,
	dopi.refinput as ref_id,
	rpfo.nom as ref_nom,
	adisu.inputname as nom_utilisateur,
	dopi.organic as biocontrole,
	dopi.n as n,
	dopi.p2o5 as p2o5,
	dopi.k2o as k2o,
	dopi.cao as cao,
	dopi.s as s,
	ip.price as prix_saisi,
	ip.priceunit as prix_saisi_unite,
	rpfo.price as prix_ref,
	rpfo.unit as prix_ref_unite,
	rpfo_bio.price as prix_ref_bio,
	rpfo_bio.unit as prix_ref_bio_unite,
	dopi.usageunit as unite_application,
	rfo.unite_teneur_ferti_orga as unite_teneur_fert
from domainorganicproductinput dopi
left join abstractdomaininputstockunit adisu on dopi.topiaid = adisu.topiaid
left join domain d on adisu.domain = d.topiaid
left join inputprice ip on adisu.inputprice = ip.topiaid
left join reffertiorga rfo on dopi.refinput = rfo.topiaid
left join refprixfertiorga rpfo on rpfo.campaign = d.campaign and rpfo.idtypeeffluent = rfo.idtypeeffluent and rpfo.organic = false 
left join refprixfertiorga rpfo_bio on rpfo.campaign = d.campaign and rpfo.idtypeeffluent = rfo.idtypeeffluent and rpfo.organic = true;
--


-- AUJOUT DES INTRANTS AUTRES
insert into entrepot_intrant (id, type, domaine_id, ref_id, nom_utilisateur, 
prix_saisi, prix_saisi_unite, prix_ref, prix_ref_unite, type_intrant_autre, duree_de_vie, caracteristique_1, caracteristique_2, caracteristique_3, unite_application)
select 
	doi.topiaid as id,
	adisu.inputtype as type,
	adisu.domain as domain_id,
	doi.refinput as ref_id,
	adisu.inputname as nom_utilisateur,
	ip.price as prix_saisi,
	ip.priceunit as prix_saisi_unite,
	rpa.price as prix_ref,
	rpa.unit as prix_ref_unite,
	roi.inputtype_c0  as type_intrant_autre,
	roi.lifetime as duree_de_vie,
	roi.caracteristic1 as caracteristique_1, 
	roi.caracteristic2 as caracteristique_2,
	roi.caracteristic3 as caracteristique_3,
	doi.usageunit as unite_application
from domainotherinput doi
left join abstractdomaininputstockunit adisu on doi.topiaid = adisu.topiaid
left join domain d on adisu.domain = d.topiaid
left join inputprice ip on adisu.inputprice = ip.topiaid
left join refotherinput roi on roi.topiaid = doi.refinput
left join refprixautre rpa on rpa.campaign = d.campaign and roi.caracteristic1 = rpa.caracteristic1 and roi.caracteristic2 = rpa.caracteristic2 and roi.caracteristic3 = rpa.caracteristic3;
-- 

-- AJOUT DES PRODUITS PHYTOS (INTRANT TYPE = APPLICATION DE PRODUITS PHYTOSANITAIRES / TRAITEMENTS DE SEMENCE / LUTTE BIOLOGIQUE)
insert into entrepot_intrant (id, type, type_produit, domaine_id, ref_id, ref_nom, nom_utilisateur, 
code_amm, biocontrole, prix_saisi, prix_saisi_unite, prix_ref, prix_ref_unite, unite_application, semence_id)
select 
		dppi.topiaid as id,
		adisu.inputtype as type,
		dppi.producttype as type_produit,
		adisu.domain as domain_id,
		dppi.refinput as ref_id,
		ratp.nom_produit as ref_nom,
		adisu.inputname as nom_utilisateur,
		ratp.code_amm as code_amm,
		ratp.nodu biocontrole,
		ip.price as prix_saisi,
		ip.priceunit as prix_saisi_unite,
		rpp.price as prix_ref,
		rpp.unit as prix_ref_unite,
		dppi.usageunit as unite_application,
		dppi.domainseedspeciesinput as semence_id -- si le produit phyto est déclaré sur un traitement de semence, identifiant de la semence sur lequel il est déclaré.
	from domainphytoproductinput  dppi
	left join abstractdomaininputstockunit adisu on dppi.topiaid = adisu.topiaid
	left join domain d on adisu.domain = d.topiaid
	left join inputprice ip on adisu.inputprice = ip.topiaid
	left join refactatraitementsproduit ratp on ratp.topiaid = dppi.refinput
	left join ( -- on ne selectionne que les premières unités rencontrées
		select distinct on (rpp.campaign, rpp.id_produit, rpp.id_traitement) 
		rpp.campaign, rpp.price, rpp.unit, rpp.id_produit, rpp.id_traitement 
		from refprixphyto rpp
	) rpp on (rpp.campaign = d.campaign and rpp.id_produit = ratp.id_produit  and rpp.id_traitement = ratp.id_traitement);


-- AJOUT DES POTS
insert into entrepot_intrant (id, type, domaine_id, ref_id, nom_utilisateur, 
 prix_saisi, prix_saisi_unite, prix_ref, prix_ref_unite, unite_application)
select 
	dpi.topiaid as id,
	adisu.inputtype as type,
	adisu.domain as domain_id,
	dpi.refinput as ref_id,
	adisu.inputname as nom_utilisateur,
	ip.price as prix_saisi,
	ip.priceunit as prix_saisi_unite,
	rpp.price as prix_ref,
	rpp.unit as prix_ref_unite,
	dpi.usageunit as unite_application
from domainpotinput dpi
left join abstractdomaininputstockunit adisu on dpi.topiaid = adisu.topiaid
left join domain d on adisu.domain = d.topiaid
left join inputprice ip on adisu.inputprice = ip.topiaid
left join refpot rp on rp.topiaid = dpi.refinput
left join refprixpot rpp on rpp.campaign = d.campaign and rpp.caracteristic1 = rp.caracteristic1;
-- 



-- AJOUT DES LOTS DE SEMENCES --> INTRANT TYPE = SEMIS
insert into entrepot_intrant (id, type, domaine_id, lot_semence_bio, lot_semence_culture_id, 
nom_utilisateur, lot_semence_type, prix_saisi, prix_saisi_unite, unite_application)
select 
		dsli.topiaid as id,
		adisu.inputtype as type,
		adisu.domain as domaine_id,
		dsli.organic as lot_semence_bio,
		dsli.cropseed as lot_semence_culture_id, 
		adisu.inputname as nom_utilisateur,
		ip.seedtype as lot_semence_type,
		ip.price as prix_saisi,
		ip.priceunit as prix_saisi_unite,
		--dsli. as prix_ref -- pas possible d'obtenir le prix de référence du lot de semence car on a besoin de la proportion des espèces qui le composent, information uniquement disponible à l'intervention. 
		dsli.usageunit as unite_application
	from domainseedlotinput dsli
	left join abstractdomaininputstockunit adisu on dsli.topiaid = adisu.topiaid
	left join domain d on adisu.domain = d.topiaid
	left join inputprice ip on dsli.seedprice = ip.topiaid;
	--left join refactatraitementsproduit ratp on ratp.topiaid = dsli.;
	

alter table entrepot_intrant
add constraint intrant_PK
PRIMARY KEY (id);


