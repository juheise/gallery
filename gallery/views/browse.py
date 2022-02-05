from datetime import datetime
from flask import url_for

import db.persistence as db

MONTH_NAMES = {
    1: "Januar",
    2: "Februar",
    3: "März",
    4: "April",
    5: "Mai",
    6: "Juni",
    7: "Juli",
    8: "August",
    9: "September",
    10: "Oktober",
    11: "November",
    12: "Dezember"
}


def process_thumbnail(img):
    
    uuid = img["uuid"]

    return {
        "uri": url_for("thumbnail", uuid=uuid),
        "details": url_for("details", uuid=uuid)
    }


def fetch_thumbnails():

    images = db.search()
    sections = []
    current_month = None

    for img in images:
        dt = img["shot_datetime"]
        this_month = dt.month
        if this_month != current_month:
            sections.append({"headline": f"{MONTH_NAMES[dt.month]} {dt.year}", "thumbnails": []})
            current_month = this_month
        sections[-1]["thumbnails"].append(process_thumbnail(img))

    return sections
