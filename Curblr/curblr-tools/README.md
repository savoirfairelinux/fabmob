# curblr-tools

- Création des données de parcometres au format Curblr.
- Filtrage selon les arrondissements/quartiers pour les villes de Québec et Montréal.
- server FastAPi pour requêtes conversions


## Setup
```sh
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```
Il faut aussi rajouter les fichiers d'authentification 'credits.json' pour l'API jalon et 'clients_secrets.json' pour google drive Api.
Veuillez contacter le développeur pour les obtenir.

## Lancer le code de conversion et observer le resultat dans Curb-Map
```sh
python3 run.py
(cd ../curb-map/; git submodule init; git submodule update; nvm use 12.7.0; yarn start)
```

## Serveur fastApi pour requêtes de conversion depuis Curb-Map
Les requêtes sont envoyées depuis le projet Curb-Map qui doit donc être préalablement lancé. 

Commentez d'abord l'appel à la fonction run() dans run.py

Pour démarrer le serveur:
```sh
uvicorn server_fastApi:app --reload
```

Sur la machine virtuelle(digital océan ubuntu)
```sh
uvicorn server_fastApi:app --host 0.0.0.0 --reload
```
en ssl
```sh
uvicorn server_fastAPI:app --host 0.0.0.0 --reload --port 443 --ssl-keyfile=/etc/ssl/private/apache-selfsigned.key --ssl-certfile=/etc/ssl/certs/apache-selfsigned.crt
```