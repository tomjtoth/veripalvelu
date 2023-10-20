create table if not exists users(
    id serial primary key,

    uname varchar(16) unique not null,
    passw text not null,

    fnames varchar(100) not null,
    lnames varchar(100) not null,

    flags integer not null
);

create table if not exists clinics(
    id serial primary key,
    cname text unique not null
);

create table if not exists consumables(
    id serial primary key,
    consumable text unique not null
);

create table if not exists donations(
    id serial primary key,
    user_id integer references users(id) not null,
    clinic_id integer references clinics(id) not null,
    ddate date default current_date
);

create table if not exists consumption(
    donation_id integer references donations(id),
    consumable_id integer references consumables(id),
    consumed_qty integer default 0
);

create table if not exists comments(
    donation_id integer references donations(id),
    comment varchar(5000) not null
);

CREATE or replace FUNCTION is_admin(integer)
RETURNS boolean
    AS 'select ($1 >> 4) & 1 = 1;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;

create or replace function sex(int)
returns text
language plpgsql
as
$$
declare
    male boolean;
begin
    select ($1 >> 3) & 1 = 1 into male;
    return case
            when male
            then 'mies'
            else 'nainen'
    end;
end;
$$;

create or replace function blood_type(int)
returns text
language plpgsql
as
$$
declare
    a boolean;
    b boolean;
    rh boolean;
begin
    select ($1 >> 2) & 1 = 1 into b;
    select ($1 >> 1) & 1 = 1 into a;
    select $1 & 1 = 1 into rh;
    return concat(
        case
            when a and b then 'AB'
            when a then 'A'
            when b then 'B'
            else '0'
        end,
        case when rh then '+' else '-' end
    );
end;
$$;

create or replace view data as
select
    ddate as date,
    cli.id as clinic_id,
    cli.cname as clinic,
    u.id as user_id,
    fnames,
    lnames,
    is_admin(flags),
    sex(flags),
    blood_type(flags),
    comment
from donations d
inner join users u on u.id = d.user_id
inner join clinics cli on cli.id = d.clinic_id
left join comments com on com.donation_id  = d.id
order by ddate desc
;

create or replace view raw_consumption as
select
    user_id,
    ddate,
    c2.consumable,
    consumed_qty
from consumption c
inner join consumables c2 on c.consumable_id = c2.id
inner join donations d on d.id = c.donation_id
;