# импортируем модуль bottle
from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

# импортирует модуль album
import album
# импортирует модуль uuid для создания уникальных
import uuid

# пороводим проверку наличие артиста в БД
@route("/albums/<artist>")
def albums(artist):
# создаем списак найденых альбомов артиста
    albums_list = album.find(artist)
# если список пуст выводим сообщение об ошибке с кодом 404
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
# если списак не пуст то выводим сообщение кол-ва и список альбомов
    else:
        album_names = [album.album for album in albums_list]
        result = "Количество альбомов: {}.<br> Список альбомов {}:<br>".format(len(albums_list), artist)
        result += "<br>".join(album_names)
    return result

# создаем веб-форму для добовления новых альбомов в базу данных
@route('/albums/')
def albums():
    return '''
        <form action="/albums/" method="post">
            Year: <input name="year" type="text" />
            Artist: <input name="artist" type="text" />
            Genre: <input name="genre" type="text" />
            Album: <input name="album" type="text" />
            <input value="Записать" type="submit" />
        </form>
    '''
# обрабатываем данные полученные из веб-формы
@route('/albums/', method='POST')
def do_albums():
    album_data = {
# генерируем и сокрощаем id
        "id_artist":str(int(uuid.uuid4()))[:19],
        "year": request.forms.get("year"),
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album")
    }
# проводим проверку на наличие повторений
    albums_list = album.find(album_data['artist'])
    album_names = [album.album for album in albums_list]
# если добовляемый объект существует в БД выводим сообщение об ошибке с кодом 409
    if album_data['album'] in album_names:
        return HTTPError(409, "Альбом с такими данными уже существует!")
    else:
# проводим проверку полученных данных
        if album.validation_album_data(album_data) == True:
            album.save_album(album_data)
            return 'Данные успешно сохранены!'
        else:
            return 'Дата записи альбома введина не верно!'


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True, reloder=True)
