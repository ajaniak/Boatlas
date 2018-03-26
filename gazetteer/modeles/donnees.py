from flask import url_for
import datetime
from .. app import db

class Authorship(db.Model):
    __tablename__ = "authorship"
    authorship_id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    authorship_place_id = db.Column(db.Integer, db.ForeignKey('place.place_id'))
    authorship_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    authorship_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user = db.relationship("User", back_populates="authorships")
    place = db.relationship("Place", back_populates="authorships")

    def author_to_json(self):
        return {
            "author": self.user.to_jsonapi_dict(),
            "on": self.authorship_date
        }
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('place.place_id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('place.place_id'))
)

#création d'une table d'association pour les connexions entre les lieux
link_lieu = db.Table('link_lieu',
    db.Column('link_id',db.Integer, autoincrement=True, primary_key=True),
    db.Column('link_parent', db.Integer, db.ForeignKey('place.place_id'),
    db.Column('link_child',db.Integer, db.ForeignKey('place.place_id'))

# On crée notre modèle
class Place(db.Model):
    place_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    place_nom = db.Column(db.Text)
    place_description = db.Column(db.Text)
    place_longitude = db.Column(db.Float)
    place_latitude = db.Column(db.Float)
    place_type = db.Column(db.String(45))
    authorships = db.relationship("Authorship", back_populates="place")
    relations = db.relationship("Relation", back_populates="place")
    liaisons = db.relationship(
        'Place', secondary=link_lieu,
        primaryjoin= id ==link_lieu.c.link_parent,
        secondaryjoin= id ==link_lieu.c.link_child,
        backref="liens")

    def to_jsonapi_dict(self):
        """ It ressembles a little JSON API format but it is not completely compatible

        :return:
        """
        return {
            "type": "place",
            "id": self.place_id,
            "attributes": {
                "name": self.place_nom,
                "description": self.place_description,
                "longitude": self.place_longitude,
                "latitude": self.place_latitude,
                "category": self.place_type
            },
            "links": {
                "self": url_for("lieu", place_id=self.place_id, _external=True),
                "json": url_for("api_places_single", place_id=self.place_id, _external=True)
            },
            "relationships": {
                 "editions": [
                     author.author_to_json()
                     for author in self.authorships
                 ]
            }
        }


    @staticmethod
    def creer_lieu(nom, latitude, longitude, description, typep):
        erreurs = []
        if not nom:
            erreurs.append("Le nom du lieu est obligatoire")
        if not latitude:
            erreurs.append("Il faut indiquer la latitude")
        if not longitude:
            erreurs.append("Il faut indiquer la longitude")

        # Si on a au moins une erreur
        if len(erreurs) > 0:
            print(erreurs, nom, latitude, description, longitude)
            return False, erreurs

        lieu = Place(
            place_nom=nom,
            place_latitude=latitude,
            place_longitude=longitude,
            place_description=description,
            place_type=typep,
            # changer le nom "type"
        )
        print(lieu)
        try:
            # On l'ajoute au transport vers la base de données
            db.session.add(lieu)
            # On envoie le paquet
            db.session.commit()

            # On renvoie l'utilisateur
            return True, lieu

        except Exception as erreur:
            return False, [str(erreur)]


    @staticmethod
    def modif_lieu(id, nom, latitude, longitude, description, typep):
        erreurs = []
        if not nom:
            erreurs.append("Le nom du lieu est obligatoire")
        if not latitude:
            erreurs.append("Il faut indiquer la latitude")
        if not longitude:
            erreurs.append("Il faut indiquer la longitude")

        # Si on a au moins une erreur
        if len(erreurs) > 0:
            print(erreurs, nom, latitude, description, longitude)
            return False, erreurs

        lieu = Place.query.get(id)

        lieu.place_nom=nom
        lieu.place_latitude=latitude
        lieu.place_description=description
        lieu.place_longitude=longitude
        lieu.place_type=typep

        try:

            # On l'ajoute au transport vers la base de données
            db.session.add(lieu)
            # On envoie le paquet
            db.session.commit()

            # On renvoie l'utilisateur
            return True, lieu

        except Exception as erreur:
            return False, [str(erreur)]


            #on crée notre classe de références bibliographiques
class Biblio(db.Model):
    biblio_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    biblio_titre = db.Column(db.Text, nullable=False)
    biblio_auteur = db.Column(db.Text, nullable=False)
    biblio_date = db.Column(db.Text)
    biblio_lieu = db.Column(db.Text)
    biblio_type = db.Column(db.Text, nullable=False)
    relations = db.relationship("Relation", back_populates="biblio")

    def to_jsonapi_dict(self):
        """ It ressembles a little JSON API format but it is not completely compatible

        :return:
        """
        return {
            "type": "biblio",
            "id": self.biblio_id,
            "attributes": {
                "titre": self.biblio_titre,
                "auteur": self.biblio_auteur,
                "date": self.biblio_date,
                "lieu": self.biblio_lieu,
                "category": self.place_type
            },
            "links": {
                "self": url_for("biblio", biblio_id=self.biblio_id, _external=True),
                "json": url_for("api_biblios_single", biblio_id=self.biblio_id, _external=True)
            },

        }

    @staticmethod
    def creer_biblio(titre, auteur, date, lieu, typep):
        """ Crée une nouvelle référence bibliographique et renvoie les informations entrées par l'utilisateur
        :param titre: Titre de la référence
        :param auteur: Auteur de la référence
        :param date: Date de publication de la référence
        :param lieu: Lieu de publication de la référence
        :param type: Type de publication
        """
        erreurs = []
        if not titre:
            erreurs.append("Le titre de l'oeuvre est obligatoire")
        if not auteur:
            erreurs.append("Il faut indiquer l'auteur")
        if not typep:
            erreurs.append("Il faut indiquer le type d'oeuvre : article ou livre")

        # Si on a au moins une erreur
        if len(erreurs) > 0:
            print(erreurs, titre, auteur, typep)
            return False, erreurs

        biblio = Biblio(
            biblio_titre=titre,
            biblio_auteur=auteur,
            biblio_date=date,
            biblio_lieu=lieu,
            biblio_type=typep,
            # changer le nom "type"
        )
        print (biblio)

        try:
            # On l'ajoute au transport vers la base de données
            db.session.add(biblio)
            # On envoie la référence
            db.session.commit()

            return True, biblio

        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def modif_biblio(id, titre, auteur, date, lieu, typep):
        erreurs = []
        if not titre:
            erreurs.append("Le titre est obligatoire")
        if not auteur:
            erreurs.append("L'auteur est obligatoire")
        if not typep:
            erreurs.append("Il faut indiquer le type d'ouvrage")

        # Si on a au moins une erreur
        if len(erreurs) > 0:
            print(erreurs, titre, auteur, date, lieu, typep)
            return False, erreurs

        biblio = Biblio.query.get(id)

        biblio.biblio_titre=titre
        biblio.biblio_auteur=auteur
        biblio.biblio_date=date
        biblio.biblio_lieu=lieu
        biblio.biblio_type=typep

        try:

            # On l'ajoute au transport vers la base de données
            db.session.add(biblio)
            # On envoie le paquet
            db.session.commit()

            # On renvoie l'utilisateur
            return True, biblio

        except Exception as erreur:
            return False, [str(erreur)]

class Relation(db.Model):
    __tablename__ = "relation"
    relation_id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    relation_place_id = db.Column(db.Integer, db.ForeignKey('place.place_id'))
    relation_biblio_id = db.Column(db.Integer, db.ForeignKey('biblio.biblio_id'))
    biblio = db.relationship("Biblio", back_populates="relations")
    place = db.relationship("Place", back_populates="relations")

    # création de la gestions des liens entre les lieux.
    @staticmethod
    def creer_liaison(nom_lieu_1, nom_lieu_2):
        erreurs = []
        if not nom_lieu_1:
            erreurs.append("Le nom du lieu parent est obligatoire")
        if not nom_lieu_2:
            erreurs.append("Il faut indiquer le nom du lieu enfant")

        # Si on a au moins une erreur
        if len(erreurs) > 0:
            print(erreurs, nom_lieu_1, nom_lieu_2)
            return False, erreurs

        lieu_liaison = Place(
            link_parent=nom_lieu_1,
            link_child=nom_lieu_2,
        )
        print(lieu_liaison)
        try:
            # On l'ajoute au transport vers la base de données
            db.session.add(lieu_liaison)
            # On envoie le paquet
            db.session.commit()

            # On renvoie l'utilisateur
            return True, lieu_liaison

        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def modif_liaison(id, nom_lieu_1, nom_lieu_2):
        erreurs = []
        if not nom_lieu_1:
            erreurs.append("Le nom du lieu est obligatoire")
        if not nom_lieu_2:
            erreurs.append("Il faut indiquer la latitude")

        # Si on a au moins une erreur
        if len(erreurs) > 0:
            print(erreurs, nom_lieu_1, nom_lieu_2)
            return False, erreurs

        lieu_liaison = link_lieu.query.get(id)

        lieu_liaison.link_parent=nom_lieu_1
        lieu_liaison.link_child=nom_lieu_2

        try:

            # On l'ajoute au transport vers la base de données
            db.session.add(lieu_liaison)
            # On envoie le paquet
            db.session.commit()

            # On renvoie l'utilisateur
            return True, lieu_liaison

        except Exception as erreur:
            return False, [str(erreur)]
