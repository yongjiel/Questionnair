from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, \
                    BooleanField, SubmitField, FieldList,\
                    RadioField, TextField, TextAreaField, FormField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models import Question
from app import db
from app.models import Answer, Question
from wtforms import Form as NoCsrfForm
import sqlalchemy
from flask import flash

## to increase type of question table, 
## must add it in this list and the dict below.
ALLOWED_TYPES = ['textarea', 'radiobox']
FIELD_TYPES = {'textarea': "TextAreaField",
               'radiobox': 'RadioField'}


def email_exist(form, field):
    ans = Answer.query.filter_by(email=field.data).first()
    if ans:
        raise ValidationError('Email addess existed!. Please use other email address!')

def type_restrict(form, field):
    if not field.data in ALLOWED_TYPES:
        print("fdsafdsafdsffdasf")
        msg = 'Only ' + ",".join(ALLOWED_TYPES) + " allowed!"
        flash(msg, category='error')
        raise ValidationError(msg)
    
class QForm(FlaskForm):
    ''' for question field list '''
    class Meta:
        csrf = False
    # for flask db init
    try:
        questions = Question.query.all()
    except sqlalchemy.exc.OperationalError as e:
        questions = []
    for i in range(len(questions)):
        name = "question" + str(i+1)
        if questions[i].type == ALLOWED_TYPES[0]:
            cmd = name + " = " + FIELD_TYPES[ALLOWED_TYPES[0]] +"(\"Question\",  validators=[DataRequired()])"
            exec(cmd)
        elif questions[i].type == ALLOWED_TYPES[1]:
            l = questions[i].choice
            l = map(lambda x: "('" + x.strip() + "','" + x.strip() + "')", l.split(","))
            s = ",".join(l)
            cmd = name + " = " + FIELD_TYPES[ALLOWED_TYPES[1]] + "(\"Question\", choices=[" + s + "])"
            exec(cmd)



class QuestionForm(FlaskForm):
    ''' for entire question form with username and submit'''
    # call all the questions from database.
    # for flask db init
    try:
        questions = Question.query.all()
    except sqlalchemy.exc.OperationalError as e:
        questions = []
    username = StringField("Username (Email address):  required", 
                            validators=[DataRequired(), 
                                        Email("Wrong format!"),
                                        email_exist])
    question_fields = FieldList(FormField(QForm), min_entries=1, max_entries=1)

    submit = SubmitField('Submit')

class QEForm(FlaskForm):
    ''' for question field list '''
    class Meta:
        csrf = False
    # for flask db init
    try:
        questions = Question.query.all()
    except sqlalchemy.exc.OperationalError as e:
        questions = []
    for i in range(len(questions)):
        name = "question" + str(i+1)
        cmd = name + " = TextField(\"Question\",  validators=[DataRequired()])"
        exec(cmd)
        name = "question_type" + str(i+1)
        cmd = name + " = TextField(\"Type\",  validators=[DataRequired(), type_restrict])"
        exec(cmd)
        name = "question_choice" + str(i+1)
        cmd = name + " = TextField(\"Choice\")"
        exec(cmd)

class QuestionEditForm(FlaskForm):
    ''' for edit questions '''
    # for flask db init
    try:
        questions = Question.query.all()
    except sqlalchemy.exc.OperationalError as e:
        questions = []
    question_fields = FieldList(FormField(QEForm), min_entries=1, max_entries=1)
    submit = SubmitField('Submit')

    

        


