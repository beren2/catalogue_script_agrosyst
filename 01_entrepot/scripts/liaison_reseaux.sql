DROP TABLE IF EXISTS entrepot_liaison_reseaux CASCADE;

CREATE TABLE entrepot_liaison_reseaux AS
select distinct
	np.network as reseau_id,
	np.parents as reseau_parent_id
from network_parents np;

DO $$
BEGIN
    BEGIN
		alter table entrepot_liaison_reseaux
		add constraint liaison_reseaux_PK
		PRIMARY KEY (reseau_id,reseau_parent_id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;