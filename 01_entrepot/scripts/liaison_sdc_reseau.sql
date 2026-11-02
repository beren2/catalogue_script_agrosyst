DROP TABLE IF EXISTS entrepot_liaison_sdc_reseau CASCADE;

CREATE TABLE entrepot_liaison_sdc_reseau AS
select 
	gn.growingsystem as sdc_id,
	gn.networks as reseau_id
from growingsystem_networks gn;

DO $$
BEGIN
    BEGIN
		alter table entrepot_liaison_sdc_reseau
		add constraint liaison_sdc_reseaux_PK
		PRIMARY KEY (sdc_id,reseau_id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;