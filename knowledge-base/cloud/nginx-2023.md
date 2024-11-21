#java [[nginx]]
# APP
vscode plugin: remote ssh, nginx config
# 重定向
return
![image-20231001103134403](image-20231001103134403.png)
重定向是客户端的，如果你写 return 301, http://localhost:8088
访问的事客户端的8088，而不是nginx服务器的8088
## 状态码
![[Springboot2023 & Restful api#Status code]]
2XX 成功
301 永久重定向 302 临时重定向
4XX 请求出错
5XX 服务器内部错误
# rewrite
![image-20231001103655172](image-20231001103655172.png)

```json
    location ~ /test.* {
        rewrite ^/test.*$ http://192.168.31.88:88/ break;
    }
```

把 http://192.168.31.88:88/test2 重定向到http://192.168.31.88:88/

last
break

![image-20231001104129495](image-20231001104129495.png)
Nginx rewrite 的last、break、redirect、permanent有四种模式：
last和break 都会跳转的rewrite的地址，区别是:
**last跳转后，会重新发起请求再匹配一次location，而break则只进行跳转，不再重新请求**。
当rewrite后的地址是一个直接可访问的地址时候，二者无区别
==当rewrite后地址是本地地址，需要匹配location再次进行路由的时候，last会进行匹配==，break则直接返回404

---
redirect和permanent都是重定向，区别是:
redirect是302，临时重定向，浏览器每次请求都请求原网址，搜索引擎不会记住新网址，而且还可能认为是作弊

permanent是301，永久重定向，浏览器缓存会记住新网址，当请求原网址，会直接向新网址请求，搜索引擎也会记住新网址。这样就可以减少中间过程，目的只是保留之前被大家熟知的域名

不加last，和break时 当你输入 /old/1.txt 会重写成 /new/1.txt 再重写成 / pages/1.txt
最后输出 this is rewrite test

加了 break时，如图， 不会再去匹url 映射
直接去找 root配的  /home/AdminLTE-3.2.0/new/1.txt

**如果加last**， 不执行余下指令，重新从头匹配， 最后输出 this is rewrite test

```json
location /baidu {  
        proxy_pass http://www.baidu.com;  
        rewrite /baidu / break;  
}
```
会跳转到 http://www.baudu.com/baidu 所以要用rewrite把后面的/baidu去掉
[[nginx#rewrite route to baidu]]
# 动静分离

![image-20231001111115422](image-20231001111115422.png)

例如我们请求 http://ruoyi.tomcat:8002/image/404.png

$url  指的是 /image/404.png -> root 替换后是  /home/www/static/image/404.png

找不到再去找 $url/   -> root 替换后是  /home/www/static/image/404.png/

再找不到转http://localhost:8080/image/404.png

# reload config in docker
docker exec -it nginx nginx -s reload

# !!!proxy_pass http://localhost:80/ vs proxy_pass http://localhost:80

```json
location /baidu/ {
proxy_pass http://localhost:80/;
}
```

location /baidu/    匹配/baidu/a /baidu/b /baidu/ 但是不匹配/baidu
location /baidu  还匹配/baidu 

proxy_pass http://localhost:80/  will remove phrase in location (any path after url will replace location path)
proxy_pass http://localhost:80 will not

- case 1
http://citi/baidu/dest
```json
location /baidu/ {
proxy_pass http://localhost:80/;
}
```

route to http://locahost:80/dest

- case2
http://citi/baidu/dest
```json
location /baidu/ {
proxy_pass http://localhost:80;
}
```

route to http://locahost:80/baidu/dest

# nginx 命令

``systemctl reload nginx``

容器下运行
```sh
# 测试nginx情况
docker exec -it nginx nginx -t

# 打印结果
nginx: configuration file /etc/nginx/nginx.conf test is successful
```
# nginx location
```json
{
	events {}
	http {
		include mine.types;
		server {
			listen 80;
			server_name localhost;
			root /sites/demo;
			location /greet {
				return 200 'hello world';
			}
		}
	}
}
```

## location 匹配方式
```json
	location = /greet #完全匹配 不加等号是前缀匹配 /greet/a /greet/b 都能匹配上
	location ~ /greet[0-9] #正则匹配 匹 /greet0 /greet1 ...	
```