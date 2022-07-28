pipeline {
      agent { kubernetes { 
            label 'local'

        }}
    stages {
        stage('install kubectl and Helm') {
            steps { 
                sh '''
			    curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"'
			    chmod +x ./kubectl && mv ./kubectl /usr/local/bin/kubectl '
                curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 && chmod +x get_helm.sh && ./get_helm.sh'
                rm -rf k8s-project1/
                '''
                
            }
        }
        stage('Deploy helm chart') {
            steps { 
                sh '''
                git clone https://github.com/ofirshi/k8s-project1
                cd $WORKSPACE/helm/consumer 
                helm dependency update && helm dependency build && helm upgrade --install consumer .
                '''
            }
        }

    }
}