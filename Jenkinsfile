pipeline {
  agent any
  stages {
    stage('Git checkout') {
      steps {
        git(credentialsId: '1234', url: 'https://github.com/rivaldojun/Epsilearn-v1.0.git', branch: 'main')
      }
    }

    stage('') {
      steps {
        sh 'ls -la'
      }
    }

  }
}