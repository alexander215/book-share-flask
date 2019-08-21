import models

import os
import sys
import secrets
import PIL import Image

from flask import Blueprint, request, jsonify, url_for, send_file

from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict

user = Blueprint('users', 'user', url_prefix='/user')


@user.route('/register', methods=["POST"])
def register():
    print(request)
    print(type(request))
    pay_file = request.files

    payload = request.form.to_dict()
    dict_file = pay_file.to_dict()

    print(payload)
    print(dict_file)

    payload['email'].lower()
    try:
        models.User.get(models.User.email == payload['email'])
        return jsonify(data={}, status={"code":401, "message": "A user with that name and/or email already exists. Try again."})

    except moodels.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        file_picture_path = save_picture(dict_file['file'])
        payload['photo'] = file_picture_path
