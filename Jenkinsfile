pipeline {
  agent any
  stages {
    stage('Git checkout') {
      steps {
        git(credentialsId: '1234', url: 'https://github.com/rivaldojun/Epsilearn-v1.0.git', branch: 'main')
      }
    }

    stage('Test') {
      steps {
        sh 'python3 -m pytest --junit-xml test-reports/results.xml'
      }
    }

    stage('Build') {
      steps {
        sh 'docker build Dockerfile .'
      }
    }

  }
}