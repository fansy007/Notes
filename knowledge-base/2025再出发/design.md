# 大负载系统的设计
Vertical scaling vs horizontal scaling
纵向 加内存 加cpu
横向 加服务器

负载均衡 是一种horizontal scale 

数据库 1mater -- 多slave 结构，一写多读

## cache的问题
expiration policy
consistency with db
缓解error -- 多缓存，备份缓存
擦除策略 -- LRU least reacent used， FIFO

## CDN
content delivery network
就近加载静态内容

TTL（time to live）


## Stateless web tire
把会话信息从server端摘出来，放在一个datacenter/分布式cache，那么每个server就是scalable的，统一从一个地方那session信息

## logging metrics automation

## database horizontal scale
sharding 每个分片存的data是唯一的，data的数据结构是一致的 例如4个分片存 userid%4的（partition key）数据

缺点
resharding 由于数据不均衡，有的分片率先容量用完了
名人问题 有的shard负载高
join and denormalization problem shard之间是要解偶的，无法用jion查询

![[Pasted image 20250925145936.png]]

# tps cash 吞吐量
每天10万条 trade
那么1个小时一万条 -- 1秒钟三条

1条split成100条child trade 1秒钟要处理300条？

# interview tips
ask right questions

# 限流
通过 nginx 限流， 通过server段直接限流（token桶，漏桶），在nginx集群的更上一层限流（redis）
通过jms层限流

返回错误代码429 503，设置重试时间在respond header

# 生成短url

一种是把长 url hash（例如sha256）之后去截断，然后做base62 转字符，但是要放重复

一种是直接生成一个唯一的数字（数据库sequence自增，雪花算法），然后做base62，转字符，不担心重复，但是多了生成数字的步骤

# Notification system
mobile push notifications， SMS， Email

provider -- APN -- ios device
![[Pasted image 20251004074032.png]]

A distribution system

JMS queue

build msg -- desination, meta info, payload
message log -- for republish if failed
user info cache
validation & filtering
msg template
安全验证 -- https 证书，oauth token