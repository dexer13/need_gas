### Proyecto:
#### Microservicios que permite solicitar gasolina si me quedé con sin gasolina
***
### Índice
1. [Características](#caracter-sticas-)
2. [Tecnologías](#tecnologías)
3. [IDE](#ide)
4. [Instalación](#instalación)
5. [Servicios](#servicios)
6. [Autor](#autor)
***

#### Características:

  - Servicios REST
  - Simulación de solicitud de un servicio por parte de un cliente

***
#### Tecnologías

  - Python
  - Django
  - Django rest framework
  - Poetry
  - celery
  
***
#### IDE
  - El proyecto se desarrolla con [PyCharm](https://www.jetbrains.com/es-es/pycharm/) con [licencia de estudiante](https://www.jetbrains.com/es-es/community/education/#students)
  - Entornos virtuales del interprete python3.8 [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
  
***
### Instalación

 - Instalar [poetry](https://python-poetry.org/) (Opcional)

Creación del entorno virtual en el sistema operativo con [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) usando python 3.8 o superior

```shell script
 $ mkvirtualenv project -p /usr/bin/python3.x
 $ workon project_env
```
Clonar el repositorio privado desde GitHub
```shell script
 $ git clone https://github.com/dexer13/need_gas.git project
 $ cd project
```

Instalar las librerías necesarias para la ejecución, puede usar poetry o instalar tradicionalmente usando pip
#### Usando poetry
```shell script
 $ poetry install
```
#### usando pip (tradicional)
```shell script
 $ pip install -Ur requirements.txt
```
Se deben ejecutar las migraciones para que cree la base de datos
```shell script
 $ python manage.py makemigrations
 $ python manage.py migrate
```
Cargar información semilla
```shell script
 $ python manage.py loaddata locations
 $ python manage.py loaddata drivers
 $ python manage.py loaddata gas_stations
```
Actualizar Información de los clientes
```shell script
 $ python manage.py update_customers
```
Actualizar Información de las gasolineras, para que agreguen a los conductores mas cercanos
```shell script
 $ python manage.py update_gas_stations
```
Levantar el proyecto
```shell script
 $ python manage.py runserver
```
Ejecutar celery
```shell script
 $ celery -A app worker -l info
```
***
### Servicios
#### Servicios solicitados
Consulta los servicios asignados en un día en específico
- [http://localhost:8000/api/v1/services_by_customer/{YYYY-MM-DD}/](http://localhost:8000/api/v1/services_by_customer/{YYYY-MM-DD}/)

Consulte los servicios de un conductor en un día en específico
- [http://localhost:8000/api/v1/services_by_driver/{driver_identification}/{YYYY-MM-DD}/](http://localhost:8000/api/v1/services_by_driver/<str:identification>/{YYYY-MM-DD}/)

Servicio que a partir de un punto de ubicación un conductor seleccionado y el tiempo que demora en llega
- [http://localhost:8000/api/v1/require_a_service/{X}/{Y}/](http://localhost:8000/api/v1/require_a_service/{X}/{Y}/)

Consulta los conductores indicando cuales estan ocupados y cuales libres ordenados por cercania a un punto de ubicación
- [http://localhost:8000/api/v1/drivers_sorted_by_distance/{X}/{Y}/](http://localhost:8000/api/v1/drivers_sorted_by_distance/{X}/{Y}/)

#### Servicios adicionales
Consulta todos los conductores, gasolineras y clientes que tienen un punto de ubicación
- [http://localhost:8000/api/v1/info_map/](http://localhost:8000/api/v1/info_map/)

Solicita un servicio, el cual simula el recorrido del conductor hasta cumplir con el servicio
- [http://localhost:8000/api/v1/request_service/{identificación_del_cliente}/](http://localhost:8000/api/v1/request_service/{identificación_del_cliente})

Puede ver los objetos en tiempo real, abriendo en el navegador el archivo **index.html**, ubicado en la raiz del proyecto
***
### Autor
Proyecto desarrollado por:
 - Denis González [GitHub](https://github.com/dexer13) [LinkedIn](https://www.linkedin.com/in/denis-eduardo-isidro-gonzalez-428a51210/)

***