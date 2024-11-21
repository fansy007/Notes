#cloud #ELK
# Install elastic search
```sh
docker pull elasticsearch:8.13.4
docker pull kibana:8.13.4
docker images
```


## config
```sh
mkdir -p /mydata/elasticsearch/config
mkdir -p /mydata/elasticsearch/data
mkdir -p /mydata/elasticsearch/plugins

cd /mydata/elasticsearch
chmod -R 777 *

docker run --restart=always --name elasticsearch -p 9200:9200 -p 9300:9300 -e discovery.type=single-node -e ES_JAVA_OPTS="-Xms64m -Xmx128m" \
-v /mydata/elasticsearch/data:/usr/share/elasticsearch/data \
-v /mydata/elasticsearch/plugins:/usr/share/elasticsearch/plugins \
-d elasticsearch:8.13.4

docker cp elasticsearch:/usr/share/elasticsearch/config/elasticsearch.yml /mydata/elasticsearch/config/elasticsearch.yml

docker rm -f elasticsearch // 安装失败时可用
docker logs elasticsearch
```

```sh
docker run --restart=always --name elasticsearch -p 9200:9200 -p 9300:9300 -e discovery.type=single-node -e ES_JAVA_OPTS="-Xms64m -Xmx128m" \
-v /mydata/elasticsearch/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml \
-v /mydata/elasticsearch/data:/usr/share/elasticsearch/data \
-v /mydata/elasticsearch/plugins:/usr/share/elasticsearch/plugins \
-d elasticsearch:8.13.4
```

setup password
```sh
docker exec -it elasticsearch bash
cd bin
./elasticsearch-setup-passwords interactive
```

登陆
curl -u elastic:198263 localhost:9200


http://192.168.31.88:9200
elastic/198263
![[Pasted image 20240519102825.png|475]]

## Install kibana
建普通用户
```sh
curl -u elastic:198263 -X POST "http://localhost:9200/_security/user/hg26502" -H 'Content-Type: application/json' -d' { "password" : "198263", "roles" : [ "kibana_system" ], "full_name" : "hg26502", "email" : "46607593@qq.com" }'

curl -u elastic:198263 -X GET "http://localhost:9200/_security/user/hg26502"

```

建立配置文件
```yml
## /mydata/kibana/config/kibana.yml 
#
# ** THIS IS AN AUTO-GENERATED FILE **
#

# Default Kibana configuration for docker target
server.host: "0.0.0.0"
server.shutdownTimeout: "5s"
elasticsearch.hosts: [ "http://192.168.31.88:9200" ]
elasticsearch.username: "hg26502"
elasticsearch.password: "198263"
monitoring.ui.container.elasticsearch.enabled: true
```

启动
```sh
docker run -d --name kibana \
-v /mydata/kibana/config/kibana.yml:/usr/share/kibana/config/kibana.yml \
--restart=always \
-p 5601:5601 kibana:8.13.4
```

登陆
localhost:5601 
elastic/198263

## 查看节点

>[!note]+ 查看健康
curl -u hg26502:198263 http://localhost:9200/_cat/health
1716090824 03:53:44 docker-cluster green 1 1 31 31 0 0 0 0 - 100.0%

>[!note]+ 查看索引
[root@192 config]# curl -u hg26502:198263 http://localhost:9200/_cat/indices
green open .internal.alerts-transform.health.alerts-default-000001            NTLWprtbR9idMN8M_v0rPg 1 0 0 0 249b 249b 249b

## kibana操作
使用kibana devTool


批量导入数据
```sh
POST /_bulk
{ "index" : { "_index" : "account", "_id":"1"}}
{"account_number":1,"balance":39225,"firstname":"Amber","lastname":"Duke","age":32,"gender":"M","address":"880 Holmes Lane","employer":"Pyrami","email":"amberduke@pyrami.com","city":"Brogan","state":"IL"}
{ "index" : { "_index" : "account", "_id":"6"}}
{"account_number":6,"balance":5686,"firstname":"Hattie","lastname":"Bond","age":36,"gender":"M","address":"671 Bristol Street","employer":"Netagy","email":"hattiebond@netagy.com","city":"Dante","state":"TN"}
```

把replica降为0， indices状态就能变绿
```sh
PUT /account/_settings
{ "index" : { "number_of_replicas" : 0 } }
```