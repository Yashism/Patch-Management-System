pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Lint') {
            steps {
                sh 'pylint patch_manager.py'
                sh 'shellcheck run_patch_manager.sh'
            }
        }

        stage('Test') {
            steps {
                sh 'python3 -m pytest tests/'
            }
        }

        stage('Deploy to Staging') {
            steps {
                sh 'ansible-playbook -i inventory/staging deploy_patch_manager.yml'
            }
        }

        stage('Validate Staging') {
            steps {
                sh 'ansible-playbook -i inventory/staging validate_patch_manager.yml'
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                input message: 'Deploy to production?', ok: 'Yes'
                sh 'ansible-playbook -i inventory/production deploy_patch_manager.yml'
            }
        }
    }

    post {
        always {
            junit 'test-reports/**/*.xml'
        }
        success {
            slackSend channel: '#devops', color: 'good', message: 'Patch Manager deployed successfully!'
        }
        failure {
            slackSend channel: '#devops', color: 'danger', message: 'Patch Manager deployment failed!'
        }
    }
}
