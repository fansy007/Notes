![[Pasted image 20250607155858.png]]

这是TPS CASH 金融交易系统的架构图，聚焦于TPS相关的组件和流程，以及上下游系统的数据流动的方向和组件之间的调用关系。

# 主要交易的产品有  
政府债 UST GILT JGB G10
Local market

EURO bond — 在发行国（公司）以外的国家以非本国货币计价的国际债券。
product country
issue country
trade currency
苹果公司 在伦敦以欧元发行的公司债

Supernational bond 世界银行发行的债券
municipal bond -- citi retired product
MMKT CP CD BCD

CDs 
REPO

MBS -- TBA， POOL，CMO 

## 模块
有这些模块：
上游 OTC， Electronic

TPS 分模块
GUI service

CORE tps cash

以matching 为界

matching之前是 FO Accept （position已经处理好了）
matching之后 MO Accept （send to trace）
最后是 BO sender

external system publish
DSP（gemfire client） pricenet（RV）Olympus

GTPL

## Postion
TPS 快速catch position，是给 trader和risk系统使用的
TES TML catch的position 将和tps catch的position进行比对

endposition roll     /region/partition/strategycode
endposition publish


## TPS系统的云原生化
tpscore， tpsdb 的component是打包到artifact仓库的

tpscore redesign 拆分到更小的粒度
每个微服务使用不同的版本


## restful JMS
消息的ACK NACK机制， 
bulk api（利用json）无需固定表结构

## ES
observable log
 input request payload，
 executing time summary

otel tracing

## BAU squad && project leader
 business as usual -- bug fix， enhancement
tight bond of business knowledge
over region collaberate
team 的整合 -- ba qa dev （team）

需求的变化
make code genetic -- make code special 







