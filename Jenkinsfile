pipeline {
    agent any

    environment {
        // Name of the folder in Jenkins; change this to your specific folder name (in lowercase)
        JENKINS_FOLDER_NAME = '.'

        // Name of the Jenkins job; update this to reflect your own job name
        JENKINS_JOB_NAME = 'recommendation-engine'

        // GitHub repository name; update this with your actual repository name
        GITHUB_REPO = '/RuleBased-Prototype/'

        // Service name to be used for image creation from the Docker Compose file.
        SERVICE_NAME = 'recommendation_engine'

        // Docker image tag; you can specify a custom tag or use this format for automatic versioning (format must be :TAG)
        IMAGE_TAG = ":0.1.${env.BUILD_NUMBER}"

        MAJOR_RELEASE = '0.1'
        HOST_URL = "http://144.76.87.115"
        HARBOR_REG = 'harbor-meliora.risa.eu'
        HARBOR_REG_CREDS = 'harbor-jenkins-creds'
    }

    stages {
        stage('Build Docker Container') {
            steps {
                script {
                    echo '***** Building Docker Containers *****'
                    sh 'docker compose up -d --build'
                }
            }
        }
    }
}