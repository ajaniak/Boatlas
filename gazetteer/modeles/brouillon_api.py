"type": "place",
            "id": self.place_id,
            "attributes": {
                "name": self.place_nom,
                "description": self.place_description,
                "longitude": self.place_longitude,
                "latitude": self.place_latitude,
                "category": self.place_type,

            },
            "links": {
                "api": url_for("get_place", id=self.place_id, _external=True),
                "self": url_for("lieu", place_id=self.place_id, _external=True)
                },

"type": "biblio",
            "id": self.biblio_id,
            "attributes": {
                "titre": self.biblio_titre,
                "auteur": self.biblio_auteur,
                "date": self.biblio_date,
                "lieu": self.biblio_lieu,
                "category": self.biblio_type,

            },
            "links": {
                "self": url_for("biblio", biblio_id=self.biblio_id, _external=True),
                "json": url_for("get_biblio", id=self.biblio_id, _external=True)
            },
