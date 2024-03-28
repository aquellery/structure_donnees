# Axelle ROY

## PROJ631 : Projet algorithmique
## Stockage de données personnelles

# 2e partie : implémentation de la méthode pour savoir où placer les données
# 4e partie : faite en même temps : on a pas une seule donnée par noeud

# on récupère tout ce qui a été fait dans structure_donnees : les classes et les objets créés
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
            for interet in liste_interet : # on prend chaque intéret dans l'ordre des id
                if interet in liste_donnees : #on regarde si la donnée est encore dans la liste des données à placer
                    if interet not in noeud.get_liste_donnees(): #on ne va pas ajouter une donnée déjà présente dans le noeud
                        if interet.get_taille()<=noeud.get_capacite(): #si y'a assez de place dans le noeud
                            noeud.ajouter_donnee(interet) #on ajoute la donnée au noeud                        
                            print("Mise à jour du noeud : "+noeud.toStringDonnees())                          
            for donnee_noeud in noeud.get_liste_donnees() :
                if donnee_noeud in liste_donnees :
                    liste_donnees.remove(donnee_noeud)
            print(len(noeud.get_liste_donnees()), "données dans le noeud ", noeud.get_id())

    print("\n------------------------ Fin du placement des données ------------------------\n\n")              
               
### zone de test : trouver le placement d'une donnée dans un noeud ###
def test_2():
    #affichage des noeuds avant l'ajout des données pour pouvoir comparer les résultats
    print(toStringDonneesNoeuds(liste_noeuds))

    print("\nPlacement automatique des données en cours\n")
    #ajout des données dans les noeuds
    placement_donnees(liste_donnees, liste_utilisateurs)

    #affichage des noeuds après ajout des données
    print(toStringDonneesNoeuds(liste_noeuds))

#test_2()

###########################################################################
###########################################################################
###########################################################################
###########################################################################
    
# 3e partie : implémentation de la méthode pour savoir où placer les données lorsque plusieurs utilisateurs sont intéressés par la même donnée

def placement_donnees_multi(liste_donnees:list[Donnees], liste_utilisateurs:list[Utilisateurs]):
    """
    Cette fonction permet de placer les données du système dans les bon noeuds en fonction des intérêts des utilisateurs.
    Elle prend comme paramètre :
    - la liste des données existantes,
    - la liste des utilisateurs
    """
    # on travaille avec deux utilisateurs
    utilisateur1=liste_utilisateurs[0]
    utilisateur2=liste_utilisateurs[1]
    # on identifie la donnée qui intéresse deux utilisateurs
    donnees_1=utilisateur1.get_liste_interet()
    donnees_2=utilisateur2.get_liste_interet()

    # on fait la liste de tous les noeuds accessibles par les utilisateurs : 
    liste_noeuds=[]
    for utilisateur in liste_utilisateurs:
        noeuds=utilisateur.get_liste_noeuds_accessible()
        for noeud in noeuds :
            if noeud not in liste_noeuds :
                liste_noeuds.append(noeud)

    # on récupère les données communes :
    """
    # cas où les deux utilisateurs pourraient avoir plusieurs données communes
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

    # on commence par placer les données automatiquement 
    placement_donnees(liste_donnees, liste_utilisateurs)

    # on affiche les données présentes dans les noeuds pour pouvoir comparer le placement des données 
    print("Données placées automatiquement : ")
    print(toStringDonneesNoeuds(liste_noeuds))
    print('\n\n')

    # on cherche maintenant où la donnée commune a été placée
    for noeud in liste_noeuds :
        if donnee_commune in noeud.get_liste_donnees():
            noeud_commun:Noeuds_systeme=noeud
            print("La donnée commune a pour id ",donnee_commune.get_id())
            print("Le noeud qui contient la donnée commune a pour id ", noeud_commun.get_id())

    # on calcule maintenant le chemin le plus cours entre ce noeud et l'utilisateur :
    print("\nCalcul de la distance entre le noeud commun et le 1e utilisateur :")
    chemin_1=chemin_le_plus_court(noeud_commun, utilisateur1)
    
    # on calcule maintenant le chemin le plus cours entre ce noeud et le 2e utilisateur :
    print("\nCalcul de la distance entre le noeud commun et le 2e utilisateur :")
    chemin_2=chemin_le_plus_court(noeud_commun, utilisateur2)

    chemin_minimiser=abs(len(chemin_1)-len(chemin_2))<=1
    if chemin_minimiser: # on regarde si la distance qui sépare le noeud commun des deux utilisateurs est égale à un noeud prêt :
        print("\nLe temps d'accès au noeud commun est minimal pour les deux utilisateurs")
    else : # si c'est pas le cas, il va falloir déplacer la donnée dans un autre noeud
        print("Le chemin n'est pas minimal pour les deux utilisateurs, il faut déplacer la donnée commune dans un autre noeud")
        # on regarde quel utilisateur est le plus éloigné de la donnée et quel chemin est le plus long :
        if len(chemin_1)<len(chemin_2):
            utilisateur_pret=utilisateur1
            utilisateur_loin=utilisateur2
            chemin_court=chemin_1
            chemin_long=chemin_2
        elif  len(chemin_1)>len(chemin_2):
            utilisateur_pret=utilisateur2
            utilisateur_loin=utilisateur1
            chemin_court=chemin_2
            chemin_long=chemin_1
        # on calcul quel noeud est placé au milieu des deux utilisateurs
        noeuds_milieu=noeud_au_milieu(utilisateur_pret, utilisateur_loin)
        noeud_milieu=noeuds_milieu[0]

        # on enlève la donnée de son noeud
        if donnee_commune in noeud_commun.get_liste_donnees() :
            noeud_commun.supprimer_donnee(donnee_commune)

        # on essaie de placer la donnée commune au milieu des deux :
        print("\nPlacement de la donnée commune au point le plus stratégique")
        donnee_placee=placement_donnee(donnee_commune, noeud_milieu)
        if len(noeuds_milieu)>1 and not donnee_placee: # si la donnée n'a pas pu être placée, on regarde si un deuxième noeud est considéré voisin (dans le cas d'une liste paire)
            donnee_placee=placement_donnee(donnee_commune, noeuds_milieu[1])
        i=0
        while (not donnee_placee) and (not chemin_minimiser) and i<len(chemin_court):
            # si la donnée a été placée et que le chemin est minimiser on arrête de chercher un autre placement pour la donnée
            i+=1 # pour éviter de rentrer dans une boucle infinie : si on a parcouru tous les noeuds mais que le chemin n'est pas minimisé ou que la donnée avait aucune autre place alors on sort de la boucle
            noeuds_voisins=[]
            for nouveau_noeud in noeud_milieu.get_liste_noeuds_accessibles() :
                noeuds_voisins.append(nouveau_noeud)
            for noeud in noeuds_voisins :
                if not donnee_placee :
                    donnee_placee=placement_donnee(donnee_commune, noeud)
                # on met à jour les nouveaux chemins pour accéder à la donnée :
                # de cette façon, on peut vérifier que la donné ne vient pas se placer à un endroit plus avantageux pour un autre utilisateur
                chemin_court=chemin_le_plus_court(noeud, utilisateur_pret)
                chemin_long=chemin_le_plus_court(noeud, utilisateur_loin)
                chemin_minimiser=abs(len(chemin_court)-len(chemin_long))<=1
                if donnee_placee and chemin_minimiser :#or len(chemin_court)>len(chemin_long):
                    break
            if donnee_placee and chemin_minimiser :#or len(chemin_court)>len(chemin_long):
                break
        if not donnee_placee and not chemin_minimiser: #si on sort du while parce qu'aucune place convenait bien, on remet la donnée là où elle était
            placement_donnee(donnee_commune, noeud_commun)
        print("\nLa donnée commune est à la place la mieux adaptée")

def chemin_le_plus_court(noeud:Noeuds_systeme, utilisateur:Utilisateurs)->list[Noeuds_systeme]:
    """Fonction recursif qui permet de trouver le chemin le plus court entre un noeud et un utilisateur"""

    noeud_direct=utilisateur.get_noeud_direct()

    def chemin_entre_deux_noeuds(noeud_visite:Noeuds_systeme,  noeud:Noeuds_systeme, chemins_possibles:list[Noeuds_systeme], liste_visite:list[Noeuds_systeme], chemin)->list[Noeuds_systeme]:
        liste_visite.append(noeud_visite)
        if noeud_visite.get_id()==noeud.get_id():
            chemin=[noeud_visite]
            chemins_possibles.append(chemin.copy())
            return chemins_possibles
        if noeud in noeud_visite.get_liste_noeuds_accessibles():
            if noeud_visite not in chemin : # à partir d'une récurrence il est déjà dedans 
                chemin.append(noeud_visite)
            chemins_possibles.append(chemin)
            return chemins_possibles
        for noeud_voisin in noeud_visite.get_liste_noeuds_accessibles():
            if noeud_visite not in chemin : # à partir d'une récurrence il est déjà dedans 
                chemin.append(noeud_visite)
            if noeud_voisin not in liste_visite : # on regarde qu'on l'a pas déjà vu
                nouveau_chemin=chemin
                if noeud_voisin not in chemin :
                    nouveau_chemin.append(noeud_voisin)
                chemins_possibles=chemin_entre_deux_noeuds(noeud_voisin, noeud, chemins_possibles, liste_visite, nouveau_chemin)
        return chemins_possibles
        
    chemins_possibles=chemin_entre_deux_noeuds(noeud_direct, noeud, [], [], [])
    if not chemins_possibles :
        raise ValueError("Il n'y a pas de chemin possible")
    if len(chemins_possibles)!=0:
        chemin_final:list[Noeuds_systeme]=min(chemins_possibles, key=len)
        chemin_final.append(noeud)
        # en cas de boucle de noeud, le chemin va garder prendre le noeud qui a la plus grande capacité
        for noeud1 in chemin_final :
            for noeud2 in chemin_final :
                if noeud1.get_id()!=noeud2.get_id():
                    if set(noeud1.get_liste_noeuds_accessibles()).issubset(set(noeud2.get_liste_noeuds_accessibles())):
                        if noeud1.get_capacite()<noeud2.get_capacite():
                            noeud_a_enlever=noeud1
                        else :
                            noeud_a_enlever=noeud2
                        liste_id=[noeud.get_id() for noeud in chemin_final]
                        print("liste avant suppresison : ", liste_id)
                        chemin_final.remove(noeud_a_enlever)

        #on remet les noeuds dans le bon sens
        id_d=chemin_final[0].get_id()
        id_a=chemin_final[-1].get_id()
        if id_d<id_a :   # noeuds par ordre d'id croissant             
            chemin_trie=sorted(chemin_final, key=lambda n: n.get_id())
        else : # noeuds par ordre d'id décroissants
            chemin_trie=sorted(chemin_final, key=lambda n: n.get_id(), reverse=True)
        liste_id=[noeud.get_id() for noeud in chemin_trie]
        print("Le chemin entre le noeud ", noeud_direct.get_id(), " et le noeud ", noeud.get_id(), " est en passant par les noeuds", liste_id)
        return chemin_trie

 ####### GPT #######
def chemin_le_plus_court_gptt(noeud: Noeuds_systeme, utilisateur: Utilisateurs) -> list[Noeuds_systeme]:
    """Fonction récursive qui permet de trouver le chemin le plus court entre un nœud et un utilisateur"""

    noeud_direct = utilisateur.get_noeud_direct()

    def chemin_entre_deux_noeuds(noeud_visite: Noeuds_systeme, noeud_destination: Noeuds_systeme, liste_visite: list[Noeuds_systeme], chemin_actuel: list[Noeuds_systeme]) -> list[Noeuds_systeme]:
        # Ajouter le nœud visité à la liste des nœuds visités
        liste_visite.append(noeud_visite)
        
        # Si le nœud visité est le nœud de destination, retourner le chemin actuel
        if noeud_visite.get_id() == noeud_destination.get_id():
            return chemin_actuel + [noeud_destination]
        
        # Initialiser une liste pour stocker les chemins possibles
        chemins_possibles = []
        
        # Parcourir les nœuds voisins du nœud visité
        for noeud_voisin in noeud_visite.get_liste_noeuds_accessibles():
            # Vérifier si le nœud voisin n'a pas été visité précédemment pour éviter les boucles infinies
            if noeud_voisin not in liste_visite:
                # Explorer récursivement le chemin entre le nœud voisin et le nœud de destination
                nouveau_chemin = chemin_entre_deux_noeuds(noeud_voisin, noeud_destination, liste_visite.copy(), chemin_actuel + [noeud_visite])
                nouveau_chemin = chemin_entre_deux_noeuds(noeud_voisin, noeud_destination, liste_visite.copy(), chemin_actuel + [noeud_visite])
                if nouveau_chemin:
                    chemins_possibles.append(nouveau_chemin)
        
        # Retourner le chemin le plus court parmi les chemins possibles
        if chemins_possibles:
            return min(chemins_possibles, key=len)
        else:
            return None

    # Appeler la fonction récursive pour trouver le chemin le plus court entre le nœud direct et le nœud de destination
    chemin_final = chemin_entre_deux_noeuds(noeud_direct, noeud, [], [])
    
    # Vérifier si un chemin a été trouvé
    if chemin_final:
        liste_id = [noeud.get_id() for noeud in chemin_final]
        print("Le chemin entre le nœud", noeud_direct.get_id(), "et le nœud", noeud.get_id(), "est en passant par les nœuds", liste_id)
        return chemin_final
    else:
        raise ValueError("Il n'y a pas de chemin possible")
        
def noeud_au_milieu(utilisateur1:Utilisateurs, utilisateur2:Utilisateurs)->list[Noeuds_systeme]:
    """Fonction qui renvoie le noeud au milieu des deux utilisateurs """
    # on va commencer par calculer le chemin le plus court entre le noeud accessible de l'utilisateur 1 et l'utilisateur 2.
    noeud_direct_1=utilisateur1.get_noeud_direct()
    chemin1=chemin_le_plus_court(noeud_direct_1, utilisateur2) #chemin le plus court entre l'utilisateur le plus prêt de la donnée commune et l'utilisateur le plus éloigné

    # on va faire pareil en sens inverse
    noeud_direct_2=utilisateur2.get_noeud_direct()
    chemin2=chemin_le_plus_court(noeud_direct_2, utilisateur1) #chemin entre l'utilisateur éloigné et l'utilisateur proche de la donnée

    if len(chemin1)!=len(chemin2):
        print("bizarre")
    
    else : #on récupère le noeud au milieu du chemin1 (ça devrait être le même que celui du chemin2)
        noeuds_1=[]
        noeuds_2=[]
        if len(chemin1)%2==0 : #si on a un nombre de noeud paire, on prend les deux noeuds d'avant et après le milieu
            noeuds_1.append(chemin1[len(chemin1)//2])
            noeuds_1.append(chemin1[len(chemin1)//2+1])
            noeuds_2.append(chemin2[len(chemin2)//2-1])
            noeuds_2.append(chemin2[len(chemin2)//2])
        elif len(chemin1)%2!=0 : #si on a un nombre de noeud impaire, on peut prendre celui du milieu
            noeuds_1.append(chemin1[len(chemin1)//2])
            noeuds_2.append(chemin2[len(chemin2)//2])

        for noeud in noeuds_1 :
            print("noeuds voisins pour l'utilisateur prêt : ", noeud.get_id())
        return noeuds_2 # on s'intéresse au chemin effectué par l'utilisateur le plus éloigné 

def placement_donnee(donnee:Donnees, noeud:Noeuds_systeme)->bool:
    #si la donnée est déjà dans le noeud on essaie pas de la replacer dans ce noeud
    if donnee in noeud.get_liste_donnees():
        print("La donnée est déjà dans le noeud ", noeud.get_id())

    # si le noeud a la capacité d'accueillir la donnée alors on la déplace.
    if noeud.get_capacite()>=donnee.get_taille():
        print("La donnée a été déplacée dans le noeud", noeud.get_id())
        noeud.ajouter_donnee(donnee)
        return True
    else :
        print("Le noeud ", noeud.get_id(), " ne peut pas prendre la donnée commune")
        return False
       
def test_3():

    #affichage des noeuds brut pour pouvoir comparé
    print(toStringDonneesNoeuds(liste_noeuds))
    print("Placement des données lorsqu'il y a un intérêt commun en cours")
    #ajout des données dans les noeuds
    placement_donnees_multi(liste_donnees, liste_utilisateurs)

    #affichage des noeuds après ajout des données
    print(toStringDonneesNoeuds(liste_noeuds))

test_3()
