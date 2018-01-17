from flask import render_template, flash, redirect
from app import app, db
from app.forms import QuestionForm, QuestionEditForm
from app.models import Question, Answer



@app.route('/', methods=['GET', 'POST'])
def index():
    form = QuestionForm()
    form.questions = Question.query.all()
    if form.validate_on_submit():
        email = form.data['username']
        qs = Question.query.all()
        for fieldname, value in form.data.items():
            if fieldname == "question_fields":
                for idx in range(len(value)):
                    a = Answer(description=value[idx], question=qs[idx], email=email)
                    db.session.add(a)
                db.session.commit()
        flash('Questions are submmited by user {}'.format(
            form.username.data))
        return redirect('/')
    return render_template('questionForm.html', title='Task1', form=form)


@app.route("/admin/question", methods=['GET', 'POST'])
def questions():
    form = QuestionEditForm()
    form.questions = Question.query.all()
    if form.validate_on_submit():
        # save to database
        for fieldname, value in form.data.items():
            if fieldname == "question_fields":
                for idx in range(len(value)):
                    q = Question.query.get(idx + 1)
                    q.description = value[idx]
                    db.session.add(q)
                db.session.commit()
        flash('Questions are update!')
        return redirect('/admin/question')
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
