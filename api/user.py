import models

#for the image upload
import os
import sys
import secrets
from PIL import Image

from flask import Blueprint, request, jsonify, url_for, send_file

from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict

user = Blueprint('users', 'user', url_prefix='/user')

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)

    f_name, f_ext = os.path.splitext(form_picture.filename)

    picture_name = random_hex + f_ext
    file_path_for_avatar = os.path.join(os.getcwd(), 'static/profile_pics/' + picture_name)

    output_size = (100, 150)
    
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(file_path_for_avatar)

    return picture_name

@user.route('/register', methods=["POST"])
def register():
    # print(user, "user (blueprint) in user.py")
    print(request, "request in user")
    print(type(request), "request type in user")

    pay_file = request.files

    payload = request.form.to_dict()
    dict_file = pay_file.to_dict()
    payload['photo'] = 'default'
    print(payload, "payload in user")
    print(dict_file, "dict_file in user")

    payload['email'].lower()
    try:
        models.User.get(models.User.email == payload['email'])
        return jsonify(data={}, status={"code":401, "message": "A user with that name and/or email already exists. Try again."})

    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        file_picture_path = save_picture(dict_file['file'])
        print(file_picture_path, '<-file_picture_path after save_picture')
        payload['photo'] = file_picture_path
        user = models.User.create(**payload)
        
        print(type(user))

        login_user(user)

        current_user.photo = file_picture_path

        user_dict = model_to_dict(user)

        print(user_dict, "user_dict")
        print(type(user_dict), "type of user_dict")

        del user_dict["password"]

        return jsonify(data=user_dict, status={"code": 201, "message": "Success"})

@user.route("/login", methods=["POST"])
def login():
    payload =request.get_json()
    print(payload, "payload in login")
    try:
        user = models.User.get(models.User.email == payload["email"])
        user_dict = model_to_dict(user)
        if (check_password_hash(user_dict["password"], payload["password"])):
            del user_dict["password"]
            login_user(user)
            print(user, "this is user in login route")
            return jsonify(data=user_dict, status={"code":200, "message": "Success"})
        else:
            return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})


