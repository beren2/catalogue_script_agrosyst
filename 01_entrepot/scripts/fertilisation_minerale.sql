CREATE TABLE entrepot_fertilisation_minerale AS
select 
	r.topiaid as id,
	r.categ as categorie,
	r.forme as forme,
	r.n,
	r.p2o5,
	r.k2o,
	r.bore,
	r.calcium,
	r.fer,
	r.manganese,
	r.molybdene,
	r.mgo,
	r.oxyde_de_sodium,
	r.so3,
	r.cuivre,
	r.zinc,
	r.type_produit
from reffertiminunifa r
where r.active is true;

alter table entrepot_fertilisation_minerale
add constraint fertilisation_minerale_PK
PRIMARY KEY (id);

