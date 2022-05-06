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


