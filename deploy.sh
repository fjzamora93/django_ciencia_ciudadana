#!/bin/bash

# Nombre del proyecto y la imagen
IMAGE_NAME="pinguiton"
DOCKER_USER="fjzamora93"
TAG="latest"

# Mostrar los comandos que se están ejecutando
set -e

echo "🚧 Construyendo la imagen Docker..."
docker build -t $IMAGE_NAME .

echo "🏷️ Etiquetando la imagen como $DOCKER_USER/$IMAGE_NAME:$TAG"
docker tag $IMAGE_NAME $DOCKER_USER/$IMAGE_NAME:$TAG

echo "🔐 Iniciando sesión en Docker Hub (si es necesario)..."
docker login

echo "⏫ Subiendo imagen a Docker Hub..."
docker push $DOCKER_USER/$IMAGE_NAME:$TAG

echo "✅ Despliegue completado: https://hub.docker.com/r/$DOCKER_USER/$IMAGE_NAME"
