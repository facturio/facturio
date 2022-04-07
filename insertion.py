

def insertion_article(cursor,connexion,liste):
    """ compter le nombre de ligne """
    cursor.execute("""INSERT INTO article(nom,description,prix) VALUES(?,?,?)""",liste)
    connexion.commit()

def insertion_utilisateur(cursor,connexion,liste):
    #convertir image logo sous forme de fichier binaire
    with open(texte,"rb") as myfile:
        blobfile=myfile.read()

    liste[0]=blobfile
    """ compter le nombre de ligne """
    cursor.execute("""INSERT INTO utilisateur(logo,nom,entreprise,corriel,courrier,tel,num_SIREN) VALUES(?,?,?,?,?,?,?,?)""",liste)
    connexion.commit()

def insertion_client_ou_entreprise():
        cursor.execute("""INSERT INTO client(nom,description,prix) VALUES(?,?,?)""",liste)
        connexion.commit()
