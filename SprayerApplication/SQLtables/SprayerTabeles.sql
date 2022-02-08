USE sprayCatalog;
CREATE TABLE plant (
    id int,
    name varchar(20),
    primary key (name)
);

CREATE TABLE spray(
    id int,
    name varchar(20),
    Decimal(13,2) price,    
    primary key (name)
);
CREATE TABLE SpraySafe(
    int sprayId,
    int plantId,
    int rating,
    Decimal(15,4) concentration,
    foreign key sprayId references spray sprayId,
    primary key (sprayId, cropId)
)
