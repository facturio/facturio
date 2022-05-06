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
        request = """INSERT INTO receipt(balance, date, note,
                      id_client, id_user) VALUES (?,?,?,?,?,?,?)"""
        # TODO: Verifier que les id_client et id_user existent et ne soient
        # pas egale a None
        values = (receipt.balance, receipt.date, receipt.note,
                  receipt.client.id_, receipt.user.id_)
        self.bdd.cursor.execute(request, values)
        self.bdd.connexion.commit()
        # On recupere l'id qui vient d'etre insere'
        max_req = "SELECT max(id_receipt) FROM receipt"
        id_ = self.bdd.cursor.execute(max_req).fetchone()
        assert(len(id_) == 1)
        receipt.set_id(id_[0])

    def update(self, receipt: ReceiptDAO):
        # TODO
    #     bdd=DBManager.get_instance()
    #     liste=liste[1:]+[liste[0]]
    #     bdd.cursor.execute("""UPDATE invoice_estimate SET balance=?,date=?,description=?,note=?,remark=?,id_client=?,id_user=? WHERE id_invoice_estimate=?""",liste)
    #     bdd.connexion.commit()
        raise NotImplementedError

    def get_all(self):
        request = "SELECT * FROM receipt"
        return bdd.cursor.fetchall()
