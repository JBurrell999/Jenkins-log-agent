pipeline {
  agent any
  options { timestamps(); ansiColor('xterm') }
  environment {
    OLLAMA_BASE_URL = "${params.OLLAMA_BASE_URL ?: 'http://localhost:11434'}"
    OLLAMA_MODEL    = "${params.OLLAMA_MODEL    ?: 'gpt-oss:20b'}"
  }
  parameters {
    string(name: 'OLLAMA_BASE_URL', defaultValue: 'http://localhost:11434', description: 'Ollama server URL')
    string(name: 'OLLAMA_MODEL',    defaultValue: 'gpt-oss:20b',            description: 'Ollama model tag')
  }
  stages {
    stage('Checkout'){ steps{ checkout scm } }

    stage('Setup Python'){
      steps {
        sh '''
          python3 -m venv .venv
          . .venv/bin/activate
          pip install --upgrade pip
          pip install -r analyzer/requirements.txt
        '''
      }
    }

    stage('Build'){
      steps {
        sh '''
          echo "Compiling..."
          mkdir -p build
          echo ok > build/app.bin
        '''
      }
    }

    stage('Test (Intentional Failure)'){
      steps {
        sh '''
          echo "Running tests..."
          echo "Traceback (most recent call last):" 1>&2
          echo "ModuleNotFoundError: No module named 'pytest'" 1>&2
          exit 1
        '''
      }
    }
  }

  post {
    always {
      script {
        def logLines = currentBuild.rawBuild.getLog(100000)
        writeFile file: 'build_log.txt', text: logLines.join("\\n")
        archiveArtifacts artifacts: 'build_log.txt', onlyIfSuccessful: false
      }
    }
    failure {
      sh '''
        . .venv/bin/activate
        python scripts/analyze_logs.py \
          --log build_log.txt \
          --out analysis.md \
          --ollama-url "$OLLAMA_BASE_URL" \
          --model "$OLLAMA_MODEL" || true
      '''
      archiveArtifacts artifacts: 'analysis.md', onlyIfSuccessful: false
    }
  }
}
