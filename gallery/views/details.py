import flask

import db.persistence as db


EXCLUDE_ATTRIBUTES = {"id", "uuid", "abspath", "file_name", "thumbnail", "hash_hex", "hash_algo"}

ATTRIBUTE_NAMES = {
    "width_px": "Breite (Pixel)",
    "height_px": "Höhe (Pixel)",
    "camera": "Kamera",
    "shot_datetime": "Aufnahmedatum"
}

DATE_TIME_FORMAT = "%d.%m.%Y %H:%M"

ATTRIBUTE_FORMATTER = {
    "shot_datetime": lambda dt: dt.strftime(DATE_TIME_FORMAT)
}


def load_picture(uuid: str):
    return db.load(uuid)


def picture_details(uuid):

    pic = db.load(uuid)
    pic["pic_url"] = flask.url_for("picture", uuid=uuid)

    for key in EXCLUDE_ATTRIBUTES:
        pic.pop(key, None)

    for key, formatter in ATTRIBUTE_FORMATTER.items():
        if key not in pic:
            continue
        pic[key] = formatter(pic[key])

    for key, formatter in ATTRIBUTE_NAMES.items():
        try:
            pic[formatter] = pic.pop(key)
        except KeyError:
            continue

    return pic
