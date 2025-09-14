# Rapport docker TP2

## V0

images sans modification / optimisation

Taille de l'image : 1.73GB

Temps de build : 89.2s

## V1

1. Changement d'image de base en une image plus légère : node:24-alpine

note : Erreur de compilation à la ligne suivante lors du build de l'image :

```Dockerfile
RUN apt-get update && apt-get install -y build-essential ca-certificates locales && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen
```

Apres avoir regarder dans le code, j'en ai conclus qu'elle n'étais pas nécéssaire au bon fonctionnement de l'application, je l'ai donc retirer.

Le serveur tourne correctement sur le port 3000 et aucun probème concernant l'horrodatage.

2. J'ai vérouillé la version de node à la 24

```Dockerfile
FROM node:24-alpine
```

Cela fait partie des bonne pratique.

Taille de l'image : 261MB

Temps de build : 16.7s
