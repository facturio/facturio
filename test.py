#import la biblio
import sqlite3
from datetime import date


"""
type date
voir pour les float
"""
#pour la creation de notre bdd
#si il existe pas il est cree
connexion=sqlite3.connect('exemple_base.db')
# execution des requetes il faut un curseur
cursor=connexion.cursor()
# on active les clés etrangere,de base elle ne le sont pas
cursor.execute("PRAGMA  foreign_keys = ON")

def creation_table(cursor,connexion):

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS  client (
    nom STRING PRIMARY KEY, prenom STRING
    );
    """)
    connexion.commit()
#creation de la deuxieme table pour un test des clé etrangere

def creation_table_type(cursor,connexion):

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS type(
    nom STRING PRIMARY KEY,
    prenom INTEGER ,
    date INTEGER
    );
    """)
    connexion.commit()
def creation_table_u_p(cursor,connexion):

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS utile(
    A INTEGER UNIQUE,
    B INTEGER UNIQUE,
    C STRING,
    PRIMARY KEY ((a),(b))
    );
    """)

def affichage_jointure(cursor,connexion):
    print("toto")

def insertion_table_u(cursor,connexion):
    cursor.execute("""INSERT INTO utile(C) VALUES(?)""",("toto"))
    connexion.commit()

def insertion_table_type(cursor,connexion):
    ici=date.today()
    cursor.execute("""INSERT INTO type(nom,prenom,date) VALUES(?,?,?)""",('olivier',1,ici))
    connexion.commit()

def insertion_table(cursor,connexion):
    cursor.execute("""INSERT INTO client(nom,prenom) VALUES(?,?)""",('olivier','tom'))
    connexion.commit()

def update_table(cursor,connexion):
    cursor.execute("""UPDATE client SET prenom= ? WHERE nom='olivier' """,('bazan',))
    connexion.commit()

def voir_les_tables(cursor):
    cursor.execute("""select name from sqlite_master""")
    print(cursor.fetchall())

def voir_la_table(cursor):
    cursor.execute("""select * from client""")
    print(cursor.fetchall())

def mettre_image(texte,cursor,connexion):
    sql="""INSERT INTO cli(logo) VALUES(?)"""

    with open(texte,"rb") as myfile:
        blobfile=myfile.read()
    print("toto")

    value =(blobfile,)
    cursor.execute(sql,value)
    connexion.commit()
    cursor.close()
    connexion.close()

def recup_image(cursor,connexion):

    sql="""SELECT logo FROM cli"""
    cursor.execute(sql)
    logo="logo"
    path="/home/tom/Bureau/do_genie/image/"+logo+".png"
    res=cursor.fetchall()
    for collon in res:
        file=collon[0]

    with open(path,'wb') as myfile:
        myfile.write(file)

    cursor.close()
    connexion.close()



#a la fin on ferme la connexion
#creation_table_u_p(cursor,connexion)

#a la fin on ferme la connexion
#creation_table(cursor,connexion)

texte="logo.png"

recup_image(cursor,connexion)
print("reussi")
connexion.close()
