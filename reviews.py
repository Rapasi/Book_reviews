from sqlalchemy.sql import text
from db import db

def get_list(entries=None, order=None):
    base_sql = "SELECT U.username,R.rating,R.Book_author,R.book_name,R.review_text, R.review_time FROM reviews R, users U WHERE U.id=R.user_id"
    if entries is None and order is None:
        sql = f"{base_sql} ORDER BY R.review_time DESC"
    else:
        if order:
            sql = f"{base_sql} ORDER BY R.{order} DESC"
        else:
            sql = f"{base_sql} ORDER BY R.review_time DESC"

        if entries:
            sql += " LIMIT :limit"
    params = {'limit': entries} if entries else {}
    result = db.session.execute(text(sql), params)
    print(sql)
    return result.fetchall()
