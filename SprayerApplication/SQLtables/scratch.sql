Use SprayCatalog
Select name from  plant;
select name from  spray;
select a.sprayName, a.plantName from SprayData as a, SprayData as b where a.plantName=b.plantName and a.sprayName =b.sprayName and a.safes <> b.safes ;
select a.sprayName, a.plantName, b.plantName from SprayData as b, SprayData as a where a.plantName='durum wheat' and a.safes=true and b.plantName='woolly plantain' and a.sprayName=b.sprayName;
select a.sprayName from SprayData as a, SprayData as b where a.sprayName=b.sprayName and (a.plantName='durum wheat' ) and (b.plantName='woolly plantain' );
select w.plantName from WeedSprayData as w, CropSprayData as c where c.sprayName = w.sprayName and (c.plantName = 'rye' and c.plantName = 'durum wheat');

select a.sprayName from (select sprayName from CropSprayData where plantName ='rye') as a,
                        (select sprayName from CropSprayData where plantName = 'durum wheat') as b
                        where a.sprayName=b.sprayName;
select DISTINCT(sprayName) from CropSprayData where plantName in ('rye','durum wheat') and (plantName in ('rye') or plantName in('durum wheat'));
select plantName from WeedSprayData where sprayName in ('2 4-d amine 4 albaugh','2 4-d amine alligare  llc');
select sprayName from WeedSprayData where sprayName in ('2 4-d amine 4 albaugh','2 4-d amine alligare  llc');
INSERT INTO spray (name,price) values ('old',10.0);

