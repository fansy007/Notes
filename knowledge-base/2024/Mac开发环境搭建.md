#basic #java #cloud
# 设置java home
>[!note]+ mac 查询 java home
/usr/libexec/java_home

>[!note]+ 写入启动脚本
echo 'export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-17.jdk/Contents/Home' >> ~/.zshrc
source ~/.zshrc

# 环境配置
**重启linux**
shutdown -r now

**Root**
sudo su -切换到root
su hg26502 - 切换到你的用户名

Boost **Item** 启动项清理可看看这些目录是否干净
```sh
~/Library/LaunchAgents
/Library/LaunchAgents
/System/Library/LaunchAgents

##以上三个目录为系统推荐放置的路径，是当登录之后启动的进程

~/Library/LaunchDaemons
/Library/LaunchDaemons
/System/Library/LaunchDaemons
```

---
## Install **Brew**
```sh
/usr/bin/ruby -e "$(curl -fsSL [https://cdn.jsdelivr.net/gh/ineo6/homebrew-install/install](https://cdn.jsdelivr.net/gh/ineo6/homebrew-install/install))"

eval "$(/opt/homebrew/bin/brew shellenv)"

##hainings-MacBook-Pro:~ zou$ 
touch .bash_profile 
export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-17.jdk/Contents/Home
export PATH=$JAVA_HOME/bin:/Users/zou/work/maven36/bin:$PATH
```
Mirror brew
```sh
echo 'export HOMEBREW_API_DOMAIN="https://mirrors.aliyun.com/homebrew-bottles/api"' >> ~/.zshrc
echo 'export HOMEBREW_BREW_GIT_REMOTE="https://mirrors.aliyun.com/homebrew/brew.git"' >> ~/.zshrc
echo 'export HOMEBREW_CORE_GIT_REMOTE="https://mirrors.aliyun.com/homebrew/homebrew-core.git"' >> ~/.zshrc
echo 'export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.aliyun.com/homebrew/homebrew-bottles"' >> ~/.zshrc
source ~/.zshrc
brew update
```


install software by brew
```sh
brew install git
brew install gradle
```

## Setup Git
[[Git - 2024]]

### git account
git: 46607593@qq.com/Yunfei@002
gitee: fansy007/198263xp

---
### check git path
```sh
##查看路径
which git 
```

---
### generate public key
```sh
ssh-keygen -t rsa -b 4096 -C "qjgeng@gmail.com"

## Copy id_rsa.pub to gitte, github
(base) hg26502@192 .ssh % cd ~/.ssh
(base) hg26502@192 .ssh % ls -al
-rw-------   1 hg26502  staff  3381  5 27 11:19 id_rsa
-rw-r--r--   1 hg26502  staff   742  5 27 11:19 id_rsa.pub
```

---

### setup git global and clone project
```sh
hg26502@192 workspace % git config --global user.name hg26502
hg26502@192 workspace % git config --global user.email qjgeng@gmail.com
git clone git@gitee.com:fansy007/gradle-java8.git
```

---
### setup config file, git ignore

~/.gitconfig
```sh
192:~ zou$ cat .gitconfig 
[user]
        name = qjgeng
        email = 46607593@qq.com
[core]
        excludesfile = /Users/zou/.gitignore_global
        autocrlf = input

192:~ zou$ cat .gitignore_global 
*~
.DS_Store
*.iml
*.class
target/
.idea/
.classpath
.project
.settings/
.springBeans
build/
.gradle/
```

also project ignore file name is ``.gitignore``

---
### push local code remote
如何在本地初始化git仓库并提交远程
```sh
##push local code remote
mkdir git-practice
cd git-practice
git init 
touch README.md
git add README.md
git commit -m "first commit"
git remote add origin https://gitee.com/fansy007/git-practice.git

git push --set-upstream origin master
# 上面指令 --set-upstream 等价于 -u，作用是使本地branch于远程master branch挂钩
# 下次可以直接提交了
```

---
## Maven
mvn path:
``/opt/homebrew/Cellar/maven/3.9.2/bin/mvn``

Brew install maven no conf folder need create manually
```sh
hg26502@192 3.9.2 % mkdir ~/.m2             
hg26502@192 3.9.2 % touch ~/.m2/settings.xml
hg26502@192 3.9.2 % chmod 755 ~/.m2/settings.xml
```

---
### Mirror repository
```sh
tee ~/.m2/settings.xml <<'EOF'
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0
                              https://maven.apache.org/xsd/settings-1.0.0.xsd">
  <mirrors>
    <mirror>
      <id>alimaven</id>
      <name>aliyun maven</name>
      <url>https://maven.aliyun.com/nexus/content/groups/public/</url>
      <mirrorOf>central</mirrorOf>       
    </mirror>
  </mirrors>
</settings>
EOF
```

---
## Gradle setup
check init.gradle
```sh
192:~ zou$ cd .gradle/
192:.gradle zou$ ls
caches                init.gradle        native                undefined-build        wrapper
daemon                jdks                notifications        workers
192:.gradle zou$ cat init.gradle
```

### Mirro gradle
```sh
tee init.gradle<<'EOF'
allprojects {
    repositories {
        mavenLocal()
        maven {
            allowInsecureProtocol = true
            url "http://maven.aliyun.com/nexus/content/groups/public/"
        }
        mavenCentral()
    }

    buildscript {
        repositories {
          mavenLocal()
           maven {
            allowInsecureProtocol = true
            url "http://maven.aliyun.com/nexus/content/groups/public/"
                 }
          mavenCentral()
        }
    }
}
EOF
```

---
## Install scala
```sh
brew search scala
brew install scala@2.13
manually add /opt/homebrew/opt/scala@2.13/bin to ~/.bash_profile
```
Add path: [[#Install **Brew**]]

# Intellij 快捷键冲突
![Pasted image 20231022201412.png](Pasted%20image%2020231022201412.png)