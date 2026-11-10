## Data paper sur Datagrosyst

### Définition

Un datapaper consiste en une restructuration d'un magasin Datagrosyst. Par restructuration, on entend :
- sélection de colonnes (suppression des données inutiles)
- renommage de colonnes (passage en anglais par exemple)

### Sur l'interface 

Les data papers sont téléchargeables sur Datagrosyst uniquement par les administrateurs de la plateforme. Les autres utilisateurs sont redirigés, grâce à la documentation, sur le répertoire externe de la publication.

### Déployer un data paper sur Datagrosyst

Déployer un data paper nécessite plusieurs configuration, assurez-vous donc :

1. d'ajouter une nouvelle ligne dans la table `entrepot_category`. La colonne `magasin_dependance` doit pointer vers la catégorie associée au magasin auquel est lié le data paper.
**Si vous n'avez pas encore créé de magasin vous ne pouvez pas créer de data paper.**

2. d'ajouter autant de lignes dans la table `entrepot_table` que vous ne souhaitez généré de tables dans votre data paper. La colonne `magasin_dependance` doit pointer vers la table du magasin permettant de générer la table (votre fichier sql de l'étape 4. devra consister en un **select** de cette table).

3. d'ajouter autant de ligne dans la table `entrepot_column` que vous ne souhaitez avoir de colonne (même procédure que pour l'entrepôt, les outils et les magasins).

4. d'ajouter au [catalogue_script_agrosyst](https://github.com/beren2/catalogue_script_agrosyst/issues) dans le répertoire [04_datapaper](https://github.com/beren2/catalogue_script_agrosyst/tree/main/04_datapaper/), les script SQL de sélection et de renommage de votre magasin. **Ceux-ci doivent porter le même nom que le **label** des tables ajoutées dans `entrepot_table` et être rangé dans le répertoire `04_datapaper/{nom_du_magasin}/`**

> Le fichier SQL peut sélectionner la table temporaire indiquée dans la colonne `magasin_dependance` de `entrepot_table` (*exemple : "SELECT sdc_id from sdc_magasin_dirodur" pour le magasin dirodur*) donc prendre en entrée les colonnes exportées. 

5. d'ajouter les restrictions pour vous assurer que seuls les administrateurs de Datagrosyst pourront accéder aux fichiers mis à jour.

6. redémarrer l'instance datagrosyst et téléchargez branche souhaitée depuis le profil administrateur pour mettre à jour les scripts de génération.


Exemple de documentation dans le cadre du datapaper DiRoDur
``` SQL
INSERT INTO public.entrepot_source (id,"label",explication,is_active,"order")
	VALUES ('datapapers','datapapers','TODO',true,3);

INSERT INTO public.entrepot_category (id,"label",explication,is_active,background_color,"order","source",documentation_markdown,magasin_dependance)
	VALUES ('dirodur_datapaper','DiRoDur','TODO',true,'#38b49b',0,'datapapers','## TODO','dirodur');

INSERT INTO public.entrepot_table (id,"label",explication,category_id,is_active,"order",required_right,"generated",magasin_dependance)
	VALUES ('sdc_dirodur_datapaper','sdc','test','dirodur_datapaper',true,0,0,true,'sdc_magasin_dirodur');

INSERT INTO public.entrepot_column (id,"label",explication,sensible_column,table_id,is_active,"order")
	VALUES ('sdc_dirodur_datapaper_cs_id','cs_id','cs_id',false,'sdc_dirodur_datapaper',true,0);

```

