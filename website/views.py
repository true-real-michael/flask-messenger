from flask import Blueprint, render_template, request, jsonify, flash
from flask_login import login_required, current_user
from .database import models

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
        models.send_message(current_user.id, id, content)

    messages = current_user.chat_with(id)
    return render_template("chat.html", messages=messages, user=current_user)


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
