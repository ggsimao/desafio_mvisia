import sqlite3
import os
from flask import g, current_app
from flask_bcrypt import bcrypt


def get_db():
    if "user_db" not in g:
        g.user_db = sqlite3.connect(
            current_app.config["USERS_DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )

    return g.user_db


def init_db() -> None:
    db = get_db()

    if not os.path.exists("./db/images"):
        os.mkdir("./db/images")

    with current_app.open_resource("./db/schemas/schema_users.sql") as f:
        db.executescript(f.read().decode("utf8"))

    db.close()


def insert_user(username: str, password: str) -> None:
    con = get_db()
    cur = con.cursor()
    pw_hash = bcrypt.hashpw(password.encode("utf-8"))
    cur.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)", (username, pw_hash)
    )
    con.commit()
    con.close()
    os.mkdir("./db/images/" + username)


def update_username(old_username: str, new_username: str) -> None:
    con = get_db()
    cur = con.cursor()
    cur.execute(
        "UPDATE users SET username = ? WHERE username = ?",
        (new_username, old_username),
    )
    con.commit()
    con.close()
    os.rename("./db/images/" + old_username, "./db/images/" + new_username)


def update_password(username: str, new_password: str) -> None:
    con = get_db()
    cur = con.cursor()
    pw_hash = bcrypt.hashpw(new_password.encode("utf-8"))
    cur.execute(
        "UPDATE users SET password = ? WHERE username = ?",
        (pw_hash, username),
    )
    con.commit()
    con.close()


def find_user(username: str):
    con = get_db()
    cur = con.cursor()
    user = cur.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    con.close()
    return user
