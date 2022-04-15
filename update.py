#faire les liste

def update_client(cursor,connexion,liste,bool):
    liste=liste[1:]+[liste[0]]

    if bool==0:
        cursor.execute("""UPDATE client SET
        last_name=?,first_name=?,e_mail=?,address=?,phone=?,remark=?
        WHERE id_client=?""",liste)
    else:
        cursor.execute("""UPDATE client SET
        last_name=?,first_name=?,e_mail=?,address=?,phone=?,remark=?
        WHERE id_client=?""",liste)
    connexion.commit()

def update_user(cursor,connexion,liste):
    liste=liste[1:]+[liste[0]]

    cursor.execute("""UPDATE user SET logo=?,company_name=?,e_mail=?,
    address=?,phone=?,num_SIREN=? WHERE id_user=?""",liste)
    connexion.commit()

def update_deposit(cursor,connexion,liste):
    liste=liste[1:]+[liste[0]]
    print("toto",liste)
    cursor.execute("""UPDATE deposit SET date=?,amount=?, id_invoice=? WHERE id_deposit=?""",liste)
    connexion.commit()

def update_invoice_dev(cursor,connexion,liste):
    liste=liste[1:]+[liste[0]]
    cursor.execute("""UPDATE invoice_devis SET amount=?,date=?,description=?,note=?,remark=?,id_client=?,id_user=? WHERE id_invoice_devis=?""",liste)
    connexion.commit()

def update_article(cursor,connexion,liste):
    liste=liste[1:]+[liste[0]]
    cursor.execute("""UPDATE article SET name=?,description=?,price=? WHERE id_article=?""",liste)
    connexion.commit()
