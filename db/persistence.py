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
