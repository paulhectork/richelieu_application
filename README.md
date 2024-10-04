# Application du projet Richelieu

Cette application est en cours de développement, voir la branche
`dev` pour les versions en cours de développement.

L'application comprend: 
- un `backend` en Flask pour l'interaction avec
  la base de données et la mise en forme des réponses en JSON
- un `frontend` en Vue pour l'interface utilisateur et la production
  de HTML à partir du JSON renvoyé par le backend
- un `staticserver` (serveur de fichiers statiques) utilisé pour afficher
  des fichiers statiques en développement local.
- la base de données est en PostgreSQL

Pour les aspects techniques de chaque appli, voir les `README.md` propres à chaque dossier.

---

## Utilisation rapide

Pour un guide détaillé, voir `backend/`, `staticserver/` et `frontend/`. 
Il faut avoir un terminal par application (un pour le back, un pour le front
et un pour `staticserver` si on s'en sert).

```bash
# utilisation en local, avec des environnements python nommés `env/`
cd staticserver  && source env/bin/activate && python main.py                      # terminal 1
cd backend && source env/bin/activate && python main.py -m dev                    # terminal 2
cd frontend && npm run dev -- --mode backend-local     # terminal 3
```

---

## Licence

GNU GPL 3.0
