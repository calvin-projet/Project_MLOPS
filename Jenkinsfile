// pipeline {
//     agent any

//     stages {
//         stage('Build') {
//             steps {
//                 sh 'docker build -t my-anime-app .'
//             }
//         }

//         stage('Test') {
//             steps {
//                 sh 'docker run --rm my-anime-app python -m unittest discover -v tests'
//             }
//         }

//         stage('Push') {
//             steps {
//                 withCredentials([usernamePassword(credentialsId: 'docker-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
//                     sh "docker login -u $DOCKER_USER -p $DOCKER_PASS"
//                     sh "docker tag my-anime-app my-registry/my-anime-app:$BUILD_NUMBER"
//                     sh "docker push my-registry/my-anime-app:$BUILD_NUMBER"
//                 }
//             }
//         }

//         stage('Deploy') {
//             steps {
//                 sshagent(['ssh-key']) {
//                     sh 'ssh -o StrictHostKeyChecking=no user@my-server "docker pull my-registry/my-anime-app:$BUILD_NUMBER"'
//                     sh 'ssh -o StrictHostKeyChecking=no user@my-server "docker stop my-anime-app || true"'
//                     sh 'ssh -o StrictHostKeyChecking=no user@my-server "docker rm my-anime-app || true"'
//                     sh 'ssh -o StrictHostKeyChecking=no user@my-server "docker run -d --name my-anime-app -p 5000:5000 my-registry/my-anime-app:$BUILD_NUMBER"'
//                 }
//             }
//         }
//     }
// }