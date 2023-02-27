pipeline {
    agent any     stages {
        stage('Build') {
            steps {
                sh 'docker build -t myapp .'
            }
        }         stage('Test') {
            steps {
                sh 'docker run --rm myapp python -m pytest'
            }
        }         stage('Push') {
            steps {
                sh 'docker tag myapp myusername/myapp'
                sh 'docker push myusername/myapp'
            }
        }         stage('Deploy') {
            steps {
                sh 'docker pull myusername/myapp'
                sh 'docker run --rm -d -p 8090:8090 myusername/myapp'
            }
        }
    }
}
