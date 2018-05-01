from .. app import db
from modeles.donnees import Place


#on crée notre classe de références bibliographiques
class Biblio(db.Model):
    __tablename__ = "biblio"
    biblio_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    biblio_titre = db.Column(db.Text, nullable=False)
    biblio_auteur = db.Column(db.Text, nullable=False)
    biblio_date = db.Column(db.Text)
    biblio_lieu = db.Column(db.Text)
    biblio_type = db.Column(db.Text, nullable=False)
    #places = db.Column(db.Integer, db.ForeignKey('relation.relation_id'), nullable=False)

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
