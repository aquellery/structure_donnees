Dans ce projet de structure de données, deux fichiers pythons permettent de gérer un système de stockage de données.

Le fichier "structure_donnees.py" regroupe les différentes classes utilisées, les méthodes utiles à l'affichage qui se fait dans le terminal ainsi que la création des objets utilisés.
Par exemple, on peut y trouver les classes : 
- Donnees qui permet de représenter une donnée avec un identifiant unique et sa taille.
- Noeuds_system qui permet de représenter un noeud avec un identifiant unique, sa capacité, la liste des données présente dans ce noeud ainsi que les noeuds accessibles depuis celui-ci.
- Utilisateurs qui permet de représenter un utilisateur avec un identifiant unique, une liste de données d'intérêt et le noeud auquel il a directement accès.
Chacune de ces classes ont des méthodes qui permetttent de manipuler leurs attributs et de créer des affichages dans le terminal.

Le fichier "gestion_donnees.py" regroupe lui les différentes méthodes de calcul utilisées pour remplir les noeuds :
- soit automatiquement vis à vis des données d'intérêt des utilisateurs
- soit en fonction des données communes que pourraient avoir les utilisateurs.

Pour faire fonctionner cet algorithme il faut : 
1) Créer les données, noeuds et utilisateurs dans le fichier "structure_donnees.py" de préférence
Actuellement, des objets sont déjà créés à la fin du fichier et permettent de tester le placement des données. 
2) Exécuter le fichier "gestion_donnees.py" pour que le placement des données se fasse automatiquement.
On aura ainsi un affichage dans le terminal qui permet de visualiser le contenu de chaque noeuds.
Dans le cas où une donnée est créée mais qu'aucun utilisateur est intéréssé par celle-ci, elle ne sera pas placée dans le système.
  



