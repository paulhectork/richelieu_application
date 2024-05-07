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

L'application peut être lancée avec différentes configurations (notamment la BDD à 
laquelle se connecter). En ligne de commande, l'argument `-m` `--mode` permet de
sélectionner une configuration: 

```bash
python main.py -m dev  # ou `-m test` pour faire des tests, `-m prod` pour mettre l'application sur serveur
```

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
# fichier de connexion dans app/utils/confidentials/
{
  "username": "<votre nom d'utilisateur.ice>", 
  "password": "<votre mdp>",
  "uri": "<l'URI de connexion à la BDD>",
  "db": "<le nom de la BDD>"
}
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
