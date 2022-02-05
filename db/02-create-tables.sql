create table if not exists gallery.images (
    id serial primary key,
    abspath text not null,
    file_name text not null,
    uuid uuid unique not null,
    thumbnail text not null,
    width_px integer not null,
    height_px integer not null,
    shot_datetime timestamp without time zone,
    camera text,
    hash_hex text unique,
    hash_algo text
);


create table if not exists gallery.tags (
    id serial primary key,
    tag text not null unique
);


create table if not exists gallery.tags_images_assoc (
    tag_id integer references gallery.tags(id),
    image_id integer references gallery.images(id),
    primary key (tag_id, image_id)
);
