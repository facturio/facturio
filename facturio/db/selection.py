#faire les liste

def selection_client(cursor,conenxion,liste,bool):
    cursor.execute("""select * from client""")
    return cursor.fetchall()
def selection_utilisateur(cursor,conenxion,liste):
    cursor.execute("""select * from utilisateur""")
    print(cursor.fetchall())
def selection_acompte(cursor,conenxion,liste):
    cursor.execute("""select * from accompte""")
    print(cursor.fetchall())
def selection_fac_dev(cursor,conenxion,liste):
    cursor.execute("""select * from facture_devis""")
    print(cursor.fetchall())
def selection_entreprise(cursor,conenxion,liste):
    cursor.execute("""select * from entreprise""")
    print(cursor.fetchall())
def selection_article(cursor,conenxion,liste):
    cursor.execute("""select * from article""")
    print(cursor.fetchall())
def selection_facture(cursor,conenxion,liste):
    cursor.execute("""select * from facture""")
    print(cursor.fetchall())
def selection_art_dev(cursor,conenxion,liste):
    cursor.execute("""select * from art_dev""")
    print(cursor.fetchall())
