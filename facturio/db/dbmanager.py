#!/usr/bin/env python3
import sqlite3


class DBManager:
    """Data Base Manager."""

    _instance = None

    def get_instance():
        """Recupere l'instance."""
        if DBManager._instance is None:
            DBManager._instance = DBManager()
        return DBManager._instance

    def __init__(self):
        """Fonction pour creation ou/et connexion a la data_base."""
        self.connexion = sqlite3.connect("facturio.db")

        # execution des requetes il faut un curseur
        self.cursor = self.connexion.cursor()

        # on active les clés etrangere, de base elle ne le sont pas
        self.cursor.execute("PRAGMA  foreign_keys = ON")

        self._creation_table_article()
        self._creation_table_user()
        self._creation_table_client()
        self._creation_table_company()
        self._creation_table_receipt()
        self._creation_table_invoice()
        self._creation_table_advance()

        # self._creation_table_art_dev()
        return

    def _creation_table_company(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS company
            (id_company INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            business_num TEXT,
            FOREIGN KEY(id_company) REFERENCES client(id_client)
            ON DELETE CASCADE)""")
        self.connexion.commit()

    def _creation_table_client(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS client
            (id_client INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            e_mail TEXT,
            address TEXT,
            phone TEXT,
            remark TEXT)""")
        self.connexion.commit()

    def _creation_table_user(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user
            (id_user INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            first_name TEXT,
            last_name TEXT,
            e_mail TEXT,
            address TEXT,
            phone TEXT,
            business_num TEXT,
            logo BLOB)""")
        self.connexion.commit()

    def _creation_table_article(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS article
            ( id_article INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            price REAL,
            quantity INTEGER,
            id_receipt INTEGER)""")
        self.connexion.commit()

    def _creation_table_receipt(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS receipt
            (id_receipt INTEGER PRIMARY KEY AUTOINCREMENT,
            balance REAL,
            taxes REAL,
            date INTEGER,
            note TEXT,
            id_client INTEGER,
            id_user INTEGER,
            FOREIGN KEY(id_user) REFERENCES user(id_user) ON DELETE CASCADE,
            FOREIGN KEY(id_client) REFERENCES client(id_client)
            ON DELETE CASCADE)""")
        self.connexion.commit()

    # def _creation_table_art_dev(self):
    #     self.cursor.execute("""
    #         CREATE TABLE IF NOT EXISTS art_dev
    #         (
    #         id_article INTEGER,
    #         id_invoice_estimate INTEGER,
    #         FOREIGN KEY(id_invoice_estimate) REFERENCES
    #         invoice_estimate(id_invoice_estimate) ON DELETE CASCADE,
    #         FOREIGN KEY(id_article) REFERENCES article(id_article))""")
    #     self.connexion.commit()

    def _creation_table_invoice(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoice
        (id_invoice INTEGER PRIMARY KEY AUTOINCREMENT,
        FOREIGN KEY(id_invoice) REFERENCES receipt(id_receipt)
        ON DELETE CASCADE)""")
        self.connexion.commit()

    def _creation_table_advance(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS advance
        (id_advance INTEGER PRIMARY KEY AUTOINCREMENT,
        date INTEGER,
        amount INTEGER,
        id_invoice INTEGER,
        FOREIGN KEY(id_invoice) REFERENCES invoice(id_invoice)
        ON DELETE CASCADE)""")
        self.connexion.commit()

    def close(self):
        """Fermeture de la BD."""
        self.connexion.close()

if __name__ == "__main__":
    exit()
    # TODO: Appeler le classe et tester que les
    # tables se sont bien crees
    # https://www.sqlite.org/faq.html#q7
