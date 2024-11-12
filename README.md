# VideoNet

VideoNet es una aplicación web para la visualización de videos, que permite a los usuarios realizar operaciones en una base de datos de videos. La aplicación está construida con Django y utiliza MySQL como sistema de gestión de bases de datos.

## Características

- Agregar nuevos videos con título, descripción y URL.
- Listar todos los videos almacenados.
- Editar la información de los videos existentes.
- Eliminar videos de la base de datos.

## Requisitos

- Python 3.10 (versión utilizada durante el desarrollo)
- MySQL
- pip (gestor de paquetes de Python)
- virtualenv (opcional, recomendado)
- Docker

## Instalación

### Kind

`sudo kind create cluster --name videonet-cluster && sudo kubectl apply -f k8s/deployment.yaml && sudo kubectl apply -f k8s/service.yaml && sudo kubectl apply -f k8s/mysql-deployment.yaml && sudo kubectl apply -f k8s/mysql-service.yaml`

Eliminar el cluster: `sudo kind delete cluster --name videonet-cluster`

Acceder al cluster: `sudo kubectl run -i --tty --rm debug --image=alpine -- sh`. Puedes ejecutar comandos como curl dentro.

#### Entrar desde el navegador

Para acceder a la aplicación desde afuera del cluster, primero encuentra la IP del nodo: `kubectl get nodes -o wide`. La IP es `INTERNAL_IP`.

Entra en tu navegador a http://`<INTERNAL_IP>`:30000.

### Compose

Antes de ejecutar docker-compose, asegúrate de que no tengas el servicio de MySQL corriendo en el puerto que mapeará el contenedor.

### Plantilla de .env

En el root del repositorio, crea un archivo llamado ".env". En este archivo se almacenan las variables de entorno utilizadas en los contenedores y en Django.

```.env
# MySQL
MYSQL_DATABASE=videonet # no modificar
MYSQL_USER=your_user
MYSQL_PASSWORD=your_password
MYSQL_ROOT_PASSWORD=your_root_password

# Azure Storage
USE_AZURE=True # True o False
AZURE_CONNECTION_STRING=your_connection_string
AZURE_CONTAINER=videos

# Django
DEBUG=True # True o False
```

### Formas de ejecución

Hay dos opciones importantes al correr la aplicación.

#### Azure

En .env, puedes establecer `USE_AZURE=False` para que el almacenamiento de videos e imágenes sea local; para activar el almacenamiento en Azure, usa`USE_AZURE=True`.

Para utilizar el almacenamiento en Azure, debes haber creado antes una Storage Account con Azure, y crea un contenedor con acceso público que tenga el nombre establecido en `AZURE_CONTAINER` en `.env`. `AZURE_CONNECTION_STRING` debe contener la cadena de conexión de tu Storage Account.

#### Docker

Para correr los contenedores de Docker con docker-compose, ejecuta el siguiente comando desde el root del repositorio:

`docker-compose -f docker-compose.dev.yml up --build`

Puedes agregar el argumento --detach para correr los contenedores en el fondo.

Para correr la aplicación sin contenedores, ejecuta el siguiente comando desde el root del repositorio:

`python videonet_project/manage.py makemigrations && python videonet_project/manage.py migrate && python videonet_project/manage.py runserver`

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la Licencia BSD-3-Clause. Consulta el archivo `LICENSE` para más detalles.
