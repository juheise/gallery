from datetime import datetime

from flask import url_for

import gallery.db.persistence as db

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

    def __init__(
        self, offset: int, limit: int, order_by: str, order: str, start_date: datetime, end_date: datetime
    ):
        images = db.search(
            offset=offset,
            limit=limit,
            order_by=order_by,
            order=order,
            start_date=start_date,
            end_date=end_date
        )
        self.sections = []
        current_month = None

        for img in images:
            dt = img["shot_datetime"]
            this_month = dt.month
            if this_month != current_month:
                self.sections.append({"headline": f"{MONTH_NAMES[dt.month]} {dt.year}", "thumbnails": []})
                current_month = this_month
            self.sections[-1]["thumbnails"].append(_process_thumbnail(img))
