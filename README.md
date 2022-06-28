# k8s-project1


# rmqp-example:
docker image prune -a -f

minikube start --cpus 2 --memory 4096 --driver vmware --insecure-registry localhost:5000 --extra-config=apiserver.service-node-port-range=1-65535

minikube addons enable registry

kubectl get service --namespace kube-system

kubectl port-forward --namespace kube-system service/registry 5000:80

git clone https://github.com/avielb/rmqp-example

docker-compose build

docker image tag rmqp-example-master_consumer:latest localhost:5000/consumer/rmqp-example-master_consumer:latest

docker image push localhost:5000/consumer/rmqp-example-master_consumer:latest

docker image tag rmqp-example-master_producer:latest localhost:5000/producer/rmqp-example-master_producer:latest

docker image push localhost:5000/producer/rmqp-example-master_producer:latest

# Checks:
curl localhost:5000/v2/_catalog

curl localhost:5000/v2/consumer/rmqp-example-master_consumer/tags/list

curl localhost:5000/v2/producer/rmqp-example-master_producer/tags/list




# rabbitmq:
helm repo add bitnami https://charts.bitnami.com/bitnami

helm repo update

helm upgrade --install rabbitmq --set auth.username=admin,auth.password=secretpassword,auth.erlangCookie=secretcookie,metrics.enabled=true bitnami/rabbitmq


# Helm Chart:
helm install k8s-project1 . --dry-run
