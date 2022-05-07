#!/usr/bin/env python3
from dbmanager import DBManager
from facturio.classes.client import Client, Company
from clientdao import ClientDAO


class CompanyDAO:
    __instance = None

    def __init__(self):
        """Recupere le manager."""
        self.bdd = DBManager.get_instance()

    def get_instance():
        """Recupere l'instance."""
        if CompanyDAO.__instance is None:
            CompanyDAO.__instance = CompanyDAO()
        return CompanyDAO.__instance

    def insert(self, company: Company):
        """Insertion de l'entrepries."""

        client_dao = ClientDAO.get_instance()
        c = Client(company.first_name, company.last_name, company.email,
                   company.address, company.phone_number)
        client_dao.insert(c)
        # cherche le max id
        self.bdd.cursor.execute("""SELECT max(id_client) FROM client""")
        self.bdd.connexion.commit()
        id_max = self.bdd.cursor.fetchall()
        company.id_ = id_max[0][0]
        req = """INSERT INTO company(id_company, company_name, business_num)
                VALUES(?,?,?)"""
        values = (company.id_, company.company_name, company.business_number)
        self.bdd.cursor.execute(req, values)
        self.bdd.connexion.commit()

    def update(self, company: Client):
        """Mis a jour du client."""
        if company.id_ is None:
            raise ValueError
        request = """UPDATE client SET first_name=?, last_name=?, e_mail=?,
                     address=?, phone=?, remark=? WHERE id_client=?"""
        data = [company.first_name, company.last_name, company.email,
                company.address, company.phone_number, company.note,
                company.id_]
        print(data)
        self.bdd.cursor.execute(request, data)

        # mis a jour de entreprise
        request = """UPDATE company SET company_name=?, business_num=?
                     WHERE id_company=?"""
        data = [company.company_name, company. business_number, company.id_]

        self.bdd.cursor.execute(request, data)
        self.bdd.connexion.commit()

    def get_all(self):
        """Renvoie une liste tous les instances entreprise sur la BD."""
        request = ("SELECT * FROM client JOIN company WHERE "
                   "id_company=id_client")
        tuples = self.bdd.cursor.execute(request).fetchall()
        res = []
        for tup in tuples:
            res.append(self._gen_company(tup))
        return res

    @staticmethod
    def _gen_company(tup):
        company = Company(first_name=tup[1],
                          last_name=tup[2],
                          email=tup[3],
                          address=tup[4],
                          phone_number=tup[5],
                          note=tup[6],
                          id_=tup[0],
                          business_number=tup[8],
                          company_name=tup[9])
        return company

    def inner(self):
        req = """
        select *
        from client
        inner join company on company.id_company=client.id_client
        """
        self.bdd.cursor.execute(req)
        self.bdd.connexion.commit()
        jointure = self.bdd.cursor.fetchall()
        # for i in jointure:
        #    print(i,"\n")
        return jointure


if __name__ == "__main__":
    dao = CompanyDAO.get_instance()
    comp = Company("LeRoy", "Ben", "Karim", "287489404",
                   "LeRoy83@sfr.fr", "12 ZAC de La Crau", "0345678910")
    # dao.inser(comp)
    # dao.inner()
    # pour update
    client = dao.inner()
    # selection de id

    id = 11
    for i in client:
        if id == i[0]:
            client = i
            break
    client = dao._gen_company(client)
    # attribut a modifier
    client.first_name = "geoge"
    client.company_name = "caca"

    dao.update(client)
