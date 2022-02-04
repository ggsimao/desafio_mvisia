import os
import sqlite3
from flask import current_app


def init_db(user, db_name) -> None:
    path = "../db/images/" + user + "/" + db_name + ".db"
    db = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    with current_app.open_resource("../db/schemas/schema_images.sql") as f:
        db.executescript(f.read().decode("utf8"))
    db.close()


def rename_db_file(user: str, old_name: str, new_name: str) -> None:
    new_path = "../db/images/" + user + "/" + new_name + ".db"
    if os.path.exists(new_path):
        raise FileExistsError("Database with the new name already exists")
    old_path = "../db/images/" + user + "/" + old_name + ".db"
    os.rename(old_path, new_path)


def get_db_files(user: str) -> list:
    path = "../db/images/" + user + "/"
    (_, _, filenames) = next(os.walk(path))
    return filenames


def delete_db_file(user: str, db_name: str) -> None:
    path = "../db/images/" + user + "/" + db_name + ".db"
    os.remove(path)
