CREATE TABLE entrepot_aliment_ration AS
  select 
  al.topiaid as id,
  rt.topiaid as ration_id, 
  rcra.alimenttype as type_aliment,
  al.quantity as quantite_aliment,
  rcra.alimentunit as unite_aliment,
  rt.startinghalfmonth as debut_ration,
  rt.endinghalfmonth as fin_ration,
  trp.topiaid as troupeau_id
  from aliment al
  join ration rt on rt.topiaid = al.ration 
  join refcattlerationaliment rcra on rcra.topiaid = al.aliment
  join cattle trp on trp.topiaid = rt.cattle
  join refcattleanimaltype rcat on rcat.topiaid = trp.animaltype
  join livestockunit l on l.topiaid = trp.livestockunit
  join entrepot_domaine d on d.id = l."domain" --fusion pour n'obtenir que des aliments/ration/troupeau de domaines actifs
  ;

DO $$
BEGIN
    BEGIN
    alter table entrepot_aliment_ration
    add constraint aliment_ration_pk
    PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;

alter table entrepot_aliment_ration
ADD FOREIGN KEY (troupeau_id) REFERENCES entrepot_troupeau(id);