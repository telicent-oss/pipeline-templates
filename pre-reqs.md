# Prerequisites

- Python 3.12+

# ⚙️ Setup 

1. Confirm access to GitHub: https://github.com/telicent-oss/pipeline-templates.git
2. Clone the repository:

  ```bash
  git clone https://github.com/telicent-oss/pipeline-templates.git

  ```

3. Create a virtual environment:

- On windows:
```bash 
python -m venv venv
```
- On a mac:
```bash 
python -m venv venv
```

4. Activate the virtual environment:

- On windows:
```bash 
venv\Scripts\activate.bat
```

- On a mac:
```bash
source venv/bin/activate
```


### 🐍 Python Dependencies
1. Install required libraries:

```bash
pip install telicent-lib==6.1.0
pip install telicent-ies-tool==2.0.0
pip install python-dotenv==1.0.1
pip install telicent-label-builder==0.1.7
pip install setuptools==80.9.0
```
⚠️ If on Windows, you might need to download and install visual studio build tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/

Optional:

Check package version:
```bash
pip show telicent-lib
pip show telicent-ies-tool
```

Uninstall a package if required:

```bash
pip uninstall package-name
```
### GitHub Branches
- you can create a new branch or switch between branches
- you can find the docker compose (next step) and other resources in the `nov25_training` branch (Note these will be updated before the second part of the training)

- to checkout a branch:
```bash
git checkout nov25_training
```

- to create a new branch and switch to it:

```bash
git checkout -b branch-name
```

### 🐳 Docker and Kafka

1. Install Docker Desktop:

On Windows: https://docs.docker.com/desktop/setup/install/windows-install/

On a mac: https://docs.docker.com/desktop/setup/install/mac-install/

2. Open Docker Desktop (You might be prompted to set up an account first)

3. Build and start Kafka and Kafka UI from the root directory. The docker compose file is on the nov25_training branch as well as attached to the email.

```bash
docker compose -f docker-compose-kafka_and_kafka_ui.yml up
```

4. Verify Kafka UI is accessible: http://localhost:18080/

### ✅ Now you are ready!


### 📌 Notes
This should be sufficient to get started, but we should have time to check these and get everything started in January.
You might have already completed some/most of these steps, but do check the library and python versions.
