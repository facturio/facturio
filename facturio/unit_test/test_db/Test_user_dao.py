import unittest
import sqlite3
from facturio.db.userdao import UserDAO
from facturio.classes.user import User


class TestUserDAO(unittest.TestCase):
    """Teste la classe UserDAO"""

    def test_insert(self):

        dao = UserDAO.get_instance()
        user = User("Facturio INC", "Yousggdsfdsef", "BENJdfdsEggLLOUN", "yb@gmail.com",
                    "427 Boulevard des armaris 8dsfdsfdfdsdsq3100 Toulon", "07 67 31 58 20",
                    "12348921 2341",)
        dao.insert(user)
        id = user.id_
        userliste = user.dump_to_list()
        self.assertEqual(dao.get_with_id(id), userliste)

    def test_update(self):
        dao = UserDAO.get_instance()
        user = dao.get()
        dao.insert(user)
        user.company_name = "tom"
        user.address = "olivier"
        dao.update_user(user)
        id = user.id_
        userliste = user.dump_to_list()
        self.assertEqual(dao.get_with_id(id), userliste)
        dao.delete(id)


if __name__ == '__main__':
    unittest.main()
