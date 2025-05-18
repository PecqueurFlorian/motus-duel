Motus-Duel est un jeu en Python inspiré de l’émission Motus, jouable en local à deux joueurs.
L’objectif est simple : trouver un mot mystère choisi par l’autre joueur, en un maximum de 5 tentatives.

Fonctionnement du jeu
Deux joueurs s'affrontent à tour de rôle.
À chaque manche (5 au total), un joueur choisit un mot secret, l'autre tente de le deviner.
Le mot est saisi de manière masquée (affichage en *).
Feedback visuel :
Lettre bien placée en vert
Lettre mal placée en jaune
Lettre absente en rouge
Un système de score détermine le vainqueur à la fin des 5 manches.
Fonctionnalités principales

Interface graphique propre avec Pygame
Saisie masquée du mot secret
Alternance automatique des manches
Affichage des scores en temps réel
Écran de résultat final
Connexion à une base de données MySQL pour enregistrer les parties

Structure des fichiers:
motus_pygame.py : point d'entrée principal du jeu
motus.py : logique de vérification et comparaison des mots
motus_ui.py : gestion de l'affichage graphique dans Pygame
database.py : (non inclus sur GitHub) interactions avec la base de données
requirements.txt : dépendances nécessaires au projet

Installation:
git clone https://github.com/PecqueurFlorian/motus-duel.git
cd motus-duel
Installer les dépendances :
pip install -r requirements.txt
Lancer le jeu :
python motus_pygame.py
Le fichier database.py contient les informations de connexion à ta base MySQL locale (MAMP + Workbench).
Il n’est pas publié dans le dépôt pour des raisons de sécurité. Tu dois le créer localement.

Technologies utilisées
Python
Pygame
SQL / MySQL

Les identifiants MySQL sont stockés localement dans database.py, exclu du dépôt via .gitignore.

 Auteur
Projet réalisé par Florian Pecqueur
