pipeline {
  agent any
   stages {
        stage('Checkout') {
            steps {
            deleteDir()
            checkout scm
            }
        }
	stage ('DID - Build Producer') {
	steps {
		withCredentials([usernamePassword(credentialsId: 'DOCKERHUB', passwordVariable: 'HUBPASSWORD', usernameVariable: 'HUBUSER')]) {
    podTemplate(yaml: '''
    apiVersion: v1
    kind: Pod
    spec:
      containers:
      - name: docker
        image: docker:19.03.1
        command:
        - sleep
        args:
        - 99d
        env:
          - name: DOCKER_HOST
            value: tcp://localhost:2375
      - name: docker-daemon
        image: docker:19.03.1-dind
        securityContext:
          privileged: true
        env:
          - name: DOCKER_TLS_CERTDIR
            value: ""
    ''') {
		node(POD_LABEL) {
			git 'https://github.com/jenkinsci/docker-jnlp-slave.git'
			container('docker') {
			sh 'echo $HUBPASSWORD | docker login ghcr.io -u $HUBUSER --password-stdin'
			sh 'apk add git curl bash openssl  --no-cache'
			sh 'curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"'
			sh 'chmod +x ./kubectl && mv ./kubectl /usr/local/bin/kubectl '
            sh' curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 && chmod +x get_helm.sh && ./get_helm.sh'
			sh 'git config --global user.name "$HUBUSER"'
            sh 'git config --global user.email "ofirs@checkpoint.com"'
			sh 'chown -R 1000:1000 *'
			dir ('$WORKSPACE/Bonuses/consumer'){
          	sh 'docker build -f Dockerfile -t ghcr.io/$HUBUSER/consumer:latest  . '
			}
			sh 'docker push ghcr.io/$HUBUSER/consumer:latest'
			dir ('$WORKSPACE/Bonuses/producer'){
          	sh 'docker build -f Dockerfile -t ghcr.io/$HUBUSER/producer:latest  . '
			}
			sh 'docker push ghcr.io/$HUBUSER/producer:latest'
          	sh 'docker logout'
			}
		}
	}
	}
	}
	}
	}
	}