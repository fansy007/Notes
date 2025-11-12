component scan exclude 
![[Pasted image 20250912092959.png]]

@Scope("prototype")

singleton 默认是启动时创建，需要lazy loading需要配置
@Lazy

@Conditional 可以用在 class level，bean level
![[Pasted image 20250912095326.png]]

# @Import
（除了@Bean方式）
@Import 可以导入class， 可以导入 ImportSelector
以全类名方式返回要导入的bean的名字

ImportBeanDefinitionRegisar -- 含有BeanDefinitionRegistar自己来注册bean
例子
```java
public class MyServiceImportBeanDefinitionRegistrar implements ImportBeanDefinitionRegistrar {

    @Override
    public void registerBeanDefinitions(AnnotationMetadata importingClassMetadata, BeanDefinitionRegistry registry) {
        // 创建一个自定义的扫描器
        ClassPathBeanDefinitionScanner scanner = new ClassPathBeanDefinitionScanner(registry, false); // false 表示不使用默认过滤器

        // 设置扫描器：只包含带有 @MyService 注解的类
        scanner.addIncludeFilter(new AnnotationTypeFilter(MyService.class));

        // 指定要扫描的基包（这里为了简单，直接指定包名。实际框架中可能从注解属性读取）
        // 例如，你可以从 importingClassMetadata 中获取 @EnableMyService 注解的 basePackages 属性
        String[] basePackages = new String[]{"com.example.service"}; // 替换成你的实际包名
        scanner.scan(basePackages);
    }
}
```

FactoryBean -- 当getBean时拿到的factoryBean产生的bean而不是factoryBean本身

当你需要创建一些复杂的需要配置的bean可以考虑这种方式
![[Pasted image 20250912101554.png]]

# 其他
初始化调用
1对象创建完成并且赋值完成时可以调@Bean(initMethod=“init”)
2继承InitializerBean接口，DisposableBean接口

## BeanPostProcessor
在 InitializerBean 的init 前，后做一些事情，加入容器就可以使用了
![[Pasted image 20250912103919.png]]
著名的BeanPostProcessor应用
ApplicationContextAwareProcessor
AutowireBeanPostProcessor

# @Vaue
可以读环境变量，配置文件
![[Pasted image 20250913095402.png]]
![[Pasted image 20250913095449.png]]

![[Pasted image 20250913101122.png]]

@Autowire 方法 属性 构造器 参数上都可以标
当只有一个有参构造器 @Autowire 可以省略

@Bean标注的方法，方法参数从容器获取，@Autowire可以省略

通过Aware接口组建，向组建注入spring核心组件

# Profile
-Dspring.profiles.active=test,intg
没标注@Profile的属性在任何环境下都生效

@Profile("test")

# AOP
spring-aspects

![[Pasted image 20250914095818.png]]

或者这么写
![[Pasted image 20250914095853.png]] 

或者抽象出来
![[Pasted image 20250914100016.png]]

切面类要加注解
![[Pasted image 20250914100240.png|500]]

配置类要开启
![[Pasted image 20250914100326.png|500]]

	pointcut 切在哪个方法

![[Pasted image 20250914100716.png|575]]
切面方法接参数，返回值，异常等等

## aspectJ 源码分析
注册一个bean -- AspectJAwareAdvisorAutoProxyCreator

这个bean 实现了2个关键的类
![[Pasted image 20250914102306.png]]
 用beanFactory注册了一个后置处理器SmartXXX。。。。。

这个后置处理器在其他bean创建前会被调用
![[Pasted image 20250914105958.png]]
在事例化之前尝试创建proxy bean
找到业务bean的增加器（advisor）（根据pointcut描述），createProxy

在目标方法调用前，把所有目标方法的advisor组织成拦截器链
![[Pasted image 20250914120811.png|575]]

## 总结 AOP的spring实现

初始化时
首先有一个 配置类加一个@EnableAspectJProxy的annotation
这个注解会通过 `AspectJAutoProxyRegistrar` 注册在spring 容器中注册一个ProxyBeanCreator的bean，事实上这个bean是一个beanPostProcessor的实现，且级别很高priotizedOrder

当spring容器初始化的时候，会首先创建这个 ProxyBeanCreator的实例

然后在create 普通bean的时候
对于普通bean在createBean之前，会调用这个ProxyBeanCreator，根据pointcut信息（会有缓存）决定这个普通bean是否需要被增强器增强，如果需要，那么会把这个普通bean包装成一个proxybean

调用时
这个proxybean会产生一个interceptor链，会在真正的方法前后，以及返回结构/抛异常时调用这个链条

本质是
通过 BeanPostProcessor 在 bean 创建生命阶段“无侵入”地替换成代理对象，代理对象内部维护一条责任链（interceptor chain），从而把横切逻辑和业务逻辑解耦。

# 申明式事务
DataSource -》JDBCTemplate

@EnableTransactionManagement 加在类上
@Transactional 加在方法上

配置事务管理器
DataSourceTransactionManager bean


@EnableTransactionManagement  -> TansactionManagerSelector 导入 AutoProxyRegister 
-》ProxyCreator （类似AOP）

ProxyTransactionConfiguration 
1 注册 advisor bean
2 注册拦截器 会注入TransactionManager

# spring重要组件
BeanPostProcessor （真实类）
==BeanFactoryPostProcessor== （工厂）-- 在BeanFactory Init之后（bean definition已经创建完成），bean 创建之前运行

BeanRegistryPostProcessor（蓝图） -- 在BeanFactory Init 之前 bean definition已经创建完成 

## ApplicationListener
监听ApplicationEvent
也可以用applicationContext定义自己的ApplicationEvent

当调用publishEvent方法时
事件多播器 ApplicationEventMultiCast 负责load所有Listener，依次派发

也可以在方法上标记@EventListener来监听事件
![[Pasted image 20250915101621.png]]

# Spring 初始化过程！！！
ApplicationContext::refresh

prefresh -- load property
创建beanFactory
postProcess beanFactory 子类重写这个方法，可以在这里做进一步设置

>[!note]+ invoke beanFactory post processor 调beanFactory后置处理器
先调 beanDefinitionRegistry post Proceccor (顺序 priorityOrdered Ordered normal)
在调beanFactory post Processor

register bean post processor 注册bean post processor
init message source 国际化的处理
初始化事件派发器
onRefresh方法，给子类重写
注册事件监听器 把容器中所有的Listener都添加到 multicaster上 
>[!note]+ **finishBeanFactoryInitialization 初始化所有单例bean**
根据bean definition，如果是单例的，开始创建bean
在创建bean之前会调用 resolveBeforeInstantiation方法看看是不是要创建一个proxy bean （InstiationAwarePostProcessor）
真正创建bean
给bean属性 赋值 
Aware接口方法执行 （例如 applicationContextAware）
调postProcessor before方法（例如 autoaware）
调init
调postProcessor after方法

把创建好的bean 放到缓存中
finishRefresh 从容器中找LifeCircleProcessor，回调onRefresh方法，发布RefreshEvent事件
暴露mbean







