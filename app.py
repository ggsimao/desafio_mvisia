import sys
from flask import Flask, g, session
from flask_bcrypt import Bcrypt
from flask_session import Session
from handlers.database_handler import database_handler
from handlers.image_handler import image_handler
from handlers.label_handler import label_handler
from handlers.user_handler import user_handler

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["USERS_DATABASE"] = "./db/users.db"
app.config["SECRET_KEY"] = "woowoowoo".encode("utf-8")
Bcrypt(app)
Session(app)
app.register_blueprint(database_handler)
app.register_blueprint(image_handler)
app.register_blueprint(label_handler)
app.register_blueprint(user_handler)


@app.teardown_appcontext
def close_db(e=None) -> None:
    db = g.pop("user_db", None)

    if db is not None:
        db.close()


if __name__ == "__main__":
    with app.app_context():
        sys.path.append("./handlers/")
        sys.path.append("./management/")

        from management.user_management import init_db

        init_db()

        app.run(port=3000, host="0.0.0.0")
