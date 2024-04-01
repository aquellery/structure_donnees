# Axelle ROY

## PROJ631 : Projet algorithmique
## Stockage de données personnelles

# 1e partie : implémentation de la structure de données 

class Donnees :
    """
    La classe Donnees permet d'obtenir la structure d'une donnée avec
    - un identifiant unique
    - sa taille.
    Tous les identifiants utilisés sont stockés dans la liste liste_id.
    Chaque donnée créée est aussi stockée dans une lsite liste_donnees.
    Elle comprends les méthodes :
    - get_id,
    - get_taille,
    - get_taille_par_id : permet de récupérer la taille d'une donnée en fonction de son identifiant
    - et getString
    """
    liste_id=[] 
    liste_donnees=[]
    def __init__(self, id:int, taille:int):
        #on vérifie que l'identifiant n'est pas déjà pris
        if id in Donnees.liste_id:
            raise ValueError("L'identifiant "+str(id)+" est déjà utilisé pour une autre donnée")
        self.id=id
        Donnees.liste_id.append(id)

        self.taille=taille
        Donnees.liste_donnees.append(self)
    
    def get_taille(self)-> int:
        return self.taille

    def get_id(self)->int:
        return self.id

    def get_taille_par_id(id)->int:
        for donnee in Donnees.liste_donnees:
            if donnee.get_id()==id :
                return donnee.get_taille()
        if donnee not in Donnees.liste_donnees :
            raise ValueError("L'identifiant "+id+" ne correspond à aucune donnée") 
            
    def toString(self):
        return f"La donnée qui a pour id : {self.id}  est de taille : {self.taille}"
    
class Noeuds_systeme :
    """
    La classe Noeuds_systeme permet d'obtenir la structure d'un noeud avec :
    - un identifiant unique
    - sa capacité
    - une liste des données accessibles depuis ce noeud
    - la liste des noeuds accessibles depuis ce noeud
    Tous les identifiants utilisés sont stockés dans la liste liste_id.
    La classe comprend les méthodes :
    - get_id,
    - get_capacite,
    - get_liste_donnees,
    - get_liste_noeuds_accessibles, 
    - modifier_capacite, 
    - ajouter_donnee : permet d'ajouter une donnée (un id) au noeud si la capacité le permets 
    - supprimer_donnee : permet de supprimer une donnée (id) du noeud 
    """
    liste_id=[]
    def __init__(self, id:int, capacite:int, liste_donnees_locales:list[Donnees], liste_noeuds_accessibles:list['Noeuds_systeme']): #list[Noeud_systeme]
        #on vérifie que l'identifiant n'est pas déjà pris
        if id in Noeuds_systeme.liste_id:
            raise ValueError("L'identifiant "+str(id)+" est déjà utilisé pour un autre noeud")
        self.id=id
        Noeuds_systeme.liste_id.append(id)

        self.capacite=capacite
        capacite_utilisee=0
        for donnee in liste_donnees_locales:
            #on vérifie que chaque identifiant correspond bien à un identifiant d'une instance de Données
            id_donnee=donnee.get_id()
            if id_donnee not in Donnees.liste_id : 
                raise ValueError("L'identifiant "+str(id_donnee)+" ne correspond  pas à un identifiant de données")
            
            # on calcule ensuite la capacité utilisée par toutes les données comprises dans le noeud
            # on récupère la Donnée associée à l'identifiant qu'on a 
            capacite_utilisee+=Donnees.get_taille_par_id(id_donnee)
        #si en ajoutant toutes les données de la liste on a encore de la place dans le noeud, alors on peut ajouter la liste de données au noeud.
        if self.capacite-capacite_utilisee>=0:
            self.liste_donnees_locales=liste_donnees_locales
            if self.capacite-capacite_utilisee==0:
                print("Attention, le noeud "+str(id)+" est plein")
        if self.capacite-capacite_utilisee<0:
            raise  ValueError("Impossible de créer le noeud "+str(id)+" avec la liste de données "+ str(liste_donnees_locales)+" car la capacité n'est pas assez importante.\n"+
                              "Le noeud a une capacité de "+str(self.capacite)+" alors que les données en utilisent "+str(capacite_utilisee)) 
            
        #on vérifie  que les noeuds accessibles sont bien des identifiants d'un noeud déjà existant
        for noeud in liste_noeuds_accessibles :   
            id=noeud.get_id()
            if id not in Noeuds_systeme.liste_id:
                raise ValueError("L'identifiant de noeud "+str(id)+" ne correspond pas à un noeud existant")
        self.liste_noeuds_accessibles=liste_noeuds_accessibles

    def get_id(self)->int:
        return self.id

    def  get_capacite(self)->int:
        return self.capacite
    
    def get_liste_donnees(self)->list[Donnees]:
        return self.liste_donnees_locales
    
    def get_liste_noeuds_accessibles(self)->list['Noeuds_systeme']:
        return self.liste_noeuds_accessibles
    
    def ajouter_noeud_accessible(self, nouveau_noeud:'Noeuds_systeme')->None:
        self.liste_noeuds_accessibles.append(nouveau_noeud)

    def diminuer_capacite(self, capacite_a_enlever:int)->None:
        self.capacite-=capacite_a_enlever
    
    def augmenter_capacite(self, capacite_a_ajouter:int)->None:
        self.capacite+=capacite_a_ajouter

    def ajouter_donnee(self, nouvelle_donnee:Donnees)->None:
        if self.get_capacite()<nouvelle_donnee.get_taille() : #on vérifie qu'il y a assez de place dans le noeud
            raise ValueError("Il n'y a pas assez de place dans le noeud "+ str(self.get_id())+" pour stocker la donnée "+str(nouvelle_donnee.get_id()))
        self.liste_donnees_locales.append(nouvelle_donnee) #on ajoute la donnée
        self.diminuer_capacite(nouvelle_donnee.get_taille()) #on réduit la taille de la capacité disponible
        
    
    def supprimer_donnee(self, donnee:Donnees)->None:
        self.liste_donnees_locales.remove(donnee)
        self.augmenter_capacite(donnee.get_taille()) #on peut réaugmenter la capacité du noeud vu que la suppression de la donnée à libérer de la place


    def toString(self)->str:
        liste_id_donnees=[]
        for donnee in self.liste_donnees_locales:
            liste_id_donnees.append(donnee.get_id())
        liste_id_noeuds=[]
        for noeud in self.liste_noeuds_accessibles:
            liste_id_noeuds.append(noeud.get_id())
        return f"Le Noeud a pour id : {self.id}, a une capacité de : {self.capacite} et a comme données locales la liste d'id de données :{liste_id_donnees} et comme noeuds accessibles la liste : {liste_id_noeuds}"

    def toStringDonnees(self)->str:
        liste_id_donnees=[]
        for donnee in self.liste_donnees_locales:
            liste_id_donnees.append(donnee.get_id())
        return f"Les données présentes dans le noeud {self.id} sont la liste d'id : {liste_id_donnees}"

class Utilisateurs :
    """
    La classe Utilisateurs permet d'obtenir la structure d'un utilisateur avec :
    - un identifiant unique
    - une liste de données d'intérêt
    - le noeud du système auquel il a accès directement
    Tous les identifiants utilisés sont stockés dans la liste liste_id.
    La classe comprend les méthodes :
    - get_id,
    - get_liste_interet, 
    - get_noeud_system_accessible, 
    - modifier_noeud_accessible, 
    - ajouter_donnee_interet,
    - supprimer_donnee_interet,
    - getString
    """
    liste_id=[]
    def __init__(self, id:int, liste_donnees_interet:list[Donnees], noeud_direct:Noeuds_systeme):
        #on vérifie que l'id donné n'est pas déjà utilisé pour un autre noeud
        if id in Utilisateurs.liste_id:
            raise ValueError("L'identifiant "+ str(id)+" est déjà utilisé pour un autre utilisateur")
        self.id=id
        Utilisateurs.liste_id.append(id)

        for donnee in liste_donnees_interet:
            if donnee.get_id() not in Donnees.liste_id :
                raise ValueError("L'identifiant "+str(donnee.get_id())+" ne correspond  pas à un identifiant de données")
            self.liste_donnes_interet=liste_donnees_interet

        if noeud_direct.get_id() not in Noeuds_systeme.liste_id : 
            raise ValueError("L'identifiant "+str(noeud_direct.get_id())+" ne correspond pas à un noeud existant")
        self.noeud_direct=noeud_direct    


    def get_id(self) ->int:
        return self.id
    
    def get_liste_interet(self)->list[Donnees]:
        return self.liste_donnes_interet
    
    def  get_noeud_direct(self)->Noeuds_systeme:
        return self.noeud_direct
    
    def modifier_noeud_direct(self, nouveau_noeud:int):
        self.noeud_direct=nouveau_noeud
    
    def get_liste_noeuds_accessible(self)->list[Noeuds_systeme]:
        return self.noeud_direct.get_liste_noeuds_accessibles()

    def ajouter_donnee_interet(self, nouvelle_donnee:Donnees):
        self.liste_donnes_interet.append(nouvelle_donnee)

    def supprimer_donnee_interet(self, donnee:Donnees):
        self.liste_donnes_interet.remove(donnee)
    
    def toString(self):
        liste_id_donnees=[]
        for donnee in self.liste_donnes_interet:
            liste_id_donnees.append(donnee.get_id())
        return f"L'utilisateur qui a pour id : {self.id} a comme intérêt les données {liste_id_donnees} Son noeud système direct a comme identifiant {self.noeud_direct.get_id()}"

    def toStringInteret(self):
        liste_id_donnees=[]
        for donnee in self.liste_donnes_interet:
            liste_id_donnees.append(donnee.get_id())
        return f"Les données d'intéret de l'utilisateur {self.id} sont la liste d'id : {liste_id_donnees}"


def toStringDonneesNoeuds(liste_noeuds:list[Noeuds_systeme])-> str :
    """Fonction qui permet de renvoyer la liste des données présentes dans chaque noeuds de la liste passée en paramètre"""
    res=""
    for noeud in liste_noeuds :
        ligne=noeud.toStringDonnees()
        res+=ligne+'\n'
    return res

####################################################################################
####################################################################################
#                      ZONE DE CREATION DES OBJETS                                 #
####################################################################################
####################################################################################

# création de données, de noeuds et d'utilisateurs ###
vtt=Donnees(id=1, taille=5)
route=Donnees(id=2, taille=4)
chat=Donnees(id=3, taille=30)
chien=Donnees(id=4, taille=15)
soleil=Donnees(id=5, taille=35)
pluie=Donnees(id=6, taille=10)
vent=Donnees(id=7, taille=10)

# test implémentation des données
#noeud_sport=Noeuds_systeme(1, 30, [vtt, route], [1] )
#noeud_animaux=Noeuds_systeme( 2, 50, [chat, chien], [1, 2])
#noeud_meteo=Noeuds_systeme(3, 40, [soleil, pluie, vent], [1, 2])

# test placement des données dans les noeuds
# noeuds avec des listes de données vides

#Noeuds de façon à ce que la donnée commune soit déjà placée :
"""
noeud_1=Noeuds_systeme(1, 10, [], [])
noeud_2=Noeuds_systeme( 2, 50, [], [noeud_1])
noeud_3=Noeuds_systeme(3, 30, [], [noeud_2])
noeud_4=Noeuds_systeme(4, 28, [], [noeud_3])
noeud_5=Noeuds_systeme(5, 22, [], [noeud_4]) 
noeud_6=Noeuds_systeme(6, 60, [], [noeud_5])
noeud_7=Noeuds_systeme(7, 38, [], [noeud_6])
noeud_1.ajouter_noeud_accessible(noeud_2) # le noeud 1 a accès et au noeud 2
noeud_2.ajouter_noeud_accessible(noeud_3) # le noeud 2 a accès au noeud 1 et le noeud 3.
noeud_3.ajouter_noeud_accessible(noeud_4) # le noeud 3 a accès au noeud 2 et au noeud 4
noeud_4.ajouter_noeud_accessible(noeud_5) # le noeud 4 a accès au noeud 3 et au noeud 5
noeud_5.ajouter_noeud_accessible(noeud_6) # le noeud 5 a accès au noeud 4 et au noeud 6
noeud_6.ajouter_noeud_accessible(noeud_7) # le noeud 6 a accès au noeud 5 et au noeud 7
"""

#Noeuds de façon à ce que la donnée commune puisse être déplacée au milieu : (le noeud 3)
"""
noeud_1=Noeuds_systeme(1, 10, [], [])
noeud_2=Noeuds_systeme( 2, 50, [], [noeud_1])
noeud_3=Noeuds_systeme(3, 40, [], [noeud_2]) # on change la taille du noeud du milieu
noeud_4=Noeuds_systeme(4, 28, [], [noeud_3])
noeud_5=Noeuds_systeme(5, 22, [], [noeud_4]) 
noeud_6=Noeuds_systeme(6, 60, [], [noeud_5])
noeud_7=Noeuds_systeme(7, 38, [], [noeud_6])
noeud_1.ajouter_noeud_accessible(noeud_2) # le noeud 1 a accès et au noeud 2
noeud_2.ajouter_noeud_accessible(noeud_3) # le noeud 2 a accès au noeud 1 et le noeud 3.
noeud_3.ajouter_noeud_accessible(noeud_4) # le noeud 3 a accès au noeud 2 et au noeud 4
noeud_4.ajouter_noeud_accessible(noeud_5) # le noeud 4 a accès au noeud 3 et au noeud 5
noeud_5.ajouter_noeud_accessible(noeud_6) # le noeud 5 a accès au noeud 4 et au noeud 6
noeud_6.ajouter_noeud_accessible(noeud_7) # le noeud 6 a accès au noeud 5 et au noeud 7
"""

#Noeuds de façon à ce que la donnée commune soit déplacée dans un autre noeud (le 4):
"""
noeud_1=Noeuds_systeme(1, 10, [], [])
noeud_2=Noeuds_systeme( 2, 50, [], [noeud_1])
noeud_3=Noeuds_systeme(3, 30, [], [noeud_2])
noeud_4=Noeuds_systeme(4, 38, [], [noeud_3])
noeud_5=Noeuds_systeme(5, 22, [], [noeud_4]) 
noeud_6=Noeuds_systeme(6, 60, [], [noeud_5])
noeud_7=Noeuds_systeme(7, 38, [], [noeud_6])
noeud_1.ajouter_noeud_accessible(noeud_2) # le noeud 1 a accès et au noeud 2
noeud_2.ajouter_noeud_accessible(noeud_3) # le noeud 2 a accès au noeud 1 et le noeud 3.
noeud_3.ajouter_noeud_accessible(noeud_4) # le noeud 3 a accès au noeud 2 et au noeud 4
noeud_4.ajouter_noeud_accessible(noeud_5) # le noeud 4 a accès au noeud 3 et au noeud 5
noeud_5.ajouter_noeud_accessible(noeud_6) # le noeud 5 a accès au noeud 4 et au noeud 6
noeud_6.ajouter_noeud_accessible(noeud_7) # le noeud 6 a accès au noeud 5 et au noeud 7
"""

# Noeuds placés en étoile et pas seulement en ligne :
noeud_1=Noeuds_systeme(1, 10, [], [])
noeud_2=Noeuds_systeme( 2, 50, [], [noeud_1])
noeud_3=Noeuds_systeme(3, 30, [], [noeud_2])
noeud_4=Noeuds_systeme(4, 58, [], [noeud_3])
noeud_5=Noeuds_systeme(5, 32, [], [noeud_3]) 
noeud_6=Noeuds_systeme(6, 60, [], [noeud_4, noeud_5])
noeud_7=Noeuds_systeme(7, 38, [], [noeud_6])
noeud_1.ajouter_noeud_accessible(noeud_2) # le noeud 1 a accès et au noeud 2
noeud_2.ajouter_noeud_accessible(noeud_3) # le noeud 2 a accès au noeud 1 et le noeud 3.
noeud_3.ajouter_noeud_accessible(noeud_4)
noeud_3.ajouter_noeud_accessible(noeud_5) # le noeud 3 a accès au noeud 2, 4 et au noeud 5
noeud_4.ajouter_noeud_accessible(noeud_6) # le noeud 4 a accès au noeud 3 et au noeud 6
noeud_5.ajouter_noeud_accessible(noeud_6) # le noeud 5 a accès au noeud 3 et au noeud 6
noeud_6.ajouter_noeud_accessible(noeud_7) # le noeud 6 a accès au noeud 4, 5 et au noeud 7

# test placement de données
gillian=Utilisateurs(1, [vtt, route, pluie, vent], noeud_1)
emma=Utilisateurs(2, [chat, chien, soleil], noeud_7)

# test placement de données avec intéret commun
#gillian.ajouter_donnee_interet(soleil)

print("Donnée vtt : "+ vtt.toString())
print("Donnée route : "+route.toString())
print("Donnée chat : "+chat.toString())
print("Donnée chient : "+chien.toString())
print("Donnée soleil : "+soleil.toString())
print("Donnée pluie : "+pluie.toString())
print("Donnée vent : "+vent.toString())
print("Noeud sport : "+ noeud_1.toString())
print("Noeud animaux : "+ noeud_2.toString())
print("Utilisateur gillian : "+gillian.toString())
print("Utilisateur emma : "+ emma.toString())

### listes utiles pour la gestion des données ###
liste_donnees=[vtt, route, chat, chien, soleil, pluie, vent]
liste_utilisateurs=[gillian, emma]
liste_noeuds=[noeud_1, noeud_2, noeud_3, noeud_4, noeud_5, noeud_6, noeud_7]