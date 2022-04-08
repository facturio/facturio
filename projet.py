#import la biblio
import sqlite3
from creation_table import *
from insertion import *

"""
autoincrement
isnertion utilisateur voir logo
"""
#pour la creation de notre bdd
#si il existe pas il est cree
connexion=sqlite3.connect('facturio.db')

# execution des requetes il faut un curseur
cursor=connexion.cursor()

# on active les clés etrangere,de base elle ne le sont pas
cursor.execute("PRAGMA  foreign_keys = ON")

""" creation des table """
creation_table_article(cursor,connexion)
creation_table_utilisateur(cursor,connexion)
creation_table_client(cursor,connexion)
creation_table_entreprise(cursor,connexion)
creation_table_facture_devis(cursor,connexion)
creation_table_facture(cursor,connexion)
creation_table_art_dev(cursor,connexion)
creation_table_acompte(cursor,connexion)
"""fonction insertion dans la bdd """
liste=["pull","un pull tres moche ",30]
insertion_article(cursor,connexion,liste)

liste=["logo.png","tomolivier283@gmail.com","avenue toto","0653536789","00543222"]
insertion_utilisateur(cursor,connexion,liste)
#fermer la connexion
connexion.close()
