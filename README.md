## Contexte:

Pour réaliser ce test nous vous laissons **1h30**. L'objectif sera de compléter et d'ajouter le maximum des fonctionnalités qui sont listées ci-dessous. Les squelettes de la partie cliente et serveur vous seront fourni au démarrage de votre test technique. La base de données vous sera transmise au travers d'un fichier **dump** qui sera dans le dépôt du serveur dans le répertoire **database/dump/**.
Il vous faudra alors créer une **biffurcation** ( *Fork* ) de ces dépôts puis réaliser le maximum des taches qui vous sont demandé. Au bout du temps imparti, nous vous demanderons de faire une **demande d'ajout** ( *Pull Request* ) sur les dépôts **originaux** sur une branche qui portera votre nom. Il est primordial que le client et le serveur puissent être lancé sans *bug* à la fin de votre production indépendemment des tâches réalisées.

## Détail des stacks à utiliser:

### Front
Le client est une application **React Typescript** utilisant **tanstack** pour réaliser le **routing**, les **requêtes** à l'API et l'affichage des **tableaux**. Certaines autres librairie sont déjà ajouté au projet pour permettre l'importation des templates de requête à l'API (n'hésitez pas à consulter le package.json !). Vous êtes libre d'utiliser n'importe quelles autres librairies que vous jugerez nécessaire si elles s'avèrent pertinentes dans le cadre de votre production.

### Back
Le server est une API développée en python via la libraire **FastAPI**. Des libraires tels que **pydantic** pour le typage ou **psycopg** sont déjà inclues au projet pour effectuer les requêtes sur la base de données. Un gestionnaire de paquet est ici aussi utilisé qui s'appelle **uvicorn** permettant tout comme yarn, npm ou pnpm d'ajouter, installer ou lancer le projet.

### Base de données
Le système de gestion de base de données à utiliser est **postgresql** dans sa version stable la plus récente. Vous pouvez si vous le souhaiter utiliser une interface graphique afin de prévisualiser le contenu de la base données à manipuler ou le faire directement depuis un terminal.

## Tâches à réaliser:

Dans une première page afficher la liste des projets actifs et inactifs (Nom du projet, date de création, date de mise à jour).
Cette liste doit pouvoir être trié par ordre alphabétiques ou par date de création.

Pour chacun des projets, différentes actions doivent être mise en place :

    - Activer / Désactiver un projet

    - Afficher le détail des indicateurs qui sont liés au projets (Nom de l'indicateur, asset, pas de temps)

    - Entrer dans un projet s'il est actif pour accéder aux valeurs numériques

Lorsque l'on choisit de naviguer vers un projet, une autre page s'affiche pour visualiser dans un tableau les différentes valeurs numériques pour chacun des pas de temps. Le tableau doit pouvoir être filtré par temps ou valeur numérique *et* trié par ordre croissant ou décroissant.

Les colonnes à afficher sont donc:

| Temps de début | Temps de fin | Indicateur 1 | ... | Indicateur N.

Ajouter une fonctionnalité permettant de **télécharger** la table au format **csv** et **json** avec la possibilité d'aggréger les valeurs numériques sur d'autre pas de temps plus large et étant un multiplicateur du pas de temps des valeurs existantes (i.e. si pas de temps de 1h pour aggréger sur 3, 6, 12h).

Penser à **l'expérience utilisateur** afin de pouvoir naviguer entre les 2 pages de l'application mais aussi la possibilité de **modifier la taille de police**.
Une application responsive sera grandement apprécié.
