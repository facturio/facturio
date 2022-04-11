def delete_client(cursor,connexion,liste):
    cursor.execute(""" DELETE FROM client WHERE id_client="""+str(liste[0]))
    connexion.commit()
def delete_acompte(cursor,connexion,liste):
    cursor.execute(""" DELETE FROM accompte WHERE id_acompte="""+str(liste[0]))
    connexion.commit()

def delete_fac_dev(cursor,connexion,liste):
    cursor.execute(""" DELETE FROM facture_devis WHERE id_facdev="""+str(liste[0]))
    connexion.commit()
def delete_facture(cursor,connexion,liste):
    cursor.execute(""" DELETE FROM facture WHERE id_facture="""+str(liste[0]))
    connexion.commit()
