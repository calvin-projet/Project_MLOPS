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
    stage('Deploy') {
      steps {
        sh 'docker pull calv20/myapp'
        sh 'docker run --rm -d -p 8090:8090 calv20/myapp'
      }
    }
  }
}
