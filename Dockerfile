FROM python:3.10-alpine
WORKDIR /app

RUN apk update \
    && apk add --no-cache gcc musl-dev \
    && apk add pkgconfig python3-dev mariadb-dev

# Instalar librerías con requirements.txt
COPY videonet_project/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY videonet_project /app/videonet_project

# Copiar el script de entrada y hacerlo ejecutable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Exponer el puerto donde se ejecuta
EXPOSE 8000

# Ejecutar la aplicación con el script de entrada
WORKDIR /app/videonet_project/
CMD ["/entrypoint.sh"]
