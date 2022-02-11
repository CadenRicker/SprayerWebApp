USE SprayCatalog;
drop table SpraySafe;
drop table plant;
drop table spray;

CREATE TABLE plant (
    name varchar(20) UNIQUE,
    crop boolean,
    primary key (name)
);

CREATE TABLE spray(
    name varchar(20) UNIQUE ,
    price Decimal(13,2),
    primary key (name)
);
CREATE TABLE SpraySafe(
    sprayName varchar(20) ,
    plantName varchar(20) ,
    rating  int,
    concentration Decimal(15,4),
    primary key (sprayName, plantName),
    foreign key (sprayName) references spray(name),
    foreign key (plantName) references  plant(name)
);
