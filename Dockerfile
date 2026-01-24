# Creamos la imagen a partir de una que ya tenga python 3.10 para correr la API y en una version ligera
# que no trae todas las librerias que no sean exclusivamente necesarias para que sea ligero.
FROM python:3.10-slim

# Instalamos en el sistema operativo de la imagen (Debian) librerias del sistema que necesitamos
# para correr la app en fastapi sin problemas.
RUN apt-get update && apt-get install -y gcc && apt-get clean

# Esto crea un directorio dentro de el sistema de la imagen y todo lo que hagamos se hara dentro de este
WORKDIR /app

# Copiamos todo el codigo fuente de la app dentro del directorio que creamos 
COPY . /app

# Instalamos las dependencias que necesita la app en el sistema.
RUN pip install --no-cache-dir -r requirements.txt


# Creamos una variable de entorno que tendra el sistema de la imagen 
# Descomentar en LOCAL
#ENV GOOGLE_APPLICATION_CREDENTIALS=/app/sensitive/service-account-key.json 


# Le indicamos a la imagen que cuando se ejecute, le debe pedir a docker que abra ese puerto en el sistema operativo
# para recibir trafico del exterior de la plataforma docker, hacia el contenedor que ejecuta esta imagen.
EXPOSE 8080


# Diferencia RUN y CMD
# RUN: Este permite ejecutar comandos en el sistema base (debian, ubuntu, etc) de la imagen comandos al momento 
# de construir la imagen para dejarla toda lista o preparada con los componentes como librerias o dependencias
# para ejecutar la app. Lo usamos para hacer todas las instalaciones necesarias.

# CMD: Este permite indicar que comandos debe ejecutar la imagen una vez la ejecutamos en el contenedor, permitiendo
# inicializar la app o ejecutar scripts que necesitamos correr al momento que la imagen se acabe de ejecutar en 
# un contenedor de la plataforma docker. Lo usamos para inicializar aplicaciones o correr scripts al momento de encender
# la maquina o imagen en el contenedor.



# Comando indica que una vez se ejecute la imagen en el contenedor debe arrancar al servidor uvicorn para que ejecute
# la aplicacion en FastAPI, donde indicamos que la ejecutaremos en 1 proceso, escuchara a en todas las interfaces no solo la local (0.0.0.0)
#y que utilizara el puerto 8080 internamente en el contenedor dentro de la plataforma docker o en su red interna.
CMD ["uvicorn", "app.main:app", "--workers", "1", "--timeout-keep-alive", "0", "--host", "0.0.0.0", "--port", "8080"]

# Expose habre el puerto 8080 en el sistema operativo de donde se ejecuta docker al momento de correr la imagen
# y el comando de uvicorn lo abre dentro del sistema de la imagen en el contenedor una vez se ejecuta, si queremos
# que el trafico al 8080 del sistema operativo vaya al del contenedor debemos mapearlo al momento de correr la imagen.





