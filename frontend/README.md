# Frontend

Le frontend comprend l'interface graphique du site; il communique avec le backend pour reçevoir des données
via une API interne, les met en forme et les affiche.

---

## Installation et utilisation

### Installation

```bash
npm install npm install
```

### Utilisation (dev)

L'argument `--mode` permet de changer de configuration, selon que le
backend auquel on est connecté soit sur serveur ou sur notre machine locale.
Le principal effet de cet argument est de déterminer quels URLs sont utilisés
pour l'API et pour le serveur de fichiers statiques.

Voir le fichier `vite.config.js` et [la documentation vite](https://vitejs.dev/config/#conditional-config)
pour plus d'informations.

**Attention: le `--` est très important pour séparer le script npm de ses arguments**

```bash
# installer les dépendances
npm install

# si le backend est en local
npm run dev -- --mode backend-local

# si le backend est sur serveur
npm run dev -- --mode backend-server
```

### Utilisation (prod)

En prod, l'application Vue est packagée en un fichier Javascript minifié. Il faut bien 
configurer le serveur pour rendre ce fichier accessible.

```bash
npm install
npm run build -- --mode backend-server
```

---

## Structure de l'application

```
/
|_vite.config.js : fichier de configuration de l'application en prod et en dev.
|
|_src/ : racine de l'appli
  |_assets/     : fichiers statiques utilisés par l'application (images...)
  |_components/ : composents vue intégrés à des pages de l'application.  
  |_modules/    : modules javascript remplissant des fonctions spécifiques. contrairement aux `utils/` qui sont génériques et faits pour pouvoir être utilisés partout, les `modules` ont une fonction précise et ne sont appelés qu'à certains endroits de l'application (par exemple, il existe un module qui gère toute la recherche rapide)
  |_plugins/    : librairies JS installés comme plugins. dans certains cas, on a pas pu installer la librairie via `npm`. On l'installe alors comme fichier JS minifié.
  |_router/     : le routeur qui gère les routes de l'application en rattachant à chaque URL des composants
  |_stores/     : les `stores` permettent de stocker des données réactives qui sont accessibles à toute l'application
  |_utils/      : fonctions utilitaires. contrairement aux `modules`, les utils peuvent être appelés à à peu près n'importe quel endroit de l'appli
  |_views/      : les views sont les "pages" : une `view` est un composant accessible depuis une URL et qui sera intégrée dans la balise `<RouterLink>` de notre `App.vue`
  |
  |_App.vue     : point d'entrée de l'application
  |_globals.js  : constantes utilisées par toute l'application
  |_main.js     : fichier JS qui monte l'application
  |_typedefs.js : types de données et structure des objets utilisés par toute l'application
```

---

## Les composants

Vue fonctionne avec des composants; les composants principaux, qui correspondent à une URL sont appelés des "vues" et sont présents dans `src/views/`. Ces vues appellent des composants secondaires réutilisables, présents dans `src/components/`.

`src/components/` contient plus de 70 composants, ça fait beaucoup. Certains types de composants sont groupés ensemble par des préfixes: 

- `AbDoc*` : contenu HTML de toutes les pages *À propos* et *Documentation* (vue `@views/AboutDocumentationView.vue`
- `AdvancedSearch*` : composants utilisés par la vue de recherche avancée `@views/AdvancedSearchView.vue`
- `Article*` : tous les articles de recherche du projet accessibles depuis la vue `@views/ArticleMainView.vue`. Ils ont tous exactement la même structure
- `Cartography*` : les composants utilisés par l'interface cartographique `@views/CartographyView.vue`
- `Err*` : les composants affichés en cas d'erreur
- `Filter*` : des barres de filtre pour filtrer les données affichées par un index de ressources.
- `FormKit*` : des [*custom inputs* FormKit](https://formkit.com/essentials/custom-inputs). ils ne couvrent pas toute la [checklist de fonctionnalités](https://formkit.com/essentials/custom-inputs) des inputs customs, mais seulement ce dont on a besoin. Par contre, ils pourraient être réutilisés et complétés par d'autres applications
  - `FormRepeatableDate.vue` : un cas particulier: ça fonctionne un peu comme un plugin formkit, sauf que ce n'est pas un plugin mais un composant JS normal.
- `Index*` : les *index* sont des composants qui servent à présenter une collection de ressources. 
  - parmi eux, `IndexBase` est très utile: il a une structure "agnostique" ce qui fait qu'il est utilisé pour pour présenter n'importe quel type de ressource (thème, entité nommée...). Il suffit juste d'utiliser le bon modèle de données.
- `The*` : tous les composants préfixés par `The` sont assez spéciaux puisqu'ils ne sont appelés qu'à un seul endroit de l'application: ce sont des élément structurants de l'appli, comme le menu, le footer ou navbar;
- `Ui*` : un ensemble de composants d'UI, qui ne contiennent pas de *logique* mais seulement de la mise en forme.
  - `UiButton*` contient une suite de boutons qui sont réutilisés un peu partout dans l'application.

---

## Style

Le style est écrit en CSS sans Bootstrap. 
- le fichier `src/assets/main.css` contient les bases du style : variables CSS (couleurs, polices), classes 
  réutilisables, styles de base utilisés par plusieurs composants).
  - on définit notamment des thèmes de couleurs (`main` et `negative`) avec des jeux de couleurs associés
- le style est réactif. 2 types d'affichage sont définis: *paysage* et *portrait*.
  - les *media queries* correspondantes sont :  `@media ( orientation:landscape )` et `@media ( orientation:portrait )`
  - dans le CSS, le *portrait* est l'affichage par défaut et on utilise des *media queries* spécifiques
    pour l'affichage en paysage. La logique, c'est que le portrait est l'affichage le plus restrictif, donc
    on l'utilise comme base avant de l'adapter au paysage, moins restrictif. Mais comme toujours, il y 
    a des exceptions :)
  - dans quelques très rares cas, on utilise des *media queries* plus précises, mais vraiment c'est rare

---

## Installation de `Modernizr`

On utilise un `custom build` de la librairie qui à priori est dans `src/plugins`. 
Si on veut modifier le build (ajouter des fonctionnalités), il faut 
[définir ses options et télécharger le fichier de conf ici](https://modernizr.com/download?setclasses)
avant de lancer les commandes:

```bash
sudo npm -g install modernizr                                # installation globale de modernizr
modernizr -c modernizr.config.json -d src/plugins/modernizr  # faire un build à partir de la config `modernizr.config.json`
```

---

## Licence

GNU GPL 3.0
