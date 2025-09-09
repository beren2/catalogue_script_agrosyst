CREATE TABLE entrepot_fertilisation_organique AS
select 
	r.topiaid as id,
	r.idtypeeffluent as type_effluent,
	r.libelle,
	r.teneur_ferti_orga_n_total as n,
	r.teneur_ferti_orga_p as p,
	r.teneur_ferti_orga_k as k,
	r.teneur_ferti_orga_cao as cao,
	r.teneur_ferti_orga_mgo as mgo, 
	r.teneur_ferti_orga_s as s,
	r.unite_teneur_ferti_orga as unite_teneur
from reffertiorga r
where r.active is true;

DO $$
BEGIN
    BEGIN
		alter table entrepot_fertilisation_organique
		add constraint fertilisation_organique_PK
		PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;
