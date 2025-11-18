CREATE TABLE entrepot_troupeau AS
  select 
  trp.topiaid as id,
  trp.code,
  trp.numberofheads as nb_de_tete,
  rcat.animaltype as type_troupeau,
  trp.livestockunit as elevage_id
  from cattle trp
  join refcattleanimaltype rcat on rcat.topiaid = trp.animaltype
  join livestockunit l on l.topiaid = trp.livestockunit
  join entrepot_domaine d on d.id = l."domain" --fusion pour n'obtenir que des aliments/ration/troupeau de domaines actifs
  ;

DO $$
BEGIN
    BEGIN
    alter table entrepot_troupeau
    add constraint troupeau_PK
    PRIMARY KEY (id);
    -- EXCEPTION
    --     WHEN others THEN
    --         RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;

alter table entrepot_troupeau
ADD FOREIGN KEY (elevage_id) REFERENCES entrepot_atelier_elevage(id);