pipeline {
    agent any
    
    environment {
        MESSAGE='hello!'
    }

    stages {
        stage('Hello') {
            agent {
                docker 'alpine'
            }
            steps {
                sh 'uname -a'
            }
        }
    }
    post {
        success {
            archiveArtifacts artifacts : '**'
        }
    }
}
