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
                    ssh-keyscan -H ${SSH_HOST} > ~/.ssh/known_hosts
                    scp notaminfo.tar root@deploy-server:/app
                    scp compose.yaml root@deploy-server:/app
                    ssh -T -o StrictHostKeyChecking=no root@deploy-server /bin/sh << EOT
                    cd /app
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
