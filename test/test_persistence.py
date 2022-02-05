from db import persistence as db

def test_insert_and_load():
    
    uuid = "c7c741ef-5535-4441-aea3-6032063e4511"
    pic = {
        "abspath": "/foo/bar.jpg",
        "file_name": "bar.jpg",
        "uuid": uuid,
        "thumbnail": "/thumbs/bar_thumb.jpg",
        "width_px": 300,
        "height_px": 400
    }

    db.configure({"dbname": "gallery_test", "user": "juheise"})
    db.initialize()
    db.insert(pic)
    
    actual = db.load(uuid)
    for key, value in pic.items():
        assert actual[key] == value
