from dataclasses import dataclass
import time

import requests
import telegram
from telegram import Audio, InputMediaAudio, MessageEntity
from yandex_music import Client, Track

from config import BACK_CHAT_ID, MAIN_CHAT_ID, TG_TOKEN, TOKEN


bot = telegram.Bot(TG_TOKEN)
client = Client(TOKEN).init()


@dataclass
class CustomAlbum:
    title: str
    tracks: list[Track]
    cover_uri: str


def get_album_info(album_id: int, cover_size: str = "1000x1000") -> CustomAlbum:
    """Получить информацию о альбоме по id."""
    album = client.albums_with_tracks(album_id)
    cover_uri = f'https://{album.cover_uri.replace("%%", cover_size)}'
    return CustomAlbum(album.title, album.volumes[0], cover_uri)


def make_entity(name: str, url: str) -> MessageEntity:
    """Создать прикрепление картинки к сообщению."""
    offset = len(name) + 1
    return MessageEntity(type="text_link", offset=offset, length=1, url=url)


def send_album_presentation(name: str, url: str) -> None:
    """Функция отправляет карточку с названием, хештегом и обложкой в канал."""
    hashtag = "#" + name.replace(" ", "_").replace("-", "_")
    text = f"{hashtag} \n{name}"
    print(f"{name} - {hashtag}")
    bot.send_message(MAIN_CHAT_ID, text, entities=[make_entity(name, url)])


def send_album_by_id(album_id: int) -> None:
    """Отпарвки всего альбома в ТГ по id."""
    album = get_album_info(album_id)
    cover = requests.get(album.cover_uri).content
    media_group = make_media_group_ids(album.tracks, cover)
    send_album_presentation(name=album.title, url=album.cover_uri)
    if len(media_group) <= 10:
        bot.send_media_group(MAIN_CHAT_ID, media=[
            InputMediaAudio(audio) for audio in media_group
        ])
        return
    for i in range(0, len(media_group), 10):
        if i >= len(media_group) - 10:
            temp_media_group = media_group[i:]
        else:
            temp_media_group = media_group[i:i+10]
        media = bot.send_media_group(MAIN_CHAT_ID, media=[InputMediaAudio(
            audio) for audio in temp_media_group])
        time.sleep(30)


def make_media_group_ids(tracks: list[Track], cover: bytes) -> tuple[Audio]:
    """."""
    media_group_ids = []
    for track in tracks:
        bin = requests.get(track.get_download_info()[
                           0].get_direct_link()).content
        performer = ", ".join(
            artist.name for artist in track.artists if artist.name is not None
        )
        msg = bot.send_audio(
            BACK_CHAT_ID, audio=bin, thumb=cover, title=track.title, performer=performer
        )
        media_group_ids.append(msg.audio)
    return media_group_ids


def main():
    ARTIST = 7461723
    ids = [album.id for album in client.artists_direct_albums(
        ARTIST, page_size=100).albums]
    ids = ids[::-1]
    for _id in ids:
        send_album_by_id(_id)


if __name__ == "__main__":
    main()
