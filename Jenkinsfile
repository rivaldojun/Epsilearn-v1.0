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
        sh '''python3 -m pytest -v --tb=no


python3 -m pytest --junitxml=results.xml
python3 -m pytest --cov=src
python3 -m pytest --cov=src --cov-report=html
ls -la'''
      }
    }

  }
}