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

---

## TODO

### Backend

Obligatoire
- réécrire `serialize_lite()` et `serialize_full()` pour que les fonctions fonctionnent plus rapidement
  (en faisant des requêtes SQL brutes qui reproduisent le même schéma)
- développer l'API publique
- ajouter de la gestion d'erreur dans les routes et préciser le fonctionnement des erreurs HTTP
- `advanced_search_iconography`: ajouter la gestion de champs répétables (donc, chaque paramètre
  peut être une liste)

Optionnel
- faire du type-checking sur les inputs libres du moteur de recherche (`i/search/iconography`)

### Frontend

Obligatoire
- Gestion des sur-thèmes et sur-entités nommées
- Cartographie principale, et donc moteur de recherche à filtre sur le corpus cartographique
- `IconographyMainView.vue`: ajouter des `v-if` dans le cartel pour gérer les informations manquantes
- `NamedEntityMainView.vue` et `ThemeMainView.vue`: créer les pages
- Articles (cf. carnet pour les détails):
  - création d'une page d'index des articles
  - création d'une page pour chaque article
    - l'article encodé
    - 2 images en grand (accessibles via visionneuse IIIF)
    - un carousel d'images supplémentaires, construit à partir d'une recherche à filtre sur la BDD

Optionnel
- `AdvancedSearchQuery.vue`: le bouton "Réinitialiser les paramètres" ne réinitialise pas
  les `custom inputs` (`FormRadioTabs.vue` et `FormSelect.vue`)


