pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS = credentials('dockerhub-creds')  // Jenkins DockerHub creds ID
        IMAGE_NAME = "karvy192003/mindbloom-app"
    }

    stages {

        stage('📁 Clone Repo') {
            steps {
                git 'https://github.com/Karvy192003/karviii.git'
            }
        }

        stage('📦 Setup & Install Requirements') {
            steps {
                dir('main') {
                    sh 'pip install --upgrade pip'
                    sh 'pip install -r requirements.txt'
                }
            }
        }

        stage('🧪 Run Tests') {
            steps {
                dir('main') {
                    sh 'pytest tests/'
                }
            }
        }

        stage('🐳 Build Docker Image') {
            steps {
                dir('main') {
                    sh 'docker build -t $IMAGE_NAME .'
                }
            }
        }

        stage('🔐 Login to Docker Hub') {
            steps {
                sh "echo $DOCKER_CREDENTIALS_PSW | docker login -u $DOCKER_CREDENTIALS_USR --password-stdin"
            }
        }

        stage('📤 Push Docker Image') {
            steps {
                dir('main') {
                    sh 'docker push $IMAGE_NAME'
                }
            }
        }

        stage('🚀 Run Container') {
            steps {
                // Optional: Stop existing container if running
                sh 'docker stop mindbloom || true'
                sh 'docker rm mindbloom || true'

                // Run new container
                sh 'docker run -d --name mindbloom -p 7860:7860 $IMAGE_NAME'
            }
        }
    }

    post {
        success {
            echo '✅ MindBloom deployed successfully!'
        }
        failure {
            echo '❌ Build failed. Please check logs.'
        }
    }
}
