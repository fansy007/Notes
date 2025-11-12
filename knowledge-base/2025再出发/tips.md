db隔离级别 脏读，幻读，重复读
-- 我们是读已经提交

readiness -- 考察 的一些基础设施
例如db jms oauth是否正常，不正常的情况下pod是无法启动成功，且route是不会把请求指向这个pod

liveness -- 考察的是运行时的状态是否保持正常，不正常是会自动重启
例如 自己写restful接口 调verticle api 看看event loop是不是正常
再例如 内存泄漏导致频繁的垃圾收集，会被探知，并且自动重启

系统的warm up，启动完之后自动跑一个调动一下

coredb core 公用component移动到云上时，注意解耦合，只有真正被所有service 依赖的包才放在那里，不要吧业务逻辑放进来

为什么要用UMB包装普通的ems，分装细节

db的主从和集群 主 从分别形成cluster，主cluster负责读写，同步，从备份
观测db的一些阈值，例如processor数量，线程数来评估性能

WIP - VIP - nginx router - app router - service - pod

下次问题 create trade api， cyber证书，白名单问题
