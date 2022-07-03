# k8s-project1


# minikube:

minikube delete --all=true --purge=true

docker image prune -a -f

minikube start --cpus 2 --memory 4096 --driver vmware --insecure-registry 0.0.0.0:5000 --extra-config=apiserver.service-node-port-range=1-65535


minikube config set WantUpdateNotification false




# rmqp-example create images:

git clone https://github.com/avielb/rmqp-example

docker-compose build


# Docker login:

docker login --username=<user> --password-stdin <<<'password'


# Tag images and push to docker hub: 


docker image tag rmqp-example-master_consumer:latest ofirsh11/rmqp-example-master_consumer:latest

docker image push ofirsh11/rmqp-example-master_consumer:latest

docker image tag rmqp-example-master_producer:latest ofirsh11/rmqp-example-master_producer:latest

docker image push ofirsh11/rmqp-example-master_producer:latest



# rabbitmq:
helm repo add bitnami https://charts.bitnami.com/bitnami

helm repo update

helm upgrade --install rabbitmq --set auth.username=admin,auth.password=secretpassword,auth.erlangCookie=secretcookie,metrics.enabled=true bitnami/rabbitmq


# Helm Chart:
helm uninstall k8s-project1

helm install k8s-project1 . --dry-run

helm upgrade --install k8s-project1 .
