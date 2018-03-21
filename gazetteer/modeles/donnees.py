from flask import url_for
import datetime

from .. app import db

class Authorship(db.Model):
    __tablename__ = "authorship"
    authorship_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
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

#création d'une table d'association
class Followers(db.Model):
    __tablename__="following"
    f_connection_id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    f_place_from = db.Column(db.Integer, db.ForeignKey('place.place_id'))
    f_place_to = db.Column(db.Integer, db.ForeignKey('place.place_id'))
    pfrom = db.relationship("Place", back_populates="place_from")


#Il faut définir la relation mais à quel endroit??
#following = Followers(extra_field=0 , to=self , from=link_place)

# On crée notre modèle
class Place(db.Model):
    place_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    place_nom = db.Column(db.Text)
    place_description = db.Column(db.Text)
    place_longitude = db.Column(db.Float)
    place_latitude = db.Column(db.Float)
    place_type = db.Column(db.String(45))
    place_connection = db.Colum(db.Integer, ForeignKey('Followers.f_place_to'))
    authorships = db.relationship("Authorship", back_populates="place")
    place_from = db.relationship ("Followers", back_populates="pfrom")


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
    def creer_lieu(nom, latitude, longitude, description, type):
        erreurs = []
        if not nom:
            erreurs.append("Le nom du lieu est obligatoire")
        if not latitude:
            erreurs.append("Il faut indiquer la latitude")
        if not longitude:
            erreurs.append("Il faut indiquer la longitude")

        # On vérifie que personne n'a utilisé cet email ou ce login


        # Si on a au moins une erreur
        if len(erreurs) > 0:
            print(erreurs, nom, latitude, description, longitude)
            return False, erreurs

        lieu = Place(
            place_nom=nom,
            place_latitude=latitude,
            place_longitude=longitude,
            place_description=description,
            place_type=type,
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


    def follow(self, place):
        if not self.is_following(place):
            self.followed.append(place)

    def unfollow(self, place):
        if self.is_following(place):
            self.followed.remove(place)

    def is_following(self, place):
        return self.followed.filter(followers.c.f_place_to == place_id).count() > 0

    def followed_connection(self):
        followed = connection.query.join(followers, (followers.c.f_place_to == connection.place_id)).filter(followers.c.f_place_from == self.id)
        own = connection.query.filter_by(place_id=self.id)
        return followed.union(own)

    @staticmethod
    def modif_lieu(id, nom, latitude, longitude, description, type):
        erreurs = []
        if not nom:
            erreurs.append("Le nom du lieu est obligatoire")
        if not latitude:
            erreurs.append("Il faut indiquer la latitude")
        if not longitude:
            erreurs.append("Il faut indiquer la longitude")

        # On vérifie que personne n'a utilisé cet email ou ce login


        # Si on a au moins une erreur
        if len(erreurs) > 0:
            print(erreurs, nom, latitude, description, longitude)
            return False, erreurs

        lieu = Place.query.get(id)

        lieu.place_nom = nom
        lieu.place_latitude = latitude
        lieu.place_description = description
        lieu.place_longitude = longitude
        lieu.place_type = type

        try:

            # On l'ajoute au transport vers la base de données
            db.session.add(lieu)
            # On envoie le paquet
            db.session.commit()

            # On renvoie l'utilisateur
            return True, lieu

        except Exception as erreur:
            return False, [str(erreur)]
