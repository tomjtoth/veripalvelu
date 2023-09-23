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
    consumable_id integer references consumables(id)
);

create table if not exists comments(
    donation_id integer references donations(id),
    comment text not null
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
    return concat(
        case 
            when male
                then 'male'
                else 'female'
        end
    );
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
    select ($1 >> 2) & 1 = 1 into a;
    select ($1 >> 1) & 1 = 1 into b;
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
    is_admin(booleans),
    sex(booleans),
    blood_type(booleans),
    string_agg(consumable, ', ') as consumption,
    comment
from donations d
inner join users u on u.id = d.user_id
inner join clinics cli on cli.id = d.clinic_id
left join consumption con1 on con1.donation_id = d.id
left join consumables con2 on con2.id = con1.consumable_id
left join comments com on com.donation_id  = d.id
group by d.id, cli.id, cli.cname, u.id, fnames, lnames, booleans, com.comment
order by ddate desc
;

