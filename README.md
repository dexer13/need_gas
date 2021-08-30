### Proyecto:
#### Microservicios que permite solicitar gasolina si me quedé con sin gasolina
***
### Índice
1. [Características](#caracter-sticas-)
3. [Tecnologías](#tecnologías)
4. [IDE](#ide)
5. [Instalación](#instalación)
6. [Demo](#demo)
7. [Autores](#autores)
8. [Institución Académica](#institución-académica)
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
 $ workon proyect_env
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
***

### Autor
Proyecto desarrollado por:
 - Denis González [GitHub](https://github.com/dexer13) [LinkedIn](https://www.linkedin.com/in/denis-eduardo-isidro-gonzalez-428a51210/)

***