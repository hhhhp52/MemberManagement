# Flask Account Management API

This project provides two RESTful HTTP APIs for creating and verifying an account and password, with detailed documentation available via Swagger.

## Table of Contents
1. [How to See Swagger API](#how-to-see-swagger-api)
2. [Use Package](#use-package)
3. [Folder Structure and Description](#folder-structure-and-description)
4. [Docker Hub URL](#docker-hub-url)
5. [Detailed User Guide for Running the Container](#detailed-user-guide-for-running-the-container)

## How to See Swagger API

1. Start the Flask application by running the following command:
    ```bash
    python app.py
    ```
2. Open your web browser and navigate to `http://127.0.0.1:5000/apidocs/`.

## Use Package

This project uses the following packages:
- `Flask`: A micro web framework for Python.
- `flasgger`: A Flask extension to extract OpenAPI-Specification from all Flask views registered in the app.
- `re`: A module for regular expressions.
- `hashlib`: A module to securely hash passwords.
- `datetime`: A module to work with date and time.
- `sqlite3`: A module to work with SQLite databases.

Install the required packages using:
```bash
pip install Flask flasgger
```

## Folder Structure and Description
.
├── dao
│   └── __init__.py
├── database
│   └── __init__.py
├── implement
│   └── __init__.py
├── test
│   ├── __init__.py
│   └── test_app.py
├── app.py
├── constants.py
├── model.py
├── Dockerfile
├── requirements.txt
└── README.md

- `dao/`: Data access objects for interacting with the database.
- `database/`: Database setup and connection handling.
- `implement/`: Implementation of business logic.
- `test/`: Test cases for the application.
  - `test_app.py`: Contains unit tests for `app.py`.
- `app.py`: The main application file where the Flask app is created and routes are defined.
- `constants.py`: Contains constant values used across the application.
- `model.py`: Contains the `Account` class representing the user accounts.

### `model.py` 
```python
# Example
class AccountManager:
    def __init__(self, username, password):
        self.username = username
        self.password = password
 ```      

## Docker Hub URL

The Docker image for this project is available at: https://hub.docker.com/repository/docker/hhhhp52/member-management-app/general

## Detailed User Guide for Running the Container

### Prerequisites

Docker must be installed on your system. You can download Docker from [here](https://www.docker.com/products/docker-desktop).

### Steps to Run the Container

1. **Pull the Docker image from Docker Hub:**
    ```bash
    docker pull hhhhp52/member-management-app:latest
    ```

2. **Run the Docker container:**
    ```bash
    docker run -d -p 5000:5000 hhhhp52/member-management-app:latest
    ```

    This command will start the container in detached mode and map port 5000 of the container to port 5000 on your host machine.

3. **Access the Swagger API documentation:**
    Open your web browser and navigate to `http://127.0.0.1:5000/apidocs/`.

### Building the Docker Image Locally

If you prefer to build the Docker image locally, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/hhhhp52/MemberManagement
    cd MemberManagement
    ```

2. **Build the Docker image:**
    ```bash
    docker build -t member-management-app .
    ```

3. **Run the Docker container:**
    ```bash
    docker run -d -p 5000:5000 member-management-app
    ```

4. **Access the Swagger API documentation:**
    Open your web browser and navigate to `http://127.0.0.1:5000/apidocs/`.

By following these steps, you should be able to run the container and access the API documentation easily. This setup ensures that the container can be successfully run using Docker with clear and detailed instructions.

