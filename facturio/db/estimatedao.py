#!/usr/bin/env python3
from facturio.classes.invoice_misc import Estimate
from facturio.db.dbmanager import DBManager
from facturio.db.receiptdao import ReceiptDAO

class EstimateDAO:
    __instance = None

    def __init__(self):
        """Recupere le manager."""
        self.bdd = DBManager.get_instance()

    def get_instance():
        """Recupere l'instance."""
        if EstimateDAO.__instance is None:
            EstimateDAO.__instance = EstimateDAO()
        return EstimateDAO.__instance


    def insert(self, estimate: Estimate):
        """Insertion du estimate."""
        receipt_dao = ReceiptDAO.get_instance()
        receipt_dao.insert(estimate)

    def update(self, estimate: Estimate):
        # TODO
        raise NotImplementedError
    #     bdd=DBManager.get_instance()
    #     liste=liste[1:]+[liste[0]]
    #     bdd.cursor.execute("""UPDATE invoice_estimate SET balance=?,date=?,description=?,note=?,remark=?,id_client=?,id_user=? WHERE id_invoice_estimate=?""",liste)
    #     bdd.connexion.commit()

    def get_all(self):
        """Renvoie tous les devis."""
        request = ("SELECT * FROM receipt JOIN invoice "
                   "ON id_receipt=id_invoice "
                   "WHERE id_invoice=NULL")
        self.bdd.cursor.execute(request)
        return self.bdd.cursor.fetchall()
