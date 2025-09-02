pipeline {
    agent any
    environment {
        SSH_OPTIONS='-o StrictHostKeyChecking=no -i /home/jenkins/.ssh/id_ed25519'
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
                    scp $SSH_OPTIONS notaminfo.tar root@deploy-server:/app
                    scp $SSH_OPTIONS compose.yaml root@deploy-server:/app
                    ssh -T $SSH_OPTIONS root@deploy-server /bin/sh << EOT
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
