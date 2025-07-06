pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDS = credentials('dockerhub-creds') // Jenkins credentials ID
        IMAGE_NAME = "yourdockerhubusername/mindbloom-app"
    }

    stages {

        stage('📦 Clone Repo') {
            steps {
                git 'https://github.com/your-username/mindbloom.git'
            }
        }

        stage('✅ Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('🧪 Run Pytest') {
            steps {
                sh 'pytest tests/'
            }
        }

        stage('🐳 Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('🔐 Docker Login') {
            steps {
                sh "echo $DOCKER_HUB_CREDS_PSW | docker login -u $DOCKER_HUB_CREDS_USR --password-stdin"
            }
        }

        stage('📤 Push Image to Docker Hub') {
            steps {
                sh 'docker push $IMAGE_NAME'
            }
        }

        stage('🚀 Deploy (Run Locally)') {
            steps {
                sh 'docker run -d -p 7860:7860 $IMAGE_NAME'
            }
        }
    }

    post {
        failure {
            echo '❌ Build Failed!'
        }
        success {
            echo '✅ Successfully Deployed MindBloom!'
        }
    }
}
