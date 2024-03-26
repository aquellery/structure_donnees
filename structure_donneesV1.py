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
    
    def get_taille(self):
        return self.taille

    def get_id(self):
        return self.id

    def get_taille_par_id(id):
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
    def __init__(self, id:int, capacite:int, liste_donnees_locales:list, liste_noeuds_accessibles:list):
        #on vérifie que l'identifiant n'est pas déjà pris
        if id in Noeuds_systeme.liste_id:
            raise ValueError("L'identifiant "+str(id)+" est déjà utilisé pour un autre noeud")
        self.id=id
        Noeuds_systeme.liste_id.append(id)

        self.capacite=capacite
        capacite_utilisee=0
        for id_donnee in liste_donnees_locales:
            #on vérifie que chaque identifiant correspond bien à un identifiant d'une instance de Données
            if id_donnee not in Donnees.liste_id : 
                raise ValueError("L'identifiant "+str(id_donnee)+" ne correspond  pas à un identifiant de données")
            
            #on calcule ensuite la capacité utilisée par toutes les données comprises dans le noeud
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
        for id in liste_noeuds_accessibles :   
            if id not in Noeuds_systeme.liste_id:
                raise ValueError("L'identifiant de noeud "+str(id)+" ne correspond pas à un noeud existant")
            self.listee_noeud_accessible=liste_noeuds_accessibles

    def get_id(self):
        return self.id

    def  get_capacite(self):
        return self.capacite
    
    def get_liste_donees(self):
        return self.liste_donnees_locales
    
    def get_liste_noeuds_accessibles(self):
        return self.get_liste_noeuds_accessibles
    
    def modifier_capacite(self, nouvelle_capacite:int):
        self.capacite=nouvelle_capacite

    def ajouter_donnee(self, nouvelle_donnee:int):
        self.liste_donnees_locales.append(nouvelle_donnee)
    
    def supprimer_donnee(self, donnee:int):
        self.liste_donnees_locales.remove(donnee)

    def toString(self):
        return f"Le Noeud a pour id : {self.id}, a une capacité de : {self.capacite} et a comme données locales la liste :{self.liste_donnees_locales} et comme noeuds accessibles la liste : {self.listee_noeud_accessible}"

    def placer_donnes(self):
        pass

class Utilisateurs :
    """
    La classe Utilisateurs permet d'obtenir la structure d'un utilisateur avec :
    - un identifiant unique
    - une liste de données (id) d'intérêt
    - le noeud (id) du système auquel il a accès directement
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
    def __init__(self, id:int, liste_donnees_interet:list, noeud_systeme_accessible:list):

        #on vérifie que l'id donné n'est pas déjà utilisé pour un autre noeud
        if id in Utilisateurs.liste_id:
            raise ValueError("L'identifiant "+ str(id)+" est déjà utilisé pour un autre utilisateur")
        self.id=id
        Utilisateurs.liste_id.append(id)

        for donnee in liste_donnees_interet:
            if donnee not in Donnees.liste_id :
                raise ValueError("L'identifiant "+str(donnee)+" ne correspond  pas à un identifiant de données")
            self.liste_donnes_interet=liste_donnees_interet

        if noeud_systeme_accessible not in Noeuds_systeme.liste_id : 
            raise ValueError("L'identifiant "+noeud_systeme_accessible+" ne correspond pas à un noeud existant")
        self.noeud_systeme_accessible=noeud_systeme_accessible

    def get_id(self):
        return self.id
    
    def get_liste_interet(self):
        return self.liste_donnes_interet
    
    def  get_noeud_system_accessible(self):
        return self.noeud_systeme_accessible
    
    def modifier_noeud_accessible(self, nouveau_noeud:int):
        self.noeud_systeme_accessible=nouveau_noeud

    def ajouter_donnee_interet(self, nouvelle_donnee:int):
        self.liste_donnes_interet.append(nouvelle_donnee)

    def supprimer_donnee_interet(self, donnee:int):
        self.liste_donnes_interet.remove(donnee)
    
    def toString(self):
        return f"L'utilisateur qui a pour id : {self.id} a comme intérêt les données {self.liste_donnes_interet} Son noeud système accessible est l'identifiant {self.noeud_systeme_accessible}"


##########################################
### zone de test : création de données, de noeuds et d'utilisateurs ###
vtt=Donnees(id=1, taille=5)
route=Donnees(id=2, taille=4)
chat=Donnees(id=3, taille=30)
chien=Donnees(id=4, taille=15)
meteo=Donnees(id=5, taille=10)
noeud_sport=Noeuds_systeme(1, 30, [1, 2, 5], [1] )
noeud_animaux=Noeuds_systeme( 2, 50, [3, 4], [1, 2])
noeud_meteo=Noeuds_systeme(3, 20, [5], [1, 2])
#noeud_test=Noeuds_systeme(3, 20, [5], [1, 4])
gillian=Utilisateurs(1, [1, 2], 1)
emma=Utilisateurs(2, [2, 3, 4], 2)

print("Donnée vtt : "+ vtt.toString())
print("Donnée route : "+route.toString())
print("Donnée chat : "+chat.toString())
print("Donnée chient : "+chien.toString())
print("Donnée météo : "+meteo.toString())
print("Noeud sport : "+ noeud_sport.toString())
print("Noeud animaux : "+ noeud_animaux.toString())
print("Utilisateur gillian : "+gillian.toString())
print("Utilisateur emma : "+ emma.toString())
