#import la biblio
import sqlite3

from class_2 import *

from datetime import date
""""
update company ne marche pas
question pour les selfet corriger deux trois truc
faire passe en parametre
"""

def main():
    #nom de ta bdd et création

    bdd=DBmanager()

    """--------------------------------- creation des table ----------"""

    """------------------------fonction insertion dans la bdd-------------------- """
    # ordre name,description,price
    liste=["pull","un pull tres moche ",30]
    article=ArticleDAO()

    article.insertion_article(liste)
    #ordre logo,company_name,e_mail,address,phone,num_SIREN
    liste=["logo.png","entreprise de reve","tomolivier283@gmail.com","avenue toto","0653536789","00543222"]
    clement=UserDAO()
    clement.insertion_user(liste)

    #booleen egale a 0 pour savoir si c'est un client et 1 pour une entreprise(a voir)
    #ordre last_name,first_name,e_mail,address,phone,remark+(company_name,num_SIRET)->entreprise
    a="text"
    liste=[a,a,a,a,a,a]
    bool=0
    client=ClientDAO()
    client.insertion_client_or_company(liste,bool)

    data=date.today()

    #recuperation des id client et utilisateur
    #ordre amount,date,description,note,remark,id_client,id_user / le 1,1 faut donc le changer
    liste=[100.0,data,"acheter des vetement","10","de la merde",1,1]
    invoice_dev=Invoice_devDAO()
    invoice=InvoiceDAO()
    invoice_dev.insertion_invoice_dev(liste)
    invoice.insertion_invoice(liste)

    #le 1 corespond a id de facture
    #la date je men occupe dans mes fonctions
    #date,amount,id_invoice
    liste=["100",1]
    deposit=DepositDAO()
    deposit.insertion_deposit(liste)

    #id article et id de fac_dev
    #odre id_article,id_invoice_devis
    liste=[1,1]
    art_dev=Art_devDAO()

    art_dev.insertion_art_dev(liste)
    """------------------- fonction update dans la bdd --------------------"""
    #les liste sont les même jai juste ajoute id au debut pour
    #modifier la bonne ligne
    liste=["1","logo.png","prise de reve","tomolivier283@gmail.com","avenue toto","0653536789","00543222"]
    clement.update_user(liste)
    liste=["1","bazan","clement","tomolivier283@gmail.com","avenue du paradi","0675849320","le plus bg"]
    #bdd.update_client(liste,bool)
    liste=[1,data,"100",1]
    deposit.update_deposit(liste)
    liste=[1,"t-shirt","un pull tres moche ",40]
    article.update_article(liste)
    liste=[1,100.0,data,"acheter des choses","10","de la merde",1,1]
    invoice_dev.update_invoice_dev(liste)
    """--------------------fonction delete dans la bdd-------------------- """

    """nom_classe.delete(id) """
    """ ------------------------fonction selection--------------------------"""
    """
    nom_classe.selection()
    """
    """ ------------------------------------------------------------------------"""

    bdd.close()

if __name__ == "__main__":
    main()
