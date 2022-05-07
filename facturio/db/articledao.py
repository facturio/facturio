from datetime import date
from facturio.classes.invoice_misc import Article
from dbmanager import DBManager


class ArticleDAO:

    __instance = None

    def __init__(self):
        """Recupere le manager."""
        self.bdd = DBManager.get_instance()

    def get_instance():
        """Verifie l'unicite de l'instance."""
        if ArticleDAO.__instance is None:
            ArticleDAO.__instance = ArticleDAO()
        return ArticleDAO.__instance

    def insert(self, article: Article):
        """Insertion de la classe article."""
        if article.id_ is not None:
            raise ValueError
        if article.id_receipt is None:
            raise ValueError
        max_req = "SELECT max(id_article) FROM article"
        article.id_ = self.bdd.cursor.execute(max_req).fetchone()[0]
        if article.id_ is None:
            article.id_ = 0
        article.id_ += 1
        values = (article.id_, article.title, article.description,
                  article.price, article.quantity, article.id_receipt)
        request = """INSERT INTO article(id_article, name, description, price,
                     quantity, id_receipt) VALUES(?,?,?,?,?,?)"""
        print(values)
        self.bdd.cursor.execute(request, values)
        self.bdd.connexion.commit()

    def update(self, article: Article):
        """
        Prend une instance de la classe Article et update
        la bd avec cette objet
        """
        if(article.id_ == None):
            raise ValueError
        values = [article.title, article.description,
                  article.price, article.quantity, article.id_]
        request = """UPDATE Article SET name=?, description=?,
                    price=?, quantity=?  WHERE id_article=?"""
        self.bdd.cursor.execute(request, values)
        self.bdd.connexion.commit()

    @staticmethod
    def _gen_article(tup):
        """
        prend un tuple(title,description,price,quantity,id)
        et renvoie une instance de la classe article
        """
        print(tup)
        article = Article(title=tup[1],
                          description=tup[2],
                          price=tup[3],
                          quantity=tup[4],
                          id_=tup[0],
                          id_receipt=tup[5])
        return article

    def get_all(self):
        tuples = self.bdd.cursor.execute("""select * from article""")
        res = []
        for tup in tuples:
            res.append(self._gen_article(tup))
        return res

    def get_all_with_id_receipt(self, id_rcp):
        request = f"SELECT * FROM article WHERE id_receipt={id_rcp}"
        articles_tup = self.bdd.cursor.execute(request).fetchall()
        res = []
        for tup in articles_tup:
            res.append(self._gen_article(tup))
        return res


if __name__ == "__main__":
    #######
    test = ArticleDAO()
    voiture = Article("Porsh", 100000, 1, "voiture rapide")
    # a=test.get_all()[0]
    # a.description=""
    # test.update(a)
    # test.insert(voiture)
