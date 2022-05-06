from facturio.classes.invoice_misc import Advance
from dbmanager import DBManager


class AdvanceDAO():
    __instance=None
    def __init__(self):
        """Recupere le manager."""
        self.bdd = DBManager.get_instance()

    def get_instance():
        """Recupere l'instance."""
        if AdvanceDAO.__instance is None:
            AdvanceDAO.__instance = AdvanceDAO()
        return AdvanceDAO.__instance


    def insertion_advance(self,  advance: Advance):
        request = """INSERT INTO advance(date, balance, id_invoice)
                     VALUES(?, ?, ?)"""
        values = (advance.date, advance.balance. advance.id_)
        self.bdd.cursor.execute()
        self.bdd.connexion.commit()

    def update_advance(self,liste):
        self.bdd=DBManager.get_instance()
        liste=liste[1:]+[liste[0]]
        self.bdd.cursor.execute("""UPDATE advance SET date=?,balance=?, id_invoice=? WHERE id_advance=?""",liste)
        self.bdd.connexion.commit()
    def delete_table(self,name, id):
        self.bdd=DBManager.get_instance()
        self.bdd.cursor.execute(""" DELETE FROM"""+name+""" WHERE id_"""+name+"""="""+str(id))
        self.bdd.connexion.commit()
    def selection_table(self,nom):
        self.bdd=DBManager.get_instance()
        self.bdd.cursor.execute("""select * from """+nom)
        return self.bdd.cursor.fetchall()

# class InvoiceDAO:
#     _instance=None
#     def get_instance():
#         if InvoiceDAO._instance==None:
#             InvoiceDAO._instance=InvoiceDAO()
#         return InvoiceDAO._instance
#     def insertion_invoice(self,liste):
#         bdd=DBManager.get_instance()
#         bdd.cursor.execute("""SELECT max(id_invoice_estimate) FROM invoice_estimate""")
#         bdd.connexion.commit()
#         id_max=bdd.cursor.fetchall()
#         bdd.cursor.execute("""INSERT INTO invoice(id_invoice,solde) VALUES(?,?)""",(id_max[0][0],liste[0]))
#         bdd.connexion.commit()
#     def selection_table(self,nom):
#         bdd=DBManager.get_instance()
#         bdd.cursor.execute("""select * from """+nom)
#         return bdd.cursor.fetchall()

# class ArticleDAO:
#     _instance=None

#     def get_instance():
#         if ArticleDAO._instance==None:
#             ArticleDAO._instance=ArticleDAO()

#         return ArticleDAO._instance
#     def insertion_article(self, liste):
#         bdd=DBManager.get_instance()
#         bdd.cursor.execute("""INSERT INTO article(name,description,price) VALUES(?,?,?)""",liste)
#         bdd.connexion.commit()
#     def update_article(self,liste):
#         bdd=DBManager.get_instance()
#         liste=liste[1:]+[liste[0]]
#         bdd.cursor.execute("""UPDATE article SET name=?,description=?,price=? WHERE id_article=?""",liste)
#         bdd.connexion.commit()
#     def selection_table(self):
#         bdd=DBManager.get_instance()
#         bdd.cursor.execute("""select * from article""")
#         return bdd.cursor.fetchall()

# class Invoice_devDAO:
#     _instance=None
#     def get_instance():
#         if Invoice_devDAO._instance==None:
#             Invoice_devDAO._instance=Invoice_devDAO()
#         return Invoice_devDAO._instance
#     def insertion_invoice_dev(self,liste):
#         bdd=DBManager.get_instance()
#         bdd.cursor.execute("""INSERT INTO invoice_estimate(balance,date,description,note,remark,id_client,id_user) VALUES(?,?,?,?,?,?,?)""",liste)
#         bdd.connexion.commit()
#     def update_invoice_dev(self,liste):
#         bdd=DBManager.get_instance()
#         liste=liste[1:]+[liste[0]]
#         bdd.cursor.execute("""UPDATE invoice_estimate SET balance=?,date=?,description=?,note=?,remark=?,id_client=?,id_user=? WHERE id_invoice_estimate=?""",liste)
#         bdd.connexion.commit()
#     def selection_table(self,nom):
#         bdd=DBManager.get_instance()
#         bdd.cursor.execute("""select * from """+nom)
#         return bdd.cursor.fetchall()
