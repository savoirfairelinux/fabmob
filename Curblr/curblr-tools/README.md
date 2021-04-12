# curblr-tools

- Création des données de parcometres au format Curblr.
- Filtrage selon les arrondissements/quartiers pour les villes de Québec et Montréal.

```sh
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
python3 run.py
(cd ../curb-map/; nvm use 12.7.0; yarn start)
```
