from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from database.db import Games, db_session

card_bp = Blueprint('basket', __name__, template_folder='templates', static_folder='static')


@card_bp.route('/')
def index_basket():
    games = db_session.query(Games).all()
    return render_template('basket.html', games=games)
