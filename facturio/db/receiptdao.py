#!/usr/bin/env python3
from facturio.classes.invoice_misc import Receipt
from facturio.db.dbmanager import DBManager

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

    def insert(self, receipt: Receipt):
        """Insertion du receipt."""
        request = """INSERT INTO receipt(balance, date, note,
                      id_client, id_user) VALUES (?, ?, ?, ?, ?)"""
        # TODO: Verifier que les id_client et id_user existent et ne soient
        # pas egale a None
        values = (receipt.balance, receipt.date, receipt.note,
                  receipt.client.id_, receipt.user.id_)
        self.bdd.cursor.execute(request, values)
        self.bdd.connexion.commit()
        # On recupere l'id qui vient d'etre insere'
        max_req = "SELECT max(id_receipt) FROM receipt"
        id_ = self.bdd.cursor.execute(max_req).fetchone()
        # Insertion des articles
        article_dao = ArticleDAO.get_instance()
        for article in receipt.articles_list:
            article_dao.insert(article)

        # mis a jour des id receipt et articles
        receipt.set_id(id_[0])

    def update(self, receipt: Receipt):
        # TODO
    #     bdd=DBManager.get_instance()
    #     liste=liste[1:]+[liste[0]]
    #     bdd.cursor.execute("""UPDATE invoice_estimate SET balance=?,date=?,description=?,note=?,remark=?,id_client=?,id_user=? WHERE id_invoice_estimate=?""",liste)
    #     bdd.connexion.commit()
        raise NotImplementedError

    def get_all(self):
        request = "SELECT * FROM receipt"
        self.bdd.cursor.execute(request)
        return self.bdd.cursor.fetchall()

if __name__ == "__main__":
    from facturio.classes.invoice_misc import Article
    from facturio.classes.client import Client, Company
    from facturio.classes.user import User
    from facturio.db.userdao import UserDAO
    from facturio.db.companydao import CompanyDAO
    from facturio.db.clientdao import ClientDAO
    from facturio.db.articledao import ArticleDAO

    user_dao = UserDAO.get_instance()
    company_dao = CompanyDAO.get_instance()

    user = User(company_name="Facturio INC", last_name="BENJELLOUN",
                first_name="Youssef", email="yb@gmail.com",
                address="427 Boulevard des armoaris 83100 Toulon",
                phone_number="07 67 31 58 20",
                business_number="12348921 2341")
    user_dao.insert(user)

    comp = Company(company_name="LeRoy", last_name="Ben",
                   first_name="Karim", business_number="287489404",
                   email="LeRoy83@sfr.fr", address="12 ZAC de La Crau",
                   phone_number="0345678910")
    company_dao.insert(comp)

    art_dao = ArticleDAO.get_instance()

    ordinateur = Article("Ordinateur", 1684.33, 3)
    cable_ethernet = Article("Cable ethernet", 5, 10)
    telephone = Article("Telephone", 399.99, 1)
    casque = Article("Casque", 69.99, 6)
    articles = [ordinateur, cable_ethernet, telephone, casque]

    receipt_dao = ReceiptDAO.get_instance()

    receipt = Receipt(user=user, client=comp, articles_list=articles,
                      date=0, taxes=0.11, balance=122,
                      note="Facture de matériel informatiques")
