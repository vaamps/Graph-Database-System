# Graph Database Setup using Kubernetes, Docker, and Helm

## Description
This section of the project focuses on deploying a graph-based system using orchestration tools like _minikube_ to manage Docker containers and build a comprehensive data ingestion pipeline. The setup includes configuring components such as Kafka, Zookeeper, and Neo4j within a Kubernetes environment.

### Project Workflow:
The project workflow encompasses four main components: Kafka, Kafka Connect, Zookeeper, and Neo4j.

#### Step 1: Setting up Minikube and Installing Components (Kafka and Zookeeper)
The initial step involves setting up minikube and installing necessary components like Kafka and Zookeeper.

#### Deployment Commands:

```bash
sudo apt update
sudo apt install -y curl wget apt-transport-https gnupg2
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
curl https://baltocdn.com/helm/signing.asc | sudo apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
echo "deb https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable.list
sudo apt update
sudo apt install helm
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
rm minikube-linux-amd64
minikube start
minikube status
```

#### Points to note:
- The environment utilized is Windows with WSL (Windows Subsystem for Linux), providing a Linux-like environment for Windows-based systems.
- Docker Desktop service is installed to facilitate the Docker environment setup.
- Minikube requires the Docker driver to initiate the service, and in this scenario, the default Docker configuration is utilized.
- Docker Desktop service integrates seamlessly with WSL environments configured on the system.

