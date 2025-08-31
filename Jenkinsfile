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
                sh '''
                    sudo usermod -a -G docker jenkins
                    docker build -t notaminfo -f "notaminfo.Dockerfile" .
                    '''
            }
        }
    }
    post {
        success {
            archiveArtifacts artifacts : '**'
        }
    }
}
