# Application du projet Richelieu

---

## Installation et utilisation

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
