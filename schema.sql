CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    role INTEGER
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role_id INTEGER REFERENCES roles
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    name TEXT,
    author TEXT
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    review_time TIMESTAMP,
    review_text TEXT,
    rating INTEGER,
    visible BOOLEAN DEFAULT TRUE
);

CREATE TABLE favorites (
    user_id INTEGER REFERENCES users,
    review_id INTEGER REFERENCES reviews,
    PRIMARY KEY (user_id, review_id)
);

