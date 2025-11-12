app定义parent为 spring-boot-starter-parent --> spring-boot-dependencies (bom)

spring-boot-start-web场景启动器
包含了
spring-boot-starter （按需加载auto configure entry）
spring-boot-start-tomcat
spring-web

...
入口
@SpringBootApplication

所有的spring 配置项都和 配置属性类绑定
server.port=8080
```java
@ConfigurationProperties(
    prefix = "server",
    ignoreUnknownFields = true
)
public class ServerProperties {
    private Integer port;
```

# 按需加载
spring-boot-starter  -- spring-boot-autoconfigure
一堆AutoConfiguration

条件注解
@ConditionalOnBean
@ConditionalOnClass
@ConditionalOnProperty

# 属性绑定
@ConfigurationProperties(
    prefix = "server",
    ignoreUnknownFields = true
)
标记类，或者标记@Bean方法

把该class的属性和配置文件的属性绑定

---

@EnableConfigurationProperties(Sheep.class) 开启Sheep的属性绑定，Sheep会自动放入容器中


# AutoConfiguration
@EnableAutoConfiguration 开启自动配置， 把auto config 组件中的配置类自动生效
-》import AutoConfigurationSelector
从meta-info下配置文件  140+ AutoConfiguration class 引入容器
类似 SPI

AutoConfiguration 按需生效（因为有条件注解）
往往和@EnableConfigurationProperties(XXXProperties.class)配合使用

## AutoConfiguration 和 普通Configuration类的区别
AutoConfiguration是对 componentScan屏蔽的，仅被metainfo下的property文件引入，需要配合
ConditionalOnXXX决定是否生效

Configuration类也可以使用ConditionalOnXXX，一般用在@bean方法后面

AutoConfiguration 项目可以吧一些实现的jar包作为compileOnly这样在打包的时候通过了编译，但是打出的jar包中是不带实现的。实际的App如果引入了实现的jar，就通过了ConditionalOnClass的判断，然后成功实现配置。

## 最佳实践
导入场景
spring-boot-starter-XXX

写配置文件

spring autoconfiguration 自动生效了 （免去了你做component scan的污染）

# yaml
![[Pasted image 20250916110414.png|300]]

对象也可以用 {}表示
birthDay可以写成 birth-day
字符串可以用 ‘’ “” 单引号不转义 例如\n

| 开头保留格式的大文本
\> 会压缩换行

--- 下面是单独文本相当于两个yml文件

可以import多个配置
```yaml
spring:
  config:
    import:
      - classpath:datasource.yml
      - classpath:redis.yml
      - classpath:external-services.yml
      - optional:file:./external-config/override.yml # 可选导入，文件不存在也不报错

app:
  name: my-modular-app
```

# log

门面
JCL（commons-logging），SLF4J

实现
log4j2
logback

springboot-start 直接引导了 spring-boot-starter-log
日志用监听器机制配置的

默认两组
web，sql

loging.level.web=info
loging.level.sql=debug

logging.file.name

![[Pasted image 20250916124137.png]]


# web
核心组件
ViewResolver 视图解析
Coverter Formatter 数据类型转化/例如日期
HttpMessageConverter 转json/string等等
ConfigurableWebBinding 把input request 数据绑定

![[Pasted image 20250916130500.png]]
第二种比较多

## WebMvcAutoConfiguration
创建bean WebMvcconfigurer
interceptor resourcehandler 
# resourceHandler
处理静态资源映射
默认静态路径 resource/static等等 
/webjars 路径  会去找 META_INFO/resources/webjar/下的资源

所有静态资源都有缓存配置

## 内容协商

![[Pasted image 20250916133704.png|525]]
springboot对于@RestController会做协商

基于请求头协商
http header
Accept： applicationion/json 
Accept： applicationion/xml

基于请求参数
/person?format=json
/person?format=xml（需要导入jackson xml binding包）

以上基于HttpMessageConverter实现

http request -》 requestMappingHandler Adapter （argumentResolver参数解析器，returnValueHandler返回值处理器）

一堆 returnValueHandler，由于标注了@ResponseBody，拿到了ResponseBodyhandler
ResponseBodyhandler利用messageConverter把消息写出去

## 支持yaml respond
![[Pasted image 20250916140948.png|475]]

加配置
![[Pasted image 20250916141230.png]]

![[Pasted image 20250916142353.png]]

自定义MessageConverter
![[Pasted image 20250916141625.png|650]]

# 错误处理
spring mvc处理错误的办法

@ExceptionHandler(Exception.class)
可以处理这个Controller的所有错误

也可以写一个
@ControllerAdvice 标注一个类集中处理错误

---
springmvc不能处理时，转给 /error page
BaseErrorController
![[Pasted image 20250916143731.png]]


# 嵌入式容器
springboot 嵌入式 tomcat, jetty，undertow
ServletWebServerFactoryAutoConfiguration

ServletWebServerApplicationContext 启动时会调上面的factory来创建web server实例（例如 tomcat）

48待续

# Vertex的一些特性
1.router 来解析restful request
2.通过 event loop机制， verticle的handler来具体处理业务
	event loop是非阻塞的，通过callback的方式的处理
	 同时也支持eventBus来publish，consume msg
3.有worker线程池来具体处理阻塞式请求

# 整合mybatis
![[Pasted image 20250917104445.png]]

配置datasource， 核心配置xml位置


SqlSessionFactory
SqlSessionTemplate
被注入容器

# 外部配置
可以在spring boot jar的外面加一个application.properties覆盖项目里的配置

命令行>配置文件>代码里
jar包外>jar包内 
profile 文件> default 文件
config文件夹中配置>根目录中的配置

# Test
@SpringBootTest
能把容器拉起来

junit5 使用了@SpringBootTest来初始化容器
junit4 需要 @Runwith(SpringRunner.class) @ContextConfiguration来做到

# 事件监听
meta-info 下有配置文件
![[Pasted image 20250918080819.png]]

引导 启动 运行 三部分
SpringApplication::run

---
引导
createBootStrapContext （读spi配置文件等等）
prepare environment

启动
prepare context
context loading (准备好 BeanDefinitionRegistry，BeanFactory)
context refresh （向容器中加载bean postprocessor等等）
调runner
ready

运行
正常运行


ApplicationListener 是spring原声的listener
SpringApplicationRunListener是springboot的一个实现，来感知启动时的生命周期

## 生命周期描述
Springboot的启动可以分为
引导 启动 运行三个阶段

引导主要找到启动的主类，SpringApplication作为BoostrapContext，并且导入property属性（不管是环境量，jvm参数还是property yaml文件）

启动类似于传统的spring准备context 容器，初始化bean，对于springboot还有一些特殊的步骤。
具体来说要做ComponentScan，AutoConfiguration，导入postProcessor 在合适的时机调用postprocessor，事件的publish，跑ApplicationRunner等等

运行就是在整个容器ready之后，可以正常去跑业务逻辑

---
liveness readyness 状态事件publish 

# 事件驱动开发

ApplicationEventPublisherAware
用这个类发布事件

![[Pasted image 20250918094152.png]]
用ApplicationListener子类来消费事件
或者用
@EventListener注解来消费事件 -- 加在方法上
还可以@Order标注Listener优先级别
# Handler Interceptor
在request之前 之后做一些事情
# Auto configuration
@AutoConfigurationPackage 把主程序package下的组件信息拿到，供Autoconfiguration时使用。

因为这些信息虽然在@ComponentScan的管理中，但是要到容器启动后才有，而AutoConfiguration是容器启动的一部分，所以在这个之前就要拿到AutoConfigurationPackage的信息

# Enable机制
![[Pasted image 20250918113119.png]]
在compoenent中定义@EnableRobot

client标注@EnableRobot使用

# Spring Security
RBAC
user roll permission

ACL
user permission
![[Pasted image 20250918152736.png]]

核心是要定义bean -- SecurityFilterChain
定义UserDetailService load user信息

![[Pasted image 20250918155014.png]]

# oauth JWT理解
oauth基本的概念 ResourceOwner，Client server，resource server，oather server

authcode 模式
Client server跳转到oather server的登陆页面，ResourceOwner填写user/pass 拿到一个authcode，并且跳回Client server，clientserver拿着authcode，client key/pass 去auth server去拿token，然后请求resource server
resource server可以做JWT解析验证token的有效性（通过 public key 验证签名），允许client server访问api

PKCE模式，auth code 加强版，在拿token时不再传递clientsecret
先用sha256获得一对 code_verifier,code_challenge
获取auth_code时，除了传userid/pass还要传codechallenge给auth server
获取token时，传clientid/authcode/code_verifier给auth server

# actuator
spring-boot-start-actuator

配置文件保护监控端点
![[Pasted image 20250919081344.png]]
localhost:8080/actuator

健康监控：生 死
指标监控: MeterRegistry

实现HealthIndicator（或者继承AbstratHealthIndicator）
![[Pasted image 20250919082501.png|600]]

## Prometheus
维护一个时序数据库
每隔n秒抓一次
![[Pasted image 20250919083215.png]]
会有一个actuator/promesus 路径访问监控数据
把这个url配置给grafana

或者在promesus界面下直接看（配置promesus的yml文件）
![[Pasted image 20250919084132.png]]

# AOT
AOT -- 提前编译
JIT -- 即时编译

JVM 即有解释器，又有JIT即时编译器（生成机器指令并且缓存效率高）

C1 C2 编译器
C1 client side compiler
C2 server side copiler

C1精简
C2复杂，效率高

## 原生镜像
把应用打包成适合本机平台的机器编码的镜像

Graalvm 也是一个JDK
可以把AOT编译成本地镜像
![[Pasted image 20250919092700.png]]

native-image 可以吧class文件编译成本地镜像例如windows下的exe

反射之类的要标注，告知graalvm来处理

maven治理 native:build打spring-boot本地包

# Springboot3 新特性
autoconfig property 位置变化
包名 javax->jakata

Graalvm aot
响应式编程

# liveness readyness

readyness一般用来探知 系统是否已经可以来接流量了。
可以用来探知 db jms oauth的状况

liveness用来探知springcontext容器是否正常

我们也可以添加新的healthindiator 并且加入readyness group来监测一些额外的外部系统

最后云原生环境下，liveness挂了系统是会自动重启的


