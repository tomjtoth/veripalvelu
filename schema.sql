create table if not exists users(
    id serial primary key,

    first_names text not null,
    last_names text not null,

    -- 0: donor, 1: admin
    spec_roles integer not null,
);

create table if not exists donor_info(
    donor_id serial primary key references users(id),

    -- 0:0, A:1, B:2, AB:3
    AB integer not null,

    -- 0: neg, 1: pos
    RH integer not null,

    -- 0: women, 1: men
    gender integer not null
);

create table if not exists clinics(
    id serial primary key,
    place_name text not null
);

create table if not exists donations(
    id serial primary key,
    donor_id integer references users(id) not null,
    clinic_id integer references clinics(id) not null,
    dt date default current_date
);

create table if not exists consumption(
    donation_id integer primary key references donations(id),
    consumable_id integer not null
);

create table if not exists comments(
    id serial primary key,
    donation_id integer references donations(id),
    
    comment text not null
);

create table if not exists photos(
    id serial primary key,
    donation_id integer references donations(id),

    photo blob not null
);
