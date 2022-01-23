create table if not exists images (
    id serial primary key,
    abspath text not null,
    file_name text not null,
    uuid uuid unique not null,
    thumbnail text not null,
    width_px integer not null,
    height_px integer not null,
    shot_datetime timestamp without time zone,
    camera text
);
