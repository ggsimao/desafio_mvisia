import sqlite3
import os
from base64 import b64encode, b64decode
from PIL import Image

thumbnail_largest_size = 128


def insert_image(user: str, db_name: str, image: Image, name: str) -> None:
    path = "../db/images/" + user + "/" + db_name + ".db"
    if not os.path.exists(path):
        raise FileNotFoundError("Database doesn't exist")
    width, height = image.size
    encoded_image = b64encode(image)

    ratio = max(width, height) / thumbnail_largest_size
    thumb_height = int(height / ratio)
    thumb_width = int(width / ratio)
    image.thumbnail(thumb_width, thumb_height)
    encoded_thumbnail = b64encode(image)

    db = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = db.cursor()
    cur.execute(
        "INSERT INTO images (name, encoded_image, thumbnail) VALUES (?, ?, ?)",
        (name, encoded_image, encoded_thumbnail),
    )
    db.commit()
    db.close()


def get_images(user: str, db_name: str) -> list:
    path = "../db/images/" + user + "/" + db_name + ".db"
    if not os.path.exists(path):
        raise FileNotFoundError("Database doesn't exist")
    db = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = db.cursor()
    images_list = cur.execute("SELECT (name, thumbnail) FROM images").fetchall()
    for image in images_list:
        image[1] = b64decode(image[1])
    db.commit()
    db.close()
    return images_list


def get_image_data(user: str, db_name: str, image_name: str) -> Image:
    path = "../db/images/" + user + "/" + db_name + ".db"
    if not os.path.exists(path):
        raise FileNotFoundError("Database doesn't exist")
    db = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = db.cursor()
    image = cur.execute("SELECT (name, encoded_image) FROM images").fetchone()
    image[1] = b64decode(image[1])
    db.commit()
    db.close()
    return image


def remove_image(user: str, db_name: str, image_name: str) -> None:
    path = "../db/images/" + user + "/" + db_name + ".db"
    if not os.path.exists(path):
        raise FileNotFoundError("Database doesn't exist")
    db = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = db.cursor()
    image_id = cur.execute(
        "SELECT id FROM images WHERE name = ?", (image_name,)
    ).fetchone()
    cur.execute("DELETE FROM labels WHERE image_id = ?", (image_id,))
    cur.execute("DELETE FROM images WHERE name = ?", (image_name,))
    db.commit()
    db.close()
