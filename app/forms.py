from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, TextField, TextAreaField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models import Question
from app import db
from app.models import Answer, Question


def email_exist(form, field):
    ans = Answer.query.filter_by(email=field.data).first()
    if ans:
        raise ValidationError('Email addess existed!. Please use other email address!')

class QuestionForm(FlaskForm):
    # call all the questions from database.
    questions = Question.query.all()
    username = StringField("Username (Email address):  required", 
                            validators=[DataRequired(), 
                                        Email("Wrong format!"),
                                        email_exist])
    
    question_fields = FieldList(TextAreaField("Question", validators=[DataRequired()]), min_entries=12)
    submit = SubmitField('Submit')

class QuestionEditForm(FlaskForm):
    questions = Question.query.all()
    question_fields = FieldList(TextField("Question", validators=[DataRequired()]), min_entries=12)
    submit = SubmitField('Submit')


