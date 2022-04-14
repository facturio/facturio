def delete_client(cursor,connexion,liste):
    cursor.execute(""" DELETE FROM client WHERE id_client="""+str(liste[0]))
    connexion.commit()
def delete_deposit(cursor,connexion,liste):
    cursor.execute(""" DELETE FROM deposit WHERE id_deposit="""+str(liste[0]))
    connexion.commit()

def delete_user(cursor,connexion,liste):
    cursor.execute(""" DELETE FROM user WHERE id_user="""+str(liste[0]))
    connexion.commit()


def delete_article(cursor,connexion,liste):
    cursor.execute(""" DELETE FROM article WHERE id_article="""+str(liste[0]))
    connexion.commit()

def delete_invoice_dev(cursor,connexion,liste):
    cursor.execute(""" DELETE FROM invoice_devis WHERE id_facdev="""+str(liste[0]))
    connexion.commit()
def delete_invoice(cursor,connexion,liste):
    cursor.execute(""" DELETE FROM invoice WHERE id_invoice="""+str(liste[0]))
    connexion.commit()
