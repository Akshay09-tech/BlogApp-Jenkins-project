pipeline {
    agent any
    environment {
        DOCKERHUB_USER = 'akshaychhallare'
        IMAGE_BACKEND  = "${DOCKERHUB_USER}/blog-backend"
        IMAGE_FRONTEND = "${DOCKERHUB_USER}/blog-frontend"
    }
    stages {
<<<<<<< HEAD

        stage('Docker Login') {
=======
        stage('Pull Code') {
            steps {
                echo 'Code pulled from GitHub'
            }
        }
        stage('Build Docker Images') {
>>>>>>> bd7dbdd (jenkins update)
            steps {
                sh "docker build -t ${IMAGE_BACKEND}:latest ./backend"
                sh "docker build -t ${IMAGE_FRONTEND}:latest ./frontend"
            }
        }
        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh "docker push ${IMAGE_BACKEND}:latest"
                    sh "docker push ${IMAGE_FRONTEND}:latest"
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                sh "kubectl apply -f k8s/"
                sh "kubectl rollout restart deployment/backend"
                sh "kubectl rollout restart deployment/frontend"
            }
        }
    }
    post {                          // ✅ HERE — outside stages
        success { echo 'Done!' }
        failure { echo 'Failed — check logs' }
    }
}
