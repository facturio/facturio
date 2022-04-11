#faire les liste

def update_client(cursor,connexion,liste,bool):
    liste=liste[1:]+[liste[0]]

    if bool==0:
        cursor.execute("""UPDATE client SET
        last_name=?,first_name=?,e_mail=?,address=?,phone=?,remark=?
        WHERE id_client=?""",liste)
    else:
        cursor.execute("""UPDATE client SET  WHERE num_client=?""",liste)
    connexion.commit()

def update_utilisateur(cursor,connexion,liste):
    liste=liste[1:]+[liste[0]]

    cursor.execute("""UPDATE utilisateur SET logo=?,company_name=?,courriel=?,
    courrier=?,tel=?,num_SIREN=? WHERE num_utilisateur=?""",liste)
    connexion.commit()

def update_acompte(cursor,connexion,liste):
    liste=liste[1:]+[liste[0]]
    print("toto",liste)
    cursor.execute("""UPDATE accompte SET date=?, id_fac=? WHERE id_acompte=?""",liste)
    connexion.commit()

def update_fac_dev(cursor,connexion,liste):
    liste=liste[1:]+[liste[0]]
    cursor.execute("""UPDATE facture_devis SET montant=?,date=?,description=?,notes=?,commentaire=?,id_client=?,id_util=? WHERE id_facdev=?""",liste)
    connexion.commit()

def update_article(cursor,connexion,liste):
    liste=liste[1:]+[liste[0]]
    cursor.execute("""UPDATE article SET nom=?,description=?,prix=? WHERE id_article=?""",liste)
    connexion.commit()
