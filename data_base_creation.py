#import la biblio
import sqlite3
from creation_table import *
from insertion import *
from delete import *
from selection import *
from update import *

from datetime import date

"""
a faire :

update entreprise

faire quant tout marche :
delete une fonction
list een objet

"""
def main():
    #pour la creation de notre bdd
    #si il existe pas il est cree
    connexion=sqlite3.connect('facturio.db')

    # execution des requetes il faut un curseur
    cursor=connexion.cursor()

    # on active les clés etrangere,de base elle ne le sont pas
    cursor.execute("PRAGMA  foreign_keys = ON")

    """--------------------------------- creation des table ----------"""

    creation_table_article(cursor,connexion)
    creation_table_user(cursor,connexion)
    creation_table_client(cursor,connexion)
    creation_table_company(cursor,connexion)
    creation_table_invoice_devis(cursor,connexion)
    creation_table_invoice(cursor,connexion)
    creation_table_art_dev(cursor,connexion)
    creation_table_deposit(cursor,connexion)

    """------------------------fonction insertion dans la bdd-------------------- """

    liste=["t-shirt","un pull tres moche ",30]
    insertion_article(cursor,connexion,liste)

    liste=["logo.png","entreprise de reve","tomolivier283@gmail.com","avenue toto","0653536789","00543222"]
    insertion_user(cursor,connexion,liste)

    #booleen egale a 0 pour savoir si c'est un client et 1 pour une entreprise
    liste=["bazan","clement","tomolivier283@gmail.com","avenue du paradi","0675849320","le plus bg","entreprise","12345678"]
    bool=1
    insertion_client_or_company(cursor,connexion,liste,bool)

    data=date.today()
    #recuperation des id client et utilisateur
    liste=[100.0,data,"acheter des vetement","10","de la merde",1,1]
    insertion_invoice_dev(cursor,connexion,liste)
    insertion_invoice(cursor,connexion,liste)
    #id de facture
    liste=["100",1]
    insertion_deposit(cursor,connexion,liste)
    #id article et id de fac_dev
    liste=[1,1]
    insertion_art_dev(cursor,connexion,liste)
    """------------------- fonction update dans la bdd --------------------"""

    liste=["1","logo.png","prise de reve","tomolivier283@gmail.com","avenue toto","0653536789","00543222"]
    update_user(cursor,connexion,liste)
    liste=["1","bazan","clement","tomolivier283@gmail.com","avenue du paradi","0675849320","le plus bg"]
    update_client(cursor,connexion,liste,bool)
    liste=[1,data,"100",1]
    update_deposit(cursor,connexion,liste)
    liste=[1,"t-shirt","un pull tres moche ",40]
    update_article(cursor,connexion,liste)
    liste=[1,100.0,data,"acheter des choses","10","de la merde",1,1]
    update_invoice_dev(cursor,connexion,liste)
    """--------------------fonction delete dans la bdd-------------------- """

    #recuperation de la ligne client quon envoie dans la fonction
    liste=[1]
    delete_client(cursor,connexion,liste)
    delete_deposit(cursor,connexion,liste)
    delete_user(cursor,connexion,liste)
    delete_article(cursor,connexion,liste)
    delete_invoice_dev(cursor,connexion,liste)
    delete_invoice(cursor,connexion,liste)

    """ ------------------------fonction selection--------------------------"""

    nom="client"
    selection_table(cursor,connexion,nom)

    """ ------------------------------------------------------------------------"""
    #fermer la connexion
    connexion.close()

if __name__ == "__main__":
    main()
