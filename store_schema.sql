PRAGMA foreign_keys=off;

DROP TABLE IF EXISTS user;
CREATE TABLE user (
  username        varchar(50) not null PRIMARY KEY,
  fname           varchar(50) not null,
  lname           varchar(50) not null,
  password        varchar(50) not null
);

DROP TABLE IF EXISTS product;
CREATE TABLE product (
  id          int(32) not null PRIMARY KEY,
  name        varchar(50) not null,
  cost        int(50) not null, 
  stock       int(3) not null, 
  category    varchar(32) not null
);

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
  order_id    int(32) not null,
  product_id  int(32) not null,
  qty         int(3) not null,
  username    varchar(50) not null,
  date        varchar(50) not null,
  price       int(50) not null, 
  PRIMARY KEY(order_id, product_id),
  FOREIGN KEY (username) REFERENCES user(username)
);

PRAGMA foreign_keys=on;

INSERT INTO user VALUES('testuser', 'test','user', 'testpass');
INSERT INTO product VALUES(1, 'Holly Wood Wand, 11 inches, Pheonix Feather Core',7, 12, 'Wands');
INSERT INTO product VALUES(2, 'Vine Wood Wand, 10 3/4 inches, Dragon Heart String Core',7, 13, 'Wands');
INSERT INTO product VALUES(3, 'Willow Wood Wand, 14 inches, Unicorn Hair Core',7, 12, 'Wands');
INSERT INTO product VALUES(4, 'Hawthorn Wood Wand, 10 inches, Unicorn Hair Core',7, 13, 'Wands');
INSERT INTO product VALUES(5, 'The Niffler',20, 13, 'Magical Creatures');
INSERT INTO product VALUES(6, 'Hippogriff',25, 14, 'Magical Creatures');
INSERT INTO product VALUES(7, 'Thestral',40, 15, 'Magical Creatures');
INSERT INTO product VALUES(8, 'Basilisk',5000, 11, 'Magical Creatures');
INSERT INTO product VALUES(9, 'Felix Felicis',4, 16, 'Potions');
INSERT INTO product VALUES(10, 'Amortentia',5, 13, 'Potions');
INSERT INTO product VALUES(11, 'Polyjuice Potion',6, 14, 'Potions');
INSERT INTO product VALUES(12, 'Veritaserum',8, 12, 'Potions');