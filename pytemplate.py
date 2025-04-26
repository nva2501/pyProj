import os
from pathlib import Path

def create_file(path: Path, content: str = ""):
    if path.exists():
        print(f"Skipped existing file: {path}")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        print(f"Created file: {path}")

def main():
    # Prompt for the application name
    app_name = input("Enter your application name (e.g., llm_app): ").strip()
    if not app_name:
        print("Application name cannot be empty.")
        return

    base_path = Path(app_name)
    if not base_path.exists():
        base_path.mkdir()

    # Define the directory structure
    dirs = [
        base_path / "api",
        base_path / "services",
        base_path / "models",
        base_path / "utils",
        base_path / "tests",
        base_path / "k8s",
    ]

    # Create directories and __init__.py files
    for dir_path in dirs:
        if dir_path not in [base_path / "k8s"]:
            dir_path.mkdir(parents=True, exist_ok=True)
            create_file(dir_path / "__init__.py")
            if dir_path == base_path / "api":
                create_file(dir_path / "routes.py")
            if dir_path == base_path / "services":
                create_file(dir_path / f"{app_name}_services.py")
            if dir_path == base_path / "models":
                create_file(dir_path / "schemas.py")
            if dir_path == base_path / "utils":
                create_file(dir_path / "helpers.py")
            if dir_path == base_path / "tests":
                create_file(dir_path / "test_main.py")

    # Create main.py
    create_file(base_path / "main.py", f'''\
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {{"message": "Welcome to {app_name}!"}}
''')

    # Create Dockerfile
    create_file(base_path / "Dockerfile", f'''\
# Use the official Python image with the desired version
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY {app_name}/ ./{app_name}/

# Expose the port that the application will run on
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["uvicorn", "{app_name}.main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

    # Create requirements.txt
    create_file(base_path / "requirements.txt", '''\
fastapi
uvicorn
''')

    # Create .env
    create_file(base_path / ".env", "ENV=development\n")

    # Create Kubernetes deployment.yaml
    create_file(base_path / "k8s" / "deployment.yaml", f'''\
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {app_name}-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: {app_name}
  template:
    metadata:
      labels:
        app: {app_name}
    spec:
      containers:
      - name: {app_name}-container
        image: your-docker-repo/{app_name}:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: {app_name}-config
''')

    # Create Kubernetes service.yaml
    create_file(base_path / "k8s" / "service.yaml", f'''\
apiVersion: v1
kind: Service
metadata:
  name: {app_name}-service
spec:
  type: LoadBalancer
  selector:
    app: {app_name}
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
''')

    # Create .gitignore
    create_file(base_path / ".gitignore", '''\
__pycache__/
*.pyc
.env
*.env
''')

    # Create README.md
    create_file(base_path / "README.md", f"# {app_name}\n\n{app_name} is a scalable Python application scaffolded with Docker and Kubernetes support.")

    print(f"Project '{app_name}' structure has been created.")

if __name__ == "__main__":
    main()
