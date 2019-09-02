# испортируем модули стандартнй библиотеки uuid и datetime
# import uuid
# import datetime

# импортируем библиотеку sqlalchemy и некоторые функции из нее 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()


class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'user'

    # идентификатор пользователя, первичный ключ
    #id = sa.Column(sa.String(36), primary_key=True)
    id = sa.Column(sa.Integer, nullable=False, unique=True, autoincrement=True, primary_key=True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    #пол
    gender = sa.Column(sa.Text)
    # адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    #дата рождения
    birthdate = sa.Column(sa.Text)
    #рост
    height = sa.Column(sa.Float)


# class LastSeenLog(Base):
#     """
#     Описывает структуру таблицу log для хранения времени последней активности пользователя
#     """
#     # задаем название таблицы
#     __tablename__ = 'log'

#     # идентификатор пользователя, первичный ключ
#     id = sa.Column(sa.String(36), primary_key=True)
#     # время последней активности пользователя
#     timestamp = sa.Column(sa.DATETIME)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()


def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    # выводим приветствие
    print("Привет! Я запишу твои данные!")
    # запрашиваем у пользователя данные
    first_name = input("Введи своё имя: ")
    last_name = input("А теперь фамилию: ")
    gender = input("Укажи свой пол (Male/Female): ")
    email = input("Мне еще понадобится адрес твоей электронной почты: ")
    birthdate = input("Напиши свою дату рождения (ГГГГ-ММ-ДД): ")
    height = input("Напиши свой рост (в метрах, например 1.72): ")
    # генерируем идентификатор пользователя и сохраняем его строковое представление
    #user_id = str(uuid.uuid4())
    # создаем нового пользователя
    user = User(
        #id=user_id,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=float(height)
    )
    # возвращаем созданного пользователя
    return user


def find(name, session):
    """
    Производит поиск пользователя в таблице user по заданному имени name
    """
    # нахдим все записи в таблице User, у которых поле User.first_name совпадает с парарметром name
    query = session.query(User).filter(User.first_name == name)
    # подсчитываем количество таких записей в таблице с помощью метода .count()
    users_cnt = query.count()
    # составляем список идентификаторов всех найденных пользователей
    #user_ids = [user.id for user in query.all()]
    # находим все записи в таблице LastSeenLog, у которых идентификатор совпадает с одним из найденных
    # last_seen_query = session.query(LastSeenLog).filter(LastSeenLog.id.in_(user_ids))
    # строим словарь вида идентификатор_пользователя: время_его_последней_активности
    # log = {log.id: log.timestamp for log in last_seen_query.all()}
    # возвращаем кортеж количество_найденных_пользователей, список_идентификаторов, словарь_времени_активности
    return (users_cnt, query.all())


# def update_timestamp(user_id, session):
#     """
#     Обновляет время последней активности пользоватля с заданным идентификатором user_id
#     """
#     # находим запись в журнале о пользователе с идентификатором user_id
#     log_entry = session.query(LastSeenLog).filter(LastSeenLog.id == user_id).first()
#     # проверяем есть уже в журнале запись о таком пользователе
#     if log_entry is None:
#         # если записи не оказалось в журнале, создаем новую
#         log_entry = LastSeenLog(id=user_id)

#     # обновляем время последней активности пользователя на текущее
#     log_entry.timestamp = datetime.datetime.now()
#     return log_entry


def print_users_list(cnt, users):
    """
    Выводит на экран количество найденных пользователей, их идентификатор и время последней активности.
    Если передан пустой список идентификаторов, выводит сообщение о том, что пользователей не найдено.
    """
    # проверяем на пустоту список идентификаторов
    if users:
        # если список не пуст, распечатываем количество найденных пользователей
        print("Найдено пользователей: ", cnt)
        # легенду будущей таблицы
        print("Идентификатор пользвоателя и его данные")
        # проходимся по каждому идентификатору
        for user in users:
            # получаем время последней активности из словаря last_seen_log
            # last_seen = last_seen_log[user_id]
            # выводим на экран идентификатор - время_последней_активности
            print("{} {} {} {} {} {} {}".format(user.id, user.first_name, user.last_name, user.gender, user.email, user.birthdate, user.height))
    else:
        # если список оказался пустым, выводим сообщение об этом
        print("Пользователей с таким именем нет.")


def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    # просим пользователя выбрать режим
    mode = input("Выбери режим.\n1 - найти пользователя по имени\n2 - ввести данные нового пользователя\n")
    # проверяем режим
    if mode == "1":
        # выбран режим поиска, запускаем его
        name = input("Введи имя пользователя для поиска: ")
        # вызываем функцию поиска по имени
        # users_cnt, user_ids, log = find(name, session)
        users_cnt, users = find(name, session)
        # вызываем функцию печати на экран результатов поиска
        print_users_list(users_cnt, users)
    elif mode == "2":
        # запрашиваем данные пользоватлея
        user = request_data()
        # добавляем нового пользователя в сессию
        session.add(user)
        # обновляем время последнего визита для этого пользователя
        # log_entry = update_timestamp(user.id, session)
        # # добавляем объект log_entry в сессию
        # session.add(log_entry)
        # # сохраняем все изменения, накопленные в сессии
        session.commit()
        print("Спасибо, данные сохранены!")
    else:
        print("Некорректный режим:(")


if __name__ == "__main__":
    main()