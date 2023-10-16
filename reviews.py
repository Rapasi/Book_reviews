from sqlalchemy.sql import text
from db import db

def get_list(entries=None, order=None):
    base_sql = "SELECT U.username,R.rating,R.Book_author,R.book_name,R.review_text, R.review_time, U.id, R.id FROM reviews R, users U WHERE U.id=R.user_id and R.visible=TRUE"
    if entries is None and order is None:
        sql = f"{base_sql} ORDER BY R.review_time DESC"
    else:
        if not order:
            sql = f"{base_sql} ORDER BY R.review_time DESC"
        else:
            if order=="book_name" or order=="book_author":
                sql = f"{base_sql} ORDER BY R.{order} ASC"
            else:
                sql = f"{base_sql} ORDER BY R.{order} DESC"

        if entries:
            sql += " LIMIT :limit"
    params = {'limit': entries} if entries else {}
    result = db.session.execute(text(sql), params)
    return result.fetchall()
