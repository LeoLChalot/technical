# Mémo : Configuration de l'environnement Backend

Ce document résume les étapes nécessaires pour configurer l'environnement de développement du serveur, y compris la mise en place de la base de données PostgreSQL à partir de zéro lorsque les identifiants ne sont pas fournis.

## Étape 1 : Configuration de l'environnement Python

Objectif : Installer les dépendances du projet et s'assurer que le serveur peut se lancer.

1.  **Installer `uv`** (si non présent) : `uv` est un gestionnaire de paquets et d'environnements virtuels rapide pour Python.
    ```bash
    # Pour macOS et Linux
    curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
    
    # Pour Windows (dans PowerShell)
    irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex
    ```
    *Note : Pensez à redémarrer le terminal après l'installation pour que la commande soit reconnue.*

2.  **Vérifier la version de Python** : Le projet peut requérir une version spécifique de Python (ex: Python 3.11). Utilisez `python --version` pour vérifier. Un outil comme `pyenv` peut être utile pour gérer plusieurs versions.

3.  **Synchroniser les dépendances** : Depuis le dossier racine du projet serveur (ex: `technical_server`), installez toutes les dépendances listées dans le fichier `pyproject.toml`.
    ```bash
    uv sync
    ```

## Étape 2 : Création de la base de données et de l'utilisateur PostgreSQL

Objectif : Créer un utilisateur et une base de données dédiés au projet.

1.  **Prérequis (Windows)** : S'assurer que les outils en ligne de commande de PostgreSQL sont accessibles. Pour cela, ajoutez le dossier `bin` de votre installation PostgreSQL (ex: `C:\Program Files\PostgreSQL\16\bin`) à la variable d'environnement `Path` du système.

2.  **Créer un nouvel utilisateur (rôle)** : Nous créons un utilisateur (`technical_user`) avec un mot de passe.
    * L'option `-U postgres` est cruciale pour se connecter en tant qu'administrateur et avoir les droits de création.
    ```bash
    # Crée un nouvel utilisateur de manière interactive (-P demande un mot de passe)
    createuser --interactive -P -U postgres
    ```
    Suivez les instructions :
    * Nom du rôle à ajouter : `technical_user`
    * Mot de passe : `(à définir et mémoriser)`
    * Doit-il être super-utilisateur ? `n`
    * Peut-il créer des bases de données ? `y`
    * Peut-il créer de nouveaux rôles ? `n`

3.  **Créer une nouvelle base de données** : Nous créons une base de données (`technical_db`) et désignons notre nouvel utilisateur comme son propriétaire.
    ```bash
    # Crée une base de données (-O spécifie le propriétaire)
    createdb -O technical_user technical_db -U postgres
    ```

## Étape 3 : Configuration de l'application FastAPI

Objectif : Permettre à l'application de se connecter à la base de données que nous venons de créer.

1.  **Ajouter l'URL de la base de données au fichier `.env`** :
    * Ouvrez le fichier `technical_server/.env`.
    * Ajoutez la ligne suivante en remplaçant `VOTRE_MOT_DE_PASSE` par celui que vous avez défini :
    ```env
    DATABASE_URL="postgresql://technical_user:VOTRE_MOT_DE_PASSE@localhost:5432/technical_db"
    ```

2.  **Mettre à jour `settings.py`** :
    * Ouvrez `technical_server/app/settings.py`.
    * Ajoutez le champ `database_url` à la classe `Settings` pour que Pydantic charge cette nouvelle variable depuis le `.env`.
    ```python
    class Settings(BaseSettings):
        # ... autres variables
        
        # Ligne à ajouter
        database_url: str = "postgresql://user:password@host:port/db" # Valeur par défaut de secours
    
        model_config = SettingsConfigDict(env_file=".env")
    ```

## Étape 4 : Restauration des données

Objectif : Peupler la base de données vide avec la structure et les données du fichier de sauvegarde (`.dump`).

1.  **Identifier le type de dump** : Après un échec avec `pg_restore`, nous avons déterminé que le fichier `.dump` était un script SQL texte brut.

2.  **Utiliser le bon outil (`psql`)** : La restauration d'un script SQL se fait avec l'outil `psql`.
    * `-U` : Spécifie l'utilisateur pour la connexion.
    * `-d` : Spécifie la base de données cible.
    * `-f` : Spécifie le fichier SQL à exécuter.
    ```bash
    # Commande finale pour restaurer la base de données
    # Assurez-vous d'adapter le chemin vers le fichier .dump
    psql -U technical_user -d technical_db -f "app/database/db.dump"
    ```
    *Le terminal demandera le mot de passe de `technical_user` avant d'exécuter le script.*
