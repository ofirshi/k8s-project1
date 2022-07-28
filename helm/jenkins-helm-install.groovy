// https://gbengaoni.com/blog/Kubernetes-CI-CD-with-Helm-and-Jenkins
podTemplate(label: 'mypod', serviceAccount: 'jenkins', containers: [
    containerTemplate(
      name: 'docker', 
      image: 'docker', 
      command: 'cat', 
      resourceRequestCpu: '100m',
      resourceLimitCpu: '300m',
      resourceRequestMemory: '300Mi',
      resourceLimitMemory: '500Mi',
      ttyEnabled: true
    ),

    containerTemplate(
      name: 'kubectl', 
      image: 'bitnami/kubectl',
      resourceRequestCpu: '100m',
      resourceLimitCpu: '300m',
      resourceRequestMemory: '300Mi',
      resourceLimitMemory: '500Mi', 
      ttyEnabled: true, 
      command: 'cat'
    ),
    containerTemplate(
      name: 'helm', 
      image: 'rancher/helm-controller:v0.12.3', 
      resourceRequestCpu: '100m',
      resourceLimitCpu: '300m',
      resourceRequestMemory: '300Mi',
      resourceLimitMemory: '500Mi',
      ttyEnabled: true, 
      command: 'cat'
    )
  ],

  volumes: [
    hostPathVolume(mountPath: '/var/run/docker.sock', hostPath: '/var/run/docker.sock'),
    hostPathVolume(mountPath: '/usr/local/bin/helm', hostPath: '/usr/local/bin/helm')
  ]
  ) {
    node('mypod') {
        stage('Check running containers') {
            container('helm') { 
                sh '''
                helm repo add bitnami https://charts.bitnami.com/bitnami
                helm repo update
                apk add git
                git clone https://github.com/ofirshi/k8s-project1
                cd k8s-project1/helm/consumer 
                helm dependency update && helm dependency build && helm upgrade --install consumer .
                '''
            }
        }         
    }
}
