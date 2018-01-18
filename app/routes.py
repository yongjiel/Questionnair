from flask import render_template, flash, redirect, request
from app import app, db
from app.forms import QuestionForm, QuestionEditForm
from app.models import Question, Answer
import re

array = {}

def save_answer(dict, email):
    for k, v in dict.iteritems():
        m = re.search(r"question(\d+)", k)
        if m:
            id = m.group(1)
            q = Question.query.get(id)
            a = Answer(description=v, question=q, email=email)
            db.session.add(a)
    db.session.commit()



@app.route('/', methods=['GET', 'POST'])
def index():
    form = QuestionForm(meta={'csrf': True})
    if request.method == 'POST' and form.validate_on_submit():
        email = form.data['username']
        for fieldname, value in form.data.items():
            if fieldname == 'question_fields':
                array[fieldname] = value[0]
                #'question_fields': [{'csrf_token': u'', 'question11': u'Bus', 
                                    #'question10': u'Edmonton', 'question12': u' Toronto', 
                                    #'question5': u'sf', 'question4': u'dsafd', 'question7': u'fdsaf', 
                                    # 'question6': u'dsa', 'question1': u'fdsafs', 'question3': u'dsaf', 
                                    #'question2': u'fdsaf', 'question9': u'fdsfds', 'question8': u'dsaf'}]
                save_answer(value[0], email)
        flash('Questions are submmited by user {}'.format(
            form.username.data))
        return redirect('/')
    else:
        form.questions = Question.query.all()
    return render_template('questionForm.html', title='Task1', form=form)

def save_question(dict):
    qs = Question.query.all()
    for q in qs:
        i = int(q.id)
        for k, v in dict.iteritems():
            m = re.search(r"question(\d+)", k)
            if m and int(m.group(1)) == i:
                q.description = v
                break
        for k, v in dict.iteritems():
            m = re.search(r"question_type(\d+)", k)
            if m and int(m.group(1)) == i:
                q.type = v
                break
        for k, v in dict.iteritems():
            m = re.search(r"question_choice(\d+)", k)
            if m and int(m.group(1)) == i:
                q.choice = v
                break
        db.session.add(q)
    db.session.commit()


@app.route("/admin/question", methods=['GET', 'POST'])
def questions():
    form = QuestionEditForm(meta={'csrf': True})
    if request.method == 'POST' and form.validate_on_submit():
        # save to database
        #'question_fields': [{'question_choice8': u'', 'question_choice9': u'', 
        #  'question_choice2': u'', 'question_choice3': u'', 'question_choice1': u'', 
        #  'question_choice6': u'', 'question_choice7': u'', 'question_choice4': u'', 
        #  'question_choice5': u'', 'question_choice10': u'Calgary,Edmonton,Airdry', 
        #  'question_choice11': u'Car,Bus,Walk', 'question_choice12': u'Chicago, Toronto, Calgary', 
        #  'question_type9': u'textarea', 'question_type8': u'textarea', 'question_type7': u'textarea', 
        #  'question_type6': u'textarea', 'question_type5': u'textarea', 'question_type4': u'textarea', 
        #  'question_type3': u'textarea', 'question_type2': u'textarea', 'question_type1': u'textarea', 
        #  'question5': u'What were your mother born?', 'question4': u'What flight company did you use last time?', 
        #  'question7': u'What is your favourite food?', 'question6': u'What is the model of your last car?', 
        #  'question1': u'What is your favourite boots?', 'question3': u'Where were your born?', 
        #  'question2': u'What is your favourite movie?', 'question9': u"What is your first pet's name?", 
        #  'question8': u'Where were your father born?', 'question11': u'How do you go to work everyday?', 
        #  'question10': u'Where are your working now?', 'question12': u'What is the last city you vistied?', 
        #  'question_type12': u'radiobox', 'question_type11': u'radiobox', 'question_type10': u'radiobox'}]
        for fieldname, value in form.data.items():
            if fieldname == 'question_fields':
                save_question(value[0])
        flash('Questions are update!')
        return redirect('/admin/question')
    else:
        form.questions = Question.query.all()
    return render_template('questionEditForm.html', title='Task1', form=form)

@app.route("/admin/answer")
def answer():
    ans = Answer.query.all()
    qs = []
    for a in ans:
        qs.append(a.question.description)
    return render_template('answerShow.html', title='Task1', question_descriptions=qs, answers=ans)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
