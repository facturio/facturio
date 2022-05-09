import unittest
import sqlite3
from facturio.db.articledao import ArticleDAO
from facturio.classes.article import Article


class TestArticleDAO(unittest.TestCase):
    """Teste la classe UserDAO"""

    def test_insert(self):

        dao = ArticleDAO.get_instance()
        article = Article()
        dao.insert(article)
        id = article.id_
        articleliste = article.dump_to_list()
        articlegetid = dao.get_with_id(id).dump_to_list()
        self.assertEqual(articlegetid, articleliste)

    def test_update(self):
        dao = articleDAO.get_instance()
        article = dao.get_all()
        article[0].first_name = "clement"
        article[0].last_name = "bazan"
        id = article[0].id_
        dao.update(article[0])

        articleliste = article[0].dump_to_list()
        articlegetid = dao.get_with_id(id).dump_to_list()
        self.assertEqual(articlegetid, articleliste)
        dao.delete(id)


if __name__ == '__main__':
    unittest.main()
