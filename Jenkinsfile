def fnSteps = evaluate readTrusted("deploy/steps.groovy")

pipeline {
    agent any
    stages {
        stage('Set Config') {
            steps { 
                script { 
                    config = fnSteps.configs("${JENKINS_ENV}", params.RUNTEST, params.INPUT_FILE, params.SUB_ENV)
                    withEnv(config) { fnSteps.call("DEPLOY") }
                }
            }
        }
        stage('Login ecr aws') {
            steps { script { fnSteps.login_aws_ecr(config) }}
        }
        stage('Create repository ecr') {
            steps { script { fnSteps.create_repository(config) }}
        }
        stage('Deploy') {
            when { expression { return params.DEPLOY }}
            steps { 
                script { 
                    fnSteps.build_latest(config)
                    fnSteps.push_aws_ecr(config)
                    fnSteps.stack_deploy(config)
                } 
            }
        }
        stage('Delete images of ecr') {
            steps { script { fnSteps.batch_delete_image_aws_ecr(config) }}
        }
        stage('Run test') {
            steps { script { fnSteps.run_task(config) }}
        }
    }
    post { 
        always { 
            echo 'Execution finished.'
            cleanWs()
        }
        success {
            echo 'Success!! :)'
            script { 
                withEnv(config) {
                    fnSteps.call("SUCCESS")
                }
            }
        }
        failure {
            echo 'Failure!! :)'
            script { 
                withEnv(config) {
                    fnSteps.call("FAILURE")
                }
            }
        }
    }
    parameters {
        booleanParam(
            name: 'DEPLOY',
            defaultValue: true, 
            description: 'Se realiza deploy del tarea de test')
        choice(
            name: 'RUNTEST',
            choices:['registro:rapido'],
            description: 'Ejecuta el test selecionado')
        string(
            name: 'INPUT_FILE',
            defaultValue: 'data-stage.xlsx', 
            description: 'Archivo de data entrada del test')
        choice(
            name: 'SUB_ENV',
            choices:['4a'],
            description: 'Sub-Enviroment')
    }
}
