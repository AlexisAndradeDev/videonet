pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Construye la imagen de Docker
                    bat 'docker-compose -f docker-compose.dev.yml build'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Ejecuta las pruebas de Django
                    bat 'docker-compose -f docker-compose.dev.yml run web python videonet_project/manage.py test videonet_project/'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Despliega la aplicación usando Docker Compose
                    bat 'docker-compose -f docker-compose.dev.yml up -d'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completada con éxito.'
            bat 'docker-compose -f docker-compose.dev.yml down --remove-orphans'
        }
        failure {
            echo 'Pipeline falló.'
            bat 'docker-compose -f docker-compose.dev.yml down --remove-orphans'
        }
    }
}