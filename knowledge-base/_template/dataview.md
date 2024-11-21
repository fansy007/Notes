![[Pasted image 20231008004810.png]]
```dataview
table file.ctime, file.mtime, file.keyword
from 
"basic" where contains(file.name, "lamda")
sort file.ctime desc
```


```dataview
table file.ctime, file.mtime, file.path
from 
"" where contains(file.tags, "java")
sort file.ctime desc
```



