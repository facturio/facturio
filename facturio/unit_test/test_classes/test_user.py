import unittest
from facturio.classes.user import User

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
            logo="logo.jpg"
            )


class TestUser(unittest.TestCase):
    """Teste la classe User"""
    def test_dump_to_list(self):
        self.assertEqual(artisan.dump_to_list(), [
            'logo.jpg', 'Facturio', 'facturio@gmail.com',
            '15 rue des champs Cuers', '0734567221', 'Tom', 'Pommier',
            '128974654'
        ])


if __name__ == '__main__':
    unittest.main()
