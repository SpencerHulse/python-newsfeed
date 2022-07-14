from flask import Blueprint, request, jsonify, session
from app.models import User, Post, Comment, Vote
from app.db import get_db

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/users", methods=["POST"])
def signup():
    data = request.get_json()
    db = get_db()

    try:
        # Attempt to create a new user
        newUser = User(
            username=data["username"], email=data["email"], password=data["password"]
        )

        # Save in the database
        db.add(newUser)
        db.commit()
    except:
        # Insert failed, so rollback the database (remove pending state) and send an error to front end
        db.rollback()
        return jsonify(message="Signup failed"), 500

    # Create session variable stored in g
    # Session requires a secret key, which was created in app/__init__.py
    session.clear()
    session["user_id"] = newUser.id
    session["loggedIn"] = True

    return jsonify(id=newUser.id)


@bp.route("/users/logout", methods=["POST"])
def logout():
    # Remove session variables
    session.clear()
    return "", 204


@bp.route("/users/login", methods=["POST"])
def login():
    data = request.get_json()
    db = get_db()

    try:
        user = db.query(User).filter(User.email == data["email"]).one()
    except:
        return jsonify(message="Incorrect credentials"), 400

    if user.verify_password(data["password"]) == False:
        return jsonify(message="Incorrect credentials"), 400

    session.clear()
    session["user_id"] = user.id
    session["loggedIn"] = True

    return jsonify(id=user.id)


@bp.route("/comments", methods=["POST"])
def comment():
    data = request.get_json()
    db = get_db()

    try:
        # Create a new comment
        newComment = Comment(
            comment_text=data["comment_text"],
            post_id=data["post_id"],
            user_id=session.get("user_id"),
        )

        db.add(newComment)
        db.commit()
    except:
        db.rollback()
        return jsonify(message="Comment failed"), 500

    return jsonify(id=newComment.id)


@bp.route("/posts/upvote", methods=["PUT"])
def upvote():
    data = request.get_json()
    db = get_db()

    try:
        # Create a new vote with the incoming id and session id
        newVote = Vote(post_id=data["post_id"], user_id=session.get("user_id"))

        db.add(newVote)
        db.commit()
    except:
        db.rollback()
        return jsonify(message="Upvote failed"), 500

    return "", 204
