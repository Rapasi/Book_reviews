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
        print(session['username'])
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

        return render_template('new_user.html')

    return render_template('create_user.html')


@app.route("/", methods=['GET', 'POST'])
def index():
    order_option = request.form.get('order_option', None)
    show_all = request.form.get('show_all', None)
    order = None
    if order_option=="name":
        order="book_name"
    elif order_option=="author":
        order="book_author"
    elif order_option=="rating":
        order="rating" 
    if show_all:
        session['show_all'] = not session.get('show_all', False)
    entries=None 
    if not session.get('show_all', False):
        entries = 5
    reviews = get_list(entries, order)
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
    sql = "INSERT INTO reviews (book_name,book_author,user_id,review_time,review_text,rating) VALUES (:book_content, :author_content,:user_id,NOW(),:review,:book_rating)"
    db.session.execute(text(sql), {"book_content":book_content,"author_content":author_content,"user_id":user_id,"review":review,"book_rating":book_rating})
    db.session.commit()
    return redirect("/")

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        sql = "SELECT id, book_name, book_author, review_text, rating FROM reviews WHERE book_name ILIKE :query OR book_author ILIKE :query OR review_text ILIKE :query"
        search_results = db.session.execute(text(sql), {'query': f"%{query}%"}).fetchall()
        return render_template('search.html', search_results=search_results)
    return render_template('search.html')


@app.route('/delete/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    print(review_id)
    if 'user_id' not in session:
        return redirect("/login") 
    result = db.session.execute(text("SELECT user_id FROM reviews WHERE id=:id"), {"id": review_id})
    result = result.fetchone()
    if not result or session['user_role'] == 0:
        return redirect("/login")
    print(session['user_id'])

    if session['user_id'] == result[0] or session['user_role'] == 0:
        db.session.execute(text(f"UPDATE reviews SET visible=FALSE WHERE id={review_id};"))
        db.session.commit()

    return redirect('/')