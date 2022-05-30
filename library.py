# import du module
import sqlite3

# création et connexion à la base de données
conn = sqlite3.connect("Bibliotheque.db")

# création d’un curseur
cur = conn.cursor()




# création de la première table Auteurs ✍️
#AUTOINCREMENT permet de faire a sorte que l'id fasse +1 a chaque nouvelle valeur ajouter.
cur.execute("""
CREATE TABLE IF NOT EXISTS Auteurs(
    id INTEGER NOT NULL ,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    CONSTRAINT Auteurs_id PRIMARY KEY (id AUTOINCREMENT)
);""")

# création de la deuxieme table Genre.
cur.execute("""
CREATE TABLE IF NOT EXISTS Genres(
    id INTEGER NOT NULL ,
    genre VARCHAR(50) NOT NULL,
    CONSTRAINT Genre_id PRIMARY KEY (id AUTOINCREMENT)
);""")

# création de la troisième table Livres 📚
cur.execute("""
CREATE TABLE IF NOT EXISTS Livres(
    id INTEGER NOT NULL ,
    titre VARCHAR(50) NOT NULL,
    annee INT NOT NULL,
    id_auteur INT NOT NULL,
    id_genre INT NOT NULL,
    CONSTRAINT Livres_id PRIMARY KEY (id AUTOINCREMENT),
    CONSTRAINT Auteur_FK FOREIGN KEY (id_auteur) REFERENCES Auteurs(id),
    CONSTRAINT Genre_FK FOREIGN KEY (id_genre) REFERENCES Genres(id)
);""")
conn.commit()




#Création des menus/sous-menus
#Création de la fonction menu qui permet de choisir si on veut ajouter un auteur, rechercher des données ou de quitter le programme.
def menu():
    choix= -1
    while choix not in [0, 1, 2]:
        choix = int(input("1.Ajouter un auteur\n2 Rechercher des données.\n0 Quitter\n"))
        if choix== 1:
            inserer()
        elif choix == 2:
            rechercher()
        elif choix == 0:
            return None
            



#Création de la fonction inserer qui permet de choisir entre ajouter un auteur, un livre ou un genre.
def inserer():
    choix=-1
    while choix not in [0, 1, 2,3]:
        print("1. Ajouter un auteur\n2. Ajouter un genre\n3. Ajouter un livre\n0. Retour")
        choix = int(input("Quel est votre choix ?\n"))
        if choix==1:
            auteur()
        elif choix==2:
            genre()
        elif choix ==3:
            livre()
        elif choix==0:
            return menu()
        



#Création de la fonction auteur qui permet d'ajouter un auteur (Ex: Asimov Isaac)
def auteur():
    nom = input("Nom ?")
    prenom = input("Prénom ?")
    donnees_auteur=[]
    donnees_auteur.extend((nom,prenom))
    cur.execute("""
    INSERT INTO Auteurs(nom, prenom)
    VALUES (?, ?);""", donnees_auteur)
    conn.commit()
    print("Auteur ajouter avec succés")
    return inserer()




#Création de la fonction genre qui permet d'ajouter un genre (Ex: Fantastique)
def genre():
    genre = input("Genre ?")
    donnees_genre=[]
    donnees_genre.append(genre)
    cur.execute("""
    INSERT INTO Genres(genre)
    VALUES (?);""", donnees_genre)
    conn.commit()
    return inserer()




#Création de la fonction livre qui permet d'ajouter un livre (Ex: Fondation)
def livre():
    titre = input("Titre ?")
    annee = int(input("Année ?"))
    id_auteur = int(input("Id_Auteur ?"))
    id_genre = int(input("Id_Genre ?"))
    donnees_livre=[]
    donnees_livre.extend((titre,annee,id_auteur,id_genre))
    cur.execute("""
    INSERT INTO Livres(titre,annee,id_auteur,id_genre)
    VALUES (?,?,?,?);""", donnees_livre)
    conn.commit()
    return inserer()




#Crétion de la fonction rechercher qui permet de rechecher dans les différentes tables par titre, auteur ou genre.
def rechercher():
    print("")
    choix= -1
    print("Rechercher un livre :\n1- Par titre\n2- Par auteur\n3- Par genre\n0- Retour")
    while choix not in [0, 1, 2,3]:
        choix = int(input("Quel est votre choix ? "))
    if choix == 0:
        return menu()
    elif choix == 1:
        rechercher_titre()
    elif choix == 2:
        rechercher_auteur()
    elif choix == 3:
        rechercher_genre()





#Permet de rechercher un livre par titre
def rechercher_titre():
    titre=input("Entrez un titre de livre afin de trouver le(s) livre(s) correspondant(s) : ")
    cur.execute("""SELECT Livres.titre,Livres.annee,Auteurs.nom,Auteurs.prenom,Genres.genre 
        FROM Livres,Auteurs,Genres 
        WHERE Genres.id = Livres.id_genre 
        AND Auteurs.id = Livres.id_auteur 
        AND titre= ?;""", (titre,))
    sortie=cur.fetchall()
    if sortie == []:
        print("Aucun livre ne correspond à ce titre")
    else:
        print("")
        for i in range(0,len(sortie)):
            print(sortie[i])
    return rechercher()





#Permet de rechercher un livre par son auteur
def rechercher_auteur():
    auteur=input("Entrez un nom d'auteur afin de trouver les livres correspondant(s) : ")
    cur.execute("""SELECT Livres.titre,Livres.annee,Auteurs.nom,Auteurs.prenom,Genres.genre 
        FROM Livres,Auteurs,Genres 
        WHERE Genres.id = Livres.id_genre 
        AND Auteurs.id = Livres.id_auteur 
        AND Auteurs.nom= ?;""", (auteur,))
    sortie=cur.fetchall()
    if sortie == []:
        print("Aucun livre ne correspond à cet auteur")
    else:
        print("")
        for i in range(0,len(sortie)):
            print(sortie[i])
    return rechercher()





#Permet de rechercher un livre avec son genre
def rechercher_genre():
    genre=input("Entrez un genre afin de trouver le(s) livre(s) correspondnt(s) : ")
    cur.execute("""SELECT Livres.titre,Livres.annee,Auteurs.nom,Auteurs.prenom,Genres.genre 
        FROM Livres,Auteurs,Genres 
        WHERE Genres.id = Livres.id_genre 
        AND Auteurs.id = Livres.id_auteur 
        AND Genres.genre= ?;""", (genre,))
    sortie=cur.fetchall()
    if sortie == []:
        print("Aucun livre ne correspond à ce genre")
    else:
        print("")
        for i in range(0,len(sortie)):
            print(sortie[i])
    return rechercher()

menu()


#transmition à Biblioteque.db
conn.commit()
#déco
cur.close()
conn.close()
