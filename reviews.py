from sqlalchemy.sql import text
from db import db
from flask import session

def get_list(entries=None, order=None):
    current_user_id=session["user_id"]
    base_sql = f"""SELECT 
    U.username,
    R.rating,
    B.author,
    B.name,
    R.review_text, 
    R.review_time, 
    U.id, 
    R.id,
    CASE WHEN F.user_id IS NOT NULL THEN TRUE ELSE FALSE END AS is_favorite
FROM reviews R
JOIN users U ON U.id = R.user_id
JOIN books B ON R.id = B.id
LEFT JOIN favorites F ON R.id = F.review_id AND F.user_id = {current_user_id}
WHERE R.visible = TRUE"""
    if entries is None and order is None:
        sql = f"{base_sql} ORDER BY R.review_time DESC"
    else:
        if not order:
            sql = f"{base_sql} ORDER BY R.review_time DESC"
        else:
            if order=="name" or order=="author":
                sql = f"{base_sql} ORDER BY B.{order} ASC"
            else:
                sql = f"{base_sql} ORDER BY R.{order} DESC"

        if entries:
            sql += " LIMIT :limit"
    params = {'limit': entries} if entries else {}
    result = db.session.execute(text(sql), params)
    return result.fetchall()

