# Deploying the Gallery

## NAS Samba Share

Create directory for the share
```
sudo mkdir -p /mnt/mycloudex2ultra/bilder
```

`/etc/fstab` entry:

```
//mycloudex2ultra/Bilder  /mnt/mycloudex2ultra/bilder  cifs  uid=gallery,credentials=/home/juheise/.smbcredentials,iocharset=utf8 0 0
```

Perform mount (one-time only, should auto-mount after reboot):

```
sudo mount -a
```

## Postgres Setup

### Create Database

```
juheise@ubuntu:~$ sudo su postgres
postgres@ubuntu:/home/juheise$ psql
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
