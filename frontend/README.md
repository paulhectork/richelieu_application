# Frontend

---

## Installation et utilisation

### Installation

```bash
npm install npm install
```

### Utilisation (dev)

L'argument `--mode` permet de changer de configuration, selon que le
backend auquel on est connecté soit sur serveur ou sur notre machine locale.
Voir le fichier `vite.config.js` et [la documentation vite](https://vitejs.dev/config/#conditional-config)
pour plus d'informations.

**Attention: le `--` est très important pour séparer le script npm de ses arguments**

```bash
# si le backend est en local
npm run dev -- --mode backend-local

# si le backend est sur serveur
npm run dev -- --mode backend-server
```

Si on installe le frontend sur serveur et que l'on veut accéder à l'appli
depuis un navigateur, il faut exposer l'appli avec `--host`:

```bash
# logiquement, ici on se connecte au backend qui est sur le serveur
npm run dev -- --mode backend-server --host
```

### Utilisation (prod)

TODO

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
---
---

## default conf
This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
npm run test:unit
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```