pipeline {
    agent any
    stages {
        stage('Build') {
            // Build image, output is stereum/installer-build
            steps {   
                checkout scm                                                         
                sh 'sed s/%%STEREUM_VERSION_TAG%%/${RELEASE}/ -i frontend/public/index.html'                
                sh 'docker build -f Dockerfile -t stereum/control-center-web:${RELEASE} .'                
            }
        }        
        stage('Push') {            
            steps {                
                sh 'docker push stereum/control-center-web:${RELEASE}'
            }
        }
        stage('Cleanup') {
            // cleanup local images
            steps {                
                sh 'docker rmi -f stereum/control-center-web:${RELEASE}'
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
