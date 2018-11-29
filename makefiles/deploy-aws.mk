.PHONY: login.aws.ecr \
		 create.repository.aws.ecr \
		 batch.delete.image.aws.ecr \
		 build.latest \
		 push.aws.ecr \
		 stack.deploy \
		 stack.delete \
		 run.task   

## DEPLOY ##
ACCOUNT_ID 		  ?= 929226109038
BUILD_TIMESTAMP   ?= 20180918
BUILD_NUMBER 	  ?= 1
BRANCH_BUILD	  ?= $(shell git branch | grep '*' | awk '{print $$2}')
DEPLOY_REGION     ?= ap-northeast-1
MEMORY_SIZE 	  ?= 128
TEST_ENV          ?= ${ENV}
STORAGE           ?= file
CLICK_OPTION	  ?= registro:rapido
INPUT_FILE        ?= data-stage.xlsx

BUILD_NUMBER_DEPLOY = $(shell echo `printf %05d ${BUILD_NUMBER}`)
TAG_DEPLOY		    = ${BUILD_TIMESTAMP}.${BUILD_NUMBER_DEPLOY}
IMAGE_DEPLOY	    = ${PROJECT_NAME}:${TAG_DEPLOY}
DEPLOY_REGISTRY     = ${ACCOUNT_ID}.dkr.ecr.${DEPLOY_REGION}.amazonaws.com
ECS_CLUSTER		    = ${OWNER}-${ENV}
MAX_IMAGES_ALLOWED  = 5

## TARGET ##

login.aws.ecr: ## Login en ecr de aws: make login.aws.ecr
	aws ecr \
		get-login \
		--no-include-email\
		--region $(DEPLOY_REGION) | sh

create.repository.aws.ecr: ## Crear repositorio en ecr de aws: create.repository.aws.ecr
	$(eval EXITS_REPOSITORY := $(shell aws ecr \
		describe-repositories \
		--repository-name ${PROJECT_NAME} \
		--region $(DEPLOY_REGION) \
		| grep "repositoryName" \
		| sed 's/repositoryName//g'\
		| sed 's/://g'| sed 's/,//g'| sed 's/ //g'| sed 's/"//g'))
	@if [ "${EXITS_REPOSITORY}" != "${PROJECT_NAME}" ]; then \
		$(info "Create repository ${PROJECT_NAME} in the region ${DEPLOY_REGION}...") \
		aws ecr create-repository --repository-name ${PROJECT_NAME} --region $(DEPLOY_REGION); \
	fi

batch.delete.image.aws.ecr: ## Eliminar imagenes de docker del repositorio: make batch.delete.image.aws.ecr
	$(eval TOTAL_IMAGES := $(shell aws --region \
								${DEPLOY_REGION} \
								ecr list-images \
								--repository-name ${PROJECT_NAME} \
								| grep imageTag \
								| cut -d'"' -f4 \
								| sort -rn | wc -l))

	$(info "Total Imagen: $(TOTAL_IMAGES)")
	if [ ${TOTAL_IMAGES} -gt ${MAX_IMAGES_ALLOWED} ]; then \
		$(eval FILE_IMAGES:= $(shell echo '${PWD}/file_images.${BUILD_NUMBER_DEPLOY}')) \
		$(eval TOTAL_LINE:= $(shell echo '${TOTAL_IMAGES} - ${MAX_IMAGES_ALLOWED}' | bc)) \
		aws --region \
			${DEPLOY_REGION} \
			ecr list-images \
			--repository-name ${PROJECT_NAME} \
			| grep imageTag \
			| cut -d'"' -f4 \
			| sort -rn > ${FILE_IMAGES};\
		\
		for line in `cat ${FILE_IMAGES} | tail -n ${TOTAL_LINE}`; do \
			aws ecr batch-delete-image --repository-name ${PROJECT_NAME} --image-ids imageTag=$${line} --region ${DEPLOY_REGION}; \
			echo "Deleting image: $${line}"; \
		done; \
	fi
	
	@if [ -f ${FILE_IMAGES} ]; then \
		rm -rf ${FILE_IMAGES}; \
	fi

build.latest: ## Construir imagen para deploy: make build.latest
	docker build \
		-f docker/latest/Dockerfile \
		--no-cache \
		--build-arg IMAGE=$(IMAGE_DEV) \
		-t $(DEPLOY_REGISTRY)/$(IMAGE_DEPLOY) .

push.aws.ecr: ## Publicar imagen en ecr de aws: make push.aws.ecr
	docker push \
		$(DEPLOY_REGISTRY)/$(IMAGE_DEPLOY)

stack.deploy: ## Despliega el stack con cloudformation: make stack.deploy
	$(info "Deploy stack in cloudformation...")
	aws cloudformation deploy \
	--template-file ./cloudformation/sam.yml \
	--stack-name $(PROJECT_NAME) \
	--parameter-overrides \
		Owner=$(OWNER) \
		ServiceName=$(SERVICE_NAME) \
		Environment=$(ENV) \
		Image=$(DEPLOY_REGISTRY)/$(IMAGE_DEPLOY) \
		MemorySize=$(MEMORY_SIZE) \
	--capabilities CAPABILITY_NAMED_IAM \
	--region $(DEPLOY_REGION)

stack.delete: ## Elimina el stack con cloudformation: make stack.delete
	$(info "Deleting stack...")
	@aws cloudformation delete-stack \
		--stack-name $(PROJECT_NAME) \
		--region $(DEPLOY_REGION)

run.task: ## Ejecuta el task: make run.task
	aws ecs run-task --cluster ${ECS_CLUSTER} \
		--task-definition ${OWNER}-${ENV}-task-${SERVICE_NAME} \
		--overrides '{"containerOverrides":[{"command":["cli","${CLICK_OPTION}", "--env", "${TEST_ENV}", "--storage", "${STORAGE}", "--input_file", "${INPUT_FILE}"],"name":"${OWNER}-${ENV}-task-${SERVICE_NAME}"}]}' \
		--region $(DEPLOY_REGION)
