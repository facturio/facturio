import unittest
import sqlite3
from facturio.db.companydao import CompanyDAO
from facturio.classes.client import Company


class TestCompanyDAO(unittest.TestCase):
    """Teste la classe CompanyDAO"""

    def test_insert(self):

        dao = CompanyDAO.get_instance()
        company = Company("Facturio INC", "Yousggsef", "BENJEggLLOUN", "yb@gmail.com",
                          "427 Boulevard des armaris 8dsfdsfdsq3100 Toulon", "07 67 31 58 20",
                          "12348921 2341",)
        dao.insert(company)
        id = company.id_
        companyliste = company.dump_to_list()
        self.assertEqual(dao.get_with_id(id).dump_to_list(), companyliste)

    def test_update(self):
        dao = CompanyDAO.get_instance()
        company = dao.get_all()
        company[0].company_name = "tom"
        company[0].address = "olivier"
        dao.update(company[0])
        id = company[0].id_
        print(id)
        companyliste = company[0].dump_to_list()
        self.assertEqual(dao.get_with_id(id).dump_to_list(), companyliste)
        dao.delete(id)


if __name__ == '__main__':
    unittest.main()
