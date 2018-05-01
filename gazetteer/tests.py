from gazetteer.app import db, config_app, login
from gazetteer.modeles.utilisateurs import User
from gazetteer.modeles.donnees import Place, Authorship, Biblio, Authorship
from unittest import TestCase

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

class PlaceModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def creation(self):
        l = Place(place_nom='Marseille', place_latitude='43.300000', place_longitude='5.400000')
        self.assertEqual(l=l)


class BiblioModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def creation(self):
        l = Place(biblio_titre='Versailles, un palais pour la sculpture', biblio_auteur='Alexandre Maral', biblio_date='2013')
        self.assertEqual(l=l)

    def test_association_ref(self, biblio_id):
        lieu1 = Place(place_nom='Athènes', place_latitude='37.983810', place_longitude='23.727539', place_type='capitale')
        livre1 = Biblio(biblio_titre='Les Perses', biblio_auteur='Eschyle', biblio_type='tragédie grecque')
        db.session.add(lieu1)
        db.session.add(livre1)
        db.session.commit()
        self.assertEqual(lieu1.relations.all(), [])
        self.assertEqual(livre1.relations.all(), [])

        lieu1.associer_reference(livre1)
        db.session.commit()
        self.assertTrue(lieu1.associer_reference(u2))

        lieu1.supprimer_association(livre1)
        db.session.commit()
        self.assertFalse(lieu1.associer_reference(u2))

class RelationModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    """def creation(self):
        #demander à Ella quelles données ont été liées entre elles pour l'écriture du test!
        l = Place(relation_id=, relation_place_id=, relation_biblio_id=)
        self.assertEqual(l=l)"""




if __name__ == '__main__':
    unittest.main(verbosity=2)"""
