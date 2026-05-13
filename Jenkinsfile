pipeline {
    agent any

    stages {

        stage('Code Build') {
            steps {
                echo 'Building Docker image for Flask web application...'
                sh 'docker build -t flask-webapp:latest .'
            }
        }

        stage('Unit Testing') {
            steps {
                echo 'Running unit test cases...'
                sh 'pip3 install -r requirements.txt || true'
                sh 'python3 -m pytest tests/'
            }
        }

        stage('Containerized Deployment') {
            steps {
                echo 'Deploying Flask application in Docker container...'
                sh 'docker rm -f webapp || true'
                sh 'docker run -d --name webapp -p 5000:5000 flask-webapp:latest'
            }
        }

        stage('Containerized Selenium Testing') {
            steps {
                echo 'Building Selenium test Docker image...'
                sh 'docker build -t selenium-tests:latest selenium_tests/'

                echo 'Running Selenium test container...'
                sh 'docker network create test-network || true'
                sh 'docker network connect test-network webapp || true'
                sh 'docker run --rm --network test-network selenium-tests:latest'
            }
        }
    }

    post {
        success {
            echo 'CI/CD Pipeline executed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check console output for errors.'
        }
    }
}