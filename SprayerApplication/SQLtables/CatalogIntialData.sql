USE SprayCatalog;
delete from SpraySafe where TRUE = TRUE;
delete from plant where TRUE = TRUE;
delete from spray where TRUE = TRUE;

INSERT INTO plant (name, crop) values
('Kentucky Blue Grass',TRUE),
('Barely', TRUE),
('Red Wheat',TRUE),
('Pepper Mint', TRUE),
('Red Clover', TRUE),
('Potatoes',TRUE),
('Alfalfa',TRUE),
('Common Mallow',FALSE),
('Common Fennel', FALSE),
('Gorse',FALSE),
('Italian Arum',FALSE),
('Knapweeds', FALSE),
('Poison Hemlock', FALSE),
('Scotch Broom',FALSE),
('Tansy Ragwort', FALSE),
('Common Teasel',FALSE),
('Thistles',FALSE),
('Spurge Laurel',FALSE),
('Yellow Archangel',FALSE),
('English Ivy', FALSE);
INSERT INTO spray (name, price) VALUES
('Round Up',10)
('Alachlor',3)
('Bensulide',3)
Bentazon
Benefiin
Bicyclopyrone
Suppress EC
Suppress EC


('2 4-D Amine 4',5);

