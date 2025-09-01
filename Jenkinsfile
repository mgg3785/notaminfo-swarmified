pipeline {
    agent any
    
    environment {
        MESSAGE='hello!'
    }

    stages {
        stage('Build') {
            steps {
                sh '''
                    docker build -t notaminfo -f "notaminfo.Dockerfile" .
                    docker image ls
                '''
            }
        }
        stage('test') {
            steps {
                sh '''
                    docker compose -f "compose.yaml" up -d
                    docker ps
                    docker compose exec -T django uv run pytest
                    docker compose down
                    '''
            }
        }
        stage('deploy') {
            steps {
                sh '''
                    docker save notaminfo -o notaminfo.tar
                    yes | scp notaminfo.tar root@deploy-server
                    ssh root@deploy-server
                    docker load -i notaminfo.tar

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
