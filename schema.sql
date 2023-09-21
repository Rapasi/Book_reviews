CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role INTEGER
);
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    book_name TEXT,
    book_author TEXT,
    user_id INTEGER REFERENCES users,
    review_time TIMESTAMP,
    review_text TEXT,
    rating INTEGER
);