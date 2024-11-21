# Build

```json
stages {
  stage("build") {
    steps {
      echo 'building the application'
    }
  }
}
```



# When EXP

```json
stage("test") {
  when {
  	expression {
  		BRANCH_NAME == 'dev' || BRANCH_NAME== 'master'
		}
	}
  steps {
    echo 'test the application...'
  }
}
```



# ENV params

Localhost:8080/env-vars.html/      -- system env



```json
pipline {
  environment {
  	NEW_VERSION= ‘1.3’
	}

	stages {
    stage("build") {
      echo "${NEW_VERSION}"
    }
  }
}
```



define a credential @ jekins webpage and use it ( you set name server-credential)



```json
pipline {
  environment {
	}
  
	stages {
    stage("build") {
    	steps {
        withCredentials([
          // fetch username password
          usernamePassword(credentials: 'server-credential', usernameVariable: USER, passwordVariable: PWD)
        ]) {
          sh "some script: ${USER} ${PWD}"
          
        }
      }
  	}
  }
}
```



# params

Web page can pass params, and jekins file use it

![image-20230910083903535](image-20230910083903535.png)

```json
pipline {
  parameters {
  	string(name: 'VERSION', defaultValue: '1.0', description: '')
		choice(name: 'VERSION', choices: ['1.0', '2.0'], description: '')
		booleanParam(name: 'exeTests', defaultValue: true, deccrption: '')
	}

	stages {
    
    stage("build") {
      when {
        expression {
       		params.exeTests   
        }
        steps {
          echo 'start test....'
        }
      }
    }
  }
  
}
```



# groovy



```json
steps {
  stages {
  	stage("init") {
      script {
        // write groovy here
        gv =load "script.groovy "
      }
    }

		stage("build") {
      script {
      	gv.buildApp()
    	}
    }
  
	}

}
```



In scritp.groovy define functions

```groovy
def builApp() {
  echo 'build ....'
}
```

