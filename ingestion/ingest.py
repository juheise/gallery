import os
from time import strftime
import uuid

from PIL import Image
import exif

import db.persistence as db


INCLUDED_EXIF_ATTRIBUTES = [
    "datetime",
    "model",
#    "gps_latitude",
#    "gps_longitude",
    "pixel_x_dimension",
    "pixel_y_dimension"
]

EXIF_RENAME = {
    "model": "camera",
    "pixel_x_dimension": "width_px",
    "pixel_y_dimension": "height_px",
    "datetime": "shot_datetime"
}

EXIF_CONVERT = {
    "datetime": lambda dt: strftime("dddd-mm-dd HH:MM:ss", dt)
}


def thumbnail_filename(in_path, suffix):
    file_name = os.path.basename(in_path)
    parts = file_name.split(".")
    joined = ".".join(parts[:-1])
    return f"{joined}_thumbnail.{suffix}"


def create_thumbnail(in_path, out_path, size):
    with Image.open(in_path) as img:
        crop_size = min(img.size[0], img.size[1])
        cropped = img.crop((0,0, crop_size, crop_size))
        cropped.thumbnail((size, size))
        cropped.save(out_path, "JPEG")


def create_entry(in_path, thumbnail_path):
    return {
        "abspath": in_path,
        "file_name": os.path.basename(in_path),
        "uuid": uuid.uuid4().hex,
        "thumbnail": thumbnail_path
    }


def add_meta_data(entry):

    with open(entry["abspath"], 'rb') as f:
        img = exif.Image(f)

    # todo: read non-exif metadata

    if not img.has_exif:
        return
    
    for key in INCLUDED_EXIF_ATTRIBUTES:
        try:
            value = getattr(img, key, None)
            if value is None:
                continue
            entry[EXIF_RENAME.get(key, key)] = EXIF_CONVERT.get(key, lambda v: v)(value)
        except Exception as e:
            print(f"warning: cannot read {key} from {entry['abspath']} due to: {e.__class__.__name__}: {e}")


def import_image(in_path, thumbnail_dir, thumbnail_size=128):
    
    thumb_dir = "gallery/static/thumbnails"
    thumb_file = thumbnail_filename(in_path, "jpg")
    create_thumbnail(in_path, os.path.join(thumb_dir, thumb_file), thumbnail_size)

    entry = create_entry(in_path, thumb_file)
    add_meta_data(entry)
    db.insert(entry)

# todo write cli for ingest whole directory....