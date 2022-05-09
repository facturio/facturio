from xdg import BaseDirectory
import sqlite3
from datetime import date

class Data_base:

    def __init__(self , name):
        #nom de la table
        self.name=name
        #fonction pour creation ou/et connexion
        # a la data_base
        self.connexion=sqlite3.connect(BaseDirectory.save_data_path("facturio") + self.name+'.db')

        # execution des requetes il faut un curseur
        self.cursor=self.connexion.cursor()

        # on active les clés etrangere,de base elle ne le sont pas
        self.cursor.execute("PRAGMA  foreign_keys = ON")

        self.__creation_table_article()
        self.__creation_table_user()
        self.__creation_table_client()
        self.__creation_table_company()
        self.__creation_table_invoice_devis()
        self.__creation_table_invoice()
        self.__creation_table_art_dev()
        self.__creation_table_deposit()


    def __creation_table_company(self):
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS company
            (id_company INTEGER PRIMARY KEY,
            company_name STRING,
            num_SIRET INTEGER ,
            FOREIGN KEY(id_company) REFERENCES client(id_client) ON DELETE CASCADE
            )
            """)
            self.connexion.commit()

    def __creation_table_client(self):
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS client
            (id_client INTEGER PRIMARY KEY,
            last_name STRING,
            first_name STRING,
            e_mail STRING,
            address STRING,
            phone STRING,
            remark STRING
            )
            """)
            self.connexion.commit()

    def __creation_table_user(self):
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user
            ( id_user INTEGER PRIMARY KEY AUTOINCREMENT,
            logo BLOB,
            company_name STRING,
            e_mail STRING,
            address STRING,
            phone STRING,
            num_SIREN STRING
            )
            """)
            self.connexion.commit()

    def __creation_table_article(self):
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS article
            ( id_article INTEGER PRIMARY KEY AUTOINCREMENT,
            name STRING,
            description STRING,
            price float
            )
            """)
            self.connexion.commit()

    def db_delete_client(self, id_):
        """
        Prend un objet client et le supprime de la BD
        """
        if id_ is None:
            raise ValueError
        self.cursor.execute("DELETE FROM CLIENT WHERE id_client="+str(id_))
        self.connexion.commit()

    def find_client(self, id_):
            """
            Prend un objet client et le supprime de la BD
            """
            if id_ is None:
                raise ValueError
            request = f"SELECT * FROM client where id_client = {id_}"
            tup = self.cursor.execute(request).fetchone()
            print(tup)
            return tup

    def __creation_table_invoice_devis(self):
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoice_devis
            ( id_invoice_devis INTEGER PRIMARY KEY AUTOINCREMENT,
            amount FLOAT,
            date INTEGER,
            description STRING,
            note STRING,
            remark STRING,
            id_client INTEGER,
            id_user INTEGER,
            FOREIGN KEY(id_user) REFERENCES user(id_user),
            FOREIGN KEY(id_client) REFERENCES client(id_client) ON DELETE CASCADE
            )
            """)
            self.connexion.commit()

    def __creation_table_art_dev(self):
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS art_dev
            (
            id_article INTEGER,
            id_invoice_devis INTEGER,
            FOREIGN KEY(id_invoice_devis) REFERENCES invoice_devis(id_invoice_devis) ON DELETE CASCADE,
            FOREIGN KEY(id_article) REFERENCES article(id_article)
            )
            """)
            self.connexion.commit()

    def __creation_table_invoice(self):
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoice
            (
            id_invoice INTEGER PRIMARY KEY AUTOINCREMENT,
            solde INTEGER
            )
            """)
            self.connexion.commit()

    def __creation_table_deposit(self):
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS deposit
            (id_deposit INTEGER PRIMARY KEY AUTOINCREMENT,
            date INTEGER,
            amount STRING,
            id_invoice INTEGER,
            FOREIGN KEY(id_invoice) REFERENCES invoice(id_invoice) ON DELETE CASCADE
            )
            """)
            self.connexion.commit()

    def selection_table(self,nom):
            self.cursor.execute("""select * from """+nom)

            return self.cursor.fetchall()

    def delete_table(self,name, id):
            self.cursor.execute(""" DELETE FROM"""+name+""" WHERE id_"""+name+"""="""+str(id))
            self.connexion.commit()

    def insertion_article(self, liste):
            self.cursor.execute("""INSERT INTO article(name,description,price) VALUES(?,?,?)""",liste)
            self.connexion.commit()

    def insertion_user(self,liste):
            texte=liste[0]
            #convertir image logo sous forme de fichier binaire
            #with open(texte,"rb") as myfile:
            #   blobfile=myfile.read()

            liste[0]="img"

            self.cursor.execute("""INSERT INTO user(logo,company_name,e_mail,address,phone,num_SIREN) VALUES(?,?,?,?,?,?)""",liste)
            self.connexion.commit()

    def insertion_client_or_company(self,liste,bool):
                """ envoi dun bouleen"""
                liste_c=liste[:6]
                self.cursor.execute("""INSERT INTO client(last_name,first_name,e_mail,address,phone,remark) VALUES(?,?,?,?,?,?)""",liste_c)
                self.connexion.commit()
                if bool==1:
                    self.cursor.execute("""SELECT max(id_client) FROM client""")
                    self.connexion.commit()
                    id_max=self.cursor.fetchall()

                    liste_e=[id_max[0][0]]+liste[6:]
                    """ recuperation de id """
                    self.cursor.execute("""INSERT INTO company(id_company,company_name,num_SIRET) VALUES(?,?,?)""",liste_e)
                    self.connexion.commit()

    def insertion_invoice_dev(self,liste):
            self.cursor.execute("""INSERT INTO invoice_devis(amount,date,description,note,remark,id_client,id_user) VALUES(?,?,?,?,?,?,?)""",liste)
            self.connexion.commit()

    def insertion_invoice(self,liste):
            self.cursor.execute("""SELECT max(id_invoice_devis) FROM invoice_devis""")
            self.connexion.commit()
            id_max=self.cursor.fetchall()
            self.cursor.execute("""INSERT INTO invoice(id_invoice,solde) VALUES(?,?)""",(id_max[0][0],liste[0]))
            self.connexion.commit()

    def insertion_deposit(self,liste):
            data=date.today()
            self.cursor.execute("""INSERT INTO deposit(date,amount,id_invoice) VALUES(?,?,?)""",(data,liste[0],liste[1]))
            self.connexion.commit()

    def insertion_art_dev(self,liste):
            """ liste de 2 indice
            le premier pour id de article
            le deuxieme pour id de fac_dev   """
            self.cursor.execute("""INSERT INTO art_dev(id_article,id_invoice_devis) VALUES(?,?)""",(liste))
            self.connexion.commit()

    def update_client(self,liste,bool):
        liste=liste[1:]+[liste[0]]

        if bool==0:
            self.cursor.execute("""UPDATE client SET
            last_name=?,first_name=?,e_mail=?,address=?,phone=?,remark=?
            WHERE id_client=?""",liste)
        else:
            self.cursor.execute("""UPDATE client SET
            last_name=?,first_name=?,e_mail=?,address=?,phone=?,remark=?
            WHERE id_client=?""",liste)
        self.connexion.commit()

    def update_user(self,liste):
        liste=liste[1:]+[liste[0]]

        self.cursor.execute("""UPDATE user SET logo=?,company_name=?,e_mail=?,
        address=?,phone=?,num_SIREN=? WHERE id_user=?""",liste)
        self.connexion.commit()

    def update_deposit(self,liste):
        liste=liste[1:]+[liste[0]]

        self.cursor.execute("""UPDATE deposit SET date=?,amount=?, id_invoice=? WHERE id_deposit=?""",liste)
        self.connexion.commit()

    def update_invoice_dev(self,liste):
        liste=liste[1:]+[liste[0]]
        self.cursor.execute("""UPDATE invoice_devis SET amount=?,date=?,description=?,note=?,remark=?,id_client=?,id_user=? WHERE id_invoice_devis=?""",liste)
        self.connexion.commit()

    def update_article(self,liste):
        liste=liste[1:]+[liste[0]]
        self.cursor.execute("""UPDATE article SET name=?,description=?,price=? WHERE id_article=?""",liste)
        self.connexion.commit()
