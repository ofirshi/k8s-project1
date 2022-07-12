# k8s-project1

# Prerequisites

1. Jenkins Installed (https://github.com/jenkinsci/helm-charts/blob/main/charts/jenkins/VALUES_SUMMARY.md)
2. Minikube / Kubernetes Cluster
3. Docker Hub Account (https://hub.docker.com/) / Github registry (https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)


# Install & config gcloud
https://cloud.google.com/sdk/docs/install

# Create GCP VM
gcloud compute --project=<GCP_PRJ> firewall-rules create anyall --direction=INGRESS --priority=100 --network=default --action=ALLOW --rules=all --source-ranges=0.0.0.0/0 --target-tags=any

gcloud compute disks create stagingdisk --image-project centos-cloud --image-family centos-7 --zone us-east1-b --project=<GCP_PRJ>

gcloud compute images create nested-vm-image --source-disk=stagingdisk --source-disk-zone=us-east1-b --licenses=https://www.googleapis.com/compute/v1/projects/vm-options/global/licenses/enable-vmx  --project=<GCP_PRJ>

gcloud compute disks delete stagingdisk --zone us-east1-b  --project=<GCP_PRJ> -q

gcloud compute instances create nested-vm-image1 --zone us-east1-b --min-cpu-platform "Intel Haswell" --machine-type n1-standard-16 --image nested-vm-image  --project=<GCP_PRJ> --boot-disk-size=300GB --enable-display-device --boot-disk-type=pd-ssd --tags=any --can-ip-forward --metadata serial-port-enable=TRUE

gcloud compute ssh nested-vm-image1 --zone=us-east1-b






# Install Software:
sudo yum install -y kubectl

sudo mkdir kubectl

sudo chmod +x kubectl

sudo mv ./kubectl /usr/local/bin/kubectl

sudo yum install kernel-headers-$(uname -r) kernel-devel kernel-devel-$(uname -r) kernel-headers make patch gcc wget conntrack -y

sudo yum install qemu-kvm libvirt libvirt-python libguestfs-tools virt-install -y

sudo modprobe -r kvm_intel

sudo modprobe kvm_intel nested=1

sudo touch /etc/modprobe.d/kvm_intel.conf

sudo echo "options kvm_intel nested=1" > /etc/modprobe.d/kvm_intel.conf

sudo systemctl restart libvirtd.service

sudo systemctl enable libvirtd.service

sudo wget https://download.docker.com/linux/centos/docker-ce.repo -O /etc/yum.repos.d/docker.repo

sudo yum install docker-ce -y

sudo yum-complete-transaction --cleanup-only

sudo systemctl start docker

sudo systemctl enable docker

sudo usermod -aG kvm $USER

sudo usermod -aG libvirt $USER

sudo wget https://download.virtualbox.org/virtualbox/rpm/el/virtualbox.repo -P /etc/yum.repos.d

sudo yum install VirtualBox-6.1 -y

sudo systemctl start vboxdrv 

sudos systemctl status vboxdrv

sudo curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && chmod +x minikube

sudo cp minikube /usr/bin/

sudo wget https://download.virtualbox.org/virtualbox/6.1.34/Oracle_VM_VirtualBox_Extension_Pack-6.1.34.vbox-extpack

sudo VBoxManage extpack install --replace --accept-license=33d7284dc4a0ece381196fda3cfe2ed0e1e8e7ed7f27b9a9ebc4ee22e24bd23c Oracle_VM_VirtualBox_Extension_Pack-6.1.34.vbox-extpack


curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash



# minikube:

minikube stop

minikube delete --all=true --purge=true

docker image prune -a -f

minikube start --kubernetes-version=stable --driver=kvm2 --cpus 4 --memory 8192


### Modify settings:
minikube config set cpus 4

minikube config set memory 8196

minikube config set disk-size 10240MB

minikube config set WantUpdateNotification false




# rmqp-example create images:

git clone https://github.com/avielb/rmqp-example

cd rmqp-example/

docker-compose build --no-cache --pull --quiet


# Docker login:

docker login --username=<user> --password-stdin <<<'password'

OR:

https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry



# Tag images and push to docker hub: 


docker image tag rmqp-example_consumer:latest ofirsh11/rmqp-example_consumer:latest

docker image push ofirsh11/rmqp-example_consumer:latest

docker image tag rmqp-example_producer:latest ofirsh11/rmqp-example_producer:latest

docker image push ofirsh11/rmqp-example_producer:latest 



# rabbitmq:
helm repo add bitnami https://charts.bitnami.com/bitnami

helm repo update

helm upgrade --install rabbitmq --set auth.username=admin,auth.password=secretpassword,auth.erlangCookie=secretcookie,metrics.enabled=true,service.type=NodePort bitnami/rabbitmq

## RabbitMQ 
   
Credentials:
    echo "Username      : admin"
    echo "Password      : $(kubectl get secret --namespace default rabbitmq -o jsonpath="{.data.rabbitmq-password}" | base64 -d)"
    echo "ErLang Cookie : $(kubectl get secret --namespace default rabbitmq -o jsonpath="{.data.rabbitmq-erlang-cookie}" | base64 -d)"

Note that the credentials are saved in persistent volume claims and will not be changed upon upgrade or reinstallation unless the persistent volume claim has been deleted. If this is not the first installation of this chart, the credentials may not be valid.
This is applicable when no passwords are set and therefore the random password is autogenerated. In case of using a fixed password, you should specify it when upgrading.
More information about the credentials may be found at https://docs.bitnami.com/general/how-to/troubleshoot-helm-chart-issues/#credential-errors-while-upgrading-chart-releases.

RabbitMQ can be accessed within the cluster on port 5672 at rabbitmq.default.svc.cluster.local

To access for outside the cluster, perform the following steps:

Obtain the NodePort IP and ports:

    export NODE_IP=$(kubectl get nodes --namespace default -o jsonpath="{.items[0].status.addresses[0].address}")
    export NODE_PORT_AMQP=$(kubectl get --namespace default -o jsonpath="{.spec.ports[?(@.name=='amqp')].nodePort}" services rabbitmq)
    export NODE_PORT_STATS=$(kubectl get --namespace default -o jsonpath="{.spec.ports[?(@.name=='http-stats')].nodePort}" services rabbitmq)

To Access the RabbitMQ AMQP port:

    echo "URL : amqp://$NODE_IP:$NODE_PORT_AMQP/"

To Access the RabbitMQ Management interface:

    echo "URL : http://$NODE_IP:$NODE_PORT_STATS/"

To access the RabbitMQ Prometheus metrics, get the RabbitMQ Prometheus URL by running:

    kubectl port-forward --namespace default svc/rabbitmq 9419:9419 &
    echo "Prometheus Metrics URL: http://127.0.0.1:9419/metrics"

Then, open the obtained URL in a browser.


If user minikube docker: 
kubectl port-forward --address 0.0.0.0 service/rabbitmq $NODE_PORT_STATS:15672

list of URLS: 
minikube service rabbitmq --url

# Helm Chart:
helm uninstall k8s-project1 --dry-run
                                                    
helm uninstall k8s-project1

helm dependency update
                                                    
helm upgrade --install k8s-project1 . --dry-run

helm upgrade --install k8s-project1 .


# Jenkins Install

(https://devopscube.com/setup-jenkins-on-kubernetes-cluster/)

helm repo remove jenkins
helm uninstall jenkins

helm repo add jenkins https://charts.jenkins.io

helm repo update

helm upgrade --install jenkins jenkins/jenkins --set controller.adminPassword=EfpkNXuBNyBm7Xbw,controller.installLatestSpecifiedPlugins=true --wait --cleanup-on-fail --atomic

kubectl --namespace default port-forward svc/jenkins 8080:8080 --address=0.0.0.0
