from gallery.db import persistence as db


def init_db_for_test():
    db.configure({"dbname": "gallery_test", "user": "juheise"})
    db.initialize(force_clean=True)
