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
    emat.id as materiel_ref_id,
    em.id as materiel_id,
    em.appartient_eta_cuma as materiel_eta_cuma,
    em.nom as materiel_nom,
    emat.type_materiel_1 as materiel_caracteristique1,
    emat.type_materiel_2 as materiel_caracteristique2,
    emat.type_materiel_3 as materiel_caracteristique3,
    emat.type_materiel_4 as materiel_caracteristique4,
    emat.utilisation_annuelle,
    emat.utilisation_annuelle_unite,
    emat.charges_fixes_par_unite_de_volume_de_travail_annuel as cout_par_unite_travail_annuel 
from entrepot_composant_parc_materiel em
left join entrepot_combinaison_outil eco on eco.tracteur_composant_parc_materiel_id = em.id 
left join entrepot_domaine ed on ed.id = em.domaine_id
left join entrepot_materiel emat on emat.id = em.materiel_id
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
    emat.id as materiel_ref_id,
    em.id as materiel_id,
    em.appartient_eta_cuma as materiel_eta_cuma,
    em.nom as materiel_nom,
    emat.type_materiel_1 as materiel_caracteristique1,
    emat.type_materiel_2 as materiel_caracteristique2,
    emat.type_materiel_3 as materiel_caracteristique3,
    emat.type_materiel_4 as materiel_caracteristique4,
    emat.utilisation_annuelle,
    emat.utilisation_annuelle_unite,
    emat.charges_fixes_par_unite_de_volume_de_travail_annuel as cout_par_unite_travail_annuel 
from entrepot_composant_parc_materiel em 
left join entrepot_combinaison_outil_composant_parc_materiel ecom on ecom.composant_parc_materiel_id = em.id
left join entrepot_combinaison_outil eco on eco.id = ecom.combinaison_outil_id
left join entrepot_domaine ed on ed.id = em.domaine_id
left join entrepot_materiel emat on emat.id = em.materiel_id
join entrepot_domaine_filtres_outils_can edifoc on ed.id = edifoc.id
where em.categorie in ('Outil', 'Irrigation');