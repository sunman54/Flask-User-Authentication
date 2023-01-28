from flask import Flask, render_template, url_for, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.permanent_session_lifetime = timedelta(minutes=1) # days=1

db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    note = db.Column(db.String(400))
    def __int__(self, name, note):
        self.name = name
        self.note = note

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.permanent = True
        user = request.form['name']
        session['user'] = user

        found_user = Users.query.filter_by(name = user).first()

        if found_user:
            session['note'] = found_user.note
        else:
            usr = Users(name = user, note = "")
            db.session.add(usr)
            db.session.commit()
        return redirect(url_for('user'))

    else:
        if 'user' in session:
            return redirect(url_for('user'))
        else:
            return render_template('login.html')

@app.route('/user/', methods=['GET', 'POST'])
def user():
        if 'user' in session:
            user = session['user']

            if request.method == 'POST':
                note = request.form['note']
                session['note'] = note
                found_user = Users.query.filter_by(name=user).first()
                found_user.note = note

                db.session.commit()

            else:
                if 'note' in session:
                    note = session['note']


            return render_template('dashboard.html', user = user)
        else:
            return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None )
    return redirect(url_for('home'))


@app.route('/view')
def view():
    return render_template('view.html', values = Users.query.all())

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)