# FastApi-test-task

## Documentation
![Screenshot 2024-05-01 at 15.54.33.png](screens%2FScreenshot%202024-05-01%20at%2015.54.33.png)
**link:**  http://127.0.0.1:8000/docs#/ (First you should raise the project)


## Prerequisites

Ensure you have Python 3.8 or higher and pip installed on your machine. It is also recommended to use a virtual environment to isolate project dependencies.

## Installation

   ```bash
    git clone git@github.com:Polyakiv-Andrey/FastApi-test-task.git
   
    cd project-name

    python -m venv venv
   
    source venv/bin/activate

    pip install -r requirements.txt

    psql -U postgres

    CREATE DATABASE fastapi_test;

    touch .env 
   
    echo "DB_NAME=fastapi_test" >> .env
    echo "DB_USER=postgres" >> .env
    echo "DB_PASSWORD=postgres" >> .env
    echo "DB_HOST=localhost" >> .env
    echo "DB_PORT=5432" >> .env
    
    mk_dir certs
    
    openssl genrsa -out certs/jwt-private.pem 2048
    
    openssl rsa -in certs/jwt-private.pem -outform PEM -pubout -out certs/jwt-public.pem
    
    alembic upgrade head
    
    python -m uvicorn src.main:app --reload 
    
    