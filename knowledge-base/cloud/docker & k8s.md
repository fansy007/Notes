**Bridge mode config**
IPv4 地址 . . . . . . . . . . . . : 192.168.7.111(首选)
 子网掩码 . . . . . . . . . . . . : 255.255.255.0
 默认网关. . . . . . . . . . . . . : 192.168.7.1

**remove**
```shell
[root@node1 hg26502]# yum list installed|grep docker
[root@node1 hg26502]# yum -y remove docker-ce-cli.x86_64
```
# 3、安装
## 1、centos下安装docker
> 其他系统参照如下文档

[https://docs.docker.com/engine/install/centos/](https://docs.docker.com/engine/install/centos/)

### 1、移除以前docker相关包
```bash
sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine
```


### 2、配置yum源
```bash
sudo yum install -y yum-utils
sudo yum-config-manager \
--add-repo \
http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

```

### 3、安装docker
```bash
sudo yum install -y docker-ce docker-ce-cli containerd.io


#以下是在安装k8s的时候使用
yum install -y docker-ce-19.03.5 docker-ce-cli-19.03.5  containerd.io-1.4.6
```
### 3.1 for centerOS8
```shell
#backup 
sudo cp /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
#use aliyun
sudo curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-8.repo

#refresh cache
sudo yum clean all
sudo yum makecache

yum install -y yum-utils

sudo yum-config-manager \
--add-repo \
http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

sudo yum install -y docker-ce docker-ce-cli containerd.io --allowerasing
```
```shell
#
systemctl enable docker --now

sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://01uinh3k.mirror.aliyuncs.com"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker

# run nginx
docker pull nginx

docker run --name nginx -d -p 88:80 \
--restart always  \
nginx

docker cp nginx:/etc/nginx /home/hg26502

docker stop nginx
docker rm nginx

docker run --name nginx -d -p 88:80 --restart always -v nginx

#check docker version
yum info installed docker*

```
### 4、启动
```bash
systemctl enable docker --now
```

### 5、配置加速
> 这里额外添加了docker的生产环境核心配置cgroup

```bash
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://ptkf6imk.mirror.aliyuncs.com"],
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2"
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker

---------------------------------------------------
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://01uinh3k.mirror.aliyuncs.com"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```
### 
### 6. commands
docker run -d --restart=always --name=nginx -p 88:80 nginx


# copy config out and rurun
```shell
docker cp nginx:/etc/nginx /home/hg26502
```
```shell
docker run --name nginx -d -p 88:80 \
--restart always -v /home/hg26502/nginx:/etc/nginx \
nginx
```


docker exec -it mynginx /bin/bash
docker commit -a "hg" -m "index page update" mynginx hgnginx:1.0

docker tag java-demo:v1.0 leifengyang/java-demo:v1.0docker 
docker save -o hgnginx.tar hgnginx:2.0
docker load -i hgnginx.tar 

docker login (hg26502/Yunfei@002)
docker push hg26502/hgnginx
docker pull hg26502/hgnginx:2.0

docker cp hgnginx:/etc/nginx/nginx.conf /home/hg26502/nginx

docker run -v /home/hg26502/redis/redis.conf:/etc/redis/redis.conf \
-v /home/hg26502/redis/data:/data \
-d --name hgredis --restart always \
-p 6379:6379 \
redis:latest redis-server /etc/redis/redis.conf

docker inspect mynginx |grep Mounts -A 20

**write Dockerfile**
```shell
FROM openjdk:8-jdk-slim
LABEL maintainer=hg

COPY build/libs/*.jar   /app.jar

ENTRYPOINT ["java","-jar","/app.jar"]
```

build jar file
docker build -t hgapp:1.0 .
docker run -d -p 8080:8080 --name hgapp --restart=always hgapp:1.0

**setup ip manually**
```shell
vim /etc/sysctl.conf

#配置转发
net.ipv4.ip_forward=1

#重启服务，让配置生效
systemctl restart network
```
## Kubenetes install
### 0. set hostname
```shell
hostnamectl set-hostname master
hostnamectl set-hostname node1
hostnamectl set-hostname node2
```
### 0.1 shutdown fire ball

```shell
systemctl stop firewalld --now
firewall-cmd --state

# reboost also ban firewall
systemctl disable firewalld

```

### 1、基础环境

check swap
```shell
free -m
```

> 所有机器执行以下操作

```bash

# 将 SELinux 设置为 permissive 模式（相当于将其禁用）
sudo setenforce 0
sudo sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

#关闭swap
swapoff -a  
sed -ri 's/.*swap.*/#&/' /etc/fstab

#允许 iptables 检查桥接流量
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
br_netfilter
EOF

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sudo sysctl --system

```



### 2、all machine 安装kubelet、kubeadm、kubectl
```bash
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=http://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=http://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg
   http://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
exclude=kubelet kubeadm kubectl
EOF


sudo yum install -y kubelet-1.20.9 kubeadm-1.20.9 kubectl-1.20.9 --disableexcludes=kubernetes

sudo systemctl enable --now kubelet
```
> kubelet 现在每隔几秒就会重启，因为它陷入了一个等待 kubeadm 指令的死循环

 systemctl status kubelet

## 2、使用kubeadm引导集群

### 1、下载各个机器需要的镜像
```bash
sudo tee ./images.sh <<-'EOF'
#!/bin/bash
images=(
kube-apiserver:v1.20.9
kube-proxy:v1.20.9
kube-controller-manager:v1.20.9
kube-scheduler:v1.20.9
coredns:1.7.0
etcd:3.4.13-0
pause:3.2
)
for imageName in ${images[@]} ; do
docker pull registry.cn-hangzhou.aliyuncs.com/lfy_k8s_images/$imageName
done
EOF
   
chmod +x ./images.sh && ./images.sh
```

### 2、初始化主节点
```bash
#所有机器添加master域名映射，以下需要修改为自己的
echo "192.168.31.80  cluster-endpoint" >> /etc/hosts
echo "192.168.31.81  node1" >> /etc/hosts
echo "192.168.31.82  node2" >> /etc/hosts



#主节点初始化
kubeadm init \
--apiserver-advertise-address=192.168.31.80 \
--control-plane-endpoint=cluster-endpoint \
--image-repository registry.cn-hangzhou.aliyuncs.com/lfy_k8s_images \
--kubernetes-version v1.20.9 \
--service-cidr=10.96.0.0/16 \
--pod-network-cidr=192.168.0.0/16

#所有网络范围不重叠


```
### 2.1 fail can reset
```shell
kubeadm reset

kubeadm init \
--apiserver-advertise-address=192.168.31.80 \
--control-plane-endpoint=cluster-endpoint \
--image-repository registry.cn-hangzhou.aliyuncs.com/lfy_k8s_images \
--kubernetes-version v1.20.9 \
--service-cidr=10.96.0.0/16 \
--pod-network-cidr=172.30.0.0/16

rm -rf /root/.kube/config

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config


```


```bash
Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

Alternatively, if you are the root user, you can run:

  export KUBECONFIG=/etc/kubernetes/admin.conf

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

You can now join any number of control-plane nodes by copying certificate authorities
and service account keys on each node and then running the following as root:

  kubeadm join cluster-endpoint:6443 --token y6ox0e.b373o0gsdgsfyg3x \
    --discovery-token-ca-cert-hash sha256:fd3ec2323394b0a878d8eb02adaad48da6a7f3da2ddd304c012482f94e20fc3b \
    --control-plane 

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join cluster-endpoint:6443 --token y6ox0e.b373o0gsdgsfyg3x \
    --discovery-token-ca-cert-hash sha256:fd3ec2323394b0a878d8eb02adaad48da6a7f3da2ddd304c012482f94e20fc3b 
```

on master exec
```shell
  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

### 3、根据提示继续
> master成功后提示如下：
> ![image.png](https://cdn.nlark.com/yuque/0/2021/png/1613913/1625467146849-06edb92b-9e09-4118-a5eb-8296c23d0c7c.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_37%2Ctext_YXRndWlndS5jb20gIOWwmuehheiwtw%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10#averageHue=%230a0807&height=609&id=eM2K8&originHeight=609&originWidth=1303&originalType=binary&ratio=1&rotation=0&showTitle=false&size=87942&status=done&style=none&title=&width=1303)


#### 1、设置.kube/config
复制上面命令

#### 2、安装网络组件
[calico官网](https://docs.projectcalico.org/getting-started/kubernetes/self-managed-onprem/onpremises#install-calico-with-kubernetes-api-datastore-more-than-50-nodes)
```bash
curl https://docs.projectcalico.org/manifests/calico.yaml -O

kubectl apply -f calico.yaml
```

```bash
#查看集群所有节点
kubectl get nodes

#根据配置文件，给集群创建资源
kubectl apply -f xxxx.yaml

#查看集群部署了哪些应用？
docker ps   ===   kubectl get pods -A
# 运行中的应用在docker里面叫容器，在k8s里面叫Pod
kubectl get pods -A
```

### 4、加入node节点
```bash
kubeadm join cluster-endpoint:6443 --token y6ox0e.b373o0gsdgsfyg3x \
    --discovery-token-ca-cert-hash sha256:fd3ec2323394b0a878d8eb02adaad48da6a7f3da2ddd304c012482f94e20fc3b 
```
> 

```shell
watch -n 1 kubectl get pods -A
```
> 
> 新令牌
> kubeadm token create --print-join-command


> _**高可用部署方式，也是在这一步的时候，使用添加主节点的命令即可**_



### 5、验证集群

- 验证集群节点状态
   - kubectl get nodes


### 6、部署dashboard
#### 1、部署
> kubernetes官方提供的可视化界面
> [https://github.com/kubernetes/dashboard](https://github.com/kubernetes/dashboard)

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.3.1/aio/deploy/recommended.yaml
```

```yaml
# Copyright 2017 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

apiVersion: v1
kind: Namespace
metadata:
  name: kubernetes-dashboard

---

apiVersion: v1
kind: ServiceAccount
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: kubernetes-dashboard

---

kind: Service
apiVersion: v1
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: kubernetes-dashboard
spec:
  ports:
    - port: 443
      targetPort: 8443
  selector:
    k8s-app: kubernetes-dashboard

---

apiVersion: v1
kind: Secret
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard-certs
  namespace: kubernetes-dashboard
type: Opaque

---

apiVersion: v1
kind: Secret
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard-csrf
  namespace: kubernetes-dashboard
type: Opaque
data:
  csrf: ""

---

apiVersion: v1
kind: Secret
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard-key-holder
  namespace: kubernetes-dashboard
type: Opaque

---

kind: ConfigMap
apiVersion: v1
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard-settings
  namespace: kubernetes-dashboard

---

kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: kubernetes-dashboard
rules:
  # Allow Dashboard to get, update and delete Dashboard exclusive secrets.
  - apiGroups: [""]
    resources: ["secrets"]
    resourceNames: ["kubernetes-dashboard-key-holder", "kubernetes-dashboard-certs", "kubernetes-dashboard-csrf"]
    verbs: ["get", "update", "delete"]
    # Allow Dashboard to get and update 'kubernetes-dashboard-settings' config map.
  - apiGroups: [""]
    resources: ["configmaps"]
    resourceNames: ["kubernetes-dashboard-settings"]
    verbs: ["get", "update"]
    # Allow Dashboard to get metrics.
  - apiGroups: [""]
    resources: ["services"]
    resourceNames: ["heapster", "dashboard-metrics-scraper"]
    verbs: ["proxy"]
  - apiGroups: [""]
    resources: ["services/proxy"]
    resourceNames: ["heapster", "http:heapster:", "https:heapster:", "dashboard-metrics-scraper", "http:dashboard-metrics-scraper"]
    verbs: ["get"]

---

kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard
rules:
  # Allow Metrics Scraper to get metrics from the Metrics server
  - apiGroups: ["metrics.k8s.io"]
    resources: ["pods", "nodes"]
    verbs: ["get", "list", "watch"]

---

apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: kubernetes-dashboard
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: kubernetes-dashboard
subjects:
  - kind: ServiceAccount
    name: kubernetes-dashboard
    namespace: kubernetes-dashboard

---

apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: kubernetes-dashboard
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: kubernetes-dashboard
subjects:
  - kind: ServiceAccount
    name: kubernetes-dashboard
    namespace: kubernetes-dashboard

---

kind: Deployment
apiVersion: apps/v1
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: kubernetes-dashboard
spec:
  replicas: 1
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      k8s-app: kubernetes-dashboard
  template:
    metadata:
      labels:
        k8s-app: kubernetes-dashboard
    spec:
      containers:
        - name: kubernetes-dashboard
          image: kubernetesui/dashboard:v2.3.1
          imagePullPolicy: Always
          ports:
            - containerPort: 8443
              protocol: TCP
          args:
            - --auto-generate-certificates
            - --namespace=kubernetes-dashboard
            # Uncomment the following line to manually specify Kubernetes API server Host
            # If not specified, Dashboard will attempt to auto discover the API server and connect
            # to it. Uncomment only if the default does not work.
            # - --apiserver-host=http://my-address:port
          volumeMounts:
            - name: kubernetes-dashboard-certs
              mountPath: /certs
              # Create on-disk volume to store exec logs
            - mountPath: /tmp
              name: tmp-volume
          livenessProbe:
            httpGet:
              scheme: HTTPS
              path: /
              port: 8443
            initialDelaySeconds: 30
            timeoutSeconds: 30
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            runAsUser: 1001
            runAsGroup: 2001
      volumes:
        - name: kubernetes-dashboard-certs
          secret:
            secretName: kubernetes-dashboard-certs
        - name: tmp-volume
          emptyDir: {}
      serviceAccountName: kubernetes-dashboard
      nodeSelector:
        "kubernetes.io/os": linux
      # Comment the following tolerations if Dashboard must not be deployed on master
      tolerations:
        - key: node-role.kubernetes.io/master
          effect: NoSchedule

---

kind: Service
apiVersion: v1
metadata:
  labels:
    k8s-app: dashboard-metrics-scraper
  name: dashboard-metrics-scraper
  namespace: kubernetes-dashboard
spec:
  ports:
    - port: 8000
      targetPort: 8000
  selector:
    k8s-app: dashboard-metrics-scraper

---

kind: Deployment
apiVersion: apps/v1
metadata:
  labels:
    k8s-app: dashboard-metrics-scraper
  name: dashboard-metrics-scraper
  namespace: kubernetes-dashboard
spec:
  replicas: 1
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      k8s-app: dashboard-metrics-scraper
  template:
    metadata:
      labels:
        k8s-app: dashboard-metrics-scraper
      annotations:
        seccomp.security.alpha.kubernetes.io/pod: 'runtime/default'
    spec:
      containers:
        - name: dashboard-metrics-scraper
          image: kubernetesui/metrics-scraper:v1.0.6
          ports:
            - containerPort: 8000
              protocol: TCP
          livenessProbe:
            httpGet:
              scheme: HTTP
              path: /
              port: 8000
            initialDelaySeconds: 30
            timeoutSeconds: 30
          volumeMounts:
          - mountPath: /tmp
            name: tmp-volume
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            runAsUser: 1001
            runAsGroup: 2001
      serviceAccountName: kubernetes-dashboard
      nodeSelector:
        "kubernetes.io/os": linux
      # Comment the following tolerations if Dashboard must not be deployed on master
      tolerations:
        - key: node-role.kubernetes.io/master
          effect: NoSchedule
      volumes:
        - name: tmp-volume
          emptyDir: {}
```

#### 2、设置访问端口
```bash
kubectl edit svc kubernetes-dashboard -n kubernetes-dashboard
```
> type: ClusterIP 改为 type: NodePort


```bash
kubectl get svc -A |grep kubernetes-dashboard
## 找到端口，在安全组放行
```

访问： https://集群任意IP:端口      https://192.168.31.80:32715

#### 3、创建访问账号
```yaml
#创建访问账号，准备一个yaml文件； vi dash.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
```
```bash
kubectl apply -f dash.yaml
```
#### 4、令牌访问
```bash
#获取访问令牌
kubectl -n kubernetes-dashboard get secret $(kubectl -n kubernetes-dashboard get sa/admin-user -o jsonpath="{.secrets[0].name}") -o go-template="{{.data.token | base64decode}}"
```

```json
eyJhbGciOiJSUzI1NiIsImtpZCI6Ik1tX0hMc2dsYXJTOElRdG5CcFZaMTlLMkJLbDdHX3c5MUtxZmlyQUNHRzgifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlcm5ldGVzLWRhc2hib2FyZCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLXBucDk4Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiJjNzcyNGIzNC00YWZkLTRkOWMtODRhZS05ZDlhMjlhNDU0OGYiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZXJuZXRlcy1kYXNoYm9hcmQ6YWRtaW4tdXNlciJ9.QCIGvHx6rwHIDgFYX4eenRialOkXr1yi4_j3wVxHCcYYl34Jv7asQmZ2noJDNwZ_lQ9CjU9pie7IBTKaQeuKPFwDoidezWCRbgfXYnBA9Bh6vkNwE1AD5PAXyfe-y9h7FPFwJ3CxW-GswWefki5lIIY4ZWMGdNSWdR-BZStf3i0CaNNQCMRBUiBwVTwfC_e1tnINAtiwwzi36JJZDlQKtB8-IrVAEfjxIni3TL9iZEiCOEvXIrQE7Yb6iHntGCaF3SoaOd9VJY6a9Xo1t9cT9LWkp5-ycqvwXnge857hCPfIlVR_O-rGzJ1jGKs7_vUfrSH49bH-HJwTLWZk3_FIKQ
```
#### 5、界面
![image.png](https://cdn.nlark.com/yuque/0/2021/png/1613913/1625476485187-1893393c-5e0b-4d0a-ab57-e403b3a714dd.png?x-oss-process=image%2Fwatermark%2Ctype_d3F5LW1pY3JvaGVp%2Csize_54%2Ctext_YXRndWlndS5jb20gIOWwmuehheiwtw%3D%3D%2Ccolor_FFFFFF%2Cshadow_50%2Ct_80%2Cg_se%2Cx_10%2Cy_10#averageHue=%23d9c9b0&height=447&id=YBWct&originHeight=894&originWidth=1910&originalType=binary&ratio=1&rotation=0&showTitle=false&size=100346&status=done&style=none&title=&width=955)
# Kubenetes


reboost and gen token
```shell
1.回到kubernees-maser  依次输入列命令
systemctl stop kubelet
systemctl stop docker
iptables --flush
iptables -tnat --flush
systemctl start kubelet
systemctl start docker


  2.重新生成新token
  在kubernetse-master重新生成token：

# kubeadm token create

  424mp7.nkxx07p940mkl2nd

# openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | openssl dgst -sha256 -hex | sed 's/^.* //'

  d88fb55cb1bd659023b11e61052b39bbfe99842b0636574a16c76df186fd5e0d

 

   3.在kubernetes-slave中执行此命令 join就成功了

#  kubeadm join 192.168.169.21:6443 –token 424mp7.nkxx07p940mkl2nd \ --discovery-token-ca-cert-hash sha256:d88fb55cb1bd659023b11e61052b39bbfe99842b0636574a16c76df186fd5e0d
```
## after join
```shell
 kubectl get pod -A -w
```
dashboard
```shell
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.3.1/aio/deploy/recommended.yaml
```
## 设置访问端口
```bash
kubectl edit svc kubernetes-dashboard -n kubernetes-dashboard
```
> type: ClusterIP 改为 type: NodePort


## look log
```shell
 kubectl logs -n  kube-system calico-node-njmhm 
 kubectl describe pod calico-node-njmhm -n kube-system

```
## delelte node
```
kubectl drain node1 --delete-local-data --force --ignore-daemonsets node/node1
kubectl delete node node1

kubectl drain node2 --delete-local-data --force --ignore-daemonsets node/node2
kubectl delete node node2
```
## reget token
```shell
[root@master hg26502]# kubeadm token create --print-join-command
kubeadm join cluster-endpoint:6443 --token nfasxh.8i6irg9wxduo35ie     --discovery-token-ca-cert-hash sha256:762995a0736ab6e44f183df85e3bbb390241bb257956c8bd8153cdc3e6239011 

```
## reboost pods
```shell
 kubectl replace --force -f recommended.yaml 
```
