# Deploying the Gallery

## NAS Samba Share

Create directory for the share
```
sudo mkdir -p /mnt/my-server/pictures
```

`/etc/fstab` entry:

```
//mycloudex2ultra/Bilder  /mnt/my-server/pictures  cifs  uid=gallery,credentials=/home/gallery/.smbcredentials,iocharset=utf8 0 0
```

Perform mount (one-time only, should auto-mount after reboot):

```
sudo mount -a
```

## Postgres Setup

### Create Database

```
gallery@ubuntu:~$ sudo su postgres
postgres@ubuntu:/home/gallery$ psql
psql (13.5 (Ubuntu 13.5-0ubuntu0.21.04.1))
Type "help" for help.

postgres=# create user gallery;
CREATE ROLE
postgres=# create database gallery;
CREATE DATABASE
postgres=# alter database gallery owner to gallery;
ALTER DATABASE
postgres=# grant all on database gallery to gallery;
```


## Webserver Setup

### uWSGI

```
sudo apt-get install -y build-essential python-dev
```
