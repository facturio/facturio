from facturio.db.receiptdao import ReceiptDAO
from facturio.db.clientdao import ClientDAO
from facturio.db.userdao import UserDAO
from facturio.db.articledao import ArticleDAO
from facturio.db.advancedao import AdvanceDAO
from facturio.db.companydao import CompanyDAO
from facturio.db.dbmanager import DBManager
from facturio.classes.invoice_misc import Invoice

class InvoiceDAO:
    __instance=None

    def get_instance():
        """Recupere l'instance."""
        if InvoiceDAO.__instance is None:
            InvoiceDAO.__instance = InvoiceDAO()
        return InvoiceDAO.__instance

    def __init__(self):
        """Recuperation du DBManager."""
        self.db = DBManager.get_instance()

    def insert(self, invoice: Invoice):
        """Insertion de la facture."""
        rdao = ReceiptDAO.get_instance()
        rdao.insert(invoice)
        max_req = "SELECT max(id_receipt) FROM receipt"
        id_rcp = self.db.cursor.execute(max_req).fetchone()[0]
        # TODO: CHANGER SOLDE PAR BALANCE PARTOUT
        request = "INSERT INTO invoice(id_invoice, solde) VALUES(?,?)"
        self.db.cursor.execute(request, (id_rcp, invoice.balance))
        self.db.connexion.commit()
        # insertion des accomptes
        adv_dao = AdvanceDAO.get_instance()
        for advance in invoice.advances_list:
            advance.id_invoice = id_rcp
            adv_dao.insert(advance)

    # def _set_id(self, invoice: Invoice, id_inv):
    #     """Mis a jour l'id_invoice des acomptes."""
    #     for advance in invoice.advances_list:
    #         advance.id_invoice = id_inv

    def get_all(self):
        """Renvoie des tous les instances de Invoice dans la bd."""
        req = """SELECT *
                FROM invoice
                INNER JOIN receipt ON invoice.id_invoice=receipt.id_receipt"""
        invoices = self.db.cursor.execute(req).fetchall()
        res = []
        for inv in invoices:
            res.append(self._gen_invoice(inv))
        return res

    def get_with_id(self, id_inv):

        request = ("SELECT * FROM invoice "
                   "INNER JOIN receipt ON "
                   "invoice.id_invoice=receipt.id_receipt "
                   f"WHERE invoice.id_invoice={id_inv}")
        tup = self.db.cursor.execute(request).fetchone()
        print(tup)
        return self._gen_invoice(tup)


    def _gen_invoice(self, tup):
        udao = UserDAO.get_instance()
        cdao = ClientDAO.get_instance()
        compdao = CompanyDAO.get_instance()
        user = udao.get()
        # entreprise ou client?
        # Verifier si l'id est un entrprise
        id_cli_comp = tup[7]
        request = f"SELECT * FROM company where id_company={id_cli_comp}"
        client = None
        if self.db.cursor.execute(request).fetchone() is None:
            client = cdao.get_with_id(id_cli_comp)
        else:
            client = compdao.get_with_id(id_cli_comp)

        user = udao.get()
        art_dao = ArticleDAO.get_instance()
        articles = art_dao.get_all_with_id_receipt(tup[0])
        adv_dao = AdvanceDAO.get_instance()
        advances = adv_dao.get_all_with_id_invoice(tup[0])
        return Invoice(user=user,
                       client=client,
                       articles_list=articles,
                       taxes=tup[4],
                       date=tup[5],
                       balance=tup[1],
                       advances_list=advances,
                       note=tup[6],
                       id_=tup[0])

        # TODO
        raise NotImplementedError

    def delete(self, invoice: Invoice):
        """Supprime la entree represente par invoice."""
        # TODO
        raise NotImplementedError

    def update(self, invoice: Invoice):
        """Mise a jour de la entree represente par invoice."""
        # TODO
        raise NotImplementedError

if __name__ == "__main__":
    from facturio.classes.invoice_misc import Article, Advance
    from facturio.classes.client import Client, Company
    from facturio.classes.user import User
    from facturio.db.articledao import ArticleDAO


    user = User(company_name="Facturio INC", last_name="BENJELLOUN",
                first_name="Youssef", email="yb@gmail.com",
                address="427 Boulevard des armoaris 83100 Toulon",
                phone_number="07 67 31 58 20",
                business_number="12348921 2341")

    comp = Company(company_name="LeRoy", last_name="Ben",
                   first_name="Karim", business_number="287489404",
                   email="LeRoy83@sfr.fr", address="12 ZAC de La Crau",
                   phone_number="0345678910")

    ordinateur = Article("Ordinateur", 1684.33, 3)
    cable_ethernet = Article("Cable ethernet", 5, 10)
    telephone = Article("Telephone", 399.99, 1)
    casque = Article("Casque", 69.99, 6)
    articles = [ordinateur, cable_ethernet, telephone, casque]
    paiements = [Advance(1230.0), Advance(654)]
    fact = Invoice(user=user, client=comp, articles_list=articles,
                   advances_list=paiements, date=0, taxes=0.2, balance=12,
                   note="Facture de matériel informatiques")

    user_dao = UserDAO.get_instance()
    client_dao = ClientDAO.get_instance()
    company_dao = CompanyDAO.get_instance()
    receipt_dao = ReceiptDAO.get_instance()
    art_dao = ArticleDAO.get_instance()
    inv_dao = InvoiceDAO.get_instance()

    def show():
        """Affiche toutes les tables"""
        print("user")
        print(user_dao.get())
        print("client")
        print(client_dao.get_all())
        print("company")
        print(company_dao.get_all())
        print("receipt")
        print(receipt_dao.get_all())
        print("article")
        print(art_dao.get_all())
        print("invoice")
        print(inv_dao.get_all())
