-- clé primaire : (materiel_id, combinaison_outil_id)

-- materiel_id --> peut être du materiel OU un tracteur. 
-- attention : si on compare strictement avec le fichier de la can, on a moins de ligne. 
-- ceci est la conséquence du filtrage dans entrepot_criteres_selection, plus force que celui en place dans exports_agronomes_criteres 
-- (environ 400 domaines de différénce)
select 
    ed.code as domaine_code, 
    ed.id as domaine_id,
    ed.nom as domaine_nom, 
    ed.campagne as domaine_campagne,
    eco.id as combinaison_outil_id,
    eco.code as combinaison_outil_code,
    eco.nom as combinaison_outils_nom,
    em.materiel_id as materiel_ref_id,
    em.id as composant_id,
    em.appartient_eta_cuma,
    em.nom as composant_nom
from entrepot_composant_parc_materiel em
left join entrepot_combinaison_outil eco on eco.tracteur_materiel_id = em.id 
left join entrepot_domaine ed on ed.id = em.domaine_id
join entrepot_domaine_filtres_outils_can edifoc on ed.id = edifoc.id
where em.categorie in ('Automoteur', 'Tracteur')
union all
-- cas 2 : on sélectionne les materiels classiques
select 
    ed.code as domaine_code, 
    ed.id as domaine_id,
    ed.nom as domaine_nom, 
    ed.campagne as domaine_campagne,
    eco.id as combinaison_outil_id,
    eco.code as combinaison_outil_code,
    eco.nom as combinaison_outils_nom,
    em.materiel_id,
    em.id as composant_id,
    em.appartient_eta_cuma,
    em.nom as composant_nom
from entrepot_composant_parc_materiel em 
left join entrepot_combinaison_outil_materiel ecom on ecom.materiel_id = em.id
left join entrepot_combinaison_outil eco on eco.id = ecom.combinaison_outil_id
left join entrepot_domaine ed on ed.id = em.domaine_id
join entrepot_domaine_filtres_outils_can edifoc on ed.id = edifoc.id
where em.categorie in ('Outil', 'Irrigation');