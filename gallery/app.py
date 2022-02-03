from flask import Flask, render_template, send_file

from gallery.views.browse import fetch_thumbnails
from gallery.views.details import load_picture


app = Flask(__name__)


@app.route("/pictures")
def browse():
    return render_template("browse.html", sections=fetch_thumbnails())


@app.route("/pictures/<uuid>")
def picture(uuid):
    pic = load_picture(uuid)
    return send_file(pic["abspath"], mimetype="image/jpeg")


@app.route("/pictures/<uuid>/thumbnail")
def thumbnail(uuid):
    pic = load_picture(uuid)
    return send_file(pic["thumbnail"], mimetype="image/jpeg")
