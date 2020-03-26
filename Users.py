
import sqlalchemy as sa  # устанавливаем сокращенное название модуля
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DP = "sqlite:///sochi_athletes.sqlite3" #указываем путь к базе и записываем в переменную DP
Base = declarative_base() #создаем новый класс, который называем Base

def choice_gender():#проверяем правильность указания пола
  a=0
  while a not in [1, 2]:
      a = int(input("Ваш пол? (1-мужской, 2-женский): "))
      if a == 1:
        gender = "Male"
      elif a == 2:
        gender = "Female"
      else:
        print("Попробуйте ввести Ваш пол еще раз!")
  return gender

def valid_email(email): #проверяем правильность указания имейла
  if email.find(".", email.find("@")) == -1 or email.find("@") == -1:
    return False
  elif email.count("@") > 1:
    return False
  else:
    return True

class ATHLETE(Base): #создаем класс ATHLETE, для того, чтобы обрисовать таблицу и то, какие поля в нее будут входить
    __tablename__ = "user"
    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)

def connecting_db():
  engine = sa.create_engine(DP) #устанавливаем соединение с базой по соответствующему пути
  Base.metadata.create_all(engine)#передает нашe соединение с базой для того, чтобы подключиться  к базе данных. Если таблиц в базе, к которой мы подключаемся нет, то создаем их
  session = sessionmaker(engine) #создаем сессию с базой, чтобы потом передавать в нее данные
  return session() #на выходе из функции получаем новую сессию, готовую к работе

def request_data(): #Собираем необходимые данные и создаем из них список atheletes
    print("Пожалуйста, сообщите данные о себе!")
    first_name = input("Ваше имя: ")
    last_name = input("Ваша фамилия: ")
    gender = choice_gender()#предоставляем возможность выбрать один из вариантов пола
    email = input("Введите свой имейл: ")
    while valid_email(email) == False:
      email=input("Вы ввели емейл неверно. Попробуйте еще раз(обращая внимание на символы . и @):")
    birthdate = input("Введите дату рождения в формате ГГГГ-ММ-ДД. Например, 1987-02-08: ")
    height = input("Ваш рост в метрах? (В формате 1.75): ")
    print("Спасибо за предоставленную информацию!")
    athelete = ATHLETE(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )
    return athelete

def main(): #управляющая функция, которая обрабатывает ввод данных от пользователя
  session = connecting_db()
  athelete = request_data()
  session.add(athelete)
  session.commit()
  print("Данные успешно сохранены!")

if __name__ == "__main__":
  main()