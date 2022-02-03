from flask import url_for

import db.persistence as db


def process_thumbnail(img):
    
    uuid = img["uuid"]

    return {
        "uri": url_for("thumbnail", uuid=uuid),
        "details": url_for("picture", uuid=uuid)
    }


def fetch_thumbnails():

    images = db.search()
    entries = [process_thumbnail(img) for img in images]

    return [
        {
            "headline": f"{len(images)} Bilder",
            "thumbnails": entries
        },
    ]
