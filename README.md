# Projet DevNet - Automatisation avec Netmiko

Ce projet réalise les tâches d'automatisation réseau sur une topologie Cisco (R1, R2, SW1, SW2) via le protocole Telnet (adapté pour les environnements de simulation CML).

## Objectifs du TP
1. Connexion aux routeurs et switchs.
2. Récupération des informations système (`show version`).
3. Affichage des interfaces (`show ip interface brief`).
4. Affichage de la table de routage (`show ip route`).

## Structure du projet
- `main.py` : Script principal contenant la logique de connexion Netmiko et l'exécution des commandes.
