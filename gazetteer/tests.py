from gazetteer.app import db, config_app, login
from gazetteer.modeles.utilisateurs import User
from gazetteer.modeles.donnees import Place, Authorship, Biblio, Authorship
from unittest import TestCase
from coverage import coverage
cov = coverage(branch=True, omit=['flask/*', 'tests.py'])
cov.start()

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

class TestApi(Base):
    places = [
        Place(
            place_nom='Hippana',
            place_description='Ancient settlement in the western part of Sicily, probably founded in the seventh century B.C.',
            place_longitude=37.7018481,
            place_latitude=13.4357804,
            place_type='settlement'
        )
    ]

    def setUp(self):
        self.app = config_app("test")
        self.db = db
        self.client = self.app.test_client()
        self.db.create_all(app=self.app)

    def tearDown(self):
        self.db.drop_all(app=self.app)

    def insert_all(self, places=True):
        # On donne à notre DB le contexte d'exécution
        with self.app.app_context():
            if places:
                for fixture in self.places:
                    self.db.session.add(fixture)
            self.db.session.commit()

    def test_single_place(self):
        """ Vérifie qu'un lieu est bien traité """
        self.insert_all()
        response = self.client.get("/api/places/1")
        # Le corps de la réponse est dans .data
        # .data est en "bytes". Pour convertir des bytes en str, on fait .decode()
        content = response.data.decode()
        self.assertEqual(
            response.headers["Content-Type"], "application/json"
        )
        json_parse = loads(content)
        self.assertEqual(json_parse["type"], "place")
        self.assertEqual(
            json_parse["attributes"],
            {'name': 'Hippana', 'latitude': 13.4357804, 'longitude': 37.7018481, 'category': 'settlement',
             'description': 'Ancient settlement in the western part of Sicily, probably '
                            'founded in the seventh century B.C.'}
        )
        self.assertEqual(json_parse["links"]["self"], 'http://localhost/place/1')

        # On vérifie que le lien est correct
        seconde_requete = self.client.get(json_parse["links"]["self"])
        self.assertEqual(seconde_requete.status_code, 200)


if __name__ == '__main__':
    unittest.main(verbosity=2)

if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    print("\n\nCoverage Report:\n")
    cov.report()
    print("HTML version: " + os.path.join(basedir, "tmp/coverage/index.html"))
    cov.html_report(directory='tmp/coverage')
    cov.erase()
