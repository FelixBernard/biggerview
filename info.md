# to built server from ground up:

1. fill server_config

2. system_setup.py
    create db

3. system.py
    init server



# local execution without docker

## Windows
$env:DB_HOST="localhost"
$env:DB_USER="dein_lokaler_mysql_benutzer"
$env:DB_PASSWORD="dein_lokales_mysql_passwort"
$env:DB_NAME="deine_lokale_datenbank"
python main.py

## Linux
export DB_HOST=localhost
export DB_USER=dein_lokaler_mysql_benutzer
export DB_PASSWORD=dein_lokales_mysql_passwort
export DB_NAME=deine_lokale_datenbank
python main.py



# build docker compose

1. docker-compose up --build

