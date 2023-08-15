# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from textblob import TextBlob


app = Flask(__name__)
final=[]
final1=[]
final2=[]

def parse(string):
    try:
        final.clear()
        final1.clear()
        final2.clear()
        txt = TextBlob(string)
        for sentence in txt.sentences:
            genQuestion(sentence)
            quest(sentence)       
    except Exception as e:
        raise e
    

def quest(text):
    if type(text) is str:     # If the passed variable is of type string.
        text = TextBlob(text) # Create object of type textblob.blob.TextBlob

    bucket1 = {}  
    
    for i,j in enumerate(text.tags):  # line.tags are the parts-of-speach in English
        if j[1] not in bucket1:
            bucket1[j[1]] = i
            
            question1 = ' '
    b1=['NN','VBZ']
    b2=['NNP','VBZ']
    
    if all(key in  bucket1 for key in b1): #'NNP', 'VBG' in sentence.
        final1.append('Define' + ' ' + text.words[bucket1['NN']] +' '+ '.')
       
        
    elif all(key in  bucket1 for key in b2): #'NNP', 'VBG' in sentence.
        final1.append('Define' + ' ' + text.words[bucket1['NNP']] +' '+ '.')
        
    if 'VBZ' in bucket1 and text.words[bucket1['VBZ']] == "’":
        final1.append(final1.replace(" ’ ","'s "))
        
    

def genQuestion(line):
    if type(line) is str:     # If the passed variable is of type string.
        line = TextBlob(line) # Create object of type textblob.blob.TextBlob

    bucket = {}  
    
    for i,j in enumerate(line.tags):  # line.tags are the parts-of-speach in English
        if j[1] not in bucket:
            bucket[j[1]] = i
            
           
            
    l1 = ['NNP', 'VBG', 'VBZ', 'IN']
    l2 = ['NNP', 'VBG', 'VBZ']
    l3 = ['PRP', 'VBG', 'VBZ', 'IN']
    l4 = ['PRP', 'VBG', 'VBZ']
    l5 = ['PRP', 'VBG', 'VBD']
    l6 = ['NNP', 'VBG', 'VBD']
    l7 = ['NN', 'VBG', 'VBZ']

    l8 = ['NNP', 'VBZ', 'JJ']
    l9 = ['NNP', 'VBZ', 'NN']

    l10 = ['NNP', 'VBZ']
    l11 = ['PRP', 'VBZ']
    l12 = ['NNP', 'NN', 'IN']
    l13 = ['NN', 'VBZ']
    
    if all(key in  bucket for key in l1): #'NNP', 'VBG', 'VBZ', 'IN' in sentence.
        final.append('What' + ' ' + line.words[bucket['VBZ']] +' '+ line.words[bucket['NNP']]+ ' '+ line.words[bucket['VBG']] + '?')

    
    elif all(key in  bucket for key in l2): #'NNP', 'VBG', 'VBZ' in sentence.
        final.append('What' + ' ' + line.words[bucket['VBZ']] +' '+ line.words[bucket['NNP']] +' '+ line.words[bucket['VBG']] + '?')

    
    elif all(key in  bucket for key in l3): #'PRP', 'VBG', 'VBZ', 'IN' in sentence.
        final.append('What' + ' ' + line.words[bucket['VBZ']] +' '+ line.words[bucket['PRP']]+ ' '+ line.words[bucket['VBG']] + '?')

    
    elif all(key in  bucket for key in l4): #'PRP', 'VBG', 'VBZ' in sentence.
       final.append('What ' + line.words[bucket['PRP']] +' '+  ' does ' + line.words[bucket['VBG']]+ ' '+  line.words[bucket['VBG']] + '?')

    elif all(key in  bucket for key in l7): #'NN', 'VBG', 'VBZ' in sentence.
        final.append('What' + ' ' + line.words[bucket['VBZ']] +' '+ line.words[bucket['NN']] +' '+ line.words[bucket['VBG']] + '?')

    elif all(key in bucket for key in l8): #'NNP', 'VBZ', 'JJ' in sentence.
        final.append('What' + ' ' + line.words[bucket['VBZ']] + ' ' + line.words[bucket['NNP']] + '?')

    elif all(key in bucket for key in l9): #'NNP', 'VBZ', 'NN' in sentence
        final.append('What' + ' ' + line.words[bucket['VBZ']] + ' ' + line.words[bucket['NNP']] + '?')

    elif all(key in bucket for key in l11): #'PRP', 'VBZ' in sentence.
        if line.words[bucket['PRP']] in ['she','he']:
           final.append('What' + ' does ' + line.words[bucket['PRP']].lower() + ' ' + line.words[bucket['VBZ']].singularize() + '?')

    elif all(key in bucket for key in l10): #'NNP', 'VBZ' in sentence.
        final.append('What' + ' does ' + line.words[bucket['NNP']] + ' ' + line.words[bucket['VBZ']].singularize() + '?')

    elif all(key in bucket for key in l13): #'NN', 'VBZ' in sentence.
        final.append('What' + ' ' + line.words[bucket['VBZ']] + ' ' + line.words[bucket['NN']] + '?')

    # When the tags are generated 's is split to ' and s. To overcome this issue.
    if 'VBZ' in bucket and line.words[bucket['VBZ']] == "’":
        final.append(final.replace(" ’ ","'s "))

    # Print the genetated questions as output.
    #if question != '':
    #print('\n', 'Question: ' + question )
        
  
        

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'shreya'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)

# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/pythonlogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/pythonlogin/profile',methods=["POST"])
def profile():
    # Check if user is loggedin
    questions=[]
    textinput=request.form.get("name")
    parse(textinput)
    final2=final1+final
    questions=[]
    for val in final2:
        if val!=' ' and val not in questions: 
            questions.append(val) 
         
    return render_template("profile.html", questions=questions)
    
@app.route('/')
def start():
    return render_template("Welcome.html")



if __name__ == '__main__':
    app.run()
