#!/usr/bin/env python3
from facturio.db.dbmanager import DBManager
from facturio.db.receiptdao import ReceiptDAO
from facturio.db.clientdao import ClientDAO
from facturio.db.articledao import ArticleDAO
from facturio.db.userdao import UserDAO
from facturio.db.companydao import CompanyDAO
from facturio.classes.invoice_misc import Estimate

class EstimateDAO:
    __instance = None

    def __init__(self):
        """Recupere le manager."""
        self.db = DBManager.get_instance()

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
        """# TODO."""
    #     bdd=DBManager.get_instance()
    #     liste=liste[1:]+[liste[0]]
    #     bdd.cursor.execute("""UPDATE invoice_estimate SET balance=?,date=?,description=?,note=?,remark=?,id_client=?,id_user=? WHERE id_invoice_estimate=?""",liste)
    #     bdd.connexion.commit()
        raise NotImplementedError

    def _gen_estimate(self, tup):
        udao = UserDAO.get_instance()
        cdao = ClientDAO.get_instance()
        compdao = CompanyDAO.get_instance()
        user = udao.get()
        # entreprise ou client?
        # Verifier si l'id est un entrprise
        id_client = tup[5]
        assert(id_client is not None)
        request = f"SELECT * FROM company where id_company={id_client}"
        client = None
        if self.db.cursor.execute(request).fetchone() is None:
            client = cdao.get_with_id(id_client)
        else:
            client = compdao.get_with_id(id_client)
        art_dao = ArticleDAO.get_instance()
        articles = art_dao.get_all_with_id_receipt(tup[0])
        return Estimate(id_=tup[0],
                        balance=tup[1],
                        taxes=tup[2],
                        date=tup[3],
                        note=tup[4],
                        articles_list=articles,
                        client=client,
                        user=user)

    def get_with_id(self, id_est):
        """Revoie l'instance avec l'id id_est."""
        # TODO: Verifier qu'il s'agit bien d'un devis
        request = ("SELECT * FROM receipt "
                   f"WHERE id_receipt={id_est}")
        tup = self.db.cursor.execute(request).fetchone()
        return self._gen_estimate(tup)

    def get_all(self):
        """Renvoie tous les devis."""
        request = ("SELECT * FROM receipt WHERE id_receipt NOT IN "
                   "(SELECT id_invoice FROM invoice)")
        all_tup = self.db.cursor.execute(request).fetchall()
        res = []
        for tup in all_tup:
            res.append(self._gen_estimate(tup))
        return res
