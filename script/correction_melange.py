"""La fonction correction_melange est un exemple de fonction de pré-traitement des données agrosyst.
Elle permet de corriger la colonne "melange_especes" de la table culture en  :
- vérifiant que la culture associée est bien un mélange d'espèces si melange_especes est à True
- vérifiant que la culture associée n'est pas un mélange d'espèces si melange_especes est à False
Cette correction est nécessaire car la colonne "melange_especes" a été rajoutée tardivement (2021)
"""

import pandas as pd

def correction_melange(data):
    """"
    	data : dictionnaire avec au moins 3 clés : ["culture", "composant", "espece"]
        data['culture'] 	  : 	df de 3 colonnes ["culture_id", "melange_especes"]
        data['composant'] 	:	  df de 3 colonnes ["composant_id", "culture_id", "espece_id"]
        data['espece'] 		  : 	df de 2 colonnes ["espece_id", "nom"]
    """
    df_culture = data['culture']
    df_composant = data['composant']

    #on groupe le composants par culture_id
    df_composant_par_culture = df_composant[['culture_id', 'espece_id']].groupby('culture_id')

    #on compte le nombre de composant par culture
    left = df_culture[['culture_id', 'melange_especes']]
    right = df_composant_par_culture.size().reset_index().rename(columns={0 : 'espece_count'})
    merge = pd.merge(left=left, right=right, on = 'culture_id', how = 'left')

    #on corrige la valeur de melange_especes en fonction du nombre de mélanges trouvés.
    merge.loc[merge['espece_count'] > 1, 'melange_especes'] = True

    #on corrige la valeur de melange_especes en fonction du nombre de mélanges trouvés.
    merge.loc[merge['espece_count'] > 1, 'melange_especes'] = True

    df_culture[["culture_id", "melange_especes"]] = merge[["culture_id", "melange_especes"]]

    data['culture'] = df_culture

    return data
