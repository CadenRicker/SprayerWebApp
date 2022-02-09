USE SprayCatalog;
drop table SpraySafe;
drop table plant;
drop table spray;

CREATE TABLE plant (
    id int(11) NOT NULL UNIQUE ,
    name varchar(20),
    primary key (id)
);

CREATE TABLE spray(
    id int (11)NOT NULL UNIQUE ,
    name varchar(20),
    price Decimal(13,2),
    primary key (id)
);
CREATE TABLE SpraySafe(
    sprayId int(11) NOT NULL ,
    plantId int(11) NOT NULL ,
    rating  int,
    concentration Decimal(15,4),
    primary key (sprayId, plantId),
    foreign key (sprayId) references spray(Id),
    foreign key (plantId) references  plant(Id)

);
