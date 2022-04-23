#import la biblio
import sqlite3
from creation_table import *
from insertion import *
from delete import *
from selection import *
from update import *
from classe_bd import *

from datetime import date
"update company ne marche pas "

def main():
    #nom de ta bdd et création
    name_bdd='facturio'
    bdd=Data_base(name_bdd)

    #pour la creation de notre bdd
    #si il existe pas il est cree
    connexion=sqlite3.connect('facturio.db')

    # execution des requetes il faut un curseur
    cursor=connexion.cursor()

    # on active les clés etrangere,de base elle ne le sont pas
    cursor.execute("PRAGMA  foreign_keys = ON")

    """--------------------------------- creation des table ----------"""

    """------------------------fonction insertion dans la bdd-------------------- """
    # ordre name,description,price
    liste=["pull","un pull tres moche ",30]
    bdd.insertion_article(liste)

    #ordre logo,company_name,e_mail,address,phone,num_SIREN
    liste=["logo.png","entreprise de reve","tomolivier283@gmail.com","avenue toto","0653536789","00543222"]
    bdd.insertion_user(liste)

    #booleen egale a 0 pour savoir si c'est un client et 1 pour une entreprise(a voir)
    #ordre last_name,first_name,e_mail,address,phone,remark+(company_name,num_SIRET)->entreprise
    liste=["bazan","clement","tomolivier283@gmail.com","avenue du paradi","0675849320","le plus bg","entreprise","12345678"]
    bool=1
    bdd.insertion_client_or_company(liste,bool)

    data=date.today()

    #recuperation des id client et utilisateur
    #ordre amount,date,description,note,remark,id_client,id_user / le 1,1 faut donc le changer
    liste=[100.0,data,"acheter des vetement","10","de la merde",1,1]
    bdd.insertion_invoice_dev(liste)
    bdd.insertion_invoice(liste)

    #le 1 corespond a id de facture
    #la date je men occupe dans mes fonctions
    #date,amount,id_invoice
    liste=["100",1]
    bdd.insertion_deposit(liste)

    #id article et id de fac_dev
    #odre id_article,id_invoice_devis
    liste=[1,1]
    bdd.insertion_art_dev(liste)
    """------------------- fonction update dans la bdd --------------------"""
    #les liste sont les même jai juste ajoute id au debut pour
    #modifier la bonne ligne
    liste=["1","logo.png","prise de reve","tomolivier283@gmail.com","avenue toto","0653536789","00543222"]
    bdd.update_user(liste)
    liste=["1","bazan","clement","tomolivier283@gmail.com","avenue du paradi","0675849320","le plus bg"]
    bdd.update_client(liste,bool)
    liste=[1,data,"100",1]
    bdd.update_deposit(liste)
    liste=[1,"t-shirt","un pull tres moche ",40]
    bdd.update_article(liste)
    liste=[1,100.0,data,"acheter des choses","10","de la merde",1,1]
    bdd.update_invoice_dev(liste)
    """--------------------fonction delete dans la bdd-------------------- """

    #la ligne que tu veux surprimmer sera normalement sous forme de liste
    #donc on selectionne id dans la liste et le nom de la table
    #normal :
    #id=liste[0]
    #test:
    id=1
    nom_table="client"
    #bdd.delete_table(name,id)
    """ ------------------------fonction selection--------------------------"""
    #tu dis le nom de la table que tu veux voir
    name="client"
    liste=bdd.selection_table(name)
    print(liste)
    """ ------------------------------------------------------------------------"""
    #fermer la connexion
    connexion.close()

if __name__ == "__main__":
    main()
