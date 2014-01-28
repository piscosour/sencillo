drop table if exists users;
create table user (
	id integer primary key autoincrement,
	username text not null,
	password text not null,
	email text not null,
	phone text
);
drop table if exists payments;
create table payments (
	id integer primary key autoincrement,
	sender text not null,
	recipient text not null,
	amount integer not null,
	timestamp text not null,
	description text
);
