from flask import Blueprint, render_template, request, jsonify, flash
from flask_login import login_required, current_user
from .database import db

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/chats/<int:id>', methods=["GET", "POST"])
@login_required
def chat(id=None):
    if request.method == "POST":
        content = request.form.get("content")
        db.send_message(current_user.id, id, content)

    messages = db.get_messages(current_user.id, id)
    return render_template("chat.html", messages=messages, user=current_user)


@views.route('/friends')
@login_required
def friends():
    user_friends = db.friends_of(current_user.id)
    return render_template("friends.html", user=current_user, user_friends=user_friends)


@views.route('/find_friends', methods=["GET", "POST"])
@login_required
def find_friends():
    if request.method == "POST":
        friend_id = int(request.form.get("friend_id"))
        db.follow(current_user.id, friend_id)

    return render_template("find_friends.html", user=current_user, users=db.all_users())
