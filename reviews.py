from sqlalchemy.sql import text
from db import db
def get_list():
    sql = "SELECT U.username,R.rating,R.Book_author,R.book_name,R.review_text, R.review_time FROM reviews R, users U"
    result = db.session.execute(text(sql))
    return result.fetchall()
