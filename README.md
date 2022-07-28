## About K8s RabbitMQ project

The project infrastructure is based on a queueing mechanism implemented using RabbitMQ.

This is the meaning of each component in the system:
1. Producer - will send messages every X seconds to a queue found in rabbitmq server.
2. RabbitMQ - an application that is able to store data in a queue fashion allowing us to
have the ability to maintain a queue of messages
3. Consumer - will listen to new messages on a queue in RabbitMQ server and will print
them to STDOUT.

![alt text](https://github.com/ofirshi/k8s-project1/blob/main/Kubernetes_Project.jpg?raw=true)


# Prerequisites

1. Jenkins Installed (https://github.com/jenkinsci/helm-charts/blob/main/charts/jenkins/VALUES_SUMMARY.md)
2. Minikube / Kubernetes Cluster
3. Docker Hub Account (https://hub.docker.com/) / Github registry (https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)


# Install & config gcloud
https://cloud.google.com/sdk/docs/install




# Bare Metal:
sudo curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

sudo curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

sudo install minikube-linux-amd64 /usr/local/bin/minikube

sudo curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

yum install conntrack git wget -y

git clone https://github.com/Mirantis/cri-dockerd.git

wget https://storage.googleapis.com/golang/getgo/installer_linux

wget https://storage.googleapis.com/golang/getgo/installer_linux

chmod +x ./installer_linux

./installer_linux

source ~/.bash_profile

cd cri-dockerd

mkdir bin

go get && go build -o bin/cri-dockerd

mkdir -p /usr/local/bin

install -o root -g root -m 0755 bin/cri-dockerd /usr/local/bin/cri-dockerd

cp -a packaging/systemd/* /etc/systemd/system

sed -i -e 's,/usr/bin/cri-dockerd,/usr/local/bin/cri-dockerd,' /etc/systemd/system/cri-docker.service

systemctl daemon-reload

systemctl enable cri-docker.service

systemctl enable --now cri-docker.socket

cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo

[kubernetes]

name=Kubernetes

baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-\$basearch

enabled=1

gpgcheck=1

gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg

exclude=kubelet kubeadm kubectl

EOF

# Set SELinux in permissive mode (effectively disabling it)

sudo setenforce 0

sudo sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

sudo yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes

sudo systemctl enable --now kubelet


sudo -E /usr/local/bin/minikube start --driver=none --kubernetes-version=stable --v=5 --alsologtostderr --extra-config=kubelet.cgroup-driver=systemd,kubeadm.ignore-preflight-errors=SystemVerification

### Modify settings:
minikube config set cpus 4

minikube config set memory 8196

minikube config set disk-size 10240MB

minikube config set WantUpdateNotification false

minikube stop

minikube delete --all=true --purge=true

docker rm -v $(docker ps --filter status=exited -q)

docker image prune -a -f



# Docker login:

docker login --username=<user> --password-stdin <<<'password'

OR:

https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry



# Create images:

DOCKER_BUILDKIT=1 docker build  --no-cache --progress=plain  --label=consumer --tag=ghcr.io/chkp-ofirs/consumer:latest .

docker push ghcr.io/chkp-ofirs/consumer:latest

docker image rm ghcr.io/chkp-ofirs/consumer:latest


DOCKER_BUILDKIT=1 docker build  --no-cache --progress=plain  --label=producer --tag=ghcr.io/chkp-ofirs/producer:latest .

docker push ghcr.io/chkp-ofirs/producer:latest

docker image rm ghcr.io/chkp-ofirs/producer:latest



docker run  --rm -p 9422 -it ghcr.io/chkp-ofirs/consumer:latest /bin/bash

docker run  --rm -it ghcr.io/chkp-ofirs/producer:latest /bin/bash



# Helm Chart:

helm uninstall consumer --dry-run
                                                    
helm uninstall consumer

helm uninstall rabbitmq 

helm repo remove bitnami

kubectl delete pvc --all 

kubectl delete pv --all 

helm dependency update && helm dependency build && helm upgrade --install consumer . --wait --cleanup-on-fail --atomic --dry-run
                                                   
helm dependency update && helm dependency build && helm upgrade --install consumer . --wait --cleanup-on-fail --atomic


# Jenkins Install

(https://devopscube.com/setup-jenkins-on-kubernetes-cluster/)

helm repo remove jenkins
helm uninstall jenkins
kubectl delete serviceaccount jenkins
kubectl delete clusterrolebinding.rbac.authorization.k8s.io jenkins
cat<<EOF >>jenkins-rbac-admin.yaml  
apiVersion: v1
kind: ServiceAccount
metadata:
  name: jenkins
  namespace: default
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: jenkins
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
  - kind: ServiceAccount
    name: jenkins
    namespace: default
EOF
kubectl apply -f jenkins-rbac-admin.yaml

helm repo add jenkins https://charts.jenkins.io

helm repo update

helm upgrade --install jenkins jenkins/jenkins --set controller.adminPassword=EfpkNXuBNyBm7Xbw,controller.installLatestSpecifiedPlugins=false,controller.serviceType=NodePort,serviceAccount.name=jenkins,serviceAccountAgent.name=jenkins --wait --cleanup-on-fail --atomic

kubectl --namespace default port-forward svc/jenkins 8080:8080 --address=0.0.0.0
