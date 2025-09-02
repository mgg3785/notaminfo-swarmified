pipeline {
    agent any

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
                    export COMPOSE_ENV_FILES=./.env.test
                    docker compose -f "compose.yaml" up -d
                    docker ps
                    docker compose logs > docker-test.logs
                    docker compose exec -T django uv run pytest
                    docker compose down
                    '''
            }
        }
        stage('deploy') {
            steps {
                sh '''
                    export COMPOSE_ENV_FILES=.env.test
                    docker save notaminfo -o notaminfo.tar
                    yes | scp notaminfo.tar root@deploy-server
                    scp compose.yaml root@deploy-server
                    ssh -T -o StrictHostKeyChecking=no root@deploy-server /bin/sh << EOT
                    docker load -i notaminfo.tar
                    docker compose up -d
                    sleep 10
                    docker compose logs > docker-deploy.logs
                    EOT
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
