import sqlite3
import os


def insert_label(user: str, db_name: str, image_name: str, label: str) -> None:
    path = "../db/images/" + user + "/" + db_name + ".db"
    if not os.path.exists(path):
        raise FileNotFoundError("Database doesn't exist")

    db = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = db.cursor()

    cur.execute("INSERT OR IGNORE INTO labels name VALUES ?", (label,))
    label_id = cur.execute("SELECT id FROM labels WHERE name = ?", (label,)).fetchone()

    image_id = cur.execute(
        "SELECT id FROM images WHERE name = ?", (image_name,)
    ).fetchone()

    cur.execute(
        "INSERT INTO labeling (image_id, label_id) VALUES (?, ?)",
        (label_id, image_id),
    )
    db.commit()
    db.close()


def edit_label_from_image(
    user: str, db_name: str, image_name: str, new_label: str, old_label: str
) -> None:
    path = "../db/images/" + user + "/" + db_name + ".db"
    if not os.path.exists(path):
        raise FileNotFoundError("Database doesn't exist")

    db = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = db.cursor()

    image_id = cur.execute(
        "SELECT id FROM images WHERE name = ?", (image_name,)
    ).fetchone()

    cur.execute(
        "UPDATE labels SET name = ? WHERE (name, image_id) = (?, ?)",
        (new_label, old_label, image_id),
    )
    db.commit()
    db.close()


def get_labels_from_image(user: str, db_name: str, image_name: str) -> list:
    path = "../db/images/" + user + "/" + db_name + ".db"
    if not os.path.exists(path):
        raise FileNotFoundError("Database doesn't exist")

    db = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = db.cursor()

    image_id = cur.execute(
        "SELECT id FROM images WHERE name = ?", (image_name,)
    ).fetchone()

    label_list = cur.execute(
        "SELECT name FROM labels WHERE image_id = ?", (image_id,)
    ).fetchall()

    db.commit()
    db.close()

    return label_list


def delete_label(user: str, db_name: str, image_name: str, label: str) -> None:
    path = "../db/images/" + user + "/" + db_name + ".db"
    if not os.path.exists(path):
        raise FileNotFoundError("Database doesn't exist")

    db = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = db.cursor()

    image_id = cur.execute(
        "SELECT id FROM images WHERE name = ?", (image_name,)
    ).fetchone()

    cur.execute("DELETE FROM labels WHERE (name, image_id) = (?, ?)", (label, image_id))

    db.commit()
    db.close()
