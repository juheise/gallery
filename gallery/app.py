import flask

from gallery.views.browse import fetch_thumbnails
from gallery.views.details import load_picture, picture_details


app = flask.Flask(__name__)


@app.route("/")
def root():
    return flask.redirect("/pictures")


@app.route("/pictures")
def browse():
    return flask.render_template("browse.html", sections=fetch_thumbnails())


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
    pic_url = pic.pop("pic_url")
    return flask.render_template("details.html", pic=pic, pic_url=pic_url)
