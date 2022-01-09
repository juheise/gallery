from flask import url_for


def fetch_thumbnails():
    return [
        {
            "headline": "1. Januar",
            "thumbnails": [
                {
                    "uri": url_for('static', filename='pictures/20201223_130902_001_thumb128.jpg'),
                    "details": url_for("static", filename="pictures/20201223_130902_001.jpg")
                },
                {
                    "uri": url_for('static', filename='pictures/20201223_130902_001_thumb128.jpg'),
                    "details": url_for("static", filename="pictures/20201223_130902_001.jpg")
                }
            ]
        },
        
    ]
