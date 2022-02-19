USE SprayCatalog;
drop table SprayData;
drop table plant;
drop table spray;

CREATE TABLE plant (
    name varchar(30) UNIQUE,
    crop boolean,
    primary key (name)
);

CREATE TABLE spray(
    name varchar(30) UNIQUE ,
    price Decimal(13,2),
    primary key (name)
);
CREATE TABLE SprayData(
    sprayName varchar(30) ,
    plantName varchar(30) ,
    rating  int,
    safes BOOLEAN,
    concentration Decimal(15,4),
    gallonsPerAcr DECIMAL(15,4),
    primary key (sprayName, plantName),
    foreign key (sprayName) references spray(name),
    foreign key (plantName) references  plant(name)
);
