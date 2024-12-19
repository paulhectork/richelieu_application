# Application du projet Richelieu

## 🪩🪩🪩

clone personnel de l'application [Quartier Richelieu](https://quartier-richelieu.inha.fr) développée pour le projet *Richelieu. Histoire du quartier* à l'INHA.

ce clone date du 17.12.2024 et ne sera pas mis à jour. le dépôt officiel se trouve sur le [GitLab de l'INHA](https://gitlab.inha.fr/snr/rich.data/application), avec [tous les autres outils](https://gitlab.inha.fr/snr/rich.data/) développés pour le projet.

---

## Présentation

L'application comprend: 
- un `backend` en Flask pour l'interaction avec
  la base de données et la mise en forme des réponses en JSON
- un `frontend` en Vue pour l'interface utilisateur et la production
  de HTML à partir du JSON renvoyé par le backend
- la base de données est en PostgreSQL
  - un dump est disponible dans `db/`
  - pour la documentation de la base de données, voir [ici](./db/README.md)
  
Pour les aspects techniques de chaque appli, voir les `README.md` propres à chaque dossier.

---

## Utilisation rapide

Pour un guide détaillé, voir `backend/`, et `frontend/`. 
Il faut avoir un terminal par application (un pour le back, un pour le front).

```bash
# utilisation en local, avec des environnements python nommés `env/`, postgresql et `libpq-dev` déjà installés
bash scripts/run_backend.sh
bash scripts/run_frontend.sh
```

---

## Licence

GNU GPL 3.0
