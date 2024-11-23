FROM python:3.10-alpine
WORKDIR /app

RUN apk update \
    && apk add --no-cache gcc musl-dev \
    && apk add pkgconfig python3-dev mariadb-dev \
    && apk add --no-cache bash

# Copiar el resto de la aplicación
COPY videonet_project /app/videonet_project
RUN pip install --no-cache-dir -r videonet_project/requirements.txt

# Usar bash para evitar errores de permisos
SHELL ["/bin/bash", "-c"]
# Copiar el script de entrada y hacerlo ejecutable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Exponer el puerto donde se ejecuta
EXPOSE 8000

# Ejecutar la aplicación con el script de entrada
CMD ["/app/entrypoint.sh"]
