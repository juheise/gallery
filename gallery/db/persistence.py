import os

import psycopg2


DB_CONNECTION = {
    "dbname": "gallery",
    "user": "gallery"
}

GALLERY_HOME = "./"


def configure_from_env():
    
    global DB_CONNECTION, GALLERY_HOME
    
    dbname = os.getenv("GALLERY_DB_NAME")
    if dbname:
        DB_CONNECTION["dbname"] = dbname
    
    username = os.getenv("GALLERY_DB_USER")
    if username:
        DB_CONNECTION["user"] = username
    
    gallery_home = os.getenv("GALLERY_HOME")
    if gallery_home:
        GALLERY_HOME = gallery_home if not gallery_home.endswith("/") else gallery_home[:-1]


def configure(connection):
    global DB_CONNECTION
    DB_CONNECTION = connection


def _exec_from_file(path: str) -> None:
    with open(path) as f:
        statements = f.read()
    _exec_update(statements)


def _fetch_one(statement, args=None):
    with psycopg2.connect(**DB_CONNECTION) as connection:
        with connection.cursor() as cursor:
            cursor.execute(statement, args)
            return cursor.fetchone()


def _exec_update(statement):
    with psycopg2.connect(**DB_CONNECTION) as connection:
        connection.set_session(readonly=False, autocommit=True)
        with connection.cursor() as cursor:
            cursor.execute(statement)
            connection.commit()


def initialize(force_clean: bool = False):

    _exec_from_file(f"{GALLERY_HOME}/gallery/db/01-create-schema.sql")
    _exec_from_file(f"{GALLERY_HOME}/gallery/db/02-create-tables.sql")

    if not force_clean:
        return
        
    _exec_update("delete from gallery.tags_images_assoc")
    _exec_update("delete from gallery.tags")
    _exec_update("delete from gallery.images")


def insert(entry):

    keys = str.join(", ", entry.keys())
    values = str.join(", ", [f"%({key})s" for key in entry.keys()])

    with psycopg2.connect(**DB_CONNECTION) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                f"insert into gallery.images ({keys}) values ({values})",
                entry
            )
            connection.commit()


def search(order_by: str = "shot_datetime", order: str = "desc", offset: int = 0, limit: int = 100):
    with psycopg2.connect(**DB_CONNECTION) as connection:
        with connection.cursor() as cursor:
            # todo ensure sanitized arguments
            cursor.execute(f"select * from gallery.images order by {order_by} {order} limit {limit} offset {offset}")
            result = cursor.fetchall()
            keys = [col.name for col in cursor.description]

    mapped = []
    for row in result:
        obj = {}
        for i in range(len(keys)):
            obj[keys[i]] = row[i]
        mapped.append(obj)
    
    return mapped
    

def load(uuid: str):
    with psycopg2.connect(**DB_CONNECTION) as connection:
        with connection.cursor() as cursor:
            cursor.execute("select * from gallery.images where uuid=%s", (uuid,))
            result = cursor.fetchone()
            keys = [col.name for col in cursor.description]
        
    obj = {}
    for i in range(len(keys)):
        obj[keys[i]] = result[i]
    
    return obj


def remove_image_tag(pic_id: int, tag_id: int):
    with psycopg2.connect(**DB_CONNECTION) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "delete from gallery.tags_images_assoc where image_id=%s and tag_id=%s",
                (pic_id, tag_id)
            )
            connection.commit()
            cursor.execute("select * from gallery.tags_images_assoc where tag_id=%s", (tag_id,))
            result = cursor.fetchone()
            if result is None:
                cursor.execute("delete from gallery.tags where id=%s", (tag_id,))
                connection.commit()


def set_image_tag(pic_id: int, tag_id: int):
    with psycopg2.connect(**DB_CONNECTION) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "insert into gallery.tags_images_assoc values (%s, %s)",
                (tag_id, pic_id)
            )
            connection.commit()


def insert_tag(tag: str):
    with psycopg2.connect(**DB_CONNECTION) as connection:
        with connection.cursor() as cursor:
            cursor.execute("insert into gallery.tags (tag) values (%s)", (tag,))
            connection.commit()


def load_tag(tag: str, create: bool=False):
    with psycopg2.connect(**DB_CONNECTION) as connection:
        with connection.cursor() as cursor:
            cursor.execute("select * from gallery.tags where tag=%s", (tag,))
            result = cursor.fetchone()
            keys = [col.name for col in cursor.description]
    
    if result is None:
        if create:
            insert_tag(tag)
            return load_tag(tag)
        else:
            return None

    obj = {}
    for i in range(len(keys)):
        obj[keys[i]] = result[i]
    
    return obj


def load_image_tags(pic_id: int):
    with psycopg2.connect(**DB_CONNECTION) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "select t.tag as tag, t.id as id from gallery.tags as t "
                "join gallery.tags_images_assoc as a on a.tag_id=t.id "
                "where a.image_id=%s", 
                (pic_id,)
            )
            result = cursor.fetchall()
            keys = [col.name for col in cursor.description]

    mapped = []
    for row in result:
        obj = {}
        for i in range(len(keys)):
            obj[keys[i]] = row[i]
        mapped.append(obj)
    
    return mapped
