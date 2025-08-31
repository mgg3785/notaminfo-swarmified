pipeline {
    agent any
    
    environment {
        MESSAGE='hello!'
    }

    stages {
        stage('Build') {
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
