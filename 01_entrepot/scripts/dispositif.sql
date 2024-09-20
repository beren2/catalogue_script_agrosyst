CREATE TABLE entrepot_dispositif AS
  select
    gp.topiaid id,
    gp.code code,
    gp.name nom,
    gp.type "type",
    d.campagne,
    d.id as domaine_id
  FROM growingplan gp
  JOIN entrepot_domaine d on gp."domain" = d.id -- fusion pour n'obtenir que les domaines actifs
  WHERE gp.active is True; -- vérification que le dispositif est actif

alter table entrepot_dispositif
add constraint dispositif_PK
PRIMARY KEY (id);

alter table entrepot_dispositif
ADD FOREIGN KEY (domaine_id) REFERENCES entrepot_domaine(id);
