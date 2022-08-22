use portfolio;
create table clients(
id int primary key auto_increment,
clients int(100),
project int (100),
workhour int (100),
award int (100)
);
create table contacts(
id int primary key auto_increment,
namez varchar (50),
subjects varchar(50),
msg varchar (200),
dates varchar (50),
email varchar (20)
);
create table skills(
id int primary key auto_increment,
skill varchar (50),
expert int(100)
);
create table ports(
id int primary key auto_increment,
typew varchar (50),
type1 varchar (50),
namez varchar (80),
image varchar (80),
link varchar (300)
);
Insert into clients value(1,2,4,5,6)