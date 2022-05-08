import unittest
from facturio.classes.user import User
from facturio.classes.client import Client, Company
from facturio.classes.invoice_misc import Advance, Article, Estimate, Invoice

# Initialisation d'instance de classes pour les tests
if(User.exists()):
    artisan = User.get_instance()
else:
    artisan = User(
            company_name="Facturio",
            address="15 rue des champs Cuers",
            phone_number="0734567221",
            business_number="128974654",
            first_name="Tom",
            last_name="Pommier",
            email="facturio@gmail.com",
            logo="logo.jpg",
            id_=3
    )

client_physique = Client(
        last_name="Lombardo",
        first_name="Quentin",
        email="quentin.lombardo@email.com",
        address="HLM Sainte-Muse Toulon",
        phone_number="0678905324",
        id_=4
)

client_moral = Company(
        company_name="LeRoy",
        email="LeRoy83@sfr.fr",
        address="12 ZAC de La Crau",
        phone_number="0345678910",
        first_name="Ben",
        last_name="Karim",
        business_number="287489404",
        id_=6
)

ordinateur = Article("ordinateur", 1684.33, 3, "Asus spire", 5, 2)
cable_ethernet = Article("cable ethernet", 9.99, 10, "15m", 6, 2)
telephone = Article("telephone", 399.99, 1, "téléphone clapet", 8, 2)
casque = Article("casque", 69.99, 6, "casque sans fils", 7, 2)
bureau = Article("Bureau", 500, 2, "Bureau à 6pieds", 9, 2)
articles = [ordinateur, cable_ethernet, telephone, casque, bureau]
paiements = [
    Advance(1230.0, date=1652017305, id_=7, id_invoice=2),
    Advance(654, date=1652017305, id_=8, id_invoice=2)
]


fact = Invoice(
        user=artisan,
        client=client_moral,
        articles_list=articles,
        advances_list=paiements,
        taxes=0.2,
        note="Invoice de matériel informatiques",
        date=1230,
        balance=100,
        id_=2
    )
dev = Estimate(
        user=artisan,
        client=client_physique,
        articles_list=articles,
        date=1230,
        taxes=0,
        note="Invoice de matériel informatiques",
        id_=2
)


class TestArticle(unittest.TestCase):
    """Teste la classe Article"""
    def test_dump_to_list(self):
        self.assertEqual(
            ordinateur.dump_to_list(),
            ['ordinateur', 'Asus spire', 1684.33, 3, 5, 2]
        )


class TestAdvance(unittest.TestCase):
    """Teste la classe Advance"""
    def test_dump_to_list(self):
        self.assertEqual(
            Advance(1230.0, date=1652017305, id_=7, id_invoice=2)
            .dump_to_list(),
            [1230.0, 1652017305, 7, 2]
        )

    def test_date_string(self):
        self.assertEqual(
            Advance(1230.0, date=1652017305, id_=7, id_invoice=2)
            .date_string(),
            "08/05/2022"
        )


class TestReceipt(unittest.TestCase):
    """Teste la classe Receipt"""

    def test_dump_to_list(self):
        self.assertEqual(
            dev.dump_to_list(), [
                artisan, client_physique, 1230, articles, 0, None,
                "Invoice de matériel informatiques", 2
            ]
        )

    def test_subtotal(self):
        amount = 0
        for art in dev.articles_list:
            amount += art.price * art.quantity
        amount = round(amount, 2)
        self.assertEqual(dev.subtotal(), amount)

    def test_total_of_taxes(self):
        self.assertEqual(dev.subtotal()*dev.taxes, dev.total_of_taxes())

    def test_total_with_taxes(self):
        self.assertEqual(dev.subtotal()*(1+dev.taxes), dev.total_with_taxes())


class TestInvoice(unittest.TestCase):
    """Teste la classe Receipt"""
    def test_dump_to_list(self):
        self.assertEqual(fact.dump_to_list(), [
            artisan, client_moral, 1230, articles, paiements, 0.2, 100,
            "Invoice de matériel informatiques", 2
        ])

    def test_total_with_advances(self):
        self.assertEqual(
            round(fact.total_with_taxes()-fact.total_of_advances(), 2),
            fact.total_with_advances()
        )

    def test_total_of_advances(self):
        amount = 0
        if(fact.advances_list is not None):
            for adv in fact.advances_list:
                amount += adv.amount
        amount = round(amount, 2)
        self.assertEqual(amount, fact.total_of_advances())


class TestEstimate(unittest.TestCase):
    """Teste la classe Receipt"""


if __name__ == '__main__':
    unittest.main()
