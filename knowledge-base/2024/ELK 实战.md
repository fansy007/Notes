#cloud #ELK

# QUERY DSL

查多条
```sh
GET /account/_search
{
  "query": {
    "match_all": {}
  },
  "sort": [
    {
      "account_number": "asc"
    },
    {
      "balance": "desc"
    }
  ],
  "size": 100,
  "from": 0
}
```

查一个非字符串是精确匹配
```sh
GET /account/_search
{
  "query": {
    "match": {
      "account_number": 100
    }  
  }
}
```


>[!note]+ 完全匹配用keyword 
match_phrase 查文本不分词，但也不是完全匹配
	例如 address=“123 456 789”
	 match_phrase "123 456"会 hit
	 keyword “123 456”不会 hit	

term用来查非String的精确查询
其他情况下会分词匹配
```sh
GET /account/_search
{
  "query": {
    "match": {
      "address.keyword": "282 Kings Place"
    }  
  }
}
```

bool - must[] must中的所有条件是and关系
```sh
GET /account/_search
{
  "query": {
    "bool": {
      "must": [
        {"match": {
          "address": "Kings"
        }},
        {"match": {
          "address": "305"
        }}
      ]
    }
  }
}
```

boolean - should[] should中的所有条件是or关系
```sh
GET /account/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "range": {
            "account_number": {
              "lte": 30
            }
          }
        },{
          "range": {
            "account_number": {
              "gte": 100
            }
          }
        }
      ]
    }
  }
}
```

范围查找
```sh

GET /account/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "range": {
            "account_number": {
              "lte": 30
            }
          }   
        }
      ]  
    }
  }
```

正则
地址以数字开头的记录
```sh
GET /account/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "regexp": {
            "address": "\\d.*"
          }
          
        }
      ]
      
    }
  }
}
```

# 聚合
aggs
自定义名，选类型
terms做count
avg求平均

size 0 不现实记录只看agg信息
```sh
GET /account/_search
{
  "query": {
    "regexp": {
      "address": "\\d.*"
    }
  },
  "aggs": {
    "count": {
      "terms": {
        "field": "age"
      }
    },
    "avgAge": {
      "avg": {
        "field": "age"
      }
    }
  },
  "size": 0
}
```

terms之下还可以子聚合，算每个group的平均值
```sh
GET /account/_search
{
  "query": {
    "regexp": {
      "address": "\\d.*"
    }
  },
  "aggs": {
    "count": {
      "terms": {
        "field": "age"
      },
      "aggs": {
        "avgBalance": {
          "avg": {
            "field": "balance"
          }
        }
      }
    }
  },
  "size": 0
}
```

# 看字段类型 
GET /account/_mapping

# index迁移
迁移后原index会被删除

先建立新index
PUT /bank

迁移
```sh
POST _reindex
{
  "source": {
    "index": "account"
  },
  "dest": {
    "index": "bank"
  }
}
```