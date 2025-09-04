pipeline {
    agent any
    environment {
        JSSH_OPTIONS='-o StrictHostKeyChecking=no'
        JSSH_KEY='/var/.ssh/id_ed25519'
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
                    eval "$(ssh-agent -s)"
                    ssh-add $JSSH_KEY
                    ssh $JSSH_OPTIONS root@deploy-server "mkdir -p /app && chmod 755 /app"
                    scp $JSSH_OPTIONS notaminfo.tar root@deploy-server:/app/
                    scp $JSSH_OPTIONS compose.yaml root@deploy-server:/app/
                    ssh $JSSH_OPTIONS root@deploy-server /bin/bash << EOT
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
