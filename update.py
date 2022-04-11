#faire les liste

def update_client(cursor,connexion,liste,bool):
    liste=[liste[0]]+liste[1:]
    if bool==0:
        cursor.execute("""UPDATE client SET
        nom=?,prenom=?,courriel=?,courrier=?,tel=?,commentaire=?
        WHERE num_client=?""",liste)
    else:
        cursor.execute("""UPDATE client SET  WHERE num_client=?""",liste)
    connexion.commit()

def update_utilisateur(cursor,connexion,liste):
    liste=[liste[0]]+liste[1:]
    cursor.execute("""UPDATE utilisateur SET logo=?,nom_entreprise=?,courriel=?,
    courrier=?,tel=?,num_SIREN=? WHERE num_utilisateur=?""",liste)
    connexion.commit()

def update_acompte(cursor,connexion,liste):
    liste=[liste[0]]+liste[1:]
    cursor.execute("""UPDATE accompte SET date=? id_fac=? WHERE id_accompte=?""",liste)
    connexion.commit()

def update_fac_dev(cursor,connexion,liste):
    liste=[liste[0]]+liste[1:]
    cursor.execute("""UPDATE facture_devis SET montant=?,date=?,description=?,notes=?,commentaire=?,id_client=?,id_util=? WHERE id_facdev=?""",liste)
    connexion.commit()

def update_article(cursor,connexion,liste):
    liste=[liste[0]]+liste[1:]
    cursor.execute("""UPDATE article SET nom=?,description=?,prix=? WHERE id_article=?""",liste)
    connexion.commit()
