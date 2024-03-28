pipeline {
  agent any
  stages {
    stage('Git checkout') {
      steps {
        git(credentialsId: '1234', url: 'https://github.com/rivaldojun/Epsilearn-v1.0.git', branch: 'main')
      }
    }

    stage('error') {
      parallel {
        stage('error') {
          steps {
            sh 'ls -la'
          }
        }

        stage('Running test') {
          steps {
            sh 'pip install -r requirementss.txt'
            sh 'gunicorn -w 3 app:app'
            sh './ngrok http 8000'
          }
        }

      }
    }

  }
}