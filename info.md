# to built server from ground up:

1. system_setup.py
    create db

2. run the main.py app



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

