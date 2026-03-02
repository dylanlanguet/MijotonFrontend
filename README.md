# 🍳 Mijotons - Application de Recettes de Cuisine

Mijotons est une plateforme de partage de recettes culinaires et de cocktails. Ce projet est développé dans le cadre d'un TP de développement Web full-stack, utilisant **Django** pour la partie logicielle et le rendu.

## 🚀 Fonctionnalités
- **Consultation :** Liste des recettes avec filtres par catégorie.
- **Détails :** Ingrédients, étapes, difficulté et temps de préparation.
- **Recherche :** Moteur de recherche par nom ou catégorie.
- **Gestion (À venir) :** Système de vote, commentaires et espace membre.

## 🛠 Prérequis
Avant de commencer, assurez-vous d'avoir installé :
- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)

## 📦 Installation et Configuration

Suivez ces étapes pour lancer le projet localement :

### 1. Cloner le projet
```bash
git clone https://github.com/dylanlanguet/mijotons.git
cd mijotons
```

### 2. Créer un environnement virtuel

Il est fortement recommandé d'isoler les dépendances du projet.

# Sur Windows
```bash
python -m venv venv
venv\Scripts\activate
```

# Sur macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install django
# Si vous avez un fichier requirements.txt :
# pip install -r requirements.txt
```

### 4. Configurer la base de données

Appliquez les migrations pour créer la structure de la base de données SQLite par défaut.
```bash
python manage.py migrate
```

### 5. Créer un compte administrateur (Optionnel)

Pour accéder à l'interface de gestion de Django (/admin) et ajouter des recettes facilement :
```bash
python manage.py createsuperuser
```

## 🏃 Lancement de l'application

Démarrez le serveur de développement :
```bash
python manage.py runserver
```

L'application sera accessible à l'adresse suivante : http://127.0.0.1:8000/
## 📂 Structure du projet
- mijotons/ : Configuration principale du projet (settings, urls).
- recettes/ : Application gérant la logique métier, les modèles et les vues.
- templates/ : Fichiers HTML (Django Templates).
- static/ : Fichiers CSS, images et JavaScript.
