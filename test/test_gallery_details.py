import gallery.db.persistence as db
from test.conftest import init_db_for_test
import gallery.views.details as details


UUID = "c7c741ef-5535-4441-aea3-6032063e4511"
PIC = {
    "abspath": "/foo/bar.jpg",
    "file_name": "bar.jpg",
    "uuid": UUID,
    "thumbnail": "/thumbs/bar_thumb.jpg",
    "width_px": 300,
    "height_px": 400
}

def test_replace_tags_with_new_tags():

    init_db_for_test()
    db.insert(PIC)
    details.replace_tags(UUID, "a, b, c")

    pic_id = db.load(UUID)["id"]
    assert [tag["tag"] for tag in db.load_image_tags(pic_id)] == ["a", "b", "c"]


def test_replace_tags_with_existing_tags():

    init_db_for_test()
    db.insert(PIC)
    details.replace_tags(UUID, "a, b, c")

    pic_id = db.load(UUID)["id"]
    assert [tag["tag"] for tag in db.load_image_tags(pic_id)] == ["a", "b", "c"]
