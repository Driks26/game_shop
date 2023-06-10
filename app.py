from flask import Flask, render_template, request, url_for, flash, redirect
from database.db import Clients, session, engine, Games

app = Flask(__name__)
app.static_folder = 'static'

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
        login = request.form.get("login")
        password = request.form.get('password')
        password2 = request.form.get('password2')
        email_field = request.form.get('email')

        if not (name and login and password and password2 and email_field):
            flash("Please fill all fields")
        elif password != password2:
            flash("Passwords are not equal!")
        else:
            existing_user = session.query(Clients).filter_by(login=login).first()
            if existing_user:
                flash("Username already exists. Please choose a different username.")
            else:
                new_user = session.query(Clients)(login=login, name=name, password=generate_password_hash(password), email=email_field)
                session.add(new_user)
                session.commit()
                flash("Registration successful. You can now login.")
                return redirect(url_for('.login_page'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
