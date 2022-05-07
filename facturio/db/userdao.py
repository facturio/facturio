#!/usr/bin/env python3
from facturio.classes.user import User
from dbmanager import DBManager


class UserDAO:
    """User controleur pour la DB."""

    __instance = None

    def __init__(self):
        """Recupere le manager."""
        self.bdd = DBManager.get_instance()

    def get_instance():
        """Recupere l'instance."""
        if UserDAO.__instance is None:
            UserDAO.__instance = UserDAO()
        return UserDAO.__instance

    def insert(self, user: User):
        """Insertion de l'utilisateur."""
        # Tester que sur la table il n'aie pas deja un user
        request = """select * from user """
        self.bdd.cursor.execute(request)
        self.bdd.connexion.commit()
        ligne = self.bdd.cursor.fetchone()
        if len(ligne) >= 2:
            return
        #  Modifier l'ordre des attributs pour respecter la table
        request = """INSERT INTO user(company_name, first_name, last_name
        , e_mail, address, phone, business_num,logo)
                     VALUES(?, ?, ?, ?, ?, ?, ?, ?)"""
        # convertir image logo sous forme de fichier binaire
        logo = None
        if user.logo is not None:
            with open(texte, "rb") as user.logo:
                logo = myfile.read()
        values = [user.company_name, user.first_name,
                  user.last_name, user.email, user.address, user.phone_number,
                  user.business_number, logo]
        self.bdd.cursor.execute(request, values)
        self.bdd.connexion.commit()

        # On recupere l'id qui vient d'etre insere' 1 parce que
        # il y une seule instance
        user.id_ = 1

    def update_user(self, user: User):
        """Maj de l'utilisateur."""
        request = """UPDATE user SET logo=?,company_name=?,e_mail=?,
                     address=?,phone=?,business_num=? WHERE id_user=1"""
        # convertir image logo sous forme de fichier binaire
        logo = None
        if user.logo is not None:
            with open(texte, "rb") as user.logo:
                logo = myfile.read()
        values = [logo, user.company_name, user.email, user.address,
                  user.phone_number, user.business_number]

        self.bdd.cursor.execute(request, values)

        self.bdd.connexion.commit()

    def get(self):
        """Renvoie une liste tous les instances des client sur la BD."""
        data = self.bdd.cursor.execute("select * from user").fetchone()
        # VERIFIER QUE IL Y A UNE LIGNE SINON ERROR
        if len(data) >= 2:
            return
        if not User.exits():
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


if __name__ == "__main__":

    dao = UserDAO.get_instance()
    user = User("Facturio INC", "Yousggsef", "BENJEggLLOUN", "yb@gmail.com",
                "427 Boulevard des armaris 8dsfdsfdsq3100 Toulon", "07 67 31 58 20",
                "12348921 2341")
    # dao.insert(user)
    dao.update_user(user)
