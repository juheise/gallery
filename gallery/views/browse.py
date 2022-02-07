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


def _process_thumbnail(img):
    
    uuid = img["uuid"]

    return {
        "uri": url_for("thumbnail", uuid=uuid),
        "details": url_for("details", uuid=uuid)
    }


class Thumbnails:

    def __init__(self, offset: int, limit: int, order_by: str, order: str):

        images = db.search(offset=offset, limit=limit, order_by=order_by, order=order)
        self.sections = []
        current_month = None

        for img in images:
            dt = img["shot_datetime"]
            this_month = dt.month
            if this_month != current_month:
                self.sections.append({"headline": f"{MONTH_NAMES[dt.month]} {dt.year}", "thumbnails": []})
                current_month = this_month
            self.sections[-1]["thumbnails"].append(_process_thumbnail(img))


class Pagination:
    def __init__(self, offset: int, limit: int, order_by: str, order: str):
        self.next = url_for("browse", offset=offset+limit, limit=limit, order_by=order_by, order=order)
        self.prev = url_for("browse", offset=max(offset-limit, 0), limit=limit, order_by=order_by, order=order)
        self.order_date_asc = url_for("browse", offset=0, limit=limit, order_by="shot_datetime", order="asc")
        self.order_date_desc = url_for("browse", offset=0, limit=limit, order_by="shot_datetime", order="desc")
