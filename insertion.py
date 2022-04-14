from datetime import date

def insertion_article(cursor,connexion,liste):
    """ compter le nombre de ligne """
    cursor.execute("""INSERT INTO article(name,description,price) VALUES(?,?,?)""",liste)
    connexion.commit()

def insertion_user(cursor,connexion,liste):
    texte=liste[0]
    #convertir image logo sous forme de fichier binaire
    with open(texte,"rb") as myfile:
        blobfile=myfile.read()

    liste[0]=blobfile

    cursor.execute("""INSERT INTO user(logo,company_name,e_mail,address,phone,num_SIREN) VALUES(?,?,?,?,?,?)""",liste)
    connexion.commit()

def insertion_client_or_company(cursor,connexion,liste,bool):
        """ envoi dun bouleen"""
        liste_c=liste[:6]
        cursor.execute("""INSERT INTO client(last_name,first_name,e_mail,address,phone,remark) VALUES(?,?,?,?,?,?)""",liste_c)
        connexion.commit()


        if bool==1:
            cursor.execute("""SELECT max(id_client) FROM client""")
            connexion.commit()
            id_max=cursor.fetchall()

            liste_e=[id_max[0][0]]+liste[6:]
            """ recuperation de id """
            cursor.execute("""INSERT INTO company(id_client_company,company_name,num_SIRET) VALUES(?,?,?)""",liste_e)
            connexion.commit()

def insertion_invoice_dev(cursor,connexion,liste):
    print(liste)
    cursor.execute("""INSERT INTO invoice_devis(amount,date,description,note,remark,id_client,id_util) VALUES(?,?,?,?,?,?,?)""",liste)
    connexion.commit()

def insertion_invoice(cursor,connexion,liste):

    cursor.execute("""SELECT max(id_facdev) FROM invoice_devis""")
    connexion.commit()
    id_max=cursor.fetchall()

    cursor.execute("""INSERT INTO invoice(id_invoice,solde) VALUES(?,?)""",(id_max[0][0],liste[0]))
    connexion.commit()

def insertion_deposit(cursor,connexion,liste):
    data=date.today()
    cursor.execute("""INSERT INTO deposit(date,amount,id_fac) VALUES(?,?,?)""",(data,liste[0],liste[1]))
    connexion.commit()

def insertion_art_dev(cursor,connexion,liste):
    """ liste de 2 indice
    le premier pour id de article
    le deuxieme pour id de fac_dev   """
    cursor.execute("""INSERT INTO art_dev(id_article,id_facdev) VALUES(?,?)""",(liste))
    connexion.commit()
