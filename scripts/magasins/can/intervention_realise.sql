-- On génère d'abord la table agrégée complète
CREATE TEMPORARY TABLE entrepot_intervention_realise_agrege AS
SELECT DISTINCT 
    nuirac.intervention_realise_id AS id, 
    nuirac.plantation_perenne_realise_id, 
    nuirac.zone_id, 
    nuirac.noeuds_realise_id, 
    nuirac.plantation_perenne_phases_realise_id, 
    nuirac.parcelle_id, 
    nuirac.sdc_campagne, 
    nuirac.sdc_id, 
    nuirac.domaine_id, 
    nuirac.dispositif_id
FROM
    entrepot_intervention_realise eir 
LEFT JOIN "entrepot_utilisation_intrant_realise_agrege" nuirac on eir.id = nuirac.intervention_realise_id
UNION 
SELECT 
    id, 
    plantation_perenne_realise_id, zone_id, noeuds_realise_id, plantation_perenne_phases_realise_id, parcelle_id, sdc_campagne, sdc_id, domaine_id, dispositif_id
FROM entrepot_intervention_realise_manquant_agrege;

SELECT 
    d.code as domaine_code,
    d.id as domaine_id,
    d.nom as domaine_nom,
    d.campagne as domaine_campagne,
    sdc.code as sdc_code,
    sdc.id as sdc_id,
    sdc.nom as sdc_nom,
    p.id as parcelle_id,
    p.nom as parcelle_nom,
    z.id as zone_id,
    z.nom as zone_nom, 
    z.code as zone_code, 
    pppr.id as phase_id, 
    pppr.type as phase,
    c.id as culture_id, 
    replace(replace(c.nom,CHR(13)||CHR(10),'<br>'), CHR(10), '<br>') as culture_nom,
    cr.culture_intermediaire_id as ci_id,
    replace(replace(c_intermediaire.nom,CHR(13)||CHR(10),'<br>'), CHR(10), '<br>') as ci_nom,
    CASE ir.concerne_ci WHEN true THEN 'oui' WHEN false THEN 'non' END concerne_la_ci,
    iroc.espece_de_l_intervention as especes_de_l_intervention,
	iroc.precedent_id,
    replace(replace(iroc.precedent_nom,CHR(13)||CHR(10),'<br>'), CHR(10), '<br>'),
	iroc.precedent_especes_edi,
    nr.rang+1 as culture_rang,
    ir.id as intervention_id,
    ir.type as intervention_type,
    iroc.interventions_actions,
    ir.nom as intevention_nom,
    replace(replace(ir.commentaire,CHR(13)||CHR(10),'<br>'), CHR(10), '<br>') as intervention_comment,
    iroc.combinaison_outil_id as combinaison_outils_id,
    replace(replace(iroc.combinaison_outils_nom,CHR(13)||CHR(10),'<br>'), CHR(10), '<br>'),
    iroc.tracteur_ou_automoteur,
    iroc.outils,
    ir.date_debut,
    ir.date_fin,
    ir.freq_spatiale, 
    ir.nombre_de_passage nombre_de_passage,
    ir.psci_intervention as psci
    iroc.proportion_surface_traitee_phyto,
    iroc.psci_phyto, 
    iroc.proportion_surface_traitee_lutte_bio,
    iroc.psci_lutte_bio,
    ir.debit_de_chantier,
    ir.debit_de_chantier_unite, 
    ir.nb_personne_mobili,
    iroc.quantite_eau_mm,
    iroc.especes_semees,
    iroc.densite_semis,
    iroc.unite_semis,
    iroc.traitement_chimique_semis,
    iroc.inoculation_biologique_semis,
    iroc.type_semence
FROM  entrepot_intervention_realise ir
LEFT JOIN entrepot_intervention_realise_agrege ira ON ir.id = ira.id
LEFT JOIN entrepot_intervention_realise_outils_can iroc ON ira.id = iroc.intervention_realise_id
LEFT JOIN entrepot_zone z ON ira.zone_id = z.id
LEFT JOIN entrepot_parcelle p ON ira.parcelle_id = p.id
LEFT JOIN entrepot_sdc sdc ON ira.sdc_id = sdc.id
LEFT JOIN entrepot_domaine d ON ira.domaine_id = d.id
LEFT JOIN entrepot_noeuds_realise nr ON ira.noeuds_realise_id = nr.id
LEFT JOIN entrepot_connection_realise cr ON nr.cible_noeuds_realise_id = nr.id
LEFT JOIN entrepot_culture c ON nr.culture_id = c.id
LEFT JOIN entrepot_culture c_intermediaire ON cr.culture_intermediaire_id = c_intermediaire.id
LEFT JOIN entrepot_plantation_perenne_phases_realise pppr ON ira.plantation_perenne_phases_realise_id = pppr.id;

