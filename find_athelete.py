import sqlalchemy as sa, datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DP = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class ATHLETE(Base):
    __tablename__ = 'athelete' #задаем название таблицы, с которой будем работать
    # названия полей берем из БД
    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    weight = sa.Column(sa.Integer)
    name = sa.Column(sa.Text)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

class USER(Base):
    __tablename__ = 'user'

    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)

def connecting_db(): #создаем соединение с БД и формируем сессию

    engine = sa.create_engine(DP)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def request_data():
    user_id = input("Введите пожалуйста идентификатор пользователя: ")
    return int(user_id)  # на выходе получаем идентификатор пользователя в числовом формате

def str_to_date(str_date):

    split_to_parts = str_date.split("-") # отделяем символы друг от друга используя в качестве разделителя "-"
    parts_to_int = map(int, split_to_parts) # превращаем куски в число
    date = datetime.date(*parts_to_int) # превращаем число в дату
    return date

def search_birth(user, session):

    athletes_list = session.query(Athelete).all() #запрашиваем список всех атлетов
    athlete_id_bd = {} #создаем пустой словарь из ID
    for athlete in athletes_list: #пробегаемся по списку всех атлетов
        bd = str_to_date(athlete.birthdate) #приводим дату рождения каждого атлета к формату Дата
        # и записываем в переменную bd
        athlete_id_bd[athlete.id] = bd #сохраняем дату рождения в словарь по соответствующему ID

    user_bd = str_to_date(user.birthdate)
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


def search_by_height(user, session):

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

    session = connecting_db()
    user_id = request_data()
    user = session.query(USER).filter(USER.id == user_id).first()
    if not user:
        print("К сожалению, такого пользователя найти не удалось!")
    else:
        bd_athlete, bd = search_birth(user, session)
        height_athlete, height = search_by_height(user, session)
        print(
            "Ближайший по дате рождения атлет: {}, он родился: {}".format(bd_athlete, bd)
        )
        print(
            "Ближайший по росту атлет: {}, его рост: {}".format(height_athlete, height)
        )


if __name__ == "__main__":
    main()