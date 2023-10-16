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
            return redirect("/login")   
    return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/login")

@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        new_username = request.form["new_username"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]
        user_role=1
        result = db.session.execute(text("SELECT username FROM users WHERE username=:username"), {"username": new_username})
        existing_user = result.fetchone()
        
        if existing_user:
            return redirect("/create_user")
        
        if new_password != confirm_password:
            return redirect("/create_user")
        
        hash_value = generate_password_hash(new_password)
        
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(text(sql), {"username":new_username, "password":hash_value})
        db.session.execute(text("INSERT INTO roles (role) VALUES (:role)"), {"role":user_role})
        db.session.commit()

        return render_template("new_user.html")

    return render_template("create_user.html")


@app.route("/", methods=["GET", "POST"])
def index():
    show_all =None
    order_option = request.form.get("order_option", None)
    show_all = request.form.get("show_all", None)
    order = None
    if order_option=="name":
        order="name"
    elif order_option=="author":
        order="author"
    elif order_option=="rating":
        order="rating" 
    if show_all:
        session["show_all"] = not session.get("show_all", False)
    entries=None 
    if not session.get("show_all", False):
        entries = 5
    reviews = get_list(entries, order)
    for review in reviews:
        print(review,'\n')
    return render_template("index.html", messages=reviews)

@app.route("/new")
def new():
    allow = False
    try:
        if users.is_admin():
            allow = True
        elif users.is_user():
            allow = True
    except KeyError:
        pass  

    if allow:
        print("Allow")
        return render_template("new.html")
    else:
        error="missing_user"
        print("Not allowed")  
        return render_template("error.html", error=error, error_message="No rights for this page. Please login to add reviews.")

@app.route("/send", methods=["POST"])
def send():
    book_content = request.form.get("book_content")
    book_rating = request.form.get("book_rating")
    author_content = request.form.get("author_content")
    review = request.form.get("free_review")
    if len(review)>500:
        error="over_max_length"
        return render_template("error.html",error=error,error_message="Review is too long. The maximum legth is 500 characters.")
    user_id=session["user_id"]
    now=datetime.now() 
    sql = "INSERT INTO reviews (user_id,review_time,review_text,rating) VALUES (:user_id,NOW(),:review,:book_rating)"
    db.session.execute(text(sql), {"user_id":user_id,"review":review,"book_rating":book_rating})
    db.session.execute(text("INSERT INTO books (name,author) VALUES (:book_content,:author_content)"),{"book_content":book_content,"author_content":author_content})
    db.session.commit()
    return redirect("/")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form.get("query")
        sql = "SELECT r.id, B.name, B.author, r.review_text, r.rating FROM reviews r, books B WHERE B.name ILIKE :query OR B.author ILIKE :query OR r.review_text ILIKE :query"
        search_results = db.session.execute(text(sql), {"query": f"%{query}%"}).fetchall()
        return render_template("search.html", search_results=search_results)
    return render_template("search.html")


@app.route("/delete/<int:review_id>", methods=["POST"])
def delete_review(review_id):

    if "user_id" not in session:
        return redirect("/login") 
    
    result = db.session.execute(text("SELECT user_id FROM reviews WHERE id=:id"), {"id": review_id})
    result = result.fetchone()
    
    if not result or session["user_role"] == 0:
        return redirect("/login")
    
    if session["user_id"] == result[0] or session["user_role"] == 0:
        db.session.execute(text(f"UPDATE reviews SET visible=FALSE WHERE id={review_id};"))
        db.session.commit()

    return redirect("/")

@app.route("/favorite/<int:review_id>", methods=["POST"])
def favorite_review(review_id):
    if "user_id" not in session:
        return "You must be logged in to save a favorite review.", 401

    db.session.execute(text(f"INSERT INTO favorites (user_id, review_id) VALUES ({session['user_id']},{review_id})"))
    db.session.commit()

    return redirect("/")

@app.route("/favorites")
def show_favorites():
    if "user_id" not in session:
        return redirect("/login")
    

    user_id = session["user_id"]
    sql=text(f"""
    SELECT R.id, B.name as book_name, B.author, R.review_text, R.rating, R.review_time 
    FROM reviews R
    INNER JOIN books B ON B.id = R.id
    INNER JOIN favorites f ON f.review_id = R.id
    WHERE f.user_id = {user_id} AND R.visible = TRUE
    """)
    result=db.session.execute(sql)

    messages = result.fetchall()
    return render_template("favorites.html", messages=messages)