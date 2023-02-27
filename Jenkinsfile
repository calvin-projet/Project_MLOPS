pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh 'docker build -t myapp .'
      }
    }
    stage('Test') {
      steps {
        sh 'docker run --rm myapp python -m pytest'
      }
    }
    stage('Push') {
      steps {
        sh 'docker tag myapp calv20/myapp'
        sh 'docker push calv20/myapp'
      }
    }
    stage('Pushing to Dockerhub')
      steps {
         sh 'docker push calv20/api-prediction-image:latest'
         sh 'docker push calv20/frontend-prediction-image:latest'
         }
     }
  }
}
