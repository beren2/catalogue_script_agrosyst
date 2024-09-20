CREATE TABLE entrepot_materiel AS
SELECT 
e.topiaid as id,
e.code,
e."name" as nom,
d.campagne,
CASE e.materieleta
      WHEN true THEN 'oui'
      WHEN false THEN 'non'
END materiel_ETA_CUMA,
case 
	when e.refmateriel like '%Traction%' then 'Tracteur'
	when e.refmateriel like '%Automoteur%' then 'Automoteur'
	when e.refmateriel like '%Outil%' then 'Outil'
	when e.refmateriel like '%Irrigation%' then 'Irrigation'
end categorie_materiel,
rm.topiaid as ref_materiel_id,
rm.idtypemateriel type_materiel,
rm.typemateriel1 as materiel_caracteristique1,
rm.typemateriel2 as materiel_caracteristique2,
rm.typemateriel3 as materiel_caracteristique3,
rm.typemateriel4 as materiel_caracteristique4,
rm.uniteparan as utilisation_annuelle,
rm.unite as utilisation_annuelle_unite,
rm.chargesfixesparunitedevolumedetravailannuel AS cout_par_unite_travail_annuel,
d.id as domaine_id
FROM equipment e
JOIN entrepot_domaine d on e."domain" = d.id -- obtention uniquement des domaines actifs
JOIN refmateriel rm ON e.refmateriel = rm.topiaid;

alter table entrepot_materiel
add constraint materiel_PK
PRIMARY KEY (id);

alter table entrepot_materiel
ADD FOREIGN KEY (domaine_id) REFERENCES entrepot_domaine(id);
