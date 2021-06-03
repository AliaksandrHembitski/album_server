# импортируем модуль sqlalchemy
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# импортирует модуль serverAlbums
import serverAlbums
# создаем переменную пути к БД
DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

# создаем класс с разметкой таблицы в sqlite
class Album(Base):


    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

# создаем сессию подключения к БД
def connect_db():

    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

# функция поиска по запросу пользователя
def find(artist):

    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums
# функция добавления нового объекта в БД
def save_album(album_data):

    album = Album(
        id = album_data['id_artist'],
        year = album_data['year'],
        artist = album_data['artist'],
        genre = album_data['genre'],
        album = album_data['album']
    )
    session = connect_db()
    session.add(album)
    session.commit()
    return album
# функция проверки полученных данных
def validation_album_data(album_data):
    try:
        if type(int(album_data['year'])) == int and 1860 <= int(album_data['year']) <= 2021:
            return True
    except ValueError:
        pass
