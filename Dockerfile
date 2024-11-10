FROM python:3.10-alpine
WORKDIR /app

# instalar librerías con requirements.txt
COPY videonet_project/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copiar el resto de la aplicacion
COPY . .

# exponer el puerto donde se ejecuta
EXPOSE 8000

# Ejecutar la  aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
