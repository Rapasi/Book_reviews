from app import app
from flask import render_template
from datetime import datetime
from flask import redirect, render_template, request, session, flash
from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
import users
from reviews import get_list



@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not users.login(username,password):
            flash("Username does not exist")
            return redirect("/login")   
    return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/login")

@app.route("/create_user", methods=['GET', 'POST'])
def create_user():
    if request.method == "POST":
        new_username = request.form["new_username"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]
        user_role=1
        result = db.session.execute(text("SELECT username FROM users WHERE username=:username"), {"username": new_username})
        existing_user = result.fetchone()
        
        if existing_user:
            flash("Username already exists")
            return redirect("/create_user")

        if new_password != confirm_password:
            flash("Passwords do not match")
            return redirect("/create_user")
        
        # Hash the password before storing it (use a strong hash function like bcrypt)
        hash_value = generate_password_hash(new_password)
        
        sql = "INSERT INTO users (username, password,role) VALUES (:username, :password,:role)"
        db.session.execute(text(sql), {"username":new_username, "password":hash_value,"role":user_role})
        db.session.commit()

        return redirect('/')

    return render_template('create_user.html')


@app.route("/")
def index():
    result = db.session.execute(text("SELECT * FROM reviews"))
    reviews = result.fetchall()
    return render_template("index.html", count=len(reviews), messages=get_list()) 

@app.route("/new")
def new():
    allow = False
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    book_content = request.form.get("book_content")
    book_rating = request.form.get("book_rating")
    author_content = request.form.get("author_content")
    review = request.form.get("free_review")
    user_id=session["user_id"]
    now=datetime.now() 
    sql = "INSERT INTO reviews (book_name,book_author,user_id,review_time,review_text,rating) VALUES (:book_content, :author_content,:user_id,NOW(),:review,:book_rating)"
    db.session.execute(text(sql), {"book_content":book_content,"author_content":author_content,"user_id":user_id,"review":review,"book_rating":book_rating})
    db.session.commit()
    return redirect("/")