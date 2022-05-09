import unittest
import sqlite3
from facturio.db.userdao import UserDAO
from facturio.classes.user import User


class TestAdvanceDAO(unittest.TestCase):
    """Teste la classe UserDAO"""

    def test_insert(self):

        dao = UserDAO.get_instance()
        user = User("Facturio INC", "Yousggsef", "BENJEggLLOUN", "yb@gmail.com",
                    "427 Boulevard des armaris 8dsfdsfdsq3100 Toulon", "07 67 31 58 20",
                    "12348921 2341",)
        dao.insert(user)
        id = user.id_
        userliste = user.dump_to_list()
        self.assertEqual(dao.get_with_id(id), userliste)

    def test_updatre(self):
        dao = UserDAO.get_instance()
        user = dao.get()
        dao.insert(user)
        user.company_name = "tom"
        user.address = "olivier"
        dao.update_user(user)
        id = user.id_
        userliste = user.dump_to_list()
        print(userliste, dao.get_with_id(id))
        self.assertEqual(dao.get_with_id(id), userliste)
        dao.delete(id)


if __name__ == '__main__':
    unittest.main()
