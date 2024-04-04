from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """return a list with all the images"""
    if data:
        return jsonify(data), 200
    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    found_image = find_image_by_id(id)
    if data and found_image:
        return jsonify(found_image[0]), 200 
    return {"message": "not-found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    if data:
        picture = request.json
        found_image = find_image_by_id(picture['id'])
        if not found_image:
            data.append(picture)
            return jsonify(picture), 201
        return {"Message": f"picture with id {picture['id']} already present"}, 302
    return {"message": "Internal server error"}, 500

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    if data:
        picture = request.json
        found_image = find_image_by_id(picture['id'])
        if found_image:
            data.remove(found_image[0])
            data.append(picture)
            return jsonify(picture), 200
        return {"message": "picture not found"}, 404
    return {"message": "Internal server error"}, 500

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    if data:
        found_image = find_image_by_id(id)
        if found_image:
            data.remove(found_image[0])
            return jsonify(found_image), 204
        return {"message": "picture not found"}, 404
    return {"message": "Internal server error"}, 500

def find_image_by_id(id):
    return [image for image in data if image['id'] == id]