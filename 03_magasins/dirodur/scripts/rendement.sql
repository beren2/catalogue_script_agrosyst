-- En réalisé
select * from entrepot_rendement_realise_dirodur errd
join entrepot_itk_filtre eif on (errd.noeud_id = eif.noeuds_realise_id and errd.culture_id = eif.culture_id)
union all
select * from entrepot_rendement_synthetise_dirodur ersd
join entrepot_itk_filtre eif on (ersd.connexion_id = eif.connection_synthetise_id);


