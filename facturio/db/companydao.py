#!/usr/bin/env python3

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
        client_dao.insert(company)
        assert(company.id_ is not None)
        req = """INSERT INTO company(id_company, company_name, business_num)
                VALUES(?,?,?)"""
        values = (company.id_, company.company_name, company.business_number)
        self.bdd.cursor.execute(req, values)
        self.bdd.connexion.commit()

    def update(self, client: Client):
        raise NotImplementedError
        # TODO: Faire l'update
        # """Mis a jour du client."""
        # if client.id_ is None:
        #     raise ValueError
        # request = """UPDATE client SET first_name=?, last_name=?, e_mail=?,
        #              address=?, phone=?, remark=? WHERE id_client=?"""
        # data = client.to_list()
        # data.append(client.id_)
        # self.bdd.cursor.execute(request, data)
        # self.bdd.connexion.commit()
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
                          adress=tup[4],
                          phone_number=tup[5],
                          note=tup[6],
                          id_=tup[0],
                          business_number=tup[8],
                          company_name=tup[9])
        return company



if __name__ == "__main__":
    dao = CompanyDAO.get_instance()
    comp = Company("LeRoy", "Ben", "Karim", "287489404",
                "LeRoy83@sfr.fr", "12 ZAC de La Crau", "0345678910")
