from datetime import date
from facturio.classes.invoice_misc import Article
from dbmanager import DBManager

class ArticleDAO:
    #TODO tester
    __instance=None

    def __init__(self):
        """Recupere le manager."""
        self.bdd = DBManager.get_instance()

    def get_instance():
         """Verifie l'unicite de l'instance"""
         if ArticleDAO.__instance is None:
             ArticleDAO.__instance=ArticleDAO()
         return ArticleDAO.__instance

    def insert(self, article: Article):
         """
         Prend une isntance de la classe article
         et l'ajoute a la bd
         """
         request="""INSERT INTO article(id_article,name,description,price,quantity)
                            VALUES(?,?,?,?,?)"""
         if(article.id_!=None):
             raise ValueError
         max_req = "SELECT max(id_article) FROM article"
         article.id_ = self.bdd.cursor.execute(max_req).fetchone()[0]
         if article.id_==None:
             article.id_=0
         article.id_+=1
         values= ( article.id_, article.title, article.description,
                  article.price, article.quantity)
         print(values)
         self.bdd.cursor.execute(request, values)
         self.bdd.connexion.commit()

    def update(self, article: Article):
         """
         Prend une instance de la classe Article et update
         la bd avec cette objet
         """
         if(article.id_==None):
             raise ValueError
         values= [article.title, article.description,
                  article.price, article.quantity, article.id_]
         request=""" UPDATE Article SET name=?, description=?,
                     price=?, quantity=?  WHERE id_article=?"""
         self.bdd.cursor.execute(request, values)
         self.bdd.connexion.commit()

    @staticmethod
    def _gen_article(tup):
        """
        prend un tuple(title,description,price,quantity,id)
        et renvoie une instance de la classe article
        """
        article = Article(title=tup[1],
                          description=tup[2],
                          price=tup[3],
                          quantity=tup[4],
                          id_=tup[0],
                          )
        return article


    def get_all(self):
        tuples=self.bdd.cursor.execute("""select * from article""")
        res=[]
        for tup in tuples:
           res.append(self._gen_article(tup))
        return res

if __name__ == "__main__":
    #######
    test=ArticleDAO()
    voiture=Article("Porsh",100000,1,"voiture rapide")
    a=test.get_all()[0]
    a.description=""
    test.update(a)
    test.insert(voiture)
