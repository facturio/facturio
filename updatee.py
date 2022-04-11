#faire les liste

def update_client(cursor,conenxion,liste,bool):
    cursor.execute("""UPDATE client SET  WHERE num_utilisateur=?""",liste)
    connexion.commit()
def update_utilisateur(cursor,conenxion,liste):
    cursor.execute("""UPDATE utilisateur SET logo=? WHERE num_utilisateur=?""",liste)
    connexion.commit()
def update_acompte(cursor,conenxion,liste):
    cursor.execute("""UPDATE accompte SET date=? id_fac=? WHERE id_accompte=?""",liste)
    connexion.commit()
def update_fac_dev(cursor,conenxion,liste):
    cursor.execute("""UPDATE facture_devis SET  WHERE id_facdev=?""",liste)
    connexion.commit()
