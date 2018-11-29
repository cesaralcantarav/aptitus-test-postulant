def call(String buildResult) {
  if ( buildResult == "DEPLOY" ) {
    sh 'git log HEAD\\^..HEAD --pretty="%h %an - %s" > GIT_CHANGES'
    def lastChanges = readFile('GIT_CHANGES')
    slackSend (
      channel: "${SLACK_CHANNEL}",
      color: "#FFFF00", 
      message: "Started `${env.JOB_NAME} Build#${env.BUILD_NUMBER}`\n\n_The changes:_\n${lastChanges} <${env.RUN_DISPLAY_URL}|Open in Jenkins>"
    )
  }
  if ( buildResult == "SUCCESS" ) {
    slackSend (
      channel: "${SLACK_CHANNEL}",
      color: "good",
      message: ":+1::grinning: SUCCESSFUL: Job : `${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.RUN_DISPLAY_URL}|Open in Jenkins>"
    )
  }
  else if( buildResult == "FAILURE" ) { 
    slackSend (
      channel: "${SLACK_CHANNEL}",
      color: 'warning', message: ":-1::face_with_head_bandage: FAILED: Job `${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.RUN_DISPLAY_URL}|Open in Jenkins>"
    )
  }
  else if( buildResult == "UNSTABLE" ) { 
    slackSend (
      channel: "${SLACK_CHANNEL}",
      color: 'warning', 
      message: ":-1::face_with_head_bandage: FAILED: Job `${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.RUN_DISPLAY_URL}|Open in Jenkins>"
    )
  }
}

def showEnviroment(def config) {
    echo "Enviroment:"
    for(e in config){
        echo "--> ${e}"
    }
}

def login_aws_ecr(def config) {
  withEnv(config) {
    sh 'make login.aws.ecr'
  }
}

def create_repository(def config) {
  withEnv(config) {
    sh 'make create.repository.aws.ecr'
  }
}


def batch_delete_image_aws_ecr(def config) {
  withEnv(config) {
    sh 'make batch.delete.image.aws.ecr'
  }
}

def build_latest(def config) {
  withEnv(config) {
    sh 'make build'
    sh 'make venv.create'
    sh 'make venv.lib.install'
    sh 'make build.latest'
  }
}

def push_aws_ecr(def config) {
  withEnv(config) {
    sh 'make push.aws.ecr'
  }
}

def stack_deploy(def config) {
  withEnv(config) {
    sh 'make stack.deploy'
  }
}

def stack_delete(def config) {
  withEnv(config) {
    sh 'make stack.delete'
  }
}

def run_task(def config) {
  withEnv(config) {
    sh 'make run.task'
  }
}

def getRegions(def enviroment) {
  def REGIONS = [
      dev:'eu-west-1',
      pre:'us-west-2',
      prod:'us-east-1'
  ]
  return REGIONS[enviroment]
}

def configs(def enviroment, def runtest, def input_file, def sub_env) {
  region = getRegions(enviroment)
  def config = [
    "ENV=${enviroment}",
    "DEPLOY_REGION=${region}",
    "INFRA_BUCKET=infraestructura.${enviroment}",
    "SLACK_CHANNEL=apt-testing",
    "ACCOUNT_ID=929226109038",
    "MEMORY_SIZE=128",
    "TEST_ENV=${enviroment}.${sub_env}",
    "STORAGE=s3",
    "INPUT_FILE=${input_file}",
    "CLICK_OPTION=${runtest}"
    "SUB_ENV=${sub_env}"
  ]

  return config
}

return this
