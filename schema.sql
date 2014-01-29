drop table if exists users;
create table users (
	id integer primary key autoincrement,
	username text not null,
	password text not null,
	email text not null,
	mobile text,
	credit integer
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
