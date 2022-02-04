from flask import current_app, request, session, Blueprint, Response
from management.database_management import (
    init_db,
    rename_db_file,
    get_db_files,
    delete_db_file,
)
from sqlite3 import IntegrityError
from typing import Tuple

database_handler = Blueprint("database_handler", __name__)


@database_handler.route("/create-db", methods=["POST"])
def create_database() -> Response:
    user = session["user"]
    db_name = request.form["db_name"]

    if not user:
        return Response(status=401)
    if not db_name:
        return Response(status=400)
    try:
        init_db(user, db_name)
        return Response(status=201)
    except IntegrityError:
        return Response(status=409)


@database_handler.route("/rename-db", methods=["PUT"])
def rename_database() -> Response:
    user = session["user"]
    new_db_name = request.form["new_db_name"]
    old_db_name = request.form["old_db_name"]
    if not user:
        return Response(status=401)
    if not (new_db_name and old_db_name):
        return Response(status=400)
    try:
        rename_db_file(user, old_db_name, new_db_name)
        return Response(status=200)
    except FileExistsError:
        return Response(status=409)


@database_handler.route("/list-db", methods=["GET"])
def list_databases() -> Response:
    user = session["user"]
    if not user:
        return Response(response=None, status=401)
    filenames = get_db_files(user)
    if len(filenames) > 0:
        return Response(response=filenames, status=200)
    return Response(response=filenames, status=204)


@database_handler.route("/delete-db", methods=["DELETE"])
def delete_database() -> Response:
    user = session["user"]
    db_name = request.form["db_name"]
    if not user:
        return Response(status=401)
    if not db_name:
        return Response(status=400)
    try:
        delete_db_file(user, db_name)
        return Response(status=200)
    except FileNotFoundError:
        return Response(status=409)
