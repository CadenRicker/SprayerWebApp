Drop Database if Exists SprayCatalog;
Create Database SprayCatalog;
USE SprayCatalog;


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
    pintsPerAcre DECIMAL(15,4),
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
CREATE TABLE users(
    username varchar(40) NOT NULL,
    passwd varchar(20) NOT NULL,
    PRIMARY KEY (username)
);
DELIMITER //
create procedure addSpray(sprayName varchar(40), sprayPrice Decimal(13,2)) Begin
    Start Transaction;
        insert into spray (name,price) values (sprayName,sprayPrice);
    commit;
end//
create procedure addCropToSpray( nameOfPlant varchar(30),nameOfSpray varchar(40), ppa Decimal(15,4))Begin
    Start Transaction;
        insert into CropSprayData (plantName,sprayName,pintsPerAcr) values (nameOfPlant,nameOfSpray,ppa);
    commit;
end//

create procedure addWeedToSpray( nameOfPlant varchar(30),nameOfSpray varchar(40))Begin
    Start Transaction;
        insert into WeedSprayData (plantName,sprayName) values (nameOfPlant,nameOfSpray);
    commit;
end//
DELIMITER ;