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
#test_2()

# 3e partie : implémentation de la méthode pour savoir où placer les données lorsque plusieurs utilisateurs sont intéressés par la même donnée

def placement_donnees_multi(liste_donnees:list[Donnees], liste_utilisateurs:list[Utilisateurs]):
    """
    Cette fonction permet de placer les données du système dans les bon noeuds en fonction des intérêts des utilisateurs.
    Elle prend comme paramètre :
    - la liste des données existantes,
    - la liste des utilisateurs
    """
    # on identifie la donnée qui intéresse deux utilisateurs
    donnees_1=liste_utilisateurs[0].get_liste_interet()
    donnees_2=liste_utilisateurs[1].get_liste_interet()

    #on récupère les données communes :
    """
    donnees_communes=list[Donnees]
    for donnee1 in donnees_1:
        if donnee1 in donnees_2 :
            donnees_communes.append(donnee1)
    """

    # cas où il ya une seule donnée commune aux deux utilisateurs
    for donnee in donnees_1 :
        if donnee in donnees_2:
            donnee_commune=donnee
        else :
            donnee_commune=None
            print("Pas de donnée commune")

    # on commence par placer les données en fonction du 1e utilisateur :
    placement_donnees(liste_donnees, [gillian])
    print("id de la donnée commune : ",donnee_commune.get_id())

    # fait la liste de tous les noeuds accessibles par les utilisateurs : 
    liste_noeuds=[]
    for utilisateur in liste_utilisateurs:
        noeuds=utilisateur.get_liste_noeuds_accessible()
        for noeud in noeuds :
            if noeud not in liste_noeuds :
                liste_noeuds.append(noeud)

    # on cherche maintenant où la donnée commune a été placée
    for noeud in liste_noeuds :
        if donnee_commune in noeud.get_liste_donnees():
            noeud_commun=noeud
            print("id du noeud qui contient la donnée commune : ", noeud_commun.get_id())

    # on calcule maintenant le chemin le plus cours entre ce noeud et l'utilisateur :
    print("\nCalcul de la distance entre le noeud commun et le 1e utilisateur :")
    chemin_1=chemin_le_plus_court(noeud_commun, liste_utilisateurs[0])
    
    # on calcule maintenant le chemin le plus cours entre ce noeud et le 2e utilisateur :
    print("\nCalcul de la distance entre le noeud commun et le 2e utilisateur :")
    chemin_2=chemin_le_plus_court(noeud_commun, liste_utilisateurs[1])

    if abs(len(chemin_1)-len(chemin_2))<=1: # on regarde si la distance qui sépare le noeud commun des deux utilisateurs est égale à un noeud prêt :
        print("\nLe temps d'accès au noeud commun est minimal pour les deux utilisateurs")
    else : # si c'est pas le cas, il va falloir déplacer la donnée.
        print("Le chemin n'est pas minimal pour les deux utilisateurs, il faut déplacer la donnée commune dans un autre noeud")

        #### RESTE A FAIRE ####
    print("Revoir chemin le plus court avec de la récursion")



def chemin_le_plus_court(noeud_commun:Noeuds_systeme, utilisateur:Utilisateurs) ->list[Noeuds_systeme]:
    """ Fonction qui permet de calculer le chemin le plus court entre un noeud et un utilisateur """
    liste_noeuds=[]
    noeud_direct=utilisateur.get_noeud_direct()
    if noeud_commun==noeud_direct :
        print("Le noeud est le noeud direct de l'utilisateur.")
        liste_noeuds.append(noeud_direct) 
    elif noeud_commun in noeud_direct.get_liste_noeuds_accessibles():
        print("Le noeud est voisin à celui direct de l'utilisateur : un seul noeud sépart l'utilisateur du noeud recherché.")
        print("id noeud direct : ", noeud_direct.get_id())
        print("id noeud commun : ", noeud_commun.get_id())
        liste_noeuds.append(noeud_direct)
        liste_noeuds.append(noeud_commun)
    else :
        for noeud in noeud_direct.get_liste_noeuds_accessibles():
            if noeud_commun in noeud.get_liste_noeuds_accessibles():
                liste_noeuds.append(noeud_direct)
                liste_noeuds.append(noeud)
                liste_noeuds.append(noeud_commun)
                print("coucou")
            print("Le noeud est séparer par deux autres noeuds de l'utilisateur")
            print("id noeud direct : ", noeud_direct.get_id())
            print("id noeud : ", noeud.get_id())
            print("id noeud commun : ", noeud_commun.get_id())           
    return liste_noeuds


def test_3():
    liste_donnees=[vtt, route, chat, chien, soleil, pluie, vent]
    liste_utilisateurs=[gillian, emma]

    print("Noeud 1 : "+ noeud_1.toString())
    print("Noeud 2 : "+ noeud_2.toString())
    print("Noeud 3 : "+noeud_3.toString())

    print("Placement des données lorsqu'il y a un intérêt commun en cours")
    #ajout des données dans les noeuds
    placement_donnees_multi(liste_donnees, liste_utilisateurs)
test_3()