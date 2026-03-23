📝 Three-Tier Blogging App — CI/CD Pipeline on AWS

🚀 Project Overview

A fully automated CI/CD pipeline that deploys a Three-Tier Blogging Web Application on AWS EC2 using Jenkins, Docker, and Kubernetes.  
Every time code is pushed to GitHub — Jenkins automatically builds Docker images, pushes them to DockerHub, and deploys to Kubernetes. No manual steps required.

---

🖥️ App Preview

![App Preview](https://raw.githubusercontent.com/Akshay09-tech/BlogApp-Jenkins-project/main/Screenshot%202026-03-21%20162402.png)




🏗️ Three-Tier Architecture

---
```

Tier 1 — Frontend → Nginx (Alpine) serves index.html
↓
Tier 2 — Backend → Flask (Python 3.9) REST API on port 5000
↓
Tier 3 — Database → SQLite (blog.db) embedded in backend container

```
⚙️ CI/CD Pipeline Flow
---
```

Developer pushes code to GitHub
↓
GitHub Webhook triggers Jenkins (port 8080)
↓
Jenkins Pipeline starts on EC2
↓
Stage 1 → Pull latest code
Stage 2 → Build Docker images (frontend + backend)
Stage 3 → Push images to DockerHub
Stage 4 → kubectl apply → Kubernetes deploys
↓
App is Live! 🎉

```
---

🔧 Tech Stack

- **Frontend:** HTML, CSS, JavaScript, Nginx  
- **Backend:** Python, Flask, Flask-CORS  
- **Database:** SQLite  
- **Containerization:** Docker  
- **Image Registry:** DockerHub  
- **CI/CD:** Jenkins  
- **Orchestration:** Kubernetes (Minikube)  
- **Cloud:** AWS EC2 (Ubuntu 22.04)  
- **Version Control:** GitHub + Webhooks  



📁 Project Structure
---
```
BlogApp-Jenkins/
├── backend/
│ ├── app.py # Flask API
│ ├── requirements.txt # flask, flask-cors
│ └── Dockerfile # Python 3.9 base image
├── frontend/
│ ├── index.html # Blog UI
│ └── Dockerfile # Nginx Alpine base image
├── k8s/
│ ├── backend-deployment.yaml
│ ├── backend-service.yaml
│ ├── frontend-deployment.yaml
│ ├── frontend-service.yaml
│ └── ingress.yaml
└── Jenkinsfile # Pipeline definition

```
---

🛠️ Setup & Installation

### Prerequisites

- AWS EC2 (Ubuntu 22.04, t2.medium or higher)  
- Ports open: 22, 80, 8080, 5000, 8081  

---

### Step 1 — Install Dependencies on EC2

**Java**  
Jenkins is a Java-based application, so Java must be installed first on the EC2 instance before Jenkins can run.

**Jenkins Repository & Install**  
Jenkins is not available in the default Ubuntu package list, so the official Jenkins repository and its GPG key must be added manually. Once the repo is added, Jenkins can be installed via apt and started as a system service.

**Docker**  
Docker is required to build and run container images. After installing Docker, the jenkins user must be added to the docker group — otherwise the Jenkins pipeline cannot run docker commands. A Jenkins restart is required after this for the group change to take effect.

**kubectl**  
kubectl is the command-line tool that communicates with the Kubernetes cluster. It is downloaded as a binary from the official Kubernetes release page and moved to /usr/local/bin so it is accessible system-wide.

**Minikube**  
Minikube runs a single-node Kubernetes cluster locally on the EC2 instance. It is downloaded as a binary and installed similar to kubectl. Minikube must be started with the Docker driver since Docker is already installed. The Ingress addon must also be enabled so that external traffic can reach the services inside the cluster.

---

### Step 2 — Jenkins Setup

1. Go to http://EC2_IP:8080  
2. Install suggested plugins  
3. Add DockerHub credentials:  
   - Manage Jenkins → Credentials → Add  
   - ID: dockerhub-creds  

---

### Step 3 — Give Jenkins kubectl Access

**Why this is needed:**  
Minikube is started by the ec2-user, so all the Kubernetes certificates and config files are stored in the ec2-user home directory. Jenkins runs as a separate jenkins user which cannot access these files by default.

**What needs to be done:**

- Copy `.minikube` → `/var/lib/jenkins/.minikube`  
- Copy `.kube/config` → `/var/lib/jenkins/.kube/config`  
- Update paths inside config file  
- Change ownership to jenkins user  
- Fix permissions  

Once done, Jenkins can run kubectl commands successfully.

---

### Step 4 — Create Jenkins Pipeline Job

- New Item → Pipeline → Pipeline script from SCM  
- SCM: Git  
- Repo URL: https://github.com/YOUR_USERNAME/BlogApp-Jenkins  
- Branch: */main  
- Script Path: Jenkinsfile  
- Build Triggers: GitHub hook trigger for GITScm polling ✅  

---

### Step 5 — GitHub Webhook

- GitHub Repo → Settings → Webhooks → Add webhook  
- Payload URL: http://EC2_IP:8080/github-webhook/  
- Content type: application/json  
- Event: Just the push event  

---

🚀 Access the App

```bash
# Start port-forward
kubectl port-forward service/frontend-service 8081:80 --address 0.0.0.0 &
kubectl port-forward service/backend-service 5000:5000 --address 0.0.0.0 &

# Open in browser
http://EC2_PUBLIC_IP:8081
