import os
import sqlite3
from management.image_management import (
    insert_image,
    get_images,
    remove_image,
    get_image_data,
)
from flask import request, session, Blueprint, Response
from PIL import Image

image_handler = Blueprint("image_handler", __name__)


@image_handler.route("/upload-image", methods=["POST"])
def upload_image() -> Response:
    user = session["user"]
    db_name = request.form["db_name"]
    image = Image.frombytes(request.form["image"])
    image_name = request.form["image_name"]

    if not user:
        return Response(status=401)
    if not (db_name and image and image_name):
        return Response(status=400)
    try:
        insert_image(user, db_name, image, image_name)
        return Response(status=201)
    except FileNotFoundError:
        return Response(status=409)


@image_handler.route("/list-images", methods=["GET"])
def list_images() -> Response:
    user = session["user"]
    db_name = request.args["db_name"]

    if not user:
        return Response(response=None, status=401)
    if not db_name:
        return Response(response=None, status=400)
    try:
        images = get_images(user, db_name)
        if len(images) > 0:
            return Response(response=images, status=200)
        return Response(response=images, status=204)
    except FileNotFoundError:
        return Response(response=None, status=409)


@image_handler.route("/get-image", methods=["GET"])
def get_image() -> Response:
    user = session["user"]
    db_name = request.args["db_name"]
    image_name = request.args["image_name"]

    if not user:
        return Response(response=None, status=401)
    if not (db_name and image_name):
        return Response(response=None, status=400)
    try:
        image = get_image_data(user, db_name, image_name)
        return Response(response=image, status=200)
    except FileNotFoundError:
        return Response(response=None, status=409)


@image_handler.route("/delete-image", methods=["DELETE"])
def delete_image() -> Response:
    user = session["user"]
    db_name = request.form["db_name"]
    image_name = request.form["image_name"]

    if not user:
        return Response(status=401)
    if not db_name or not image_name:
        return Response(status=400)
    try:
        remove_image(user, db_name, image_name)
        return Response(status=200)
    except (FileNotFoundError, sqlite3.IntegrityError):
        return Response(status=409)
