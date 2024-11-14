# VideoNet

VideoNet es una aplicación web para la visualización de videos, que permite a los usuarios realizar operaciones en una base de datos de videos. La aplicación está construida con Django y utiliza MySQL como sistema de gestión de bases de datos.

## Características

- Agregar nuevos videos con título, descripción y URL.
- Listar todos los videos almacenados.
- Editar la información de los videos existentes.
- Eliminar videos de la base de datos.
- Manejo de usuarios.

## Requisitos

- Python 3.10 (versión utilizada durante el desarrollo)
- MySQL
- pip (gestor de paquetes de Python)
- virtualenv (opcional, recomendado)
- Docker

## Instalación

### (!) Encoding incorrecto (Windows)

El archivo entrypoint.sh puede ocasionar problemas si End of Line (EOL) está configurado como CRLF, que al clonar el repositorio en Windows podría guardarse con encoding CRLF. Asegúrate de cambiarlo a LF y guardar el archivo (puedes hacerlo en Visual Studio Code; en la parte inferior derecha se muestra CRLF, cámbialo a LF), o recibirás un error `web_1  | standard_init_linux.go:228: exec user process caused: no such file or directory` al ejecutar `docker-compose`.

### Kind

`sudo kind create cluster --name videonet-cluster && sudo kubectl apply -f k8s/configmap.yaml && sudo kubectl apply -f k8s/deployment.yaml && sudo kubectl apply -f k8s/service.yaml && sudo kubectl apply -f k8s/mysql-deployment.yaml && sudo kubectl apply -f k8s/mysql-service.yaml`

Una vez que los servicios estén corriendo, comprobable con `kubectl get pods` (Running), puedes ingresar al sitio web.

Eliminar el cluster: `sudo kind delete cluster --name videonet-cluster`

Acceder al cluster: `sudo kubectl run -i --tty --rm debug --image=alpine -- sh`. Puedes ejecutar comandos como curl dentro.

#### Entrar desde el navegador

#### Opción 1

Para acceder a la aplicación desde afuera del cluster, primero encuentra la IP del nodo: `kubectl get nodes -o wide`. La IP es `INTERNAL_IP`.

Entra en tu navegador a http://`<INTERNAL_IP>`:30000.

#### Opción 2 (configuración problemática de WSL2)

En ocasiones, puede no tenerse acceso directo desde Windows al puerto vinculado a la IP interna de WSL2. Esto puede solucionarse ejecutando `kubectl port-forward service/videonet 8000:8000`, que redirige el puerto 8000 del servicio videonet al puerto 8000 en localhost en la máquina host.

Entra en tu navegador a http://localhost:8000/.

Para Jenkins, utiliza `kubectl port-forward service/jenkins 8080:8080`.

### Compose

Antes de ejecutar docker-compose, asegúrate de que no tengas el servicio de MySQL corriendo en el puerto que mapeará el contenedor.

### Plantilla de .env

En el root del repositorio, crea un archivo llamado ".env". En este archivo se almacenan las variables de entorno utilizadas en los contenedores y en Django.

```.env
# MySQL
MYSQL_DATABASE=videonet
MYSQL_USER=your_user # No puede usarse el usuario root
MYSQL_PASSWORD=your_password
MYSQL_ROOT_PASSWORD=your_root_password

# Azure Storage
USE_AZURE=False # True o False
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

`docker build . && docker-compose -f docker-compose.dev.yml up --build`

Puedes agregar el argumento --detach para correr los contenedores en el fondo.

Para correr la aplicación sin contenedores, ejecuta el siguiente comando desde el root del repositorio:

`python videonet_project/manage.py makemigrations && python videonet_project/manage.py migrate && python videonet_project/manage.py runserver`

#### Comprobar contenido del contenedor (web)

Ejecuta en la carpeta root: `docker-compose -f docker-compose.dev.yml run web sh`. Puedes ejecutar comandos como `ls` para comprobar el contenido.

## Jenkins

Si estás usando Kubernetes, puedes acceder a Jenkins por medio de un contenedor. Con los siguientes comandos puedes crear los recursos de Jenkins: `sudo kubectl apply -f k8s/jenkins-pvc.yaml && sudo kubectl apply -f k8s/jenkins-deployment.yaml && sudo kubectl apply -f k8s/jenkins-service.yaml`.

Ahora puedes entrar con http://localhost:30001, que te llevará a la interfaz de Jenkins. Si la página se muestra como no encontrada, una solución pude ser `kubectl port-forward service/jenkins 8080:8080` y entrar a http://localhost:8080. La primera vez que accedas, necesitarás desbloquear Jenkins. Ejecuta este comando para encontrar la contraseña: `kubectl exec -it <jenkins-pod-name> -- cat /var/jenkins_home/secrets/initialAdminPassword`. El nombre del pod puedes obtenerlo con `kubectl get pods`.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la Licencia BSD-3-Clause. Consulta el archivo `LICENSE` para más detalles.
