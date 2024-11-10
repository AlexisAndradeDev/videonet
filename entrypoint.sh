#!/bin/sh

# Esperar a que la base de datos esté lista
while ! nc -z db 3306; do
  echo "Esperando a que la base de datos esté lista..."
  sleep 1
done

# Ejecutar las migraciones
python manage.py makemigrations
python manage.py migrate

# Iniciar el servidor
exec python manage.py runserver 0.0.0.0:8000