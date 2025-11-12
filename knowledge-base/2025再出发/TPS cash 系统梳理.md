![[Pasted image 20250607155858.png]]

这是TPS CASH 金融交易系统的架构图，聚焦于TPS相关的组件和流程，以及上下游系统的数据流动的方向和组件之间的调用关系。

花旗大背景 下的FICC描述：
fixed income， currencies， commodities
tps cash 主要的业务 -- UST credit FXLM MBS
RFQ -- request for quote 

花旗主要的业务， 自营（或者对冲），做市商，承销发行
分Bank chain， Corp Chain

GSP （global spread product）
RATES （BOND）

上游 bbg tradeweb 走fix协议，把fix msg，或者是gfi entity 传到citi的front office

中台的主要工作是 trade enrich，trade matching，money calculation，trade split，money calculation，quality control，position capture and risk management（smart check）， regulation report，lifecircle event management

settle相关的信息
SDI Fedwire DTC Euroclear等等 （fedwire split 50M）

FICC fix income clearing cooperation下有专门的mbs 清算部门mbsd
tba -- pool 的转化

tpscash trade 要经历三个阶段 FO ACCEPT， MO ACCEPT，BO ACCEPT
FO ACCEPT是传进来的前台做的那条trade -- capture position，MO ACCEPT是整个TXN （包括allocation，currency leg，hedge leg都被接受了）-- 发regulatory， BO ACCEPT 是back office的返回


验证 trader sales的role，通过产品+账户，计算出是否active并且给出businessline，不同的business line走不同的position，regulation，settle 路径
验证 哪些人可以access哪些account，通过eems rmcc code等等计算

trader 有 cooperate hiarachy
legal entity -- subbusiness -- partition -- strategy code -- firm account

product 有 rmcc code

Euro bond --
product country -- 比如说ibm债券
issue country -- 日本
product currency -- 日元

samura bond，外国公司跑到日本发债券


product country -- 比如说 劳斯莱斯债券
issue country -- 美国
product currency -- 美元

yanki 债券




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







