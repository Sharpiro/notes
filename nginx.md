## basic auth

### setup

```sh
apt install apache2-utils
htpasswd -c /etc/nginx/.htpasswd bro
```

### config

```nginx
location /content {
    root /var/www/;
    try_files $uri $uri/ =404;
    autoindex on;
    auth_basic "Restricted Content";
    auth_basic_user_file /etc/nginx/.htpasswd;
}
```