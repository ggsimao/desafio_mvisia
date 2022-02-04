from sqlite3 import IntegrityError
from management.user_management import (
    find_user,
    insert_user,
    update_password,
    update_username,
)
from flask import current_app, request, session, Blueprint, Response
from flask_bcrypt import bcrypt

user_handler = Blueprint("user_handler", __name__)


@user_handler.route("/login", methods=["GET"])
def login() -> Response:
    username = request.args["username"]
    password = request.args["password"]

    user = find_user(username)

    if not user:
        return Response(status=401)
    if not bcrypt.checkpw(password.encode("utf-8"), user[2].encode("utf-8")):
        return Response(status=401)
    session["user"] = username
    return Response(status=200)


@user_handler.route("/register", methods=["POST"])
def register() -> Response:
    username = request.form["username"]
    password = request.form["password"]

    try:
        insert_user(username, password)
        return Response(status=201)
    except IntegrityError:
        return Response(status=409)


@user_handler.route("/edit-username", methods=["PUT"])
def edit_username() -> Response:
    old_username = session["user"]
    new_username = request.form["new_username"]

    if not session["user"]:
        return Response(status=401)
    try:
        update_username(
            old_username,
            new_username,
        )
        return Response(status=200)
    except IntegrityError:
        return Response(status=409)


@user_handler.route("/edit-password", methods=["PUT"])
def edit_password() -> Response:
    username = session["user"]
    new_password = request.form["new_password"]

    if not username:
        return Response(status=401)
    try:
        update_password(
            username,
            new_password,
        )
        return Response(status=200)
    except IntegrityError:
        return Response(status=409)
