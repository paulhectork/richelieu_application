# Application du projet Richelieu

Cette application est en cours de développement, voir la branche 
`dev` pour les versions en cours de développement.

Pour les aspects techniques relatifs au *backend* et au *frontend*, 
voir les `README.md` propres à chaque dossier.

---

## Utilisation rapide

Pour un guide détaillé, voir `backend/` et `frontend/`. Il faut avoir
deux terminaux ouverts, l'un pour le back, l'autre le front. 

```bash
# utilisation en local
python main.py -m dev
npm run dev -- --mode backend-local

# utilisation du front en local, backend sur serveur
python main.py -m prod                # commande à faire connecté en SSH
npm run dev -- --mode backend-server  # commande à faire en local

# utilisation sur serveur (les deux commandes doivent être lancées en SSH au serveur)
python main.py -m prod
npm run dev -- --mode backend-server --host
```

