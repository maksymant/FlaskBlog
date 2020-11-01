from flask import url_for, current_app
from app import mail
from flask_mail import Message
from PIL import Image
import secrets
import os


def save_picture(form_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    img = Image.open(form_pic)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''
To reset yo ur password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request - ignore this email
'''
    mail.send(msg)
