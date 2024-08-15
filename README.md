# Clip Search Web App
A web based solution which allows for the indexing and searching of twitch clips

# Quick Start
After cloning the repository, there are a few steps to get the webapp going
- Make sure you have some form of docker installed, Docker Desktop, Docker CLI doesn't matter
- Create a `secrets` folder in the root directory
    - inside this folder create two files, `mysql_password.txt` and `mysql_root_password.txt`. It doesnt matter what the content is as long as it doesn't contain any illegal characters
    - once done the directory structure should look like this
    ```
    ClipSearchWeb/
        |
        L app/
        L mysql/
        L nginx/
        L secrets/
            L mysql_password.txt
            L mysql_root_password.txt
        L docker-compose.yml
        L Dockerfile
        L README.md
    ```
- Start the containers by running `docker compose up --build` from the root directory
- The database will be empty initially, you can fill it with mock data or ask Moff for a backup of the real database
- Once the containers are running, the webserver should be running on port 80 (default for http)