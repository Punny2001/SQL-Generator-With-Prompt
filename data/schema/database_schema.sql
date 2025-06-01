CREATE TABLE netflix_titles (
    show_id VARCHAR(256) NOT NULL,
    "type" VARCHAR(256),
    title VARCHAR(256),
    director VARCHAR(256),
    "cast" TEXT,
    country VARCHAR(256),
    date_added DATE,
    release_year INT,
    rating VARCHAR(256),
    duration VARCHAR(256),
    listed_in VARCHAR(256),
    "description" TEXT 
)