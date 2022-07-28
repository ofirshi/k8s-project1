pipeline {
  agent any
   stages {
        stage('Checkout') {
            steps {
            deleteDir()
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
            git branch: 'main', url: 'https://github.com/ofirshi/k8s-project1.git'
            sh 'git clone https://github.com/ofirshi/k8s-project1.git'
          	sh 'chown -R 1000:1000 *'
            sh 'cd ${workspace}/k8s-project1/Bonuse/consumer/ && DOCKER_BUILDKIT=1 docker build  --no-cache --progress=plain  --label=consumer --tag=ghcr.io/$HUBUSER/consumer:latest . '
          	sh 'cd ${workspace}/k8s-project1/Bonuse/producer/ && DOCKER_BUILDKIT=1 docker build  --no-cache --progress=plain  --label=producer --tag=ghcr.io/$HUBUSER/producer:latest . '
            sh 'docker image  push ghcr.io/$HUBUSER/consumer:latest'
			sh 'docker image  push ghcr.io/$HUBUSER/producer:latest'
          	sh 'docker logout'
			}
		}
	}
	}
	}
	}
     stage('Install Helm Chart') {
            steps {
            sh 'apk add git curl bash openssl  --no-cache'
            sh' curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 && chmod +x get_helm.sh && ./get_helm.sh'
            git branch: 'main', url: 'https://github.com/ofirshi/k8s-project1.git'
            sh 'git clone https://github.com/ofirshi/k8s-project1.git'
          	sh 'cd k8s-project1/helm/consumer && helm dependency update && helm dependency build && helm upgrade --install consumer . '
            }
	}
	}
    }