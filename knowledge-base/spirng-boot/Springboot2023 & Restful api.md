#java #springboot [[spring-boot]]
# Restful fundamentals

the getPerson RPC-style endpoint is translated into ==GET /api/v1/persons in REST== 
endpoint名词化，用method name: GET 做动词

==https:// demo.app/api/v1/persons is a REST endpoint. 
Additionally, ==/api/v1/persons== is the endpoint path 

and ==persons== is the REST resource
## 无状态

每次call GET可 reproduce获取同样的结果
## URI

分两种 URL， URN
URL不仅仅用于http 地址， 还包括FTP JDBC MAILTO等等

URI 结构
```ssh
scheme:[//authority]path[?query][#fragment]
```
例子
```sh
GET https://www.domain.com/api/v1/order/
```

| 内容           | 名称作用    |
| -------------- | ----------- |
| GET            | Method name |
| https://       | scheme      |
| www.domain.com | hostname    |
| /api/v1/order/ | path        |

URL是URI的子集：URI是一个identifier， URL不仅仅是identifier，还告诉你如何get to it

URN是另一种标识，restful不用urn
## HTTP methods

• POST: Create or search（查询条件复杂时不得不post 一个body）
• GET: Read
• PUT: Update
• DELETE: Delete
• PATCH: Partial update
## Status code

There are five categories of HTTP status codes, as follows:
• Informational responses (100–199)
• Successful responses (200–299)
• Redirects (300–399)
• Client errors (400–499)
• Server errors (500–599)
## REST 设计原则

- 使用名词， 动词给method
- 用复数查询 GET /resources
- respond中使用link HATEOAS
```html
With HATEOAS, RESTful web services provide information dynamically through hypermedia. Hypermedia is the part of the content you receive from a REST call response. This hypermedia content contains links to different types of media such as text, images, and videos. Machines, aka REST clients/browsers, can follow links when they understand the data format and relationship types.
```
- versioning your apis
  两种方法
  - head上加Accept
    ```ssh
    Accept: application/vnd.github.v3+json
    ```
  - endpoint path上加version
    ```ssh
    GET https://demo.app/api/v1/persons
    ```

---
## Status code 429
Too many requests
rate limit 可以防止api被过度使用

responds header可以告知客户端api limit 信息
```html
• X-Ratelimit-Limit: The number of allowed requests in the current period, for example, X-Ratelimit-Limit: 60.
• X-Ratelimit-Remaining: The number of remaining requests in the current period, for example,X-Ratelimit-Remaining: 55.
• X-Ratelimit-Reset: The number of seconds left in the current period, for example, X-Ratelimit-Reset: 1601299930.
• X-Ratelimit-Used: The number of requests used in the current period, for example, X-Ratelimit-Used: 5. This information then might be used by the client to keep track of the total number of available API calls for the given period.
```

# OAS
open api definition structure

openapi.yaml 对于API的定义
## components section

![[Pasted image 20231028180216.png|550]]
 six main types for component definition
```html
OAS supports six basic data types, which are as follows (all are in lowercase):
• string • number • integer • boolean • object • array
```

在这六种类型的基础上，还可以定义format
![[Pasted image 20231028180805.png|550]]

```html
There are some other common formats you can use along with types, as follows:
• type: number with format: float: This will contain the floating-point number
• type: number with format: double: This will contain the floating-point number with double precision
• type: integer with format: int32: This will contain the int type (signed 32-bit integer)
• type: integer with format: int64: This will contain the long type (signed 64-bit integer)
• type: string with format: date: This will contain the date as per RFC 3339 – for example, 2020-10-22
• type: string with format: byte: This will contain the Base64-encoded values
• type: string with format: binary: This will contain the binary data (and can be
used for files)
```

类型的引用
```sh
$ref: '#/components/schemas/{type}'
```

也可以引用别的文件
```sh
# Relative Schema Document
$ref: Cart.yaml
# Relative Document with embedded Schema
$ref: definitions.yaml#/Cart
```

---
## Path section
![[Pasted image 20231028190037.png|975]]
## chapter3 build gradle project
```gradle
id 'org.hidetake.swagger.generator' version '2.19.2'
```
openapi.yaml定义了api的结构，model的结构。
plugin根据这个文件生成 代码，以及swagger ui

### 依赖

```json
plugins {
    id 'org.springframework.boot' version '3.0.1'
    id 'io.spring.dependency-management' version '1.1.0'
    id 'java'
    id 'org.hidetake.swagger.generator' version '2.19.2'
}
dependencies {
    // OpenAPI Starts
    swaggerCodegen 'org.openapitools:openapi-generator-cli:6.2.1'
    swaggerUI 'org.webjars:swagger-ui:3.52.5'
    compileOnly 'io.swagger:swagger-annotations:1.6.4'
    compileOnly 'org.springframework.boot:spring-boot-starter-validation'
    compileOnly 'org.openapitools:jackson-databind-nullable:0.2.3'
    implementation 'com.fasterxml.jackson.dataformat:jackson-dataformat-xml'
    implementation 'org.springframework.boot:spring-boot-starter-hateoas'
    // required for schema in swagger generated code
    implementation 'io.springfox:springfox-oas:3.0.0'
    // OpenAPI Ends
    implementation 'org.springframework.boot:spring-boot-starter-web'
    implementation 'javax.servlet:javax.servlet-api:4.0.1'
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
}
```

### 生成代码

``./gradlew generateSwaggerCode``
config.json
```json
{
  "library": "spring-boot",
  "dateLibrary": "java8",
  "hideGenerationTimestamp": true,
  "modelPackage": "com.packt.modern.api.model",
  "apiPackage": "com.packt.modern.api",
  "invokerPackage": "com.packt.modern.api",
  "serializableModel": true,
  "useTags": true,
  "useGzipFeature" : true,
  "hateoas": true,
  "unhandledException": true,
  "useSpringBoot3": true,
  "useSwaggerUI": true,
  "importMappings": {
    "ResourceSupport":"org.springframework.hateoas.RepresentationModel",
    "Link": "org.springframework.hateoas.Link"
  }
}
```

```json
swaggerSources {
    def typeMappings = 'URI=URI'
    def importMappings = 'URI=java.net.URI'
    eStore {
        def apiYaml = "${rootDir}/src/main/resources/api/openapi.yaml"
        def configJson = "${rootDir}/src/main/resources/api/config.json"
        inputFile = file(apiYaml)
        def ignoreFile = file("${rootDir}/src/main/resources/api/.openapi-generator-ignore")
        code {
            language = 'spring'
            configFile = file(configJson)
            rawOptions = ['--ignore-file-override', ignoreFile, '--type-mappings',
                          typeMappings, '--import-mappings', importMappings] as List<String>
            components = [models: true, apis: true, supportingFiles: 'ApiUtil.java']
            dependsOn validation
        }
    }
}

compileJava.dependsOn swaggerSources.eStore.code
sourceSets.main.java.srcDir "${swaggerSources.eStore.code.outputDir}/src/main/java"
sourceSets.main.resources.srcDir "${swaggerSources.eStore.code.outputDir}/src/main/resources"
```

### 生成swagger ui

可用task调起来也可指令单独运行 

``./gradlew generateSwaggerUI :generateSwaggerUIEStore``

```json
swaggerSources {
    eStore {
        inputFile = file("${rootDir}/src/main/resources/api/openapi.yaml")
    }
}

task deleteSwaggerUI(type: Delete) {
    delete "${rootDir}/src/main/resources/static/swagger-ui"
}

task moveSwaggerUI(type: Copy) {
    dependsOn generateSwaggerUI
    dependsOn deleteSwaggerUI
    from "${rootDir}/build/swagger-ui-eStore"
    into "${rootDir}/src/main/resources/static/swagger-ui"
}

processResources {
    dependsOn generateSwaggerCode
    dependsOn moveSwaggerUI
}
```

