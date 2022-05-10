import sqlite3
from datetime import date
from xdg import BaseDirectory

class DBmanager:
    __instance=None
    def get_instance():
        if DBmanager.__instance==None:
            DBmanager.__instance=DBmanager()
        return DBmanager.__instance

    def __init__(self):
        #nom de la table
        self.name="facturio"
        #fonction pour creation ou/et connexion
        # a la data_base
        self.connexion=sqlite3.connect(BaseDirectory.save_data_path('facturio') + '/' + self.name + '.db')

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
    def close(self):
        self.connexion.close()
class ClientDAO:
    __instance=None
    def get_instance():
        if clientDAO.__instance==None:
            clientDAO.__instance=ClientDAO()
        return clientDAO.__instance
    def insertion_client_or_company(self,liste,bool):
        bdd=DBmanager.get_instance()
        """ envoi dun bouleen"""
        liste_c=liste[:6]
        bdd.cursor.execute("""INSERT INTO client(last_name,first_name,e_mail,address,phone,remark) VALUES(?,?,?,?,?,?)""",liste_c)
        bdd.connexion.commit()
        if bool==1:
            bdd.cursor.execute("""SELECT max(id_client) FROM client""")
            bdd.connexion.commit()
            id_max=bdd.cursor.fetchall()
            liste_e=[id_max[0][0]]+liste[6:]
            """ recuperation de id """
            bdd.cursor.execute("""INSERT INTO company(id_company,company_name,num_SIRET) VALUES(?,?,?)""",liste_e)
            bdd.connexion.commit()
    def update_client(self,liste,bool):
        bdd=DBmanager.get_instance()
        liste=liste[1:]+[liste[0]]
        if bool==0:
            bdd.cursor.execute("""UPDATE client SET
            last_name=?,first_name=?,e_mail=?,address=?,phone=?,remark=?
            WHERE id_client=?""",liste)
        else:
            bdd.cursor.execute("""UPDATE client SET
            last_name=?,first_name=?,e_mail=?,address=?,phone=?,remark=?
            WHERE id_client=?""",liste)
        bdd.connexion.commit()
    def delete_table(self,name, id):
            bdd.cursor.execute(""" DELETE FROM"""+name+""" WHERE id_"""+name+"""="""+str(id))
            bdd.connexion.commit()
    def selection_table(self,nom):
            bdd.cursor.execute("""select * from  client""")
            return bdd.cursor.fetchall()

class UserDAO:
    __instance=None
    def get_instance():
        if userDAO.__instance==None:
            userDAO.__instance=userDAO()
        return userDAO.__instance
    def insertion_user(self,liste):
        bdd=DBmanager.get_instance()
        texte=liste[0]
        #convertir image logo sous forme de fichier binaire
        with open(texte,"rb") as myfile:
            blobfile=myfile.read()

        liste[0]=blobfile

        bdd.cursor.execute("""INSERT INTO user(logo,company_name,e_mail,address,phone,num_SIREN) VALUES(?,?,?,?,?,?)""",liste)
        bdd.connexion.commit()
    def update_user(self,liste):
        bdd=DBmanager.get_instance()
        liste=liste[1:]+[liste[0]]
        bdd.cursor.execute("""UPDATE user SET logo=?,company_name=?,e_mail=?,
        address=?,phone=?,num_SIREN=? WHERE id_user=?""",liste)
        bdd.connexion.commit()
    def delete_table(self,name, id):
        bdd=DBmanager.get_instance()
        bdd.cursor.execute(""" DELETE FROM"""+name+""" WHERE id_"""+name+"""="""+str(id))
        bdd.connexion.commit()
    def selection_table(self,nom):
        bdd=DBmanager.get_instance()
        bdd.cursor.execute("""select * from """+nom)
        return bdd.cursor.fetchall()

class DepositDAO():
    __instance=None
    def get_instance():
        if DepositDAO.__instance==None:
            DepositDAO.__instance=DepositDAOs()
        return DepositDAO.__instance
    def insertion_deposit(self,liste):
        bdd=DBmanager.get_instance()
        data=date.today()
        bdd.cursor.execute("""INSERT INTO deposit(date,amount,id_invoice) VALUES(?,?,?)""",(data,liste[0],liste[1]))
        bdd.connexion.commit()
    def update_deposit(self,liste):
        bdd=DBmanager.get_instance()
        liste=liste[1:]+[liste[0]]
        bdd.cursor.execute("""UPDATE deposit SET date=?,amount=?, id_invoice=? WHERE id_deposit=?""",liste)
        bdd.connexion.commit()
    def delete_table(self,name, id):
        bdd=DBmanager.get_instance()
        bdd.cursor.execute(""" DELETE FROM"""+name+""" WHERE id_"""+name+"""="""+str(id))
        bdd.connexion.commit()
    def selection_table(self,nom):
        bdd=DBmanager.get_instance()
        bdd.cursor.execute("""select * from """+nom)
        return bdd.cursor.fetchall()

class InvoiceDAO:
    __instance=None
    def get_instance():
        if InvoiceDAO.__instance==None:
            InvoiceDAO.__instance=InvoiceDAO()
        return InvoiceDAO.__instance
    def insertion_invoice(self,liste):
        bdd=DBmanager.get_instance()
        bdd.cursor.execute("""SELECT max(id_invoice_devis) FROM invoice_devis""")
        bdd.connexion.commit()
        id_max=bdd.cursor.fetchall()
        bdd.cursor.execute("""INSERT INTO invoice(id_invoice,solde) VALUES(?,?)""",(id_max[0][0],liste[0]))
        bdd.connexion.commit()
    def selection_table(self,nom):
        bdd=DBmanager.get_instance()
        bdd.cursor.execute("""select * from """+nom)
        return bdd.cursor.fetchall()

class ArticleDAO:
    __instance=None

    def get_instance():
        if ArticleDAO.__instance==None:
            ArticleDAO.__instance=ArticleDAO()

        return ArticleDAO.__instance
    def insertion_article(self, liste):
        bdd=DBmanager.get_instance()
        bdd.cursor.execute("""INSERT INTO article(name,description,price) VALUES(?,?,?)""",liste)
        bdd.connexion.commit()
    def update_article(self,liste):
        bdd=DBmanager.get_instance()
        liste=liste[1:]+[liste[0]]
        bdd.cursor.execute("""UPDATE article SET name=?,description=?,price=? WHERE id_article=?""",liste)
        bdd.connexion.commit()
    def selection_table(self):
        bdd=DBmanager.get_instance()
        bdd.cursor.execute("""select * from article""")
        return bdd.cursor.fetchall()

class Invoice_devDAO:
    __instance=None
    def get_instance():
        if Invoice_devDAO.__instance==None:
            Invoice_devDAO.__instance=Invoice_devDAO()
        return Invoice_devDAO.__instance
    def insertion_invoice_dev(self,liste):
        bdd=DBmanager.get_instance()
        bdd.cursor.execute("""INSERT INTO invoice_devis(amount,date,description,note,remark,id_client,id_user) VALUES(?,?,?,?,?,?,?)""",liste)
        bdd.connexion.commit()
    def update_invoice_dev(self,liste):
        bdd=DBmanager.get_instance()
        liste=liste[1:]+[liste[0]]
        bdd.cursor.execute("""UPDATE invoice_devis SET amount=?,date=?,description=?,note=?,remark=?,id_client=?,id_user=? WHERE id_invoice_devis=?""",liste)
        bdd.connexion.commit()
    def selection_table(self,nom):
        bdd=DBmanager.get_instance()
        bdd.cursor.execute("""select * from """+nom)
        return bdd.cursor.fetchall()

class Art_devDAO:
    __instance=None
    def get_instance():
        if art_dev.__instance==None:
            art_dev.__instance=DBmanager()
        return art_dev.__instance
    def insertion_art_dev(self,liste):
        bdd=DBmanager.get_instance()
        """ liste de 2 indice
        le premier pour id de article
        le deuxieme pour id de fac_dev   """
        bdd.cursor.execute("""INSERT INTO art_dev(id_article,id_invoice_devis) VALUES(?,?)""",(liste))
        bdd.connexion.commit()
    def update_invoice_dev(self,liste):
        bdd=DBmanager.get_instance()
        liste=liste[1:]+[liste[0]]
        bdd.cursor.execute("""UPDATE invoice_devis SET amount=?,date=?,description=?,note=?,remark=?,id_client=?,id_user=? WHERE id_invoice_devis=?""",liste)
        bdd.connexion.commit()
    def selection_table(self,nom):
        bdd=DBmanager.get_instance()
        bdd.cursor.execute("""select * from """+nom)
        return bdd.cursor.fetchall()
