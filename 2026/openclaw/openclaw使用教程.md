#程序 #ai 
# 配置向导
## model
[https://api.siliconflow.cn/v1](https://api.siliconflow.cn/v1)
sk-lpyhpmlunfmzzqeqtwmwdrqclvahyrduufufdzhdajpfqqwh

## 通用配置
https://github.com/daheiai/easy-openclaw#

## 代理
请用代理[http://127.0.0.1:7890](http://127.0.0.1:7890)

## 杀僵尸进程
(base) hg26502@192 sessions % ps aux | grep openclaw
hg26502          77105   0.0  0.2 436539984  58288 s000  T    五11上午   0:02.32 openclaw-logs    
hg26502          77104   0.0  0.1 436167072  39008 s000  T    五11上午   0:00.07 openclaw   
hg26502          77029   0.0  0.2 436538720  58288 s000  T    五11上午   0:02.98 openclaw-logs    
hg26502          77027   0.0  0.1 436166800  39008 s000  T    五11上午   0:00.06 openclaw   
hg26502          76583   0.0  0.2 436405376  58320 s000  T    五11上午   0:08.27 openclaw-logs    
hg26502          76581   0.0  0.1 436166880  39008 s000  T    五11上午   0:00.07 openclaw   
hg26502          26172   0.0  0.0 435301664   1376 s000  S+    1:08下午   0:00.00 grep openclaw

(base) hg26502@192 sessions % kill -9 77105 77104 77029 77027 76583 76581



RSS订阅
https://news.daheiai.com/rss.php
# 安装skill
npm i -g clawhub

Tavily Web Search
clawhub install "tavily-search"

vercel skills
npx指令直接安装github 里的skills

![[Pasted image 20260312100420.png]]

查看对话调了哪些模块
/new
/verbose

# 多agent
openclaw agent add
切换模型 /model

调度子agent访问 。。。。。 激发子agent


awesome-openclaw-usecases


