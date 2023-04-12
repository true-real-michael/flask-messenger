import json

from flask import Blueprint, render_template, request, jsonify, flash
from flask_login import login_required, current_user
from datetime import datetime

from .models import User
from .services import db

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


# @views.route('/friends')
# @login_required
# def friends():
#     return render_template("friends.html", user=current_user)


@views.route('/find_friends', methods=["GET", "POST"])
@login_required
def find_friends():
    if request.method == "POST":
        friend = request.form.get("friend")
        friend_if_exists = User.query.filter_by(id=friend).first()
        if friend_if_exists:
            flash("this person is already your friend", category="success")
        else:
            current_user.befriend(friend)


    return render_template("find_friends.html", user=current_user, users=User.query.all())

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
