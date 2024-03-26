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
            print("id de la donnée commune : ",donnee_commune.get_id())
            print("id du noeud qui contient la donnée commune : ", noeud_commun.get_id())

    # on calcule maintenant le chemin le plus cours entre ce noeud et l'utilisateur :
    print("\nCalcul de la distance entre le noeud commun et le 1e utilisateur :")
    chemin_1=chemin_le_plus_court(noeud_commun, utilisateur1)
    
    # on calcule maintenant le chemin le plus cours entre ce noeud et le 2e utilisateur :
    print("\nCalcul de la distance entre le noeud commun et le 2e utilisateur :")
    chemin_2=chemin_le_plus_court(noeud_commun, utilisateur2)

    if abs(len(chemin_1)-len(chemin_2))<=1: # on regarde si la distance qui sépare le noeud commun des deux utilisateurs est égale à un noeud prêt :
        print("\nLe temps d'accès au noeud commun est minimal pour les deux utilisateurs")
    else : # si c'est pas le cas, il va falloir déplacer la donnée dans un autre noeud
        print("Le chemin n'est pas minimal pour les deux utilisateurs, il faut déplacer la donnée commune dans un autre noeud")
        # on regarde quel utilisateur est le plus éloigné de la donnée :
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
        noeud_milieu:Noeuds_systeme=noeud_au_milieu(utilisateur_pret, utilisateur_loin)

        # on enlève la donnée de son noeud
        if donnee_commune in noeud_commun.get_liste_donnees() :
            noeud_commun.supprimer_donnee(donnee_commune)

        # on essaie de placer la donnée commune au milieu des deux :
        print("\nPlacement de la donnée commune au point le plus stratégique")
        donnee_placee=placement_donnee(donnee_commune, noeud_milieu)
        i=0
        while not donnee_placee or  len(chemin_court)>len(chemin_long) or i<len(chemin_court):
            i+=1 # pour ne pas rentrer dans une boucle infernale, si après avoir parcouru tous les noeuds on ne peut pas déplacer la donnée alors on la laisse à sa place
            # si on ne peut pas, on essaie de la rapprocher de l'utilisateur qui en était le plus éloigné
            noeuds_voisins=[]
            for nouveau_noeud in noeud_milieu.get_liste_noeuds_accessibles() :
                noeuds_voisins.append(nouveau_noeud)
                print("noeud voisin : ", nouveau_noeud.get_id())
            for noeud in noeuds_voisins :
                if not donnee_placee :
                    donnee_placee=placement_donnee(donnee_commune, noeud)
                # on met à jour les nouveaux chemins pour accéder à la donnée :
                chemin_court=chemin_le_plus_court(noeud, utilisateur_pret)
                chemin_long=chemin_le_plus_court(noeud, utilisateur_loin)
                if donnee_placee:
                    break
            if donnee_placee :
                break
        if not donnee_placee : #si on sort du while parce qu'aucune place convenait bien, on remet la donnée là où elle était
            noeud_commun.ajouter_donnee(donnee_commune)
        print("\nLa donnée commune est à la place la mieux adaptée")

def chemin_le_plus_court(noeud:Noeuds_systeme, utilisateur:Utilisateurs)->list[Noeuds_systeme]:
    """Fonction recursif qui permet de trouver le chemin le plus court entre un noeud et un utilisateur"""

    noeud_direct=utilisateur.get_noeud_direct()

    def chemin_entre_deux_noeuds(noeud_visite:Noeuds_systeme,  noeud:Noeuds_systeme, chemins_possibles:list[Noeuds_systeme], liste_visite:list[Noeuds_systeme], chemin)->list[Noeuds_systeme]:
        liste_visite.append(noeud_visite)
        if noeud_visite.get_id()==noeud.get_id():
            chemin=[noeud_visite]
            chemins_possibles.append(chemin)
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
        chemin_final=min(chemins_possibles, key=len)
        chemin_final.append(noeud)
        liste_id=[noeud.get_id() for noeud in chemin_final]
        print("Le chemin entre le noeud ", noeud_direct.get_id(), " et le noeud ", noeud.get_id(), " est en passant par les noeuds", liste_id)
        return chemin_final
        
def noeud_au_milieu(utilisateur1:Utilisateurs, utilisateur2:Utilisateurs):
    """Fonction qui renvoie le noeud au milieu des deux utilisateurs """
    # on va commencer par calculer le chemin le plus court entre le noeud accessible de l'utilisateur 1 et l'utilisateur 2.
    noeud_direct_1=utilisateur1.get_noeud_direct()
    chemin1=chemin_le_plus_court(noeud_direct_1, utilisateur2)

    # on va faire pareil en sens inverse
    noeud_direct_2=utilisateur2.get_noeud_direct()
    chemin2=chemin_le_plus_court(noeud_direct_2, utilisateur1)

    if len(chemin1)!=len(chemin2):
        print("bizarre")
    
    else : #on récupère le noeud au milieu du chemin1 (ça devrait être le même que celui du chemin2)
        noeud_1=chemin1[len(chemin1)//2]
        noeud_2=chemin1[len(chemin2)//2]
        if noeud_1!=noeud_2 :
            print("bizarre, les noeuds au milieu de sont pas identiques")
        else :
            return noeud_2

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
