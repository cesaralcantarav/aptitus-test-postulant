Aptitus Test Postulant
==================================
Test de Postulante

¿Que incluye?
--------------
* source Code (directorio app)
* sam.yml/registry.yml (directorio cloudformation)
* Dockerfile (directorio docker/dev/latest)
* Jenkinsfile
* Makefile (directorio makefiles)

Requerimientos
--------------
* Docker
* Docker Compose
* Cmake

Help
----
* make
* make help

Comandos
--------
```console
Target           Help                                                        Usage
------           ----                                                        -----
build.latest      Construir imagen para deploy                               make build.latest
build             Construir imagen para development                          make build
create.repository.aws.ecr  Crear repositorio en ecr de aws                            create.repository.aws.ecr
delete.repository.aws.ecr  Elimina el registro del container en aws ECR service       make delete.repository.aws.ecr
login.aws.ecr     Login en ecr de aws                                        make login.aws.ecr
push.aws.ecr      Publicar imagen en ecr de aws                              make push.aws.ecr
run.task          Ejecuta el task                                            make run.task
ssh               Conectar al container por el protocolo ssh                 make ssh
stack.delete      Elimina el stack con cloudformation                        make stack.delete
stack.deploy      Despliega el stack con cloudformation                      make stack.deploy
venv.create       Crea el entorno virtual (virtualenv)                       make venv.create
venv.lib.install  Instala las librerias en el entorno virtual (virtualenv)   make venv.lib.install
venv.lib.list     Listar librerias instaladas                                make venv.lib.list
```

Estructura del proyecto
=======================

Directorio de la Aplicacion
---------------------------
```console
app
├── bin
└── cli
requirements.txt
setup.py
```

Directorio de Cloudformation
----------------------------
```console
cloudformation
├── registry.yml
└── sam.yml
```

Directorio de Docker
--------------------
```console
docker
└── dev
    └── Dockerfile
└── latest
    └── Dockerfile
```

Deploy Stack de Cloudformation de la aplicación
===============================================
Para la aplicación debe usar los siguientes comandos:

```console
~/$ make build
~/$ make venv.create
~/$ make venv.lib.install
~/$ make build.latest
~/$ make login.aws.ecr
~/$ make create.repository.aws.ecr  (Solo se ejecuta la primera vez, para crear el repository)
~/$ make push.aws.ecr
~/$ make stack.deploy
```

**NOTE:**
Se debe construir la imagen del contenedor de docker cuando no exista en el repositorio local de docker del equipo o cuando se realize un cambio en el archivo Dockerfile, usando el siguiente comando:
```console
~/$ make build
```

Eliminar Stack de Cloudformation
================================
Para eliminar el stack de cloudformation usar el siguiente comando:

```console
~/$ make stack.delete
```
