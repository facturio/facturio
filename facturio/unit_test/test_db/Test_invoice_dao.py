import unittest
import sqlite3
from facturio.db.recieptdao import RecieptDAO
from facturio.classes.reciept import Reciept


class TestRecieptDAO(unittest.TestCase):
    """Teste la classe RecieptDAO"""

    def test_insert(self):

        dao = ReceiptDAO.get_instance()
        reciept = Reciept("Facturio INC", "Yousggsef", "BENJEggLLOUN", "yb@gmail.com",
                          "427 Boulevard des armaris 8dsfdsfdsq3100 Toulon", "07 67 31 58 20",
                          "12348921 2341",)
        dao.insert(reciept)
        id = reciept.id_
        recieptliste = reciept.dump_to_list()
        self.assertEqual(dao.get_with_id(id), recieptliste)

    def test_update(self):
        dao = RecieptDAO.get_instance()
        reciept = dao.get()
        dao.insert(reciept)
        reciept.company_name = "tom"
        reciept.address = "olivier"
        dao.update_reciept(reciept)
        id = reciept.id_
        recieptliste = reciept.dump_to_list()
        self.assertEqual(dao.get_with_id(id), recieptliste)
        dao.delete(id)


if __name__ == '__main__':
    unittest.main()
