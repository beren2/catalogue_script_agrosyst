select
    ------ CONTEXTE/IDENTIFIANTS
    recolte_id as harvesting_id,
    intervention_id as intervention_id,
    zone_id as plot_id,
    itk_id as cms_id,
	sdc_id as cs_id,
	domaine_id as farm_id,
    mode_saisie as data_input_method,
    ------- RECOLTE
    recolte_rendement as yield,
    recolte_unite as yield_unit,
    recolte_destination as yield_destination,
    ------- ESPECE/CULTURE
	typodirodur_espece as species_typology,
	typodirodur_espece_precise as species_precise_typology,
	typodirodur_espece_famille_bota as species_botanical_family,
	typodirodur_espece_periode_semis as species_theoritical_sowing_season,
	typodirodur_culture as crop_typology,
    variete_libelle as variety_label,
    ------- DATES
    intervention_date_debut as date_intervention_start,
    intervention_date_fin as date_intervention_end,
    ------- GEOGRAPHIE
    domaine_position_code_insee as city_insee_code,
	domaine_position_nom_commune as city_name,
	domaine_position_departement as department,
	domaine_position_region as region,
	domaine_position_ancienne_region as ex_region,
    ------ ALERTES
    destination_est_conforme as warning_destination_is_faithful,
	unite_est_conforme as warning_unit_is_faithful,
	espece_est_conforme as warning_species_is_faithful
from entrepot_rendement_dirodur_temporary;