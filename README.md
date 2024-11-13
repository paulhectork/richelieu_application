# Application du projet Richelieu

Cette application est en cours de développement, voir la branche
`dev` pour les versions en cours de développement.

L'application comprend: 
- un `backend` en Flask pour l'interaction avec
  la base de données et la mise en forme des réponses en JSON
- un `frontend` en Vue pour l'interface utilisateur et la production
  de HTML à partir du JSON renvoyé par le backend
- la base de données est en PostgreSQL (un dump est disponible dans `db/`

Pour les aspects techniques de chaque appli, voir les `README.md` propres à chaque dossier.

---

## Utilisation rapide

Pour un guide détaillé, voir `backend/`, et `frontend/`. 
Il faut avoir un terminal par application (un pour le back, un pour le front).

```bash
# utilisation en local, avec des environnements python nommés `env/`
bash scripts/run_backend.sh
bash scripts/run_frontend.sh
```

---

## Licence

GNU GPL 3.0
