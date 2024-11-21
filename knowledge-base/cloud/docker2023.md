#cloud [[docker & k8s]]
# 家组网方式
主wifi Lan 192.168.31.1
DHCP 设 110-254
副wifi bedroom wan 192.168.31.101
副wifi qjgeng wan 192.168.31.103

---
三网桥接
虚拟机分配
桥接模式 mac_centeros manual set:
192.168.31.88

---
# reboost
```sh
systemctl restart networkManager #centeros8
shutdown -r now

```
# Install redis
prepare a folder
```sh
/home/hg26502/redis
/home/hg26502/redis/data
```

add config file

```sh
vi redis.conf
appendonly yes


docker run -v /home/hg26502/redis/redis.conf:/etc/redis/redis.conf \
-v /home/hg26502/redis/data:/data \
-d --name redis --restart always \
-p 6379:6379 \
redis:latest redis-server /etc/redis/redis.conf
```



# Install by docker compose

要启动这些服务，你需要在包含 `docker-compose.yml` 文件的目录下运行 `docker-compose up` 命令

```sh
docker compose -f docker-compose.yml up -d
```

建立/prod目录， vi 以下两个yml

docker-compose.yml

```yml
version: '3.9'

services:
  redis:
    image: redis:latest
    container_name: redis
    restart: always
    ports:
      - "6379:6379"
    networks:
      - backend

  zookeeper:
    image: bitnami/zookeeper:latest
    container_name: zookeeper
    restart: always
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
      ALLOW_ANONYMOUS_LOGIN: yes
    networks:
      - backend

  kafka:
    image: bitnami/kafka:3.4.0
    container_name: kafka
    restart: always
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      ALLOW_PLAINTEXT_LISTENER: yes
      KAFKA_CFG_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    networks:
      - backend
  
  kafka-ui:
    image: provectuslabs/kafka-ui:latest
    container_name:  kafka-ui
    restart: always
    depends_on:
      - kafka
    ports:
      - "8080:8080"
    environment:
      KAFKA_CLUSTERS_0_NAME: dev
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: kafka:9092
    networks:
      - backend

  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    restart: always
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
    networks:
      - backend

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    restart: always
    depends_on:
      - prometheus
    ports:
      - "3000:3000"
    networks:
      - backend

networks:
  backend:
    name: backend
```



prometheus.yml

```sh
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']

  - job_name: 'kafka'
    static_configs:
      - targets: ['kafka:9092']
```


