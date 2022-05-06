from datetime import date
from facturio.classes.client import Client, Company
from dbmanager import DBManager


class ClientDAO:
    """Client controleur pour la DB"""
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
                  client.adress, client.phone_number, client.note)
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
    # TODO: Tester tous les fonctions
    dao = ClientDAO.get_instance()
    c = Client("Quentin","Lombardo",
            "quentin.lombardo@email.com", "HLM Sainte-Muse Toulon",
               "0678905324")
    dao = CompanyDAO.get_instance()
    comp = Company("LeRoy", "Ben", "Karim", "287489404",
                "LeRoy83@sfr.fr", "12 ZAC de La Crau", "0345678910")

# class UserDAO:
#     _instance=None
#     def get_instance():
#         if userDAO._instance==None:
#             userDAO._instance=userDAO()
#         return userDAO._instance
#     def insertion_user(self,liste):
#         bdd=DBManager.get_instance()
#         texte=liste[0]
#         #convertir image logo sous forme de fichier binaire
#         with open(texte,"rb") as myfile:
#             blobfile=myfile.read()

#         liste[0]=blobfile

#         bdd.cursor.execute("""INSERT INTO user(logo,company_name,e_mail,address,phone,business_num) VALUES(?,?,?,?,?,?)""",liste)
#         bdd.connexion.commit()
#     def update_user(self,liste):
#         bdd=DBManager.get_instance()
#         liste=liste[1:]+[liste[0]]
#         bdd.cursor.execute("""UPDATE user SET logo=?,company_name=?,e_mail=?,
#         address=?,phone=?,business_num=? WHERE id_user=?""",liste)
#         bdd.connexion.commit()
#     def delete_table(self,name, id):
#         bdd=DBManager.get_instance()
#         bdd.cursor.execute(""" DELETE FROM"""+name+""" WHERE id_"""+name+"""="""+str(id))
#         bdd.connexion.commit()
#     def selection_table(self,nom):
#         bdd=DBManager.get_instance()
#         bdd.cursor.execute("""select * from """+nom)
#         return bdd.cursor.fetchall()

# class AdvanceDAO():
#     _instance=None
#     def get_instance():
#         if AdvanceDAO._instance==None:
#             AdvanceDAO._instance=AdvanceDAOs()
#         return AdvanceDAO._instance
#     def insertion_advance(self,liste):
#         bdd=DBManager.get_instance()
#         data=date.today()
#         bdd.cursor.execute("""INSERT INTO advance(date,balance,id_invoice) VALUES(?,?,?)""",(data,liste[0],liste[1]))
#         bdd.connexion.commit()
#     def update_advance(self,liste):
#         bdd=DBManager.get_instance()
#         liste=liste[1:]+[liste[0]]
#         bdd.cursor.execute("""UPDATE advance SET date=?,balance=?, id_invoice=? WHERE id_advance=?""",liste)
#         bdd.connexion.commit()
#     def delete_table(self,name, id):
#         bdd=DBManager.get_instance()
#         bdd.cursor.execute(""" DELETE FROM"""+name+""" WHERE id_"""+name+"""="""+str(id))
#         bdd.connexion.commit()
#     def selection_table(self,nom):
#         bdd=DBManager.get_instance()
#         bdd.cursor.execute("""select * from """+nom)
#         return bdd.cursor.fetchall()

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

# class ArticleDAO:
#     _instance=None

#     def get_instance():
#         if ArticleDAO._instance==None:
#             ArticleDAO._instance=ArticleDAO()

#         return ArticleDAO._instance
#     def insertion_article(self, liste):
#         bdd=DBManager.get_instance()
#         bdd.cursor.execute("""INSERT INTO article(name,description,price) VALUES(?,?,?)""",liste)
#         bdd.connexion.commit()
#     def update_article(self,liste):
#         bdd=DBManager.get_instance()
#         liste=liste[1:]+[liste[0]]
#         bdd.cursor.execute("""UPDATE article SET name=?,description=?,price=? WHERE id_article=?""",liste)
#         bdd.connexion.commit()
#     def selection_table(self):
#         bdd=DBManager.get_instance()
#         bdd.cursor.execute("""select * from article""")
#         return bdd.cursor.fetchall()

# class Invoice_devDAO:
#     _instance=None
#     def get_instance():
#         if Invoice_devDAO._instance==None:
#             Invoice_devDAO._instance=Invoice_devDAO()
#         return Invoice_devDAO._instance
#     def insertion_invoice_dev(self,liste):
#         bdd=DBManager.get_instance()
#         bdd.cursor.execute("""INSERT INTO invoice_estimate(balance,date,description,note,remark,id_client,id_user) VALUES(?,?,?,?,?,?,?)""",liste)
#         bdd.connexion.commit()
#     def update_invoice_dev(self,liste):
#         bdd=DBManager.get_instance()
#         liste=liste[1:]+[liste[0]]
#         bdd.cursor.execute("""UPDATE invoice_estimate SET balance=?,date=?,description=?,note=?,remark=?,id_client=?,id_user=? WHERE id_invoice_estimate=?""",liste)
#         bdd.connexion.commit()
#     def selection_table(self,nom):
#         bdd=DBManager.get_instance()
#         bdd.cursor.execute("""select * from """+nom)
#         return bdd.cursor.fetchall()



# class Art_devDAO:
#     _instance=None
#     def get_instance():
#         if art_dev._instance==None:
#             art_dev._instance=DBManager()
#         return art_dev._instance
#     def insertion_art_dev(self,liste):
#         bdd=DBManager.get_instance()
#         """ liste de 2 indice
#         le premier pour id de article
#         le deuxieme pour id de fac_dev   """
#         bdd.cursor.execute("""INSERT INTO art_dev(id_article,id_invoice_estimate) VALUES(?,?)""",(liste))
#         bdd.connexion.commit()
#     def update_invoice_dev(self,liste):
#         bdd=DBManager.get_instance()
#         liste=liste[1:]+[liste[0]]
#         bdd.cursor.execute("""UPDATE invoice_estimate SET balance=?,date=?,description=?,note=?,remark=?,id_client=?,id_user=? WHERE id_invoice_estimate=?""",liste)
#         bdd.connexion.commit()
#     def selection_table(self,nom):
#         bdd=DBManager.get_instance()
#         bdd.cursor.execute("""select * from """+nom)
#         return bdd.cursor.fetchall()
