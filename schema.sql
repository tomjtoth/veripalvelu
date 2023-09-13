create table if not exists users(
    id serial primary key,

    uname text unique not null,
    passw text not null,

    fnames text not null,
    lnames text not null,

    booleans integer not null
);

create table if not exists clinics(
    id serial primary key,
    cname text not null
);

create table if not exists donations(
    id serial primary key,
    user_id integer references users(id) not null,
    clinic_id integer references clinics(id) not null,
    dt date default current_date
);

create table if not exists consumption(
    donation_id integer primary key references donations(id),
    consumable_id integer not null
);

create table if not exists comments(
    donation_id integer primary key references donations(id),
    
    comment text not null
);
