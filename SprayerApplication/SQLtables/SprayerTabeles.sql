USE SprayCatalog;
drop table CropSprayData;
drop table WeedSprayData;
drop table plant;
drop table spray;

CREATE TABLE plant (
    name varchar(30) UNIQUE,
    crop boolean,
    primary key (name)
);

CREATE TABLE spray(
    name varchar(40) UNIQUE ,
    price Decimal(13,2),
    primary key (name)
);
CREATE TABLE CropSprayData(
    sprayName varchar(40) ,
    plantName varchar(30) ,
    concentration Decimal(15,4),
    gallonsPerAcr DECIMAL(15,4),
    primary key (sprayName, plantName),
    foreign key (sprayName) references spray(name),
    foreign key (plantName) references  plant(name)
);
CREATE TABLE WeedSprayData(
    sprayName varchar(40) ,
    plantName varchar(30) ,
    rating  int,
    primary key (sprayName, plantName),
    foreign key (sprayName) references spray(name),
    foreign key (plantName) references  plant(name)
);
