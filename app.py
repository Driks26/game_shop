from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.security import check_password_hash
import hashlib
from flask_login import login_user, login_required, logout_user

from database.db import Clients, session, engine, Games

app = Flask(__name__)
app.static_folder = 'static'
app.config['SECRET_KEY'] = 'dj22223fcx3331fwcsff'


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/base')
def base():
    print(url_for('base'))
    return render_template('base.html')


@app.route('/user')
def actors():
    clients = session.query(Clients).all()
    return render_template('clients.html', clients=clients)


@app.route('/all_games')
def all_game():
    games = session.query(Games).all()
    return render_template("show_all_games.html", games=games)


@app.route('/register', methods=('GET', 'POST'))
def register_page():
    if request.method == "POST":
        name = request.form.get("name")
        surname = request.form.get("surname")
        nickname = request.form.get("nickname")
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if not (name and surname and nickname and password and password2):
            flash("Please fill all fields")
        elif password != password2:
            flash("Passwords are not equal!")
        else:
            existing_user = session.query(Clients).filter_by(nickname=nickname).first()
            if existing_user:
                flash("Username already exists. Please choose a different username.")
            else:
                new_user = Clients(nickname=nickname, name=name, surname=surname, password=password)
                session.add(new_user)
                session.commit()
                flash("Registration successful. You can now login.")
            return redirect(url_for('login_page'))

    return render_template('reg.html')


@app.route('/login', methods=('GET', 'POST'))
def login_page():
    nickname = request.form.get("nickname")
    password = request.form.get("password")

    if request.method == 'POST':
        if nickname and password:
            user = session.query(Clients).filter_by(nickname=nickname).first()
            global password_hash
            if password is not None:
                hash_object = hashlib.sha256()
                # Преобразуем пароль в байтовую строку и вычисляем хэш
                hash_object.update(password.encode('utf-8'))
                password_hash = hash_object.hexdigest()

            if user and password_hash == user.password:
                login_user(user)
                print(password_hash, user.password)
                # login_user(user)
                # next_page = request.args.get('next')
                return redirect(url_for('index'))
            else:
                flash('Login or password are incorrect')
        else:
            flash('Please fill in login and password')

    return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
