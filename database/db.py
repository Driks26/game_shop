from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

import logging


#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

data_uri = "mysql://root:26021712@localhost/Games1"
engine = create_engine(data_uri)


# Используй функцию automap_base для автоматического отображения таблиц базы данных на классы ORM
Base = automap_base()

# Отрази существующую структуру базы данных и свяжи ее с движком
Base.prepare(engine)

#Создания модели clients
Clients = Base.classes.clients

#Создания модели cart
Cart = Base.classes.cart

#Создания модели developers
Developers = Base.classes.developers

#Создания модели games
Games = Base.classes.games

#Создания модели games_genres
Games_Genres = Base.classes.games_gernes

#Создания модели genres
Genres= Base.classes.gernes

#Создания модели orders
Orders = Base.classes.orders

#Создания модели publishers
Publishers = Base.classes.publishers

#Создания модели status
Status = Base.classes.status

db_session: Session = Session(engine)


print(engine.connect())
