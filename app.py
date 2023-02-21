from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def homepage():
    if responses:
        responses.clear()
    return render_template('home.html', survey=satisfaction_survey)


@app.route('/questions/<num>')
def show_question(num):

    if int(num) != len(responses):
        flash('Please do not attempt to access an invalid question.')
        return redirect(f'/questions/{len(responses)}')

    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thankyou')

    question_obj = satisfaction_survey.questions[int(num)]
    question = question_obj.question
    choices = question_obj.choices
    return render_template('question.html', question=question, choices=choices, num=int(num))


@app.route('/answer/<num>', methods=['POST'])
def store_answer(num):
    answer = request.form['answer']
    responses.append(answer)
    return redirect(f'/questions/{num}')


@app.route('/thankyou')
def thankyou_page():
    return render_template('thankyou.html')
