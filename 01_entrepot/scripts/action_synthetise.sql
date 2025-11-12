CREATE TABLE entrepot_action_synthetise AS
SELECT 
aa.topiaid id,
refintrav.intervention_agrosyst "type",
refintrav.reference_label as label,
aa."comment" commentaire,
aa.proportionoftreatedsurface proportion_surface_traitee,
-- semences
aa.yealdtarget semence_objectif_rendement,
aa.yealdunit semence_objectif_rendement_unite,
-- travail du sol
aa.tillagedepth profondeur_travail_sol,
aa.othersettingtool autre_outils_reglage,
-- Application de produits avec AMM 
aa.boiledquantity bouillie_volume_moy_hl,
aa.boiledquantitypertrip bouillie_volume_moy_parvoyage_hl,
aa.antidriftnozzle buse_anti_derive_pulverisateur,
aa.tripfrequency nb_voyage_parheure, -- est aussi utilise pour les actions transports
-- Transport
aa.loadcapacity volume_chargement_voyage,
aa.capacityunit volume_chargement_voyage_unite,
-- Fertilisation minerale
case when aa.burial is not null then aa.burial -- l'un est pour les epandages organiques et l'autre ferti min
    when aa.landfilledwaste is not null then aa.landfilledwaste
    when aa.burial is null and aa.landfilledwaste then aa.burial
end enfouissement_dans_24h,
aa.localizedspreading apport_localise,
-- Irrigation
aa.waterquantityaverage eau_qte_moy_mm,
aa.waterquantitymin eau_qte_min_mm,
aa.waterquantitymax eau_qte_max_mm,
aa.waterquantitymedian eau_qte_med_mm,
aa.azotequantity azote_qte_kg_ha,
-- Paturage
aa.pasturetype type_paturage,
aa.pastureload paturage_tete_ha,
aa.pasturingatnight paturage_presence_nuit,
aa.cattlecode atelier_elevage_code,
--aa.deepness, = la profondeur de semis avant le local a intrant qui a été déplacé aux usages 
eis.id intervention_synthetise_id
FROM abstractaction aa
JOIN refinterventionagrosysttravailedi refintrav ON aa.mainaction = refintrav.topiaid
JOIN practicedintervention pi on pi.topiaid = aa.practicedintervention
JOIN entrepot_intervention_synthetise eis on eis.id = aa.practicedintervention ;

DO $$
BEGIN
    BEGIN
        alter table entrepot_action_synthetise
        add constraint action_synthetise_PK
        PRIMARY KEY (id);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;

alter table entrepot_action_synthetise
ADD FOREIGN KEY (intervention_synthetise_id) REFERENCES entrepot_intervention_synthetise(id);
