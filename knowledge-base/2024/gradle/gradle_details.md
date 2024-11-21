#basic #java 
# settings.gradle
**pluginManagement** -- define plugin repository, and define plugin version
then all project use the plugin no need set version:
==plugins {
	id 'com.qj.convension'
}==

**dependencyResolutionManagement** -- 定义了仓库，porject无需再引入仓库

**rootProject.name = 'gradle-Java8'
include 'app'** -- 定义父子项目的结构
如果不设project name， 默认使用目录名做project name

运行子项目task可以直接在跟项目中跑
./gradlew :app:build

```groovy
pluginManagement {
    repositories {
        mavenLocal()
        maven {
            allowInsecureProtocol = true
            url "http://maven.aliyun.com/nexus/content/groups/public/"
        }
    }

    plugins {
        id 'com.qj.convension' version '1.0-SNAPSHOT'
    }
}

dependencyResolutionManagement {
    repositories {
        mavenLocal()
        maven {
            allowInsecureProtocol = true
            url "http://maven.aliyun.com/nexus/content/groups/public/"
        }
    }
}

rootProject.name = 'gradle-Java8'
include 'app'
```

# build.gradle

设置 plugin 和 plugin的config
```groovy
plugins {
    id 'java'
    id 'idea'
    id 'project-report'
    id 'groovy'
    id 'scala'
    id 'com.qj.convension'
}

java {  
toolchain.languageVersion.set(JavaLanguageVersion.of(17))  
}
```

---
设置dependencies
```groovy
dependencies {
    implementation 'org.scala-lang:scala-library:2.13.8'
    compileOnly 'org.projectlombok:lombok:1.18.22'
    annotationProcessor 'org.projectlombok:lombok:1.18.22'
    testImplementation 'org.junit.jupiter:junit-jupiter-api:5.7.0'
    testRuntimeOnly 'org.junit.jupiter:junit-jupiter-engine:5.7.0'
}
```

# Plugins

**core plugin**
      gradle provide, no need version
**community plugin**
      2nd party provide, need provide version
**convention plugin**
      you defined

# Tasks

life circle tasks -- gradle 系统提供
action tasks -- your own task

查看tasks
```groovy
 ./gradlew :app:tasks
```
查看 task执行的顺序
```sh
./gradlew :app:jar --console=plain

> Task :buildSrc:compileJava NO-SOURCE
> Task :buildSrc:compileGroovy NO-SOURCE
> Task :buildSrc:processResources NO-SOURCE
> Task :buildSrc:classes UP-TO-DATE
> Task :buildSrc:jar UP-TO-DATE
> Task :buildSrc:assemble UP-TO-DATE
> Task :buildSrc:compileTestJava NO-SOURCE
> Task :buildSrc:compileTestGroovy NO-SOURCE
> Task :buildSrc:processTestResources NO-SOURCE
> Task :buildSrc:testClasses UP-TO-DATE
> Task :buildSrc:test NO-SOURCE
> Task :buildSrc:check UP-TO-DATE
> Task :buildSrc:build UP-TO-DATE

> Configure project :
mytask outside
mytask2 outside

> Task :app:compileJava NO-SOURCE
> Task :app:processResources NO-SOURCE
> Task :app:classes UP-TO-DATE
> Task :app:jar UP-TO-DATE

```


