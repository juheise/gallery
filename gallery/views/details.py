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
    pic["set_tags"] = flask.url_for("set_tags", uuid=uuid)
    pic["tags"] = ", ".join([tag["tag"] for tag in db.load_image_tags(pic["id"])])

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


def replace_tags(uuid: str, tags: str):

    valid_tags = []
    for tag in tags.split(","):
        if not tag.strip():
            continue
        valid_tags.append(tag)

    pic = load_picture(uuid)
    pic_id = pic["id"]
    new_tags = [db.load_tag(tag.strip(), create=True) for tag in valid_tags]
    current_tags = db.load_image_tags(pic_id)

    for tag in current_tags:
        if tag not in new_tags:
            db.remove_image_tag(pic_id, tag["id"])

    for tag in new_tags:
        if tag in current_tags:
            continue
        db.set_image_tag(pic_id, tag["id"])
