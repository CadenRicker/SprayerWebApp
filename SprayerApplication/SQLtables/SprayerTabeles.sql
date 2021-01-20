USE sprayCatalog;
CREATE TABLE Crop(
    id int,
    name varchar(20),
    primary key (name)
);
CREATE TABLE weed(
    id int,
    name varchar(20),
    primary key (name)
);
CREATE TABLE spray(
    id int,
    name varchar(20),
    primary key (name)
);
CREATE TABLE SpraySafe(
    int sprayId,
    int cropId,
    foreign key sprayId references spray sprayId,
    primary key (sprayId, cropId)
)
