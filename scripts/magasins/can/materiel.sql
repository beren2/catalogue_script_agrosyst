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
    em.ref_materiel_id as materiel_ref_id,
    em.id as materiel_id,
    em.materiel_eta_cuma,
    em.materiel_caracteristique1,
    em.materiel_caracteristique2,
    em.materiel_caracteristique3,
    em.materiel_caracteristique4,
    em.utilisation_annuelle,
    em.utilisation_annuelle_unite,
    em.cout_par_unite_travail_annuel
from entrepot_materiel em
left join entrepot_combinaison_outil eco on eco.tracteur_materiel_id = em.id 
left join entrepot_domaine ed on ed.id = em.domaine_id
join entrepot_domaine_filtres_outils_can edifoc on ed.id = edifoc.id
where em.categorie_materiel in ('Automoteur', 'Tracteur')
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
    em.ref_materiel_id as materiel_ref_id,
    em.id as materiel_id,
    em.materiel_eta_cuma,
    em.materiel_caracteristique1,
    em.materiel_caracteristique2,
    em.materiel_caracteristique3,
    em.materiel_caracteristique4,
    em.utilisation_annuelle,
    em.utilisation_annuelle_unite,
    em.cout_par_unite_travail_annuel
from entrepot_materiel em 
left join entrepot_combinaison_outil_materiel ecom on ecom.materiel_id = em.id
left join entrepot_combinaison_outil eco on eco.id = ecom.combinaison_outil_id
left join entrepot_domaine ed on ed.id = em.domaine_id
join entrepot_domaine_filtres_outils_can edifoc on ed.id = edifoc.id
where em.categorie_materiel in ('Outil', 'Irrigation');