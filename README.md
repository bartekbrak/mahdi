# Mahdi

## About

Mahdi is a k2 infrastructure resources monitor. It aims to visually display
realtime data about various servers like disk usage, pko publisher statuses and
more. It consists of two parts:

* simple backend server `server.py` based on a microframework bottle.py to be run on a
  computer with ssh access to queried servers.
* html/javascript frontend `mahdi.html` periodically communicating with the
  backend via jsonp. It's designed tor un on 1920x1080 display called `monitor`.

The repository address is [http://rhodecode.monitor/mahdi](http://rhodecode.monitor/mahdi)

## Setup

### Backend

Ther server has only one dependency `bottle` which can be obtained via pip.
Version does not matter - we don't use anything fancy.

The preferable and tested setup is to setup nginx and proxy traffic to the 8080
port.

* Here's sample nginx config file:

```nginx
# cat /etc/nginx/sites-available/010-bottle
upstream mahdi {
    server 127.0.0.1:8080;
}

server {
    listen 80;
    server_name mahdi.backend;
    access_log      /var/log/nginx/mahdi.access.log;
    error_log       /var/log/nginx/mahdi.error.log;

    location / {
        try_files   $uri    @mahdi;
    }

    location @mahdi {
        proxy_pass      http://mahdi;
    }
}
```

* enable it in nginx and restart:

```bash
sudo su
cd /etc/nginx/sites-enabled
ln -s /etc/nginx/sites-available/010-bottle .
service nginx restart
```

* run server.py anywhere and nginx will proxy the traffic there.
* add `127.0.0.0 mahdi.backend` to /etc/hosts
* visit [http://mahdi.backend](http://mahdi.backend) and README.html will be served to you

### Frontend

Only `mahdi.html` and `js/jquery.knob.js` are needed to run the frontend. They
can be either copied to the display machine or the whole repo can be cloned.
Configure the backend address in config.js and then simply open the page in
fullscreen mode.

There's more than one way to skin a cat and I'm sure soon enough someone will
start complaing about the interface html design philosphy. That's fine. You
can change it but trust me, `position: fixed` makes things a lot easier.

## Varia

* Don't try to rename server.py, to bottle.py.
