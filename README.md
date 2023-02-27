# Project_MLOPS

## My Anime Recommendation App

This is a Flask application that predicts whether a user would enjoy a given anime based on its title, genre(s), description, type, producer, and studio. The app is dockerized and easily deployable.

### Prerequisites

Python 3.8 or higher
Docker

### Installation

1) Clone the repository to your local machine:

```
git clone https://github.com/calvin-projet/Project_MLOPS.git
cd app
```

2) Create a virtual environment and activate it:

```
python3 -m venv env
source env/bin/activate
```

3) Install the required packages:

```
pip install -r requirements.txt
```

### Usage

1) Start the app in a Docker container:

```
docker build -t my-app .
python app.py
```

2) Open a web browser and navigate to http://localhost:8090.

3) Fill out the form with an anime title, genre(s), description, type, producer, and studio, and click the "Predict" button.

### Testing

To run the automated tests, run the following command:

```
pytest
```

### Jenkins Pipeline

This repository includes a Jenkinsfile that defines a simple CI/CD pipeline. The pipeline consists of the following stages:

1) Build: Builds the Docker image.
2) Test: Runs automated tests.
3) Push: Pushes the Docker image to a Docker registry.
4) Deploy: Deploys the app
