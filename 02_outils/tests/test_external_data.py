"""
    Contient tous les tests effectués sur les données externes. 
    Ces fonctions permettent de s'assurer que les données externes dont dépend le processus 
    de génération sont conformes à ce qui est attendu en entrée.
"""

def check_BDD_donnees_attendues_CAN(donnees):
    """ 
        permet de checker la table BDD_donnees_attendues_CAN, 
        ie de s'assurer qu'elle correspond au format attendu :
        TODO 
    """
    res = (donnees['BDD_donnees_attendues_CAN'].size > 10)
    return res

def typo_especes_typo_culture(donnees):
    """
        permet de checker la table typo_especes_typo_culture,
        ie de s'assurer qu'elle correspond au format attendu :
        TODO
    """
    return True
