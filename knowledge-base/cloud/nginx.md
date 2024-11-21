## start
[[docker & k8s#1、centos下安装docker]]  [[docker2023]]
```shell
docker run --name nginx -d -p 88:80 --restart always -v /home/hg26502/nginx:/usr/share/nginx/html nginx:latest

```
## conf
```shell
mkdir /home/hg26502/nginx/conf/
docker cp nginx:/etc/nginx/ /home/hg26502/nginx/conf/
```

## rerun
```shell
docker rm -f nginx
docker run --name nginx -d -p 88:80 --restart always -v /home/hg26502/nginx:/usr/share/nginx/html \
-v /home/hg26502/nginx/conf/nginx:/etc/nginx nginx:latest
```

## conf
```shell
/etc/nginx/nginx.conf
```
## stop start
```shell
docker start nginx
docker stop nginx

```

## host

```shell
#cd C:\Windows\System32\drivers\etc
#hosts

192.168.31.80 hg.com
```

### proxy nginx

#### hg.com:82 will route to 3 nginx machines
```shell
server {
    listen       80;
    server_name  localhost;
    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}

upstream hello {
    server 192.168.31.80:88;
    server 192.168.31.81:88;
    server 192.168.31.82:88;
}

server {
    listen       82;
    server_name  hg.com;
    location / {
        proxy_pass http://hello;
    }

}

```
#### rewrite route to baidu
```shell
server {
    listen       82;
    server_name  hg.com;

    #access_log  /var/log/nginx/host.access.log  main;

    location / {
        proxy_pass http://hello;
    }

    location /baidu {
        proxy_pass http://www.baidu.com;
        rewrite /baidu / break;
    }

}

```

### map
```shell
# request method = GET, the trade_host= tpsc-query-trade-api-......
# other cases trade_host=$host

map $request_method $trade_host {
	GET tpsc-query-trade-api-......
  default $host
}
```
if $request_method=GET， $trade_host=tpsc-query-trade-api-......
other cases, $trade_host = $host
