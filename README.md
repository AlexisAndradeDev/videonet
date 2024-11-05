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

## Instalación

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/AlexisAndradeDev/videonet.git
   cd videonet
   ```

2. **Crea y activa un entorno virtual**:
   ```bash
   pip install virtualenv
   virtualenv venv
   # En Windows
   # Opción 1:
   venv\Scripts\activate
   # Opción 2:
   "venv\Scripts\activate"
   # En macOS y Linux
   source venv/bin/activate
   ```

3. **Instala las dependencias**:
   ```bash
   pip install -r videonet_project/requirements.txt
   ```

4. **Configura la base de datos**:
   - Crea una base de datos en MySQL llamada `videonet`.
   - Actualiza la configuración de la base de datos en `videonet_project/videonet_project/settings.py` con tus credenciales de MySQL.

5. **Ejecuta las migraciones**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Utiliza tu cadena de conexión de Azure Blob Storage**:
   - Crea una Storage Account en Azure.
   - Crea un contenedor para esa Storage Account llamado `videos`.
   - Cambia el nivel de acceso del contenedor para que tenga acceso anónimo.
   - Actualiza tu cadena de conexión de tu Azure Storage Account en `videonet_project/videonet_project/settings.py`, en el diccionario STORAGES.

7. **Ejecuta el servidor de desarrollo**:
   ```bash
   python manage.py runserver
   ```

8. **Accede a la aplicación**:
   Abre tu navegador y visita `http://127.0.0.1:8000/`.

## Despliegue

Para desplegar la aplicación en un entorno de producción, se recomienda utilizar Docker, Kubernetes y Terraform. Consulta los archivos `Dockerfile`, `docker-compose.yml`, y los directorios `k8s` y `terraform` para obtener detalles sobre la configuración.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la Licencia BSD-3-Clause. Consulta el archivo `LICENSE` para más detalles.
