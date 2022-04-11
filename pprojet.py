#import la biblio
import sqlite3
from creation_table import *
from insertion import *
from delete import *
from selection import *

from datetime import date
"""
a faire :


faire insertion_art_dev

partie update et delete
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
"""------------------------fonction insertion dans la bdd-------------------- """
liste=["pull","un pull tres moche ",30]
insertion_article(cursor,connexion,liste)

liste=["logo.png","entreprise de reve","tomolivier283@gmail.com","avenue toto","0653536789","00543222"]
insertion_utilisateur(cursor,connexion,liste)

#booleen egale a 0 pour savoir si c'est un client et 1 pour une entreprise
liste=["olivier","tom","tomolivier283@gmail.com","avenue du paradi","0675849320","le plus bg","entreprise","12345678"]
bool=0
insertion_client_ou_entreprise(cursor,connexion,liste,bool)

data=date.today()
#recuperation des id
liste=[100.0,data,"acheter des vetement","10","de la merde",1,1]
insertion_fac_dev(cursor,connexion,liste)
insertion_fac(cursor,connexion,liste)
#liste fac
liste=[1]
insertion_acompte(cursor,connexion,liste)

liste=[1,1]
insertion_art_dev(cursor,connexion,liste)
"""------------------- fonction update dans la bdd --------------------"""
liste=["logo.png","entreprise de reve","tomolivier283@gmail.com","avenue toto","0653536789","00543222"]
update_utilisateur(cursor,conenxion,liste)
"""--------------------fonction delete dans la bdd-------------------- """

#recuperation de la ligne client quon envoie dans la fonction
liste=[1]
#delete_client(cursor,connexion,liste)
#delete_acompte(cursor,connexion,liste)
#delete_fac_dev(cursor,connexion,liste)
delete_facture(cursor,connexion,liste)
""" ------------------------fonction selection--------------------------"""
selection_client(cursor,conenxion,liste,bool)
selection_utilisateur(cursor,conenxion,liste)
selection_acompte(cursor,conenxion,liste)
selection_fac_dev(cursor,conenxion,liste)
selection_entreprise(cursor,conenxion,liste)
selection_article(cursor,conenxion,liste)
selection_facture(cursor,conenxion,liste)
selection_art_dev(cursor,conenxion,liste)
""" ------------------------------------------------------------------------"""
#fermer la connexion
connexion.close()
