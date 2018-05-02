#class Authorship(db.Model):
    #__tablename__ = "authorship"
    #authorship_id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    #authorship_place_id = db.Column(db.Integer, db.ForeignKey('place.place_id'))
    #authorship_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    #authorship_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    #user = db.relationship("User", back_populates="authorships")
    #place = db.relationship("Place", back_populates="authorships")

    #def author_to_json(self):
        #return {
            #"author": self.user.to_jsonapi_dict(),
            #"on": self.authorship_date
        #}
