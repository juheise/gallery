import os
from time import strftime
import uuid
import typing as t

from PIL import Image
import exif
from fs.base import FS

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


def thumbnail_filename(in_path: str, suffix: str) -> str:
    """
    Extract file name from given path and convert into filename for thumbnail image.
    """
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


def create_entry(in_path: str, thumbnail_path: str):
    return {
        "abspath": in_path,
        "file_name": os.path.basename(in_path),
        "uuid": uuid.uuid4().hex,
        "thumbnail": thumbnail_path
    }


def add_meta_data(fs: FS, path: str, entry: t.Dict[str, t.Any]):

    with fs.open(path, 'rb') as f:
        img = exif.Image(f)

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


def import_image(source_fs: FS, in_path: str, thumbnail_fs: FS, thumbnail_size=128):
    
    thumb_file = thumbnail_filename(in_path, "jpg")
    abspath = source_fs.getospath(in_path).decode("utf-8")
    abspath_thumb = thumbnail_fs.getospath(thumb_file).decode("utf-8")

    create_thumbnail(abspath, abspath_thumb, thumbnail_size)
    entry = create_entry(abspath, abspath_thumb)
    add_meta_data(source_fs, in_path, entry)
    db.insert(entry)
    