from flask import Flask, render_template

from gallery.views.browse import fetch_thumbnails


app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("browse.html", sections=fetch_thumbnails())
