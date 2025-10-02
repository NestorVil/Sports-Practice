CREATE TABLE sports (
    id serial PRIMARY KEY,
    "name" varchar(20) NOT NULL UNIQUE,
    is_active BOOLEAN NOT NULL
);


INSERT INTO sports ("name", is_active) VALUES 
    ('Soccer', false), 
    ('Basketball', false),
    ('American Football', false),
    ('Baseball', false),
    ('Cricket', false),
    ('Hockey', false),
    ('Volleyball', false),
    ('Rugby', false),
    ('Rowing', false),
    ('Softball', false),
    ('Lacrosse', false)
;