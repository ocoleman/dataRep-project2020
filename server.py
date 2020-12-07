from flask import Flask, url_for, request, abort, redirect, jsonify, session, render_template, url_for
from quizDAO import quizDAO
import re
app = Flask(__name__, template_folder='static')
app.secret_key= 'somesecretkeyadaf23'


@app.route('/')
def home():
    if 'loggedin' in session:

        return render_template('home.html', username=session['username'])
    
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    msg = ""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        account = quizDAO.getUser(username, password)

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']

            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password'

    return render_template('index.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)

    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():

    msg = ""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        account = quizDAO.checkForUser(username)

        #error handling
        if account:
            msg= "Error: Account already exists!"
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = "Error: Username must contain only letters and numbers!"
        elif not username or not password:
            msg = "Error: fields were filled incorrectly"
        else:
            #valid submission
            quizDAO.createUser(username, password)
            msg = "Registration Successful"
            return redirect(url_for('login'))
        
    elif request.method == 'POST':
        #form empty
        msg = "Please fill out the form"

    return render_template('register.html', msg=msg)

@app.route('/play')
def play():
    qCount = quizDAO.getQuestionIds()
    msg = [i[0] for i in qCount]

    if 'loggedin' in session:

            return render_template('playQuiz.html', username=session['username'], msg=msg,)

@app.route('/OpenTrivaQuiz')
def thirdpartyquiz():

    if 'loggedin' in session:

        return render_template('thirdpartyquiz.html', username=session['username'])
    
    return redirect(url_for('login'))

@app.route('/createquestion')
def createQuestion():

    if 'loggedin' in session:

        return render_template('createquestion.html', username=session['username'])
    
    return redirect(url_for('login'))


@app.route('/questions')
def getAll():
    return jsonify(quizDAO.getAll())

@app.route('/questions/<int:id>')
def findById(id):
    return jsonify(quizDAO.findById(id))


@app.route('/questions', methods=['POST'])
def create():

    incorrect_answers = ""

    if not request.json:
        abort(400)
    
    for item in request.json["incorrect_answers"]:
        if item != "":
            incorrect_answers += item+"," 

    question = {
        "author": request.json["author"],
        "category": request.json["category"],
        "correct_answer": request.json["correct_answer"],
        "difficulty": request.json["difficulty"],
        "incorrect_answers": incorrect_answers,
        "question": request.json["question"],
        "type": request.json["type"]
    }
    return jsonify(quizDAO.create(question))

@app.route('/browse')
def browseQuestions():

    if 'loggedin' in session:

        return render_template('browse.html', username=session['username'])
    
    return redirect(url_for('login'))



@app.route('/questions/<int:id>', methods=['PUT'])
def update(id):
    incorrect_answers = ""
    foundQuestion = quizDAO.findById(id)
    if not foundQuestion:
        abort(404)
    
    if not request.json:
        abort(400)
    reqJson = request.json


    if 'author' in reqJson:
       foundQuestion['author'] = reqJson['author']
    if 'category' in reqJson:
       foundQuestion['category'] = reqJson['category']
    if 'correct_answer' in reqJson:
       foundQuestion['correct_answer'] = reqJson['correct_answer']
    if 'difficulty' in reqJson:
       foundQuestion['difficulty'] = reqJson['difficulty']

    if 'incorrect_answers' in reqJson:
        for item in request.json["incorrect_answers"]:
            if item != "":
                incorrect_answers += item+"," 
        foundQuestion['incorrect_answers'] = incorrect_answers

    if 'question' in reqJson:
       foundQuestion['question'] = reqJson['question']
    if 'type' in reqJson:
       foundQuestion['type'] = reqJson['type']
    
    values = (foundQuestion['author'],
            foundQuestion['category'],
            foundQuestion['correct_answer'],
            foundQuestion['difficulty'],
            foundQuestion['incorrect_answers'],
            foundQuestion['question'],
            foundQuestion['type'],
            foundQuestion['id'])

    quizDAO.update(values)
    return jsonify(foundQuestion)

@app.route('/questions/<int:id>', methods=['DELETE'])
def delete(id):
    quizDAO.delete(id)
    return jsonify({"done":True})

if __name__ == "__main__":
    print("in if")
    app.run(debug=True) #allows for realtime editing