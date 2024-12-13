# Backend

Le backend de l'application gère l'interaction avec la base de données du projet et offre deux API:

- `$root_url/i/`: l'API privée, utilisée pour la communication entre backend et frontend;
- `$root_url/api/v1`: l'API publique, qui dispose d'une documentation Swagger, utilisée pour récupérer
   et réutiliser les données du projet
- `$root_url` est la racine du site du projet: `https://quartier-richelieu.inha.fr` pour le site en ligne

---

## Installation et utilisation

### Installation

```bash
# installer postgresql et libpq pour pouvoir travailler avec postgres. ATTENTION: INSTALLATIONS SYSTEM-WIDE
if [ ! $(which psql) ]; then sudo bash ../scripts/install_postgresql_15.sh; fi;
sudo apt install libpq-dev

# installations python
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Utilisation

L'application peut être lancée avec différentes configurations (notamment la BDD à 
laquelle se connecter). En ligne de commande, l'argument `-m` `--mode` permet de
sélectionner une configuration: 

```bash
# si on veut lancer l'application sur machine locale
python main.py -m dev

# si on veut lancer des tests sur machine locale
python main.py -m test

# si on veut lancer l'application sur serveur (avec Gunicorn, comme sur le serveur Richelieu)
gunicorn prod-gunicorn:app

# si on veut lancer sur serveur sans Gunicorn (déconseillé: dans ce cas, on utilise le serveur de dev Werkzeug en prod)
python main.py -m prod
```

### Configurations

Le fichier `app/config.py` liste toutes les configurations possibles. Chaque config
correspond à une classe. Les identifiants de connexion aux différentes BDD se trouvent 
dans des fichiers `json`, dans le dossier `app/utils/confidentials/`. Il faut pointer 
vers ces fichiers dans `app/config.py`:

```python
# module app/config.py
class TEST:
  # on pointe ici vers le fichier `json` contenant les accès à la BDD
  with open(os.path.join(CONFIDENTIALS, "postgresql_credentials_local.json"), mode="r") as fh:
    params = json.load(fh)
```

Les fichiers de connexion dans `app/utils/confidentials` ont la structure 
décrite ci-dessous. Il faut que les données dedans correspondent aux 
identifiants de la BDD à laquelle on veut se connecter:

```json
// fichier de connexion dans app/utils/confidentials/
{
  "username": "<votre nom d'utilisateur.ice>", 
  "password": "<votre mdp>",
  "uri": "<l'URI de connexion à la BDD>",
  "db": "<le nom de la BDD>"
}
```

---

## Structure de l'application 

```
/
|_main.py : lancement de l'application
|_prod-gunicorn.py : lancement de l'application en prod
|
|_app/ : racine de l'application
  |
  |_orm/    : classes SQLAlchemy
  |_routes/ : routes de l'application
  |_search/ : modules de recherche avancée
  |_tests/  : modules de test
  |_utils/  : fonctions utilitaires
  |
  |_app.py    : script initiant l'application
  |_config.py : différentes configurations possibles pour l'application
```

---

## ORM et base de données

- chaque classe ORM exposée au public (via l'API ou le front-end)
  deux **sérialisations d'un objet de la classe en JSON**: 
  - `serialize_lite()`: représentation minimale, par exemple pour un catalogue
    ou lorsque l'objet est référencé par une autre table sur laquelle la requête
    est faite (par exemple, pour avoir le nom de l'auteur.ice quand on est sur
    la page d'une ressource iconographique)
  - `serialize_full()`: représentation plus complète, pour la page principale
    de l'objet, avec les données sur l'objet et sur les autres tables associées.
  - l'idée est que, dans les deux cas, on n'expose que ce qui est strictement nécessaire.
- le backend **ne s'occupe pas de transformer les données, il les structure juste**:
  - si il y a une date int4range en PostgreSQL `[1789,1800)`, le backend s'occupe 
    juste de la transformer en liste `[1789,1799]`. La mise en forme pour une lecture 
    par le client se fait au niveau du frontend (par exemple: afficher la chaîne `1789-1799` 
    à partir de cette liste).
  - pareil pour les noms de personnes: le backend renvoie un dictionnaire avec les données
    (`{"first_name": <prénom>, "last_name": <nom>}`...) et la mise en forme (`Prénom Nom`)
    sera faite par le frontend.
