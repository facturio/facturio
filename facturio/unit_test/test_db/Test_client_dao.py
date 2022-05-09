import unittest
import sqlite3
from facturio.db.clientdao import ClientDAO
from facturio.classes.client import Client


class TestClientDAO(unittest.TestCase):
    """Teste la classe UserDAO"""

    def test_insert(self):

        dao = ClientDAO.get_instance()
        client = Client("tom", "olivier", "tomolovier283@gmail.com",
                        "trou du cu", "0123456789", "chef")
        dao.insert(client)
        id = client.id_
        clientliste = client.dump_to_list()
        clientgetid = dao.get_with_id(id).dump_to_list()
        self.assertEqual(clientgetid, clientliste)

    def test_update(self):
        dao = ClientDAO.get_instance()
        client = dao.get_all()
        client[0].first_name = "clement"
        client[0].last_name = "bazan"
        id = client[0].id_
        dao.update(client[0])

        clientliste = client[0].dump_to_list()
        clientgetid = dao.get_with_id(id).dump_to_list()
        self.assertEqual(clientgetid, clientliste)
        dao.delete(id)


if __name__ == '__main__':
    unittest.main()
