# Foodgram
Foodgram is a culinary assistant with a database of recipes. It allows users to publish recipes, save favorites, and create shopping lists for selected recipes. Users can also subscribe to their favorite authors.

Technologies
- Python
- Django
- Django Rest Framework
- Docker
- Gunicorn
- NGINX
- PostgreSQL
- Continuous Integration
- Continuous Deployment
- Deployment on Remote Server

## Admin info

```
Username: aaa@aaa.com
Password: 22222222Aa
```

## Clone the repository
```
git clone https://github.com/KuzIlya/foodgram-project-react.git
```

##Install Docker and Docker Compose on the server
```
sudo apt install curl
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo apt-get install docker-compose-plugin
```

## Copy docker-compose.yml and nginx.conf from the infra folder to the server
```
scp docker-compose.yml nginx.conf username@IP:/home/username/
```

## Set up environment variables in the GitHub repository under Secrets > Actions
```
SECRET_KEY: Django project secret key
DOCKER_PASSWORD: Docker Hub password
DOCKER_USERNAME: Docker Hub username
HOST: Public IP address of the server
USER: Server username
PASSPHRASE: If SSH key is protected by a passphrase
SSH_KEY: Private SSH key
TELEGRAM_TO: Telegram account ID for sending messages
TELEGRAM_TOKEN: Token of the bot sending messages
```

## Create and run Docker containers
```
sudo docker compose up -d
```

## After successful build, perform migrations:
```
sudo docker compose exec backend python manage.py migrate
```

## Create a superuser:
```
sudo docker compose exec backend python manage.py createsuperuser
```

## Collect static files:
```
sudo docker compose exec backend python manage.py collectstatic --noinput
```

## Populate the database with content from ingredients.json:
```
sudo docker compose exec backend python manage.py loaddata ingredients.json
```

## To stop Docker containers:
```
sudo docker compose down -v     # with removal
sudo docker compose stop        # without removal
```

# Continuous Integration/Continuous Deployment (CI/CD)
After each repository update (push to the master branch), the following will occur:
Code check against PEP8 standard using flake8
Building and delivery of Docker images for frontend and backend to Docker Hub
Deployment of the project on the remote server
Sending a success message to Telegram

# Local Machine Setup

## Clone the repository:
```
git clone https://github.com/KuzIlya/foodgram-project-react.git
```

## In the foodgram directory, create a .env file and fill in your data similar to example.env:
```
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY='Django secret key'
```

## Create and run Docker containers, then perform migrations, collect static files, and create a superuser as mentioned above.
```
docker-compose -f docker-compose-local.yml up -d
```
After the project is launched, it will be available at: https://bigaboba.ddns.net/
