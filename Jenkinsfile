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
                    docker compose -f "compose.test.yaml" up -d
                    docker ps
                    docker compose -f "compose.test.yaml" logs > docker-test.logs
                    docker compose -f "compose.test.yaml" exec -T django uv run pytest
                    docker compose -f "compose.test.yaml" down --volumes
                    '''
            }
        }
        stage('deploy') {
            steps {
                sh '''
                    export COMPOSE_ENV_FILES=.env.test
                    docker tag notaminfo:latest registry:5000/mahdi/notaminfo:latest
                    eval "$(ssh-agent -s)"
                    ssh-add $JSSH_KEY
                    ssh $JSSH_OPTIONS root@node0 "rm -rf /registry-data/docker/registry/v2/repositories/*"
                    docker push registry:5000/mahdi/notaminfo:latest
                    ssh $JSSH_OPTIONS root@node0 "mkdir -p /app && chmod 755 /app"
                    scp $JSSH_OPTIONS compose.deploy.yaml .env.test root@node0:/app/
                    ssh $JSSH_OPTIONS root@node0 /bin/sh << EOT
                    export COMPOSE_ENV_FILES=$COMPOSE_ENV_FILES
                    cd /app
                    docker compose up -d
                    docker stack deploy --compose-file compose.deploy.yaml notaminfostack
                    sleep 10
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
