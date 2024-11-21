#basic #java 
 oauth2

# 授权码模式
![[Pasted image 20231209185238.png|800]]

## ==用户去向微信授权服务器发以下请求==
response_type=code返回授权码， response_type=token返回令牌 （简单模式）
scope 权限范围，在授权服务器配置
client_id 客户端id，在授权服务器注册
redirect_uri 重定向uri，授权成功后跳转
![[Pasted image 20231209182304.png]]

->
www.baidu.com/?code=abc123

## ==跳转百度时用户把拿到的授权码给了百度，百度拿着授权码向微信服务器申请token==
![[Pasted image 20231209184258.png]]


百度有了令牌可以拿着token去资源服务器请求资源

资源服务器拿着token只要密钥和微信授权服务器一致就可以把JWT的内容取出并验证


# 简单模式

省去了授权码这一步，客户端登陆微信验证服务器直接请求token，跳转百度时带上
![[Pasted image 20231209184527.png]]

baidu直接拿到token，访问资源服务器时会给传这个token

# 密码模式
![[Pasted image 20231209184754.png|750]]
用户访问百度时，直接把用户名密码给百度，百度拿着用户的name psw直接去授权服务器拿token访问资源服务器

# 客户端模式
![[Pasted image 20231209185022.png|875]]

拿到token后自己去访问