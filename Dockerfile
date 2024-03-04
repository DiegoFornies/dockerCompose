#usamos la imagen oficial de python
FROM python:3.9-slim

#establecemos el directorio de trabajo en /app
WORKDIR /app

#copiamos los archivos necesarios al contenedor
COPY . .

#instalamos las dependencias de python que no vienen por defecto
RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

#creamos la variable de entorno encargada de guardar el api key
ENV APIKEY api_key.txt

#ejecutamos la aplicación cuando se inicie el contenedor, con el api key como argumento
CMD ["python", "app.py", "$APIKEY"]
