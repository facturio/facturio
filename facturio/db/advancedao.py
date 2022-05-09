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

    def update_advance(self, advance: Advance):

        self.bdd.cursor.execute("""UPDATE advance SET date=?,balance=?,
        id_invoice=? WHERE id_advance=?""", (advance.date, advance.balance,
                                advance.id_invoice, advance.id_advance))
        self.bdd.connexion.commit()

    def delete_table(self, id):

        self.bdd.cursor.execute(
            """ DELETE FROM advance WHERE id_advance="""+str(id))
        self.bdd.connexion.commit()

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
    adv.id_advance = 3
    adv.balance = 100

    # dao.insert(adv)
    dao.update_advance(adv)
    # dao.delete_table(2)
