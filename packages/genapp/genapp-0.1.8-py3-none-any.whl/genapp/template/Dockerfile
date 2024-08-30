# Usa una imagen base de Python 3.11
FROM python:3.11

# Variables de entorno
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /api

# Instalar  dependencias
RUN apt-get update \
    && apt-get install -y libaio1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

####################################
############## ORACLE ##############
####################################
# Descargar e instalar el cliente Oracle Instant Client
# RUN mkdir -p /opt/oracle \
#     && cd /opt/oracle \
#     && apt-get install -y wget \
#     && wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basic-linuxx64.zip \
#     && unzip instantclient-basic-linuxx64.zip \
#     && rm instantclient-basic-linuxx64.zip
# RUN mv /opt/oracle/instantclient_* /opt/oracle/instantclient
# # Agregar el directorio del cliente Oracle al LD_LIBRARY_PATH
# ENV LD_LIBRARY_PATH=/opt/oracle/instantclient:$LD_LIBRARY_PATH


####################################
############ DEPENDENCIAS ##########
####################################
# Copiar el archivo de requerimientos
COPY requirements.txt .
# Instalar las dependencias, incluyendo cx_Oracle
RUN pip install --no-cache-dir -r requirements.txt

####################################
############ SQL SERVER ############
####################################
# RUN curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc
# RUN curl https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list
# RUN sed -i 's/signed-by=\/usr\/share\/keyrings\/microsoft-prod.gpg//' /etc/apt/sources.list.d/mssql-release.list
# RUN cat /etc/apt/sources.list.d/mssql-release.list
# RUN apt-get update
# RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18 
# RUN apt-get install -y unixodbc-dev nano
# RUN apt-get install -y libgssapi-krb5-2
# RUN apt-get -y --force-yes --fix-broken install
# ENV LD_LIBRARY_PATH=/usr/lib:/usr/lib64:$LD_LIBRARY_PATH
####################################
#### OPENSSL (Para SQL Server) #####
####################################
# COPY script/deploy/openssl.cnf /tmp/openssl.cnf
# RUN mv /tmp/openssl.cnf /etc/ssl/openssl.cnf

# Prueba desde la imagen docker para ver si hay conectividad con la BBDD SQL Server
#RUN isql -v -k "Driver={ODBC Driver 18 for SQL Server};Server=10.201.25.135;Database=enbase;UID=tarsys1;PWD=tarsys1234;Encrypt=no"

####################################
############## PROYECTO ############
####################################
# Copiar archivos necesarios
COPY .env ../
COPY /. /api

# Exponer el puerto
EXPOSE 8000



# Comando por defecto para ejecutar la aplicación
CMD ["python", "main.py"]
