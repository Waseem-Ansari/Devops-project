# Flask App on Kubernetes

A production-grade Flask application deployed on Kubernetes with a PostgreSQL database, persistent storage, and full observability.

---

## 🏗️ Architecture

```text
       [ Internet ]
            │
            ▼
┌───────────────────────────┐
│ NodePort Service (30080)  │
└───────────┬───────────────┘
            │
            ▼
┌───────────────────────────┐
│ Flask Deployment          │
│ (3 Replicas)              │
└───────────┬───────────────┘
            │
            ▼
┌───────────────────────────┐
│ ClusterIP Service         │
└───────────┬───────────────┘
            │
            ▼
┌───────────────────────────┐
│ Postgres Deployment       │
│ (1 Replica)               │
└───────────┬───────────────┘
            │
            ▼
┌───────────────────────────┐
│ PersistentVolumeClaim     │
│ (1Gi)                     │
└───────────────────────────┘
```

---

## 🛠️ Tech Stack

*   **Flask** (Python backend)
*   **PostgreSQL** (database)
*   **Kubernetes** (orchestration)
*   **Docker** (containerization)
*   **Minikube** (local cluster)

---

## 📋 Prerequisites

*   Docker installed
*   Minikube installed
*   `kubectl` installed

---

## 🚀 Setup

### 1. Start Minikube
```bash
minikube start
```

### 2. Create Secret (never commit real secrets)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: flask-secret
type: Opaque
stringData:
  DB_PASSWORD: your_password_here
  POSTGRES_PASSWORD: your_password_here
```

### 3. Deploy Everything
```bash
kubectl apply -f k8s/configmap.yml
kubectl apply -f k8s/secret.yml
kubectl apply -f k8s/postgres-pvc.yml
kubectl apply -f k8s/postgres-deployment.yml
kubectl apply -f k8s/postgres-service.yml
kubectl apply -f k8s/flask-deployment.yml
kubectl apply -f k8s/flask-service.yml
```

### 4. Wait for pods to be ready
```bash
kubectl get pods -w
```

### 5. Get URL and test
```bash
minikube service flask-service --url
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | GET | App info + environment |
| `/health` | GET | Health check |
| `/db-check` | GET | Database connectivity |
| `/engineers` | GET | DB read/write test |

---

## 📦 Kubernetes Resources

| Resource | Type | Purpose |
| :--- | :--- | :--- |
| `flask-config` | ConfigMap | App configuration |
| `flask-secret` | Secret | Passwords |
| `postgres-pvc` | PVC | Database storage |
| `postgres-deployment` | Deployment | Postgres pod |
| `postgres-service` | ClusterIP | Internal DB access |
| `flask-deployment` | Deployment | App pods (3 replicas) |
| `flask-service` | NodePort | External access |

---

## ✨ Key Features

*   **Self healing** — pod crashes auto restart
*   **Zero downtime** — readiness probe prevents traffic to unready pods
*   **Persistent storage** — data survives pod restarts
*   **Config separated from code** — ConfigMaps + Secrets
*   **Non root container** — security best practice
*   **Multi stage Docker build** — minimal image size

---

## 💻 Useful Commands

```bash
# see all resources
kubectl get all
 
# check logs
kubectl logs -f deployment/flask-deployment
 
# scale app
kubectl scale deployment flask-deployment --replicas=5
 
# rollback
kubectl rollout undo deployment/flask-deployment
 
# shell into pod
kubectl exec -it <pod-name> -- bash
 
# delete everything
kubectl delete -f k8s/
```

---

## 💡 Lessons Learned

*   Readiness probe prevents traffic to pods before DB connection is ready
*   PVC must be created before Deployment that uses it
*   Service name = hostname other pods use to connect
*   Secrets must never be committed to Git
