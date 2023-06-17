from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, current_app, jsonify
)
from flask_login import current_user, login_required
from builtins import sum
from database.db import Games, db_session, Clients, Cart, Orders, Base

card_bp = Blueprint('basket', __name__, template_folder='templates', static_folder='static')




@card_bp.route('add_basket/<int:game_id>', methods=['POST'])
@login_required
def add_basket(game_id):
    user = current_user

    # Проверьте, существует ли уже игра в корзине пользователя
    cart = db_session.query(Cart).filter_by(clients_idclients=user.id, games_idgames=game_id, orders_idorders=None).first()

    if cart:
        # Игра уже есть в корзине пользователя
        return jsonify({'message': 'The game is already in the basket'}), 400

    # Создайте новый объект Cart
    new_cart = Cart(quantity=1, games_idgames=game_id, clients_idclients=user.id)

    try:
        # Добавьте объект Cart в корзину пользователя
        db_session.add(new_cart)
        db_session.commit()
        return jsonify({'message': 'Game has been successfully added to the basket'}), 200
    except:
        db_session.rollback()
        return jsonify({'message': 'Failed to add the game to the basket'}), 400
    finally:
        db_session.close()


@card_bp.route('/')
@login_required
def index_basket():
    user = current_user

    # Получите все элементы корзины для текущего пользователя
    cart_items = db_session.query(Cart).filter_by(clients_idclients=user.id, orders_idorders=None).all()
    # total_price
    total_price = 0

    # Обновите объекты cart_items, чтобы включить полную информацию о каждой игре
    cart_items_with_games = []

    for cart_item in cart_items:
        game = db_session.query(Games).filter_by(idgames=cart_item.games_idgames).first()
        if game:
            cart_items_with_games.append((cart_item, game))
            total_price += game.price

    # Возвращайте шаблон, передавая в него объекты корзины и общую стоимость
    return render_template('basket.html', cart_items=cart_items_with_games, total_price=total_price)

@card_bp.route('/delete_game', methods=['POST'])
@login_required
def delete_game():
    game_id = request.form.get('game-id')
    user = current_user

    # Найти элемент корзины с указанным ID игры для текущего пользователя
    cart_item = db_session.query(Cart).filter_by(clients_idclients=user.id, games_idgames=game_id,
                                                 orders_idorders=None).first()

    if cart_item:
        try:
            # Удалить элемент корзины из базы данных
            db_session.delete(cart_item)
            db_session.commit()
            return jsonify({'message': 'Game deleted from the cart'}), 200
        except:
            db_session.rollback()
            return jsonify({'message': 'Failed to delete the game from the cart'}), 400
        finally:
            db_session.close()
    else:
        return jsonify({'message': 'Cart item not found'}), 400

@card_bp.route('/pay_basket', methods=['POST'])
@login_required
def pay_basket():
    user = current_user

    # Получите все элементы корзины для текущего пользователя
    cart_items = db_session.query(Cart).filter_by(clients_idclients=user.id, orders_idorders=None).all()

    # Рассчитайте общую стоимость товаров в корзине
    total_price = sum(item.game.price for item in cart_items)

    # Проверьте, достаточно ли средств на счету пользователя
    if user.balance is None or user.balance < total_price:
        return jsonify({'message': 'Insufficient funds'})

    try:
        # Обновите баланс пользователя
        user.balance -= total_price

        # Обновите состояние заказа
        order = Orders(total_price=total_price, clients_idclients=user, status_idstatus=1)
        db_session.add(order)

        # Привяжите корзину к заказу
        for item in cart_items:
            item.order_id = order.id
            # Очистите корзину пользователя
            db_session.delete(item)

        db_session.commit()
        return jsonify({'message': 'Payment successful'}), 200
    except:
        db_session.rollback()
        return jsonify({'message': 'Payment failed'}), 400
    finally:
        db_session.close()
