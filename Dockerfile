FROM python:3.12

# Define el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requisitos y lo instala
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación Django
COPY . /app/

# Copia el script de espera al contenedor
COPY wait-for-it.sh /app/wait-for-it.sh

# Asegúrate de que el script de espera sea ejecutable
RUN chmod +x /app/wait-for-it.sh

# Exponer el puerto de Django
EXPOSE 8000

# Comando por defecto para correr el servidor de desarrollo de Django
CMD ["sh", "-c", "/app/wait-for-it.sh db:5432 -- python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
