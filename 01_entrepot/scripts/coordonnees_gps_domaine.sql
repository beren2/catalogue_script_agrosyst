CREATE TABLE entrepot_coordonees_gps_domaine AS
  select
  	g.topiaid id,
  	g.name AS nom_coordonnees_centre_operationnel,
    d.id as domaine_id,
    g.description AS coordonnees_description_centre_operationnel,
    g.longitude,
    g.latitude
  FROM geopoint g
  JOIN entrepot_domaine d on d.id = g."domain" --fusion pour n'obtenir que des domaines actifs
  AND g.longitude!=0
  AND g.latitude !=0
  AND g.validated is true;

alter table entrepot_coordonees_gps_domaine
add constraint domaines_coordonnees_gps_PK
PRIMARY KEY (id);

alter table entrepot_coordonees_gps_domaine
ADD FOREIGN KEY (domaine_id) REFERENCES entrepot_domaine(id);
