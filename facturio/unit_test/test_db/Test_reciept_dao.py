import unittest
import sqlite3
from facturio.db.recieptdao import ReceiptDAO
from facturio.classes.invoice_misc import Receipt
from facturio.db.clientdao import ClientDAO
from facturio.classes.client import Client
from facturio.db.userdao import UserDAO
from facturio.classes.user import User
from facturio.classes.invoice_misc import Article
from facturio.db.articledao import ArticleDAO


class TestRecieptDAO(unittest.TestCase):
    """Teste la classe RecieptDAO"""

    def test_insert(self):

        daoc = ClientDAO.get_instance()
        client = Client("tom", "olivier", "tomolovier283@gmail.com",
                        "trou du cu", "0123456789", "chef")
        daoc.insert(client)

        daou = UserDAO.get_instance()
        user = User("Facturio INC", "Yousggsef", "BENJEggLLOUN", "yb@gmail.com",
                    "427 Boulevard des armaris 8dsfdsfdsq3100 Toulon", "07 67 31 58 20",
                    "12348921 2341")
        daou.insert(user)
        user = daou.get()

        daor = ReceiptDAO.get_instance()
        ordinateur = Article("Ordinateur", 1684.33, 3)
        cable_ethernet = Article("Cable ethernet", 5, 10)
        telephone = Article("Telephone", 399.99, 1)
        casque = Article("Casque", 69.99, 6)
        articles = [ordinateur, cable_ethernet, telephone, casque]
        reciept = Receipt(user=user, client=client, articles_list=articles,
                          date=0, taxes=0.11, balance=122,
                          note="Facture de matériel informatiques")
        daor.insert(reciept)

        max_req = "SELECT * FROM receipt"
        self.bdd.cursor.execute(max_req).fetchall()


if __name__ == '__main__':
    unittest.main()
