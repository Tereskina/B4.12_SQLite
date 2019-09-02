import datetime

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class Athelete(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'athelete'
    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, nullable=False, unique=True, autoincrement=True, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)


class User(Base):
    """
    Описывает структуру таблицы user, содержащую данные о пользователях
    """
    __tablename__ = 'user'

    id = sa.Column(sa.String(36), primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """

    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    print("Давай поищем атлетов похожих на одного из пользователей.")
    user_id = input("Введи id пользователя: ")
    return int(user_id)


def convert_str_to_date(date_str):
    """
    Конвертирует строку с датой в формате ГГГГ-ММ-ЧЧ в объект  datetime.date
    """
    parts = date_str.split("-")
    date_parts = map(int, parts)
    date = datetime.date(*date_parts)
    return date


def nearest_by_bd(user, session):
    """
    Ищет ближайшего по дате рождения атлета к пользователю user
    """
    athletes_list = session.query(Athelete).all()
    athlete_id_bd = {}
    for athlete in athletes_list:
        bd = convert_str_to_date(athlete.birthdate)
        athlete_id_bd[athlete.id] = bd
    
    user_bd = convert_str_to_date(user.birthdate)
    min_dist = None
    athlete_id = None
    athlete_bd = None

    for id_, bd in athlete_id_bd.items():
        dist = abs(user_bd - bd)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_bd = bd
    
    return athlete_id, athlete_bd


def nearest_by_height(user, session):
    """
    Ищет ближайшего по росту атлета к пользователю user
    """
    athletes_list = session.query(Athelete).filter(Athelete.height != None).all()
    atlhete_id_height = {athlete.id: athlete.height for athlete in athletes_list}

    user_height = user.height
    min_dist = None
    athlete_id = None
    athlete_height = None

    for id_, height in atlhete_id_height.items():
        dist = abs(user_height - height)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_height = height
    
    return athlete_id, athlete_height


def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    user_id = request_data()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        print("Такого пользователя не нашлось:(")
    else:
        bd_athlete, bd = nearest_by_bd(user, session)
        height_athlete, height = nearest_by_height(user, session)
        print(
            "Ближайший по дате рождения атлет: {}, его дата рождения: {}".format(bd_athlete, bd)
        )
        print(
            "Ближайший по росту атлет: {}, его рост: {}".format(height_athlete, height)
        )


if __name__ == "__main__":
    main()