from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<Usuario %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            'esta_activo': self.is_active,
            'calificacion': 5
            # do not serialize the password, its a security breach
        }

class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    ciudad = db.Column(db.String(250), nullable=False)
    slogan = db.Column(db.String(250), nullable=False)
    videojuegos = db.relationship('Videojuego', backref='empresa', lazy=True)

    def __repr__(self):
        return '<Company %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "himno": self.slogan,
            # do not serialize the password, its a security breach
        }
    
class Videojuego(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    genero = db.Column(db.String(250), nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'),
        nullable=False)

    def __repr__(self):
        return '<Game %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "himno": self.slogan,
            # do not serialize the password, its a security breach
        }