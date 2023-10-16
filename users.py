import os
from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

def login(name, password):
    sql = "SELECT u.id,u.password,r.role FROM users u, roles r WHERE u.username=:username"
    result = db.session.execute(text(sql), {"username":name})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user[1], password):
        return False
    session["user_id"] = user[0]
    session["user_name"] = name
    session["user_role"] = user[2]
    session["csrf_token"] = os.urandom(16).hex()
    return True

def logout():
    del session["user_id"]
    del session["user_name"]
    del session["user_role"]

def is_admin():
    try:
        return (session["user_role"] is 0)
    except KeyError:
        return False

def is_user():
    try:
        return (session["user_role"] is 1)
    except KeyError:
        return False


def user_id():
    try:
        return session["user_id"]
    except KeyError:
        return False