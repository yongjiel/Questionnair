from datetime import datetime
from app import db

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(512), index=True, unique=True)
    type = db.Column(db.String(60))
    choice = db.Column(db.String(512))
    answers = db.relationship('Answer', backref='question', lazy='dynamic', cascade="all,delete")

    def __repr__(self):
        return '<Question {}>'.format(self.description)    

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True)
    description = db.Column(db.String(512))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    def __repr__(self):
        return '<Answer {}>'.format(self.description)

