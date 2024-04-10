# Backend

---

## Installation et utilisation

### Installation

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Utilisation

Pour utiliser l'application, il faut un dossier `./app/utils/confidentials`
qui contient un fichier JSON avec les bons identifiants de connexion à la BDD
postgres. Le fichier est nommé `postgresql_credentials_local.json` pour la
BDD locale, `postgresql_credentials_remote.json` pour une BDD sur serveur.

```bash
python main.py -d local  # ou `remote` pour se connecter à la BDD sur serveur
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
