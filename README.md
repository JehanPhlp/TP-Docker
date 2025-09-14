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

Note : je n'ai pas choisi la verison de node slim parce qu'il y a des dificulté concernant la commande adduser (utile pour la suite)

Taille de l'image : 261MB

Temps de build : 16.7s

## V2

J'ai repéré une mauvaise pratique sur l'ordre des instructions du dockerfile.
Dans un premier temps il n'est pas nécéssaire de copié les node modules car il seront télécharger dans le npm install.

Ensuite l'ordre des dépendances joue sur le nombre d'étape qui seront exécuté à chaque rebuild, les étapes qui change rarement (installation des dépendances) doivent placé avant la copy du code de l'application (l'élément qui change le plus régullièrement). De cette manière on les dépendances ne seront pas réinstallé à chaque modification du code source.

Cette modification n'a pour but de diminué la taille de l'image mais de respecter les bonne pratique pour diminuer le temps de rebuild.

Taille de l'image : 267MB

## V3

J'ai choisi d'optiser cette image pour la prod. J'ai donc changer la variable d'environnement et changer le npm install par npm ci --omit=dev pour télécharger uniquement les dépendances nécéssaire pour la prod et ommettre celles pour le dev.

Taille de l'image : 263MB

## V4

Changement concernant l'utilisateur dans le conteneur. Il était en root précédemment, ce qui est une faille de sécurité.
La bonne pratique est d'utiliser un utilisateur non-privillégié.

Taille de l'image : 263MB

## V5 (Non fonctionnel)

J'ai essayé de séparer la partie runtime de la partie build pour optimiser un maximum la taille de l'image et les performance.

Pour cela j'ai essayé d'utiliser le build multistage de docker, mais cela n'a pas fonctionner.

```Dockerfile
FROM node:24-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY server.js ./
ENV NODE_ENV=production
RUN npm run build

FROM nginx:1.29-alpine-slim AS prod
EXPOSE 3000/tcp 4000/tcp 5000/tcp
COPY --from=builder /app /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/nginx.conf
```

Taille de l'image : 36.3MB
