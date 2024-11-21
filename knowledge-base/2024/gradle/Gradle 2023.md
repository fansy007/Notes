#java #basic 
[[gradle_details]]
# plugin

## simple import plugin
```json
// myproject.java-conventions.gradle
ext {
    javaVersion = 1.8
    cfg = [
        name: 'hg',
        version: 1.0    
    ]
}

// build.gradle  
apply from: "buildSrc/src/main/groovy/myproject.java-conventions.gradle"

task showSimpleVersions {  
    println "$javeVersion $cfg.name $cfg.version"  
}
```

## core plugin
no need import // see /opt/homebrew/Cellar/gradle/8.1.1/libexec/src/plugins/org/gradle/api/plugins
```json
apply plugin: 'java'

// Applying plugins with the plugins DSL
plugins {
    id 'java'
    id 'idea'
    id 'project-report'
    id 'groovy'
    id 'scala'
    //id 'com.example.hello' version '1.0-SNAPSHOT'
}
```


## binary plugin

### create a plugin project
build.gradle
```groovy
plugins {
    id 'groovy' // language support
    id 'java-gradle-plugin' // for making plugin 
    id 'maven-publish' // publish support
}

repositories {
    maven {
        allowInsecureProtocol = true
        url "http://maven.aliyun.com/nexus/content/groups/public/"
    }
    mavenLocal()
}

dependencies {
    implementation 'org.codehaus.groovy:groovy-all:3.0.9'
    testImplementation platform('org.junit:junit-bom:5.9.1')
    testImplementation 'org.junit.jupiter:junit-jupiter'
}
```

```groovy
// define your plugin
gradlePlugin {
    plugins {
        hello {
            id = 'com.example.hello'
            implementationClass = 'com.example.hello.HelloPlugin'
        }
    }
}

// publish your plugin
publishing {
    publications {
        mavenJava(MavenPublication) {
            from components.java
        }
    }
    repositories {
        mavenLocal()
    }
}
```

groovy file
```groovy
class HelloPlugin implements Plugin<Project> {
    @Override
    void apply(Project project) {
        project.task("sayHello") {
            doLast {
                print "hello, world"
            }
        }
    }

    static void main(String[] args) {
        print 'test'
    }
}
```

run ./gradlew publish
### ==Market marker artifacts==
``.m2/repository/com/example/hello/com.example.hello.gradle.plugin/1.0-SNAPSHOT``
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example.hello</groupId>
  <artifactId>com.example.hello.gradle.plugin</artifactId>
  <version>1.0-SNAPSHOT</version>
  <packaging>pom</packaging>
  <dependencies>
    <dependency>
      <groupId>com.example</groupId>
      <artifactId>HelloPlugin</artifactId>
      <version>1.0-SNAPSHOT</version>
    </dependency>
  </dependencies>
</project>
```

points to a real jar file
```sh
.m2/repository/com/example/HelloPlugin/1.0-SNAPSHOT/HelloPlugin-1.0-SNAPSHOT.jar
```

## Precompile plugin
build.gradle
```groovy
plugins {
    id "groovy-gradle-plugin"
    id 'maven-publish'
}

dependencies {
    implementation 'org.codehaus.groovy:groovy-all:3.0.9'
    testImplementation platform('org.junit:junit-bom:5.9.1')
    testImplementation 'org.junit.jupiter:junit-jupiter'
}

publishing {
    publications {
        mavenJava(MavenPublication) {
            from components.java
        }
    }
    repositories {
        mavenLocal()
    }
}
```
define a gradle file in ==src/main/groovy==
File name: ==com.qj.convension.gradle==
```groovy
task sayHi {
    doLast {
        println "hi, this is convention plugin"
    }
}

configure(allprojects) {
    apply plugin: 'maven-publish'
    publishing {
        publications {
            mavenJava(org.gradle.api.publish.maven.MavenPublication) {
                from components.java
            }
        }
        repositories {
            mavenLocal()
        }
    }
    repositories {
        maven {
            allowInsecureProtocol = true
            url "http://maven.aliyun.com/nexus/content/groups/public/"
        }
        mavenLocal()
    }
}
```

the com.qj.convension will be the plugin id auto, no need other configs!! 


## Apply this plugin to a gradle project
settings.gradle
```groovy
pluginManagement {
    repositories {
        mavenLocal()
        maven {
            allowInsecureProtocol = true
            url "http://maven.aliyun.com/nexus/content/groups/public/"
        }
    }
}

```

build.gradle

DSL invoke no need import
```groovy
id 'com.example.hello' version '1.0-SNAPSHOT'
```

if version define inside pluginManagement, then no need set version above
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
		id 'com.example.hello' version '1.0-SNAPSHOT'
	}
}
```


traditional import
```groovy
buildscript {
    repositories {
        maven {
            allowInsecureProtocol = true
            url "http://maven.aliyun.com/nexus/content/groups/public/"
        }
    }

    dependencies {
        classpath 'com.example.hello:com.example.hello.gradle.plugin:1.0-SNAPSHOT'
    }
}

apply plugin: 'com.example.hello'
```

## gradle脚本中引入package
如果想在config周期调用一个包的方法，必须在buildScript中引用
```groovy
buildscript {
	repositories {
        maven {
            allowInsecureProtocol = true
            url "http://maven.aliyun.com/nexus/content/groups/public/"
        }
    }
	dependencies {
        classpath 'org.apache.commons:commons-lang3:3.13.0'
    }
}
```
另一个办法是建一个buildSrc目录， buildSrc的build.gradle文件中 引入的dependecy等价于第一种
buildSrc目录会在build时被打成一个jar
被src中build.gradle文件在config周期直接使用

buildSrc/build.gradle
// import org.apache.commons.lang3.StringUtils;
```groovy
project.dependencies {
    implementation 'org.apache.commons:commons-lang3:3.13.0'
}
```
# File operations
```groovy
task copyAllFiles() {
    doLast {
        delete("$rootDir/build/temp")
        mkdir("$rootDir/build/temp")
        def fileTree = project.fileTree("src")
        fileTree.include("**/*.java").forEach {
            try {
                println it;
                java.nio.file.Path source = it.toPath()
                java.nio.file.Path target = new File("$rootDir/build/temp").toPath()
                Files.copy(source, target.resolve(source.getFileName()), StandardCopyOption.REPLACE_EXISTING)
            } catch (e) {
                println e
            }
        }
    }
}

task copyAllFilesNormal(type:Copy) {
    delete("$rootDir/build/temp")
    from fileTree("src").filter {it.isFile()}
    include("**/*.java")
    into "$rootDir/build/temp"
    duplicatesStrategy DuplicatesStrategy.INCLUDE
    rename {
        name -> "${name}_bak"
    }

}

task zipTemp(type:Zip,dependsOn:copyAllFilesNormal) {
    delete("$rootDir/build/zip")
    mkdir("$rootDir/build/zip")
    archiveFileName = "temp.zip"
    from fileTree("$rootDir/build/temp")
    destinationDirectory = file("$rootDir/build/zip")
}
```

# Encoding set
build.gradle

tasks.withType(JavaCompile) {  
        options.encoding = "UTF-8"  
}

intellij vm option  
-Xmx2048m  
-Dfile.enoding=UTF-8

# Dependency
## api vs implementation

- a impl b, b impl c -> a can't use c
 for example c is apache commons, a project can't invoke apache commons functions

- a impl b, b api c -> a can use c
the purpose is for multi module project, for example:
service impl dao, dao api bean -> then service no need add dependency for bean to avoid dup dependecies

## exclude
```groovy
    implementation('com.fasterxml.jackson.core:jackson-databind:2.13.3') {  
        exclude group: 'com.fasterxml.jackson.core', module: 'jackson-annotations'  
    }
    implementation 'com.fasterxml.jackson.core:jackson-annotations:2.9.0' // then this one will always being used
```

## hard dependency
```groovy
implementation 'com.fasterxml.jackson.core:jackson-core:2.8.0!!'

//or

implementation 'com.fasterxml.jackson.core:jackson-core:2.8.0' {  
    version {  
        strictly('2.8.0')  
    }  
}

// fetch max version
implementation 'com.fasterxml.jackson.core:jackson-core:2.8.+!!' // will fetch 2.8.11
```

## show depednencies
use this plugin
```json
apply plugin: 'project-report'
```

# 生命周期
init -> config -> execute
project.parent.childProjects

# Task
task方法是project对象的方法，但是task方法中的闭包的delegate是task本身，所以task的闭包可以用task对象的方法

task方法的第二个参数是一个闭包的delegate是这个返回的task对象本身，所以$name拿到了task对象的属性

```groovy
task mytask {
    println "$name outside"
    doLast {
        println "$name inside"
        println getPath()
    }
}
//等价于
task('mytask2', {
    println "$name outside"
    doLast {
        println "$name inside"
        println getPath()
    }
})


```



# Platform plugin
主要用来制作bom，contraints不会实际引入只是推荐版本，除非依赖于该bom的项目实际引入了该项目，此时版本将使用bom中的version
和maven的dependencyManagement等价

project name: abc （bom）
```groovy
plugins {  id 'java-platform'
}
dependencies {  
  constraints {  
    api 'commons-httpclient:commons-httpclient:3.1'
    runtime 'org.postgresql:postgresql:42.2.5'
    api platform('com.fasterxml.jackson:jackson-bom:2.9.8')   //引入了别的bom
  }
}
// publish platform by maven publish plugin
publishing {
  publications {  
  myPlatform(MavenPublication) {  
  from components.javaPlatform  }
  } ​}

```

invoke bom
```groovy
dependencies {
	api platform(":abc")
	api "commons-httpclient:commons-httpclient" // bom决定version
}
```

# Groovy
[[groovy#MOP]]