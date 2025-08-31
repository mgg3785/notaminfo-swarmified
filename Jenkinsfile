pipeline {
    agent any
    
    environment {
        MESSAGE='hello!'
    }

    stages {
        stage('Build') {
            agent {
                docker 'docker'
            }
            steps {
                sh 'docker build -t notaminfo -f "notaminfo.Dockerfile" .'
            }
        }
    }
    post {
        success {
            archiveArtifacts artifacts : '**'
        }
    }
}
