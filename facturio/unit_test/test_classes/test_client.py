import unittest
from facturio.classes.client import Client, Company


class TestClient(unittest.TestCase):
    """Teste la classe Client"""
    def test_dump_to_list(self):
        self.assertEqual(Client(
            "Quentin", "Lombardo",
            "quentin.lombardo@email.com", "HLM Sainte-Muse Toulon",
            "0678905324", note="Personne peu sympathique", id_=13)
            .dump_to_list(),
            [
                'Quentin', 'Lombardo', 'quentin.lombardo@email.com',
                'HLM Sainte-Muse Toulon', '0678905324',
                'Personne peu sympathique', 13
            ])

class TestCompany(unittest.TestCase):
    """Teste la classe Company"""
    def test_dump_to_list(self):
        self.assertEqual(Company(
            "LeRoy", "Ben", "Karim", "287489404", "LeRoy83@sfr.fr",
            "12 ZAC de La Crau", "0345678910", note="Investisseur important",
            id_=34).dump_to_list(),
            [
                'LeRoy', '287489404', 'LeRoy83@sfr.fr', '12 ZAC de La Crau',
                'Ben', 'Karim', '0345678910', 'Investisseur important', 34
            ])


if __name__ == '__main__':
    unittest.main()
