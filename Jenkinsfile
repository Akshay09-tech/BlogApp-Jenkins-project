pipeline {
    agent any

    environment {
        DOCKER_HUB = "akshaychhallare"
        EC2_HOST = "<EC2-2-PUBLIC-IP>"
    }

    stages {

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh 'echo $PASS | docker login -u $USER --password-stdin'
                }
            }
        }

        stage('Build Backend') {
            steps {
                sh 'docker build -t $DOCKER_HUB/blog-backend:latest backend/'
            }
        }

        stage('Build Frontend') {
            steps {
                sh 'docker build -t $DOCKER_HUB/blog-frontend:latest frontend/'
            }
        }

        stage('Push Images') {
            steps {
                sh 'docker push $DOCKER_HUB/blog-backend:latest'
                sh 'docker push $DOCKER_HUB/blog-frontend:latest'
            }
        }

        stage('Deploy to K8s') {
            steps {
                sshagent(['ec2-ssh']) {
                    sh '''
                    ssh -i /var/lib/jenkins/mumbai-key-pair.pem ec2-user@$EC2_HOST "
                    cd blog-k8s &&
                    kubectl apply -f . &&
                    kubectl rollout restart deployment backend &&
                    kubectl rollout restart deployment frontend
                    "
                    '''
                }
            }
        }
    }
}
