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

# On crée notre modèle de lieux
class Place(db.Model):
    #__tablename__ = "left"
    place_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    place_nom = db.Column(db.Text)
    place_description = db.Column(db.Text)
    place_longitude = db.Column(db.Float)
    place_latitude = db.Column(db.Float)
    place_type = db.Column(db.String(45))
#Jointure
    authorships = db.relationship("Authorship", back_populates="place")
    #biblios = db.relationship("Biblio", primaryjoin="Place.place_id==Relation.relation_biblio_id")
    relations = db.relationship("Relation", back_populates="place")

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
    #__tablename__ = "right"
    biblio_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    biblio_titre = db.Column(db.Text, nullable=False)
    biblio_auteur = db.Column(db.Text, nullable=False)
    biblio_date = db.Column(db.Text)
    biblio_lieu = db.Column(db.Text)
    biblio_type = db.Column(db.Text, nullable=False)
#Jointure
    #relation_place_id = db.relationship("Place", primaryjoin="Biblio.biblio_id==Relation.relation_place_id")
    #places = db.Column(db.Integer, db.ForeignKey('relation.relation_id'), nullable=False)
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
#Jointure
    #biblio = db.relationship("Biblio", foreign_keys=[relation_biblio_id])
    biblio = db.relationship("Biblio", back_populates="relations")
    #place = db.relationship("Place", foreign_keys=[relation_place_id])
    place = db.relationship("Place", back_populates="relations")

    @staticmethod
    def liees(biblio_id, place_id):
        reference = biblio_id
        endroit = place_id
        reference = reference.relations
        endroit = endroit.relations
        for element in endroit:
            endroit_relation = element.relations.relation_id
        for element in reference:
            reference_relation = element.relations.relation_id
        if reference_relation == endroit_relation:
            return True, reference_relation, endroit_relation

#Attention ce code est un test
    @staticmethod
    def liaison(biblio_id, place_id):
        reference_1 = Biblio.query.get(biblio_id)
        endroit_1 = Place.query.get(place_id)
        reference = reference_1.relations
        endroit = endroit_1.relations
        for element in endroit:
            endroit_relation = element.relations.relation_id
            print(endroit_relation)
            #Un ou deux = ?
            if endroit_relation == element.relations.relation_id.count() == 0:
                endroit.append(biblio.reference_1)
            # if element.relations.relation_id == None
        for element in reference:
            reference_relation = element.relations.relation_id
            if reference_relation == element.relations.relation_id.count() == 0:
                reference.append(place.endroit_1)

            return True, endroit_relation, reference_relation

    @staticmethod
    def creer_liaison(biblio_id, place_id):
        """ Crée une nouvelle référence bibliographique et renvoie les informations entrées par l'utilisateur
        :param titre: Titre de la référence
        :param auteur: Auteur de la référence
        :param date: Date de publication de la référence
        :param lieu: Lieu de publication de la référence
        :param type: Type de publication
        """
        erreurs = []
        if not biblio_id:
            erreurs.append("Le biblio_id est obligatoire")
        if not place_id:
            erreurs.append("Il faut indiquer le place_id")


        # Si on a au moins une erreur
        if len(erreurs) > 0:
            print(erreurs, biblio_id, place_id)
            return False, erreurs

        liaison = Relation(
            relation_biblio_id=biblio_id,
            relation_place_id=place_id,

            # changer le nom "type"
        )
        print (liaison)

        try:
            # On l'ajoute au transport vers la base de données
            db.session.add(liaison)
            # On envoie la référence
            db.session.commit()

            return True, liaison

        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def creer_liaison_correcte(place_id, biblio_id):
        """ Crée une nouvelle relation entre un lieu et une ou plusieurs références bibliographiques
         et renvoie les informations entrées par l'utilisateur
        :param titre: Titre de la référence
        :param place_id: ID du lieu
        """
        #erreurs = []
        #if not biblio_titre:
        #    erreurs.append("Le biblio_id est obligatoire")

        #commentaire: Si on a au moins une erreur
        #if len(erreurs) > 0:
        #    print(erreurs, place_id, biblio_titre)
        #    return False, erreurs

        titres = Biblio.query.get(biblio_titre).all()
        liaison_propre = Relation(
            #relation_biblio_id=biblio_id,
            relation_place_id=place_id,
            relation_biblio_id=biblio_id,

            # changer le nom "type"
        )
        print (liaison_propre)

        try:
            # On l'ajoute au transport vers la base de données
            db.session.add(liaison_propre)
            # On envoie la référence
            db.session.commit()

            return True, liaison_propre

        except Exception as erreur:
            return False, [str(erreur)]

    #@staticmethod
    #def creer_lien(place_id):
        """ Crée une nouvelle référence bibliographique et renvoie les informations entrées par l'utilisateur
        :param titre: Titre de la référence
        :param auteur: Auteur de la référence
        :param date: Date de publication de la référence
        :param lieu: Lieu de publication de la référence
        :param type: Type de publication
        """
        #erreurs = []
        #if not biblio_titre:
        #    erreurs.append("Le titre de la référence est obligatoire")
        #if not place_nom:
        #    erreurs.append("Il faut indiquer le nom du lieu que vous voulez relier")


        # Si on a au moins une erreur
        #if len(erreurs) > 0:
        #    print(erreurs, biblio_titre, place_nom)
        #    return False, erreurs

        #for biblio_titre:
        #    bibliographie = Biblio.query.filter(biblio_titre == Biblio.biblio_titre.like("%{}%".format(biblio_titre))

        #biblio_id = Relation.biblio.biblio_titre query.get(relation_biblio_id).filter(biblio_titre==relation_biblio_id.biblio_titre)
        #place_id=Relation.query.get(relation_place_id).filter(place_nom==relation_place_id.place_nom)

        #liaison = Relation(
        #    relation_biblio_id=biblio_id,
        #    relation_place_id=place_id,

            # changer le nom "type"
        #)
        #print (liaison)

        #try:
            # On l'ajoute au transport vers la base de données
        #    db.session.add(liaison)
            # On envoie la référence
        #    db.session.commit()

        #    return True, liaison

        #except Exception as erreur:
        #    return False, [str(erreur)]


            #if not (element.relations.relation_id == reference.relations.relation_id)
            #liaison = reference.append(reference.relations.place.place_id)
            #db.session.add(liaison)
            #db.session.commit()
            #relation_id == element.place.place_id and relation_id == reference)


    #@staticmethod
    #def liaison(biblio_id, place_id):
        #erreurs = []
        #lien_id =
