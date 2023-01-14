from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    hair_color = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<People %r>' % self.id

    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "hair_color": self.hair_color}


class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    climate = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.id

    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "climate": self.climate}


class UserFavoritePlanets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    favorite_planet_id = Column(db.Integer, db.ForeignKey('planets.id'), unique=True, nullable=False)
    user_id = Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False )
    user = relationship(User)

    def __repr__(self):
        return '<UserFavoritePlanets %r>' % self.id

    def serialize(self):
        return {"id": self.id,
                "favorite_planet_id": self.id}


class UserFavoritePeople(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    favorite_people_id = Column(db.Integer, db.ForeignKey('people.id'), unique=True, nullable=False)
    user_id = Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False )
    user = relationship(User)

    def __repr__(self):
        return '<UserFavoritePeople %r>' % self.id

    def serialize(self):
        return {"id": self.id,
                "favorite_people_id": self.id}


