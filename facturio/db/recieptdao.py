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

        # TODO:Verifier que les id_client et id_user existent et ne soient
        request = """select * from client"""
        client_table = self.bdd.cursor.execute(request).fetchall()

        request = """select* from user """
        user_table = self.bdd.cursor.execute(request).fetchall()
        flag = 0
        for i in client_table:
            if i[0] == receipt.client:
                flag += 1

        for i in user_table:
            if i[0] == receipt.user:
                flag += 1
        if flag == 2:
            print("il y a ")

        request = """INSERT INTO receipt(balance, taxes, date, note,
                      id_client, id_user) VALUES (?, ?, ?, ?, ?, ?)"""
        values = (receipt.balance, receipt.taxes, receipt.date,
                  receipt.note,
                  receipt.client.id_, receipt.user.id_)
        print("valeur= ", values)
        self.bdd.cursor.execute(request, values)
        self.bdd.connexion.commit()

        # On recupere l'id qui vient d'etre insere'
        max_req = "SELECT max(id_receipt) FROM receipt"
        id_ = self.bdd.cursor.execute(max_req).fetchall()
        max_req = "SELECT * FROM receipt"
        self.bdd.cursor.execute(max_req).fetchall()

        # Insertion des articles
        self.bdd.connexion.commit()
        print("tata")
        # mis a jour des id receipt et articles
        self._set_id(receipt, id_[0])

        return

    def update(self, receipt: Receipt):

        self.bdd.cursor.execute("""UPDATE receipt SET
            balance=?,taxes=?,date=?,note=?,id_client=?,id_user=?
            WHERE id_receipt=?""",
                                (receipt.balance, receipt.taxes,
                                 receipt.date, receipt.note,
                                 receipt.client, receipt.user, receipt.id_))
        self.bdd.connexion.commit()

    @staticmethod
    def _gen_receipt(tup):
        receipt = Receipt(balance=tup[1],
                          taxes=tup[2],
                          date=tup[3],
                          note=tup[4],
                          client=tup[5],
                          articles_list=None,
                          user=tup[6],
                          id_=tup[0])

        return receipt

    def get_all(self):
        # TODO?
        request = "SELECT * FROM receipt"
        tuples = self.bdd.cursor.execute(request).fetchall()
        self.bdd.connexion.commit()
        res = []
        for tup in tuples:

            res.append(self._gen_receipt(tup))
        return res

    def get_with_id(self, id_):
        """Renvoie une instace du user avec id_."""
        request = f"SELECT * FROM receipt where id_receipt = {id_}"
        tup = self.bdd.cursor.execute(request).fetchall()

        return self._gen_receipt(tup[0])

    def delete(self, id, idc, idu):

        self.bdd.cursor.execute(
            """ DELETE FROM receipt WHERE id_receipt="""+str(id))
        self.bdd.cursor.execute(
            """ DELETE FROM client WHERE id_client="""+str(idc))
        self.bdd.cursor.execute(
            """ DELETE FROM user WHERE id_user="""+str(idu))
        self.bdd.connexion.commit()


if __name__ == "__main__":

    receipt_dao = ReceiptDAO.get_instance()
