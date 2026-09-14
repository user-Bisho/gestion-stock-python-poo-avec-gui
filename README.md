# gestion-stock-python-poo-avec-gui
Mini projet Python POO - Application de gestion des stocks avec Tkinter


Gestion de stock Python

Petit projet Python pour gérer le stock d'une entreprise.

Le but du programme est de pouvoir ajouter des produits, les modifier, les supprimer et enregistrer des ventes. Quand une vente est faite la quantité du produit est automatiquement retirée du stock.

J'ai utilisé Tkinter pour faire une petite interface graphique pour que le programme soit plus simple à utiliser.

Fonctionnalités
Ajouter un produit
Modifier un produit
Supprimer un produit
Rechercher un produit avec son nom ou sa référence
Voir les produits dans le stock
Trier les produits
Enregistrer une vente
Mise à jour automatique du stock après une vente
Voir quelques statistiques sur les ventes
Voir les produits avec peu de stock
Sauvegarde des produits et des ventes dans des fichiers JSON
Lancer le projet

Il faut avoir Python installé.

Ensuite lancer le fichier :

python gestion_stocks.py

Normalement aucune bibliothèque supplémentaire est nécessaire car j'ai utilisé surtout Tkinter, json et datetime qui sont déjà avec Python.

Fichiers

Pour l'instant le projet contient principalement :

gestion_stocks.py
README.md

Quand le programme est utilisé il va aussi créer les fichiers :

produits.json
ventes.json

Ils servent à garder les produits et les ventes même après avoir fermé le programme.

Interface

L'interface a été faite avec Tkinter. Elle reste assez simple mais elle permet de faire les principales actions sans utiliser le terminal.
