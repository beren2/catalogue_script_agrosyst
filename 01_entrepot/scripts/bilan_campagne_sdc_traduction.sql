DROP TABLE if exists entrepot_bc_sdc_traduction;
CREATE TABLE entrepot_bc_sdc_traduction(
	nom_rubrique text, 
	nom_base text,
	traduction_interface text);
	
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de pression maladie ravageur assolee','NONE','Nulle (absence)');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de pression maladie ravageur assolee','LOW','Faible (un peu mais pas d''impact)');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de pression maladie ravageur assolee','MODERATE','Moyenne (impact sur le rendement possible)');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de pression maladie ravageur assolee','HIGH','Forte (impact certain sur le rendement et la marge)');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise maladie ravageur assolee','NONE','Aucun symptome ou presence');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise maladie ravageur assolee','LOW','Symptomes sans effet sur le rendement');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise maladie ravageur assolee','MODERATE','Rendement un peu affecté sans effet sur la marge de la culture');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise maladie ravageur assolee','HIGH','Pertes économiques sur la culture');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise maladie ravageur arbo','NONE','Aucun symptôme');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise maladie ravageur arbo','LOW','Symptômes sans effet sur le rendement ou la qualité');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise maladie ravageur arbo','MODERATE','Symptômes avec effet très limité sur le rendement et la qualité');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise maladie ravageur arbo','HIGH','Pertes économiques dues à des dégâts sur fruits, feuilles, ou arbres');

insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie feuille','ZERO','0% de ceps touchés, 0% d intensité d attaque');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie feuille','FROM_0_TO_10_2_INTENSITY','0 à 10 % de ceps touchés, moins de 2% d intensité d attaque');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie feuille','FROM_10_TO_35_2_INTENSITY','10 à 35 % de ceps touchés, moins de 2% d intensité d attaque');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie feuille','FROM_35_TO_70_2_INTENSITY','35 à 70 % de ceps touchés, moins de 2% d intensité d attaque');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie feuille','FROM_70_TO_100_2_INTENSITY','70 à 100 % de ceps touchés, moins de 2% d intensité d attaque');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie feuille','FROM_35_TO_70_2_TO_5_INTENSITY','35 à 70 % de ceps touchés, 2 à 5% d intensité d attaque');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie feuille','FROM_70_TO_100_2_TO_5_INTENSITY','70 à 100 % de ceps touchés, 2 à 5% d intensité d attaque');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie feuille','FROM_70_TO_100_5_TO_15_INTENSITY','70 à 100 % de ceps touchés, 5 à 15% d intensité d attaque');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie feuille','FROM_70_TO_100_15_TO_25_INTENSITY','70 à 100 % de ceps touchés, 15 à 25% d intensité d attaque');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie feuille','FROM_70_TO_100_25_INTENSITY','70 à 100 % de ceps touchés, > 25% d intensité d attaque');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie grappe','ZERO','0% de ceps touchés, 0% d intensité d attaque');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie grappe','FROM_0_TO_10_2_INTENSITY','0 à 10 % de ceps touchés, moins de 2% d intensité d attaque');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie grappe','FROM_10_TO_35_2_INTENSITY','10 à 35 % de ceps touchés, moins de 2% d intensité d attaque');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie grappe','FROM_35_TO_70_2_INTENSITY','35 à 70 % de ceps touchés, moins de 2% d intensité d attaque');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie grappe','FROM_70_TO_100_2_INTENSITY','70 à 100 % de ceps touchés, moins de 2% d intensité d attaque');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie grappe','FROM_35_TO_70_2_TO_5_INTENSITY','35 à 70 % de ceps touchés, 2 à 5% d intensité d attaque');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie grappe','FROM_70_TO_100_2_TO_5_INTENSITY','70 à 100 % de ceps touchés, 2 à 5% d intensité d attaque');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie grappe','FROM_70_TO_100_5_TO_15_INTENSITY','70 à 100 % de ceps touchés, 5 à 15% d intensité d attaque');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie grappe','FROM_70_TO_100_15_TO_25_INTENSITY','70 à 100 % de ceps touchés, 15 à 25% d intensité d attaque');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque maladie grappe','FROM_70_TO_100_25_INTENSITY','70 à 100 % de ceps touchés, > 25% d intensité d attaque');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque ravageurs feuille','NONE','pas de dégâts');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque ravageurs feuille','LOW','attaque faible');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque ravageurs feuille','MODERATE','attaque moyenne');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque ravageurs feuille','HIGH','attaque forte');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque ravageurs grappe','NONE','pas de dégâts');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque ravageurs grappe','LOW','attaque faible');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque ravageurs grappe','MODERATE','attaque moyenne');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('Note globale attaque ravageurs grappe','HIGH','attaque forte');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle pression adventice viti','NONE','sol nu');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle pression adventice viti','LOW','sol globalement nu avec toutefois quelques taches, sans gravité ni concurrence hydrique');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle pression adventice viti','MODERATE','enherbement sans concurrence hydrique');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle pression adventice viti','HIGH','enherbement generalise (voulu ou accidentel) avec baisse de vigeur et rendement');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de pression maladie ravageur viti','NONE','Nulle (absence)');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de pression maladie ravageur viti','LOW','Faible (un peu mais pas d''impact)');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de pression maladie ravageur viti','MODERATE','Moyenne (impact sur le rendement possible)');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de pression maladie ravageur viti','HIGH','Forte (impact certain sur le rendement et la marge)');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('evolution pression viti maladie ravageur','MUCH_HIGHER','Pression beaucoup plus forte que l''annee precedente');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('evolution pression viti maladie ravageur','HIGHER','Pression plus forte que l''annee precedente');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('evolution pression viti maladie ravageur','SAME','Pression identique à l''annee precedente');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('evolution pression viti maladie ravageur','LOWER','Pression plus faible que l''annee precedente');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('evolution pression viti maladie ravageur','MUCH_LOWER','Pression beaucoup plus faible que l''annee precedente');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise maladie ravageur viti','NONE','Aucun symptôme');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise maladie ravageur viti','LOW','Symptômes sans effet sur le rendement ou la qualité');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise maladie ravageur viti','MODERATE','Symptômes avec effet très limité sur le rendement et la qualité');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise maladie ravageur viti','HIGH','Pertes économiques dues à la maladie');

insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('irrigation','NON_IRRIGABLE','Non irrigable');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('irrigation','NOT_IRRIGATED_CROP','Irrigable, culture non irriguée');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('irrigation','IRRIGATED_CROP_LIMITED_QUANTITY','Culture irriguée, quantité limitée');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('irrigation','IRRIGATED_CROP','Culture irriguée');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('stress hydrique mineral temperature','NO_STRESS','Pas de stress');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('stress hydrique mineral temperature','STRESS_NO_IMPACT_YIELD','Stress limité sans impact sur le rendement');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('stress hydrique mineral temperature','STRESS_NO_IMPACT_PROFIT','Stress limité sans impact sur la marge');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('stress hydrique mineral temperature','STRESS_IMPACT_YIELD_PROFIT','Stress impactant le rendement et la marge');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle pression adventice assolee','NONE','Nulle (absence)');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle pression adventice assolee','LOW','Faible (presence sporadique)');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle pression adventice assolee','MODERATE','Moyenne (premiers ronds)');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle pression adventice assolee','HIGH','Forte (concurrence en voie de generalisation)');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise adventice assolee','NONE','Pas de presence');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise adventice assolee','LOW','Presence sans concurrence ni multiplication significative (sous couvert ou sur couvert)');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise adventice assolee','MODERATE','Presence de premiers ronds de concurrence directe sur ou sous couvert (avec risque de multiplication futur)');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise adventice assolee','HIGH','Concurrence en voie de generalisation (multication des zones ou "ronds") sous ou sur couvert cultive');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de risque verse','NONE','Pas de risque');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de risque verse','LOW','Risque faible (un peu mais pas d''impact)');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de risque verse','MODERATE','Risque moyenne (impact sur le rendement possible)');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de risque verse','HIGH','Risque fort (impact certain sur le rendement et la marge)');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise verse','NONE','Pas de verse');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise verse','LOW','Un peu de verse sans effet sur le rendement');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise verse','MODERATE','Verse sans effet sur la marge de la culture');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise verse','HIGH','Verse impactant la performance economique');

insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise arbo adv','NONE','Sol propre toute la saison');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise arbo adv','LOW','Sol propre à certaines periodes (recolte)');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise arbo adv','MODERATE','Enherbement permanent sans concurrence hydrique');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de maitrise arbo adv','HIGH','Enherbement permanent avec concurrence (eau,vigueur,coloration …)');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('evolution enherbement arbo adv','MUCH_HIGHER','Enherbement beaucoup plus fort que l''annee precedente');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('evolution enherbement arbo adv','HIGHER','Enherbement plus fort que l''annee precedente');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('evolution enherbement arbo adv','SAME','Enherbement identique à l''annee precedente');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('evolution enherbement arbo adv','LOWER','Enherbement plus faible que l''annee precedente');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('evolution enherbement arbo adv','MUCH_LOWER','Enherbement beaucoup plus faible que l''annee precedente');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de pression maladie ravageur arbo','NONE','Nulle (absence)');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de pression maladie ravageur arbo','LOW','Faible (un peu mais pas d''impact)');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de pression maladie ravageur arbo','MODERATE','Moyenne (impact sur le rendement possible)');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('echelle de pression maladie ravageur arbo','HIGH','Forte (impact certain sur le rendement et la marge)');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('evolution pression arbo maladie ravageur','MUCH_HIGHER','Pression beaucoup plus forte que l''annee precedente');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('evolution pression arbo maladie ravageur','HIGHER','Pression plus forte que l''annee precedente');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('evolution pression arbo maladie ravageur','SAME','Pression identique à l''annee precedente');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('evolution pression arbo maladie ravageur','LOWER','Pression plus faible que l''annee precedente');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('evolution pression arbo maladie ravageur','MUCH_LOWER','Pression beaucoup plus faible que l''annee precedente');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('pct touchee arbo','LESS_0_5','inferieur à 0.5 %');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('pct touchee arbo','FROM_0_5_TO_2','0.5 à 10 %');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('pct touchee arbo','FROM_2_TO_10','2 à 50 %');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('pct touchee arbo','FROM_10_TO_50','10 à 50 %');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('pct touchee arbo','MORE_50','superieur à 50 %');

insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('objectif rendement echelle int','4','LESS_50');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('objectif rendement echelle int','3','FROM_50_TO_75');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('objectif rendement echelle int','2','FROM_75_TO_95');
insert into entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('objectif rendement echelle int','1','MORE_95');
INSERT INTO entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('rendement echelle objectif', 'MORE_95', 'supérieur ou égal 95% de l''objectif');
INSERT INTO entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('rendement echelle objectif', 'FROM_75_TO_95', 'de 75% à 95%');
INSERT INTO entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('rendement echelle objectif', 'FROM_50_TO_75', 'de 50% à 75%'); 
INSERT INTO entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('rendement echelle objectif', 'LESS_50', '< 50%');
INSERT INTO entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('rendement echelle objectif expe', '1', 'supérieur ou égal 95% de l''objectif');
INSERT INTO entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('rendement echelle objectif expe', '2', 'de 50% à 75%');
INSERT INTO entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('rendement echelle objectif expe', '3', 'de 75% à 95%');
INSERT INTO entrepot_bc_sdc_traduction(nom_rubrique,nom_base,traduction_interface) VALUES ('rendement echelle objectif expe', '4', '< 50%');

DO $$
BEGIN
    BEGIN
		alter table entrepot_bc_sdc_traduction
		add constraint entrepot_bc_sdc_traduction_PK
		PRIMARY KEY (nom_rubrique,nom_base);
    EXCEPTION
        WHEN others THEN
            RAISE WARNING '⚠ Impossible de créer la primary key : %', SQLERRM;
    END;
END $$;