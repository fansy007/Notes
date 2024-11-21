#cloud 
[[docker2023]] [[docker & k8s]]
```html
- docker login artifactory
- docker pull base image
- docker run Dockerfile
- oc

- 使用light speed创建project， isgclient, 它会在bitbucket中创建repo (默认进行了一些设置)，并在ucd3中创建一个component（用来deploy）
- 用户写自己得代码， 写完之后需要提供Jenksifile, Dockerfile, deploy folder (needed params files, the main entrance bash script)
- 由于你提供了了Jenkinsfile文件，那么在push道bitbucket之后，默认会调用 jenkins 去build这个project，build包含了多个阶段， （初始化， build jar, build image, deploy, push to ucd, done）
- 然后在结束之后你在ucd3会发现isgclient会有一个新的版本了， 然后你去deploy道UAT进行测试， 测试没有问题，你对这个版本的status mark as test, 然后deploy prod
```


