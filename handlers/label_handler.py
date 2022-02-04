import os
import sqlite3
from management.label_management import (
    insert_label,
    edit_label_from_image,
    get_labels_from_image,
    delete_label,
)
from flask import request, session, Blueprint, Response

label_handler = Blueprint("label_handler", __name__)


@label_handler.route("/label-image", methods=["POST"])
def label_image() -> Response:
    user = session["user"]
    db_name = request.form["db_name"]
    image_name = request.form["image_name"]
    label = request.form["label"]

    if not user:
        return Response(status=401)
    if not (db_name and image_name and label):
        return Response(status=400)
    try:
        insert_label(user, db_name, image_name, label)
        return Response(status=201)
    except (FileNotFoundError, sqlite3.IntegrityError):
        return Response(status=409)


@label_handler.route("/edit-label", methods=["PUT"])
def rename_label() -> Response:
    user = session["user"]
    db_name = request.form["db_name"]
    image_name = request.form["image_name"]
    new_label = request.form["new_label"]
    old_label = request.form["old_label"]

    if not user:
        return Response(status=401)
    if not (new_label and old_label and image_name and db_name):
        return Response(status=400)
    try:
        edit_label_from_image(user, db_name, image_name, new_label, old_label)
        return Response(status=200)
    except (FileNotFoundError, sqlite3.IntegrityError):
        return Response(status=409)


@label_handler.route("/list-db", methods=["GET"])
def list_labels() -> Response:
    user = session["user"]
    db_name = request.args["db_name"]
    image_name = request.args["image_name"]

    if not user:
        return Response(response=None, status=401)
    if not (db_name and image_name):
        return Response(status=400)
    labels = get_labels_from_image(user, db_name, image_name)
    if len(labels) > 0:
        return Response(response=labels, status=200)
    return Response(response=labels, status=204)


@label_handler.route("/delete-db", methods=["DELETE"])
def unlabel_image() -> None:
    user = session["user"]
    db_name = request.form["db_name"]
    image_name = request.form["image_name"]
    label = request.form["label"]

    if not user:
        return Response(status=401)
    if not (db_name and image_name and label):
        return Response(status=400)
    try:
        delete_label(user, db_name, image_name, label)
        return Response(status=200)
    except (FileNotFoundError, sqlite3.IntegrityError):
        return Response(status=409)
