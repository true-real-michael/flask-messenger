import json

from flask import Blueprint, render_template, request, jsonify, flash
from flask_login import login_required, current_user
from datetime import datetime

# from .models import User, friendship, Chat
from .database import models

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # if request.method == 'POST':
    #     note_data = request.form.get('note')
    #     if note_data != '':
    #         new_note = Note(note_data=note_data,
    #                         note_date=datetime.now(),
    #                         user_id=current_user.id)
    #         db.session.add(new_note)
    #         db.session.commit()

    return render_template("home.html", user=current_user)


# @views.route('/chats/<int:id>', methods=["GET", "POST"])
# @login_required
# def chat(id=None):
#     chat_val = Chat.query.filter_by()
#     return render_template("chat.html", messages=messages)
#
#
@views.route('/friends')
@login_required
def friends():
    return render_template("friends.html", user=current_user)


@views.route('/find_friends', methods=["GET", "POST"])
@login_required
def find_friends():
    if request.method == "POST":
        friend_id = int(request.form.get("friend_id"))
        current_user.befriend(models.find_user_by_id(friend_id))

    return render_template("find_friends.html", user=current_user, users=models.all_users())

# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     data = json.loads(request.data)
#     noteId = data['noteId']
#     note = Note.query.get(noteId)
#     if note and current_user.id == note.user_id:
#         db.session.delete(note)
#         db.session.commit()
#
#     return jsonify({})
