DROP TABLE IF EXISTS entrepot_commune CASCADE;

CREATE TABLE entrepot_commune AS
select 
refl.topiaid id,
refl.codeinsee,
refl.commune ,
refl.petiteregionagricolecode ,
refl.petiteregionagricolenom ,
refl.departement ,
refl.codepostal ,
refl.region ,
refl.latitude ,
refl.longitude ,
refl.altitude_moy,
refl.aire_attr,
refl.arrondissement_code,
refl.bassin_vie,
refl.intercommunalite_code,
refl.unite_urbaine,
refl.zone_emploi,
refl.bassin_viticole,
refl.ancienne_region,
refp.frenchname nom_francais
from reflocation refl 
join refcountry refp on refl.refcountry = refp.topiaid 
where refl.active = true;

DO $$
BEGIN
    BEGIN
        alter table entrepot_commune
        add constraint entrepot_commune_PK
        PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;
