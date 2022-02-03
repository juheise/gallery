import db.persistence as db


def load_picture(uuid: str):
    return db.load(uuid)
