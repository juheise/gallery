import pytest

from db import persistence as db
from test.conftest import init_db_for_test


UUID = "c7c741ef-5535-4441-aea3-6032063e4511"
PIC = {
    "abspath": "/foo/bar.jpg",
    "file_name": "bar.jpg",
    "uuid": UUID,
    "thumbnail": "/thumbs/bar_thumb.jpg",
    "width_px": 300,
    "height_px": 400
}


def test_insert_and_load():

    init_db_for_test()
    db.insert(PIC)
    
    actual = db.load(UUID)
    for key, value in PIC.items():
        assert actual[key] == value


def test_insert_tag():
    init_db_for_test()
    db.insert_tag("xxx")
    assert db._fetch_one("select * from gallery.tags where tag='xxx'") is not None


@pytest.mark.parametrize("create, exists", [
    (True, True),
    (False, False)
])
def test_load_tag(create, exists):
    init_db_for_test()
    db.load_tag("xxx", create=create)
    assert (db._fetch_one("select * from gallery.tags where tag='xxx'") is not None) == exists


def test_associate_and_load_image_tags():
    init_db_for_test()
    tag = db.load_tag("a", create=True)
    db.insert(PIC)
    persistent_pic = db.load(UUID)
    db.set_image_tag(persistent_pic["id"], tag["id"])
    assert db.load_image_tags(persistent_pic["id"]) == [tag]
