.PHONY: create.venv \
		install.libs

## GENERAL ##
REQUIREMENTS_FILE = requirements.txt

venv.create: ## Crea el entorno virtual (virtualenv): make venv.create
	$(call detect_user)
	@echo "Create directory of virtualenv: ${VENV_DIR}"
	@docker container run \
		--workdir "/${APP_DIR}" \
		--rm \
		-it \
		-v "${PWD}/${VENV_DIR}":/${VENV_DIR} \
		-v "${PWD}/${APP_DIR}":/${APP_DIR} \
		--tty=false \
		${IMAGE_DEV}  \
		python3 -m venv /${VENV_DIR}
	@rm -rf ${PWD}/passwd

venv.lib.install: ## Instala las librerias en el entorno virtual (virtualenv): make venv.lib.install
	$(call detect_user)
	@echo "Install libraries from: ${REQUIREMENTS_FILE}"
	@docker container run \
		--workdir "/${APP_DIR}" \
		--rm \
		-it \
		-v "${PWD}/${VENV_DIR}":/${VENV_DIR} \
		-v "${PWD}/${APP_DIR}":/${APP_DIR} \
		--tty=false \
		${IMAGE_DEV}  \
		"/${VENV_DIR}/bin/pip" install -r ${REQUIREMENTS_FILE}
	@rm -rf ${PWD}/passwd
	
venv.lib.list: ## Listar librerias instaladas: make venv.lib.list
	@echo "List Installed libraries..."
	@docker container run \
		--workdir "/${APP_DIR}" \
		--rm \
		-it \
		-v "${PWD}/${VENV_DIR}":/${VENV_DIR} \
		-v "${PWD}/${APP_DIR}":/${APP_DIR} \
		--tty=false \
		${IMAGE_DEV}  \
		"/${VENV_DIR}/bin/pip" freeze