podTemplate(yaml: '''
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: docker
    image: docker:19.03.1-dind
    securityContext:
      privileged: true
    env:
      - name: DOCKER_TLS_CERTDIR
        value: ""
''') {
    node(POD_LABEL) {
        stage ('Docker-Login')
        container('docker')
        {
		withCredentials([usernamePassword(credentialsId: 'DOCKERHUB', passwordVariable: 'HUBPASSWORD', usernameVariable: 'HUBUSER')]) {
                         sh '''
                         echo $HUBPASSWORD | docker login ghcr.io -u $HUBUSER --password-stdin
                         '''
                    }
        }
        stage ('Docker-Build'){
        git branch: 'main', url: 'https://github.com/ofirshi/k8s-project1.git'
        container('docker') {
            sh '''
            pwd
            ls -lath *
            cd $WORKSPACE/Bonuses/consumer/ && DOCKER_BUILDKIT=1 docker build  --no-cache --progress=plain  --label=consumer --tag=ghcr.io/chkp-ofirs/consumer:latest . 
            cd $WORKSPACE/Bonuses/producer/ && DOCKER_BUILDKIT=1 docker build  --no-cache --progress=plain  --label=producer --tag=ghcr.io/chkp-ofirs/producer:latest . 
	        docker image  push ghcr.io/chkp-ofirs/consumer:latest
			docker image  push ghcr.io/chkp-ofirs/producer:latest
          	docker logout
            '''
			
        }
        }
    }
}