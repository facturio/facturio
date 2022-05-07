#!/usr/bin/env python3
from facturio.classes.invoice_misc import Advance
from facturio.db.dbmanager import DBManager


class AdvanceDAO():

    __instance = None

    def get_instance():
        """Recupere l'instance."""
        if AdvanceDAO.__instance is None:
            AdvanceDAO.__instance = AdvanceDAO()
        return AdvanceDAO.__instance

    def __init__(self):
        """Recupere le manager."""
        self.bdd = DBManager.get_instance()

    def insert(self, advance: Advance):
        """Insertion du advance."""
        request = """INSERT INTO advance(date, amount, id_invoice)
                     VALUES(?, ?, ?)"""
        # TODO s'assurer que le id_invoice existe sur la table invoice
        if advance.id_invoice is None:
            raise ValueError
        values = (advance.date, advance.amount, advance.id_invoice)
        self.bdd.cursor.execute(request, values)
        self.bdd.connexion.commit()
        max_req = "SELECT max(id_invoice) FROM advance"
        id_ = self.bdd.cursor.execute(max_req).fetchone()
        assert(len(id_) == 1)
        advance.id_ = id_[0]
        return

    def get_all_with_id_invoice(self, id_inv):
        request = f"SELECT * FROM advance WHERE id_invoice={id_inv}"
        advances_tup = self.bdd.cursor.execute(request).fetchall()
        res = []
        for tup in advances_tup:
            res.append(self._gen_advance(tup))
        return res



    # TODO:
    # def update_advance(self, advance: Advance):
    #     # TODO: Ifaire l'update
    #     raise NotImplementedError()
        # liste=liste[1:]+[liste[0]]
        # self.bdd.cursor.execute("""UPDATE advance SET date=?,balance=?, id_invoice=? WHERE id_advance=?""",liste)
        # self.bdd.connexion.commit()

    # TODO:
    # def delete_table(self,name, id):
    #     # TODO: Ifaire delete
    #     raise NotImplementedError()
        # self.bdd.cursor.execute(""" DELETE FROM"""+name+""" WHERE id_"""+name+"""="""+str(id))
        # self.bdd.connexion.commit()

    def get_all(self):

        req = "SELECT * FROM advance"
        tuples = self.bdd.cursor.execute(req).fetchall()
        res = []
        for tup in tuples:
            res.append(self._gen_advance(tup))
        return res

    @staticmethod
    def _gen_advance(tup):
        return Advance(id_=tup[0],
                       date=tup[1],
                       amount=tup[2],
                       id_invoice=tup[3])

if __name__ == "__main__":
    dao = AdvanceDAO()
    adv = Advance(1230.0)
