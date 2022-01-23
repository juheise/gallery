from flask import url_for

import db.persistence as db


def process_thumbnail(img):
    return {
        "uri": url_for("static", filename=f"thumbnails/{img['thumbnail']}"),
        "details": url_for("static", filename=f"pictures/{img['file_name']}")
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
