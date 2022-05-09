#!/usr/bin/env python3
from facturio.classes.user import User
from facturio.db.dbmanager import DBManager


class UserDAO:
    """User controleur pour la DB."""

    __instance = None

    def __init__(self):
        """Recupere le manager."""
        self.bdd = DBManager.get_instance()

    def get_instance():
        """Recupere l'instance."""
        if UserDAO.__instance  is None:
            UserDAO.__instance = UserDAO()
        return UserDAO.__instance

    def insert(self, user: User):
        """Insertion de l'utilisateur."""
        # TODO: Tester que sur la table il n'aie pas deja un user
        # TODO: Modifier l'ordre des attributs pour respecter la table
        request = """INSERT INTO user(logo, company_name, e_mail, address,
                     phone, business_num, first_name, last_name)
                     VALUES(?, ?, ?, ?, ?, ?, ?, ?)"""
        # convertir image logo sous forme de fichier binaire
        logo = None
        print(user.logo)
        if user.logo is not None and user.logo != "Aucun":
            with open(user.logo, "rb") as user.logo:
                logo = myfile.read()
        values = [logo, user.company_name, user.email, user.address,
                  user.phone_number, user.business_number, user.first_name,
                  user.last_name]
        self.bdd.cursor.execute(request, values)
        self.bdd.connexion.commit()

        # On recupere l'id qui vient d'etre insere' 1 parce que
        # il y une seule instance
        user.id_ = 1

    def update_user(self, user: User):
        """Maj de l'utilisateur."""
        request = """UPDATE user SET logo=?,company_name=?,e_mail=?,
                     address=?,phone=?,business_num=? WHERE id_user=1"""
        #convertir image logo sous forme de fichier binaire
        logo = None
        if user.logo is not None and user.logo != "Aucun":
            with open(texte,"rb") as user.logo:
                logo = myfile.read()
        values = [logo, user.company_name, user.email, user.address,
                  user.phone_number, user.business_number]

        self.bdd.cursor.execute(request, values)

        self.bdd.connexion.commit()

    def get(self):
        """Renvoie une liste tous les instances des client sur la BD."""
        data = self.bdd.cursor.execute("select * from user").fetchone()
        # TODO: VERIFIER QUE IL Y A UNE LIGNE SINON ERROR
        print(User.exists())
        print(data)
        if not User.exists():
            return self._gen_user(data)
        else:
            return User.get_instance()

    @staticmethod
    def _gen_user(tup):
        user = User(company_name=tup[1],
                    first_name=tup[2],
                    last_name=tup[3],
                    email=tup[4],
                    address=tup[5],
                    phone_number=tup[6],
                    business_number=tup[7],
                    logo=tup[8],
                    id_=tup[0])
        return user



    # def selection_table(self,nom):
    #     bdd = DBManager.get_instance()
    #     bdd.cursor.execute("""select * from """+nom)
    #     return bdd.cursor.fetchall()

if __name__ == "__main__":
    #TODO: Tester tous les fonctions
    dao = UserDAO.get_instance()
    user = User("Facturio INC", "Youssef", "BENJELLOUN", "yb@gmail.com",
                "427 Boulevard des armaris 83100 Toulon", "07 67 31 58 20",
                "12348921 2341")
    dao.insert(user)
