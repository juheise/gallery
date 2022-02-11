from datetime import datetime

import flask

from gallery.db import persistence as db
from gallery.views.browse import Thumbnails
from gallery.views.details import load_picture, picture_details, replace_tags


db.configure_from_env()
db.initialize()
app = flask.Flask(__name__)


@app.route("/")
def root():
    return flask.redirect("/pictures")


@app.route("/pictures", methods=["GET"])
def browse():

    def optional_date_param(key):
        value = args.get(key, None)
        if not value:
            return None
        return datetime.strptime(value, "%Y-%m-%d")

    args = flask.request.args
    offset = int(args.get("offset", 0))
    limit = int(args.get("limit", 100))
    order_by = args.get("order_by", "shot_datetime")
    order = args.get("order", "desc")
    start_date = optional_date_param("start_date")
    end_date = optional_date_param("end_date")
    return flask.render_template(
        "browse.html",
        thumbnails=Thumbnails(offset, limit, order_by, order, start_date, end_date)
    )


@app.route("/pictures/<uuid>")
def picture(uuid):
    pic = load_picture(uuid)
    return flask.send_file(pic["abspath"], mimetype="image/jpeg")


@app.route("/pictures/<uuid>/thumbnail")
def thumbnail(uuid):
    pic = load_picture(uuid)
    return flask.send_file(pic["thumbnail"], mimetype="image/jpeg")


@app.route("/pictures/<uuid>/details")
def details(uuid):
    pic = picture_details(uuid)
    return flask.render_template("details.html", **{
        "pic": pic,
        "pic_url": pic.pop("pic_url"),
        "set_tags_url": pic.pop("set_tags"),
        "uuid": uuid,
        "tags": pic.pop("tags")
    })


@app.route("/pictures/<uuid>/tags", methods=["POST"])
def set_tags(uuid: str):
    data = flask.request.form
    replace_tags(uuid, data["tags"])
    return flask.redirect(flask.url_for("details", uuid=uuid))
