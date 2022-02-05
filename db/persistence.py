import psycopg2


DB_CONNECTION = {
    "dbname": "gallery",
    "user": "juheise"
}


def insert(entry):

    keys = str.join(", ", entry.keys())
    values = str.join(", ", [f"%({key})s" for key in entry.keys()])

    with psycopg2.connect(**DB_CONNECTION) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                f"insert into images ({keys}) values ({values})",
                entry
            )
            connection.commit()


def search(order_by="shot_datetime", order="desc"):
    with psycopg2.connect(**DB_CONNECTION) as connection:
        with connection.cursor() as cursor:

            cursor.execute(f"select * from images order by {order_by} {order}")
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
            cursor.execute("select * from images where uuid=%s", (uuid,))
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
                "delete from tags_images_assoc where image_id=%s and tag_id=%s",
                (pic_id, tag_id)
            )
            connection.commit()
            cursor.execute("select * from tags_images_assoc where tag_id=%s", (tag_id,))
            result = cursor.fetchone()
            if result is None:
                cursor.execute("delete from tags where id=%s", (tag_id,))
                connection.commit()


def set_image_tag(pic_id: int, tag_id: int):
    with psycopg2.connect(**DB_CONNECTION) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "insert into tags_images_assoc values (%s, %s)",
                (tag_id, pic_id)
            )
            connection.commit()


def insert_tag(tag: str):
    with psycopg2.connect(**DB_CONNECTION) as connection:
        with connection.cursor() as cursor:
            cursor.execute("insert into tags (tag) values (%s)", (tag,))
            connection.commit()


def load_tag(tag: str, create: bool=False):
    with psycopg2.connect(**DB_CONNECTION) as connection:
        with connection.cursor() as cursor:
            cursor.execute("select * from tags where tag=%s", (tag,))
            result = cursor.fetchone()
            keys = [col.name for col in cursor.description]
    
    if result is None and create:
        insert_tag(tag)
        return load_tag(tag)

    obj = {}
    for i in range(len(keys)):
        obj[keys[i]] = result[i]
    
    return obj


def load_tag_by_id(id_: int):
    with psycopg2.connect(**DB_CONNECTION) as connection:
        with connection.cursor() as cursor:
            cursor.execute("select * from tags where id=%s", (id_,))
            result = cursor.fetchone()
            keys = [col.name for col in cursor.description]
    
    if result is None:
        raise ValueError(f"tag with id={id_} does not exist")

    obj = {}
    for i in range(len(keys)):
        obj[keys[i]] = result[i]
    
    return obj


def load_image_tags(pic_id: int):
    with psycopg2.connect(**DB_CONNECTION) as connection:
        with connection.cursor() as cursor:
            cursor.execute("select * from tags_images_assoc where image_id=%s", (pic_id,))
            result = cursor.fetchall()
            keys = [col.name for col in cursor.description]

    mapped = []
    for row in result:
        obj = {}
        for i in range(len(keys)):
            obj[keys[i]] = row[i]
        mapped.append(obj)
    
    return mapped
