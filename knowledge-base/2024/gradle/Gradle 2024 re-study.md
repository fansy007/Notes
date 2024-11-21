# 升级当前gradle wrapper版本
gradle wrapper --gradle-version 8.7
# init.gradle
配置仓库 放在
/Users/hg26502/.gradle
```groovy
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
```

# groovy
[[groovy]]

# settings.gradle
用来组织rootProject和childrenProject
```groovy
rootProject.name = 'root-project'
include('sub-project-a')
include('sub-project-b')
include('sub-project-c')
```

# build.gradle
```groovy
plugins {
      id("application")
}
```
这段话实际是调用了project对象的plugins方法，方法的参数是一个闭包，而这个闭包调用了id方法
```groovy
def closure = { 
	id('java');
	id('application');
}

project.plugins(closure);
```

而plugins方法把closure delegate给了PluginDependenciesSpec类，这个类实现了id方法
```groovy
void plugins(Closure closure) {
    // 获取 PluginDependenciesSpec 实例
    PluginDependenciesSpec pluginDependenciesSpec = getPluginManager().getPluginDependenciesSpec()
    // 执行闭包
    closure.delegate = pluginDependenciesSpec
    closure.call()
}
```


# GRADLE_USER_HOME
~/.gradle 保存caches daemon wrapper等

