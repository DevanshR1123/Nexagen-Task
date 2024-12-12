from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Email(db.Model):
    __tablename__ = "emails"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime)
    message_id = db.Column(db.String(120), unique=True)
    index = db.Column(db.Integer)
    sender = db.Column(db.String(120))
    subject = db.Column(db.String(255))

    def __repr__(self):
        return "<Email %r>" % self.id
