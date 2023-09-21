from sqlalchemy.sql import text
from db import db
def get_list(entries=None):
    if entries is None:
        sql = f"SELECT U.username,R.rating,R.Book_author,R.book_name,R.review_text, R.review_time FROM reviews R, users U ORDER BY R.review_time DESC"
        result = db.session.execute(text(sql))   
    else:
        sql = f"SELECT U.username,R.rating,R.Book_author,R.book_name,R.review_text, R.review_time FROM reviews R, users U ORDER BY R.review_time DESC LIMIT :limit"
        result = db.session.execute(text(sql),{'limit':entries})
    return result.fetchall()
