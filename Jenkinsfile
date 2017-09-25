pipeline {
  agent any

  stages {
    stage('Build') {
      steps {
        sh 'virtualenv -p /usr/bin/python3 .'
	    sh 'source bin/activate && pip install -e .'
      }
    }
    stage('build-docker-images') {
      steps {
        sh 'source bin/activate && make analyzers'
      }
    }
    stage('Test') {
      steps {
        sh "source bin/activate && make check"
      }

    post {
        success {
          // publish html
          publishHTML target: [
              allowMissing: false,
              alwaysLinkToLastBuild: false,
              keepAll: true,
              reportDir: 'htmlcov',
              reportFiles: 'index.html',
              reportName: 'coverage report'
            ]
        }
      }
    }
  }
}
