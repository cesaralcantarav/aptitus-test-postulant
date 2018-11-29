.DEFAULT_GOAL := help

include ./makefiles/virtual-env.mk
include ./makefiles/deploy-aws.mk

## GENERAL ##
OWNER            = aptitus
SERVICE_NAME     = testpostulant
APP_DIR          = app
VENV_DIR         = venv

## DEPLOY ##
ENV             ?= lab
DEPLOY_REGION   ?= ap-northeast-1
INFRA_BUCKET    ?= infraestructura.lab
SLACK_CHANNEL   ?= apt-testing

## RESULT_VARS ##
PROJECT_NAME    = ${OWNER}-${ENV}-${SERVICE_NAME}
IMAGE_DEV       = ${PROJECT_NAME}:dev

## FUNCTION ##
define detect_user
	$(eval WHOAMI := $(shell whoami))
	$(eval USERID := $(shell id -u))
	$(shell echo 'USERNAME:x:USERID:USERID::/app:/sbin/nologin' > $(PWD)/passwd.tmpl)
	$(shell \
		cat $(PWD)/passwd.tmpl | sed 's/USERNAME/$(WHOAMI)/g' \
			| sed 's/USERID/$(USERID)/g' > $(PWD)/passwd)
	$(shell rm -rf $(PWD)/passwd.tmpl)
endef

## TARGET ##
ssh: ## Conectar al container por el protocolo ssh: make ssh
	@docker container run \
		--workdir "/${APP_DIR}" \
		--rm \
		-it \
		-v "${PWD}/${VENV_DIR}":/${VENV_DIR} \
		-v "${PWD}/${APP_DIR}":/${APP_DIR} \
		${IMAGE_DEV} "/bin/zsh"

build: ## Construir imagen para development: make build
	@docker build \
		-f docker/dev/Dockerfile \
		-t $(IMAGE_DEV) \
		docker/dev/ \
		--no-cache

## HELP ##
help:
	@printf "\033[31m%-16s %-59s %s\033[0m\n" "Target" "Help" "Usage"; \
	printf "\033[31m%-16s %-59s %s\033[0m\n" "------" "----" "-----"; \
	grep -hE '^\S+:.*## .*$$' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' | sort | awk 'BEGIN {FS = ":"}; {printf "\033[32m%-16s\033[0m %-58s \033[34m%s\033[0m\n", $$1, $$2, $$3}'
