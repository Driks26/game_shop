import base64
import hashlib
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from Userlogin import UserLogin
from database.db import Clients, db_session, Games, engine



app = Flask(__name__)
app.static_folder = 'static'
app.config['SECRET_KEY'] = 'dj22223fcx3331fwcsff'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:26021712@localhost/Games1"

login_manager = LoginManager(app)




@login_manager.user_loader
def load_user(user_id):
    return UserLogin.fromDB(user_id, db_session)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/base')
def base():
    print(url_for('base'))
    return render_template('base.html')


@app.route('/user')
def actors():
    clients = db_session.query(Clients).all()
    return render_template('clients.html', clients=clients)


@app.route('/all_games')
def all_game():
    games = db_session.query(Games).all()
    return render_template("show_all_games.html", games=games)


@app.route('/register', methods=('GET', 'POST'))
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

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
            existing_user = db_session.query(Clients).filter_by(nickname=nickname).first()
            if existing_user:
                flash("Username already exists. Please choose a different username.")
            else:
                new_user = Clients(nickname=nickname, name=name, surname=surname, password=password)
                db_session.add(new_user)
                db_session.commit()
                flash("Registration successful. You can now login.")
            return redirect(url_for('login_page'))

    return render_template('reg.html')


@app.route('/login', methods=('GET', 'POST'))
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        nickname = request.form.get("nickname")
        password = request.form.get("password")

        if request.method == 'POST':
            if nickname and password:
                user = db_session.query(Clients).filter_by(nickname=nickname).first()
                global password_hash
                if password is not None:
                    hash_object = hashlib.sha256()
                    # Преобразуем пароль в байтовую строку и вычисляем хэш
                    hash_object.update(password.encode('utf-8'))
                    password_hash = hash_object.hexdigest()

                if user and password_hash == user.password:
                    user_login = UserLogin(user.idclients, user.nickname)
                    login_user(user_login)
                    # print(password_hash, user.password)
                    return redirect(url_for('index'))
                else:
                    flash('Login or password are incorrect')
            else:
                flash('Please fill in login and password')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    return redirect(url_for('index'))

@app.route('/upload_photo', methods=['GET', 'POST'])
def upload_photo():
    if 'photo' in request.files:
        img = request.files['photo']
        if img.mimetype.startswith('image/') and img.content_length <= 2*1024*1024:
            img_data = img.read()
            game = db_session.query(Games).first()
            game.photo = img_data
            db_session.commit()
            db_session.close()
    return render_template('photo.html', images=get_images())


def get_images():
    games = db_session.query(Games).all()
    db_session.close()
    images = []
    for game in games:
        if game.photo:
            img_data = game.photo
            img_base64 = base64.b64encode(img_data).decode('utf-8')
            images.append(img_base64)
    return images

@app.template_filter('b64encode')
def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8')

if __name__ == '__main__':
    app.run(debug=True)
