#!/usr/bin/env python3
from facturio.classes.client import Client
from facturio.db.dbmanager import DBManager


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

        request = """INSERT INTO client(first_name, last_name, e_mail, address,
                     phone, remark) VALUES (?,?,?,?,?,?)"""
        values = (client.first_name, client.last_name, client.email,
                  client.address, client.phone_number, client.note)
        req = """
        select *
        from client

        """
        # self.bdd.cursor.execute(req)
        # self.bdd.connexion.commit()
        # jointure = self.bdd.cursor.fetchall()
        # for i in jointure:
        #     if i[1]==client.first_name and i[2]==client.last_name:
        #         print("tu ne peux pas ")
        #         return
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
        data = client.dump_to_list()
        data.append(client.id_)
        self.bdd.cursor.execute(request, data)
        self.bdd.connexion.commit()

    def delete(self, client: Client):
        """
        Prend un objet client et le supprime de la BD
        """
        if client.id_ is None:
            raise ValueError
        self.bdd.cursor.execute("DELETE FROM CLIENT WHERE id_client="+str(client.id_))
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
        if tup is None:
            raise ValueError
        client = Client(first_name=tup[1],
                        last_name=tup[2],
                        email=tup[3],
                        address=tup[4],
                        phone_number=tup[5],
                        note=tup[6],
                        id_=tup[0])

        return client

    def get_with_id(self, id_):
        """Renvoie une instace du client avec id_."""
        print(id_)
        request = f"SELECT * FROM client where id_client = {id_}"
        tup = self.bdd.cursor.execute(request).fetchone()
        print("tup==",tup)
        return self._gen_client(tup)



if __name__ == "__main__":
    dao = ClientDAO.get_instance()
    a =None
    a=dao.get_all()
    #avoir celui qu'on veut
    #a=a[len(a)-1]
    #a.first_name="titit"
    #dao.update(a)

