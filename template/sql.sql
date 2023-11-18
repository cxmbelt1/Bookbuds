CREATE TABLE users
(
    id serial primary key,
    username text unique NOT NULL,
    hash text NOT NULL
);

CREATE TABLE books
(
    id serial primary key,
    isbn char(10) unique NOT NULL,
    title text NOT NULL,
    author text NOT NULL,
    year char(4) NOT NULL
);


CREATE TABLE reviews(
    id serial primary key,
    user_name text references users(username),
    book_id integer references books(id),
    rating integer NOT NULL ,
    comment varchar(1500) NOT NULL,
    timezone timestamptz
);


