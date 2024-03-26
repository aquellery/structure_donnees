# Axelle ROY

## PROJ631 : Projet algorithmique
## Stockage de données personnelles

# 2e partie : implémentation de la méthode pour savoir où placer les données

from structure_donnees import *

def placement_donnees(liste_donnees:list[Donnees], liste_utilisateurs:list[Utilisateurs]):
    """
    Cette fonction permet de placer les données du système dans les bon noeuds en fonction des intérêts des utilisateurs.
    Elle prend comme paramètre :
    - la liste des données existantes,
    - la liste des utilisateurs
    """
    for utilisateur in liste_utilisateurs : #on commence par placer les données qui intéressent des utilisateurs
        print("*-*-*-*-*-*-*-Changement d'utilisateur-*-*-*-*-*-*-")
        print('Utilisateur : ', utilisateur.id)
        print(utilisateur.toStringInteret())
        
        liste_interet=utilisateur.get_liste_interet()
        liste_interet.sort(key=lambda interet:interet.get_id())# on trie la liste de données par id
        noeud_direct=utilisateur.get_noeud_direct() # on récupère le noeud direct de l'utilisateur
        liste_noeud=noeud_direct.get_liste_noeuds_accessibles()
        liste_noeud.insert(0, noeud_direct) #on rajoute le noeud direct au début de la liste 
        print("Données à placer :", len(liste_interet))
        
        for i in range(len(liste_noeud)):
            print("-------Changement de noeud-------")
            noeud=liste_noeud[i]
            #print("noeud ", noeud.get_id())
            #print("données : "+noeud.toStringDonnees())
            for interet in liste_interet : # on prend chaque intéret dans l'ordre des id
                if interet in liste_donnees : #on regarde si la donnée est encore dans la liste des données à placer
                    #print("donnee ", interet.get_id())
                    if interet not in noeud.get_liste_donnees(): #on ne va pas ajouter une donnée déjà présente dans le noeud
                        #print("taille du noeud", noeud.get_id(), " : ", noeud.get_capacite())
                        #print("taille de la donnée", interet.get_id(), " : ", interet.get_taille())
                        #print(interet.get_taille()<=noeud.get_capacite())
                        if interet.get_taille()<=noeud.get_capacite(): #si y'a assez de place dans le noeud
                            noeud.ajouter_donnee(interet) #on ajoute la donnée au noeud                        
                            print("Mise à jour du noeud : "+noeud.toStringDonnees())                          
            for donnee_noeud in noeud.get_liste_donnees() :
                if donnee_noeud in liste_donnees :
                    liste_donnees.remove(donnee_noeud)
            #liste_donnees.remove(noeud.get_liste_donnees())
            print(len(noeud.get_liste_donnees()), "données dans le noeud ", noeud.get_id())
            #print(len(liste_interet), "données à placer dans des noeuds pour l'utilisateur", utilisateur.get_id())
            #print(len(liste_donnees), "données à placer dans des noeuds")

    print("\n------------------------ Fin du placement des données ------------------------\n\n")              
               
### zone de test : trouver le placement d'une donnée dans un noeud ###
def test_2():
    liste_donnees=[vtt, route, chat, chien, soleil, pluie, vent]
    liste_utilisateurs=[gillian, emma]

    print("Noeud 1 : "+ noeud_1.toString())
    print("Noeud 2 : "+ noeud_2.toString())
    print("Noeud 3 : "+noeud_3.toString())

    print("\nPlacement automatique des données en cours\n")
    #ajout des données dans les noeuds
    placement_donnees(liste_donnees, liste_utilisateurs)

    print("Données du noeud 1 : "+ noeud_1.toStringDonnees())
    print("Données du noeud 2 : "+ noeud_2.toStringDonnees())
    print("Données du noeud 3 : "+noeud_3.toStringDonnees())
test_2()

