from datetime import date

def insertion_article(cursor,connexion,liste):
    """ compter le nombre de ligne """
    cursor.execute("""INSERT INTO article(nom,description,prix) VALUES(?,?,?)""",liste)
    connexion.commit()

def insertion_utilisateur(cursor,connexion,liste):
    texte=liste[0]
    #convertir image logo sous forme de fichier binaire
    with open(texte,"rb") as myfile:
        blobfile=myfile.read()

    liste[0]=blobfile

    cursor.execute("""INSERT INTO utilisateur(logo,nom_entreprise,courriel,courrier,tel,num_SIREN) VALUES(?,?,?,?,?,?)""",liste)
    connexion.commit()

def insertion_client_ou_entreprise(cursor,connexion,liste,bool):
        """ envoi dun bouleen"""
        liste_c=liste[:6]
        cursor.execute("""INSERT INTO client(nom,prenom,courriel,courrier,tel,commentaire) VALUES(?,?,?,?,?,?)""",liste_c)
        connexion.commit()


        if bool==1:
            cursor.execute("""SELECT max(id_client) FROM client""")
            connexion.commit()
            id_max=cursor.fetchall()

            liste_e=[id_max[0][0]]+liste[6:]
            """ recuperation de id """
            cursor.execute("""INSERT INTO entreprise(id_client_entreprise,nom_entreprise,num_SIRET) VALUES(?,?,?)""",liste_e)
            connexion.commit()

def insertion_fac_dev(cursor,connexion,liste):

    cursor.execute("""INSERT INTO facture_devis(montant,date,description,notes,commentaire,id_client,id_util) VALUES(?,?,?,?,?,?,?)""",liste)
    connexion.commit()

def insertion_fac(cursor,connexion,liste):

    cursor.execute("""SELECT max(id_facdev) FROM facture_devis""")
    connexion.commit()
    id_max=cursor.fetchall()

    cursor.execute("""INSERT INTO facture(id_facture,solde) VALUES(?,?)""",(id_max[0][0],liste[0]))
    connexion.commit()

def insertion_acompte(cursor,connexion,liste):
    data=date.today()
    cursor.execute("""INSERT INTO accompte(date,id_fac) VALUES(?,?)""",(data,liste[0]))
    connexion.commit()

def insertion_art_dev(cursor,connexion,liste):
    """ liste de 2 indice
    le premier pour id de article
    le deuxieme pour id de fac_dev   """
    cursor.execute("""INSERT INTO art_dev(id_article,id_facdev) VALUES(?,?)""",(liste))
    connexion.commit()
