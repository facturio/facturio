#!/usr/bin/env python3
from facturio.classes.invoice_misc import Receipt
from facturio.db.dbmanager import DBManager
from facturio.db.userdao import UserDAO
from facturio.db.clientdao import ClientDAO
from facturio.db.companydao import CompanyDAO
from facturio.db.articledao import ArticleDAO
from facturio.classes.client import Client

class ReceiptDAO:
    __instance = None

    def __init__(self):
        """Recupere le manager."""
        self.bdd = DBManager.get_instance()

    def get_instance():
        """Recupere l'instance."""
        if ReceiptDAO.__instance is None:
            ReceiptDAO.__instance = ReceiptDAO()
        return ReceiptDAO.__instance


    def _set_id(self, receipt, id_receipt):
        """Mis a jour des ids local et des articles."""
        receipt.id_ = id_receipt
        for article in receipt.articles_list:
            article.id_receipt = id_receipt

    def insert(self, receipt: Receipt):
        """Insertion du receipt."""
        # Insertion de l'user
        user_dao = UserDAO.get_instance()
        user_dao.insert(receipt.user)

        if receipt.client.id_ is None:
            # On insere seulement si le client n'est pas deja sur la bd
            if type(receipt.client) == Client:
                # Insertion du client
                client_dao = ClientDAO.get_instance()
                client_dao.insert(receipt.client)
            else:
                # Insertion de l'entreprise
                company_dao = CompanyDAO.get_instance()
                company_dao.insert(receipt.client)

        request = """INSERT INTO receipt(balance, taxes, date, note,
                      id_client, id_user) VALUES (?, ?, ?, ?, ?, ?)"""

        # TODO: Verifier que les id_client et id_user existent et ne soient
        # pas egale a None
        values = (receipt.balance, receipt.taxes, receipt.date, receipt.note,
                  receipt.client.id_, receipt.user.id_)
        self.bdd.cursor.execute(request, values)
        self.bdd.connexion.commit()
        # On recupere l'id qui vient d'etre insere'
        max_req = "SELECT max(id_receipt) FROM receipt"
        id_ = self.bdd.cursor.execute(max_req).fetchone()
        # Insertion des articles
        article_dao = ArticleDAO.get_instance()
        for article in receipt.articles_list:
            article.id_receipt = id_[0]
            article_dao.insert(article)

        # mis a jour des id receipt et articles
        self._set_id(receipt, id_[0])

    def update(self, receipt: Receipt):
        raise NotImplementedError
        # TODO

    def get_all(self):
        #TODO?
        request = "SELECT * FROM receipt"
        self.bdd.cursor.execute(request)
        return self.bdd.cursor.fetchall()

if __name__ == "__main__":
    from facturio.classes.invoice_misc import Article
    from facturio.classes.client import Client, Company
    from facturio.classes.user import User
    from facturio.db.articledao import ArticleDAO


    user = User(company_name="Facturio INC", last_name="BENJELLOUN",
                first_name="Youssef", email="yb@gmail.com",
                address="427 Boulevard des armoaris 83100 Toulon",
                phone_number="07 67 31 58 20",
                business_number="12348921 2341")
    # user_dao.insert(user)

    comp = Company(company_name="LeRoy", last_name="Ben",
                   first_name="Karim", business_number="287489404",
                   email="LeRoy83@sfr.fr", address="12 ZAC de La Crau",
                   phone_number="0345678910")
    # company_dao.insert(comp)


    ordinateur = Article("Ordinateur", 1684.33, 3)
    cable_ethernet = Article("Cable ethernet", 5, 10)
    telephone = Article("Telephone", 399.99, 1)
    casque = Article("Casque", 69.99, 6)
    articles = [ordinateur, cable_ethernet, telephone, casque]


    receipt = Receipt(user=user, client=comp, articles_list=articles,
                      date=0, taxes=0.11, balance=122,
                      note="Facture de matériel informatiques")

    user_dao = UserDAO.get_instance()
    company_dao = CompanyDAO.get_instance()
    receipt_dao = ReceiptDAO.get_instance()
    art_dao = ArticleDAO.get_instance()
    client_dao = ClientDAO.get_instance()
