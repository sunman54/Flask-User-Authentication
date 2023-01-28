from flask import Flask, render_template, url_for, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta



app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.permanent_session_lifetime = timedelta(minutes=1) # days=1





@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.permanent = True
        user = request.form['name']
        session['user'] = user
        return redirect(url_for('user'))

    else:
        if 'user' in session:
            return redirect(url_for('user'))
        else:
            return render_template('login.html')

@app.route('/user/')
def user():
        if 'user' in session:
            user = session['user']
            return render_template('dashboard.html', user = user)
        else:
            return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None )
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, port=5001)