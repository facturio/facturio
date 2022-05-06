#!/usr/bin/env python3
from dbmanager import DBManager
from facturio.classes.client import Client


class ClientDAO:
    """Client controleur pour la DB."""

    __instance = None

    def __init__(self):
        """Recupere le manager."""
        self.bdd = DBManager.get_instance()

    def get_instance():
        """Recupere l'instance."""
        if ClientDAO.__instance is None:
            ClientDAO.__instance = ClientDAO()
        return ClientDAO.__instance

    def insert(self, client: Client):
        """Insertion du client."""
        # TODO: Verifier que le client ne soit pas deja
        request = """INSERT INTO client(first_name, last_name, e_mail, address,
                     phone, remark) VALUES (?,?,?,?,?,?)"""
        values = (client.first_name, client.last_name, client.email,
                  client.address, client.phone_number, client.note)
        self.bdd.cursor.execute(request, values)
        self.bdd.connexion.commit()
        # On recupere l'id qui vient d'etre insere'
        max_req = "SELECT max(id_client) FROM client"
        id_ = self.bdd.cursor.execute(max_req).fetchone()
        assert(len(id_) == 1)
        client.id_ = id_[0]
        return

    def update(self, client: Client):
        """Mis a jour du client."""
        if client.id_ is None:
            raise ValueError
        request = """UPDATE client SET first_name=?, last_name=?, e_mail=?,
                     address=?, phone=?, remark=? WHERE id_client=?"""
        data = client.to_list()
        data.append(client.id_)
        self.bdd.cursor.execute(request, data)
        self.bdd.connexion.commit()

    def get_all(self):
        """Renvoie une liste tous les instances des client sur la BD."""
        tuples = self.bdd.cursor.execute("select * from  client").fetchall()
        res = []
        for tup in tuples:
            res.append(self._gen_client(tup))
        return res

    @staticmethod
    def _gen_client(tup):
        client = Client(first_name=tup[1],
                        last_name=tup[2],
                        email=tup[3],
                        adress=tup[4],
                        phone_number=tup[5],
                        note=tup[6],
                        id_=tup[0])
        return client

if __name__ == "__main__":
    # TODO: Tester tous les fonctions
    dao = ClientDAO.get_instance()
    c = Client("Quentin","Lombardo",
            "quentin.lombardo@email.com", "HLM Sainte-Muse Toulon",
               "0678905324")