# Technical Prerequisites & Setup Guide

## 🛠️ Development Environment Requirements

### System Requirements

#### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.14+, or Ubuntu 18.04+
- **RAM**: 8GB (16GB recommended for development)
- **Storage**: 50GB free space (for models, databases, and containers)
- **CPU**: 4-core processor (8-core recommended)
- **Network**: Reliable internet connection for model downloads

#### Recommended Development Setup
- **RAM**: 16-32GB for optimal performance
- **Storage**: SSD with 100GB+ free space
- **CPU**: 8+ core processor for faster model processing
- **GPU**: Optional - NVIDIA GPU for potential ML acceleration

### Core Technologies

#### Python Environment
```bash
# Python version
Python 3.8+ (3.9 or 3.10 recommended)

# Package manager
pip 21.0+ or conda 4.10+

# Virtual environment
venv, conda, or pipenv
```

#### Database Systems
```bash
# PostgreSQL (recommended for production)
PostgreSQL 12+ with extensions:
- pg_trgm (for text search)
- uuid-ossp (for UUID generation)
- pgcrypto (for encryption)

# Redis (for caching and task queues)
Redis 6.0+ or 7.0+

# SQLite (for development/testing)
SQLite 3.31+ (usually included with Python)
```

#### Containerization
```bash
# Docker
Docker Engine 20.10+
Docker Compose 1.29+

# Container Registry (optional)
Docker Hub, AWS ECR, or Google Container Registry
```

#### Web Technologies
```bash
# Node.js (for potential frontend enhancements)
Node.js 16+ with npm 8+

# Nginx (for production load balancing)
Nginx 1.18+
```

## 📦 Python Dependencies

### Core ABSA Dependencies
```txt
# requirements.txt - Core NLP and ABSA
pandas>=2.1.0
numpy>=1.24.0
nltk>=3.8.1
stanza>=1.7.0
scikit-learn>=1.3.0
```

### Web Framework Dependencies
```txt
# Web frameworks and APIs
streamlit>=1.28.0
fastapi>=0.104.0
uvicorn>=0.24.0
jinja2>=3.1.2
python-multipart>=0.0.6
```

### Database Dependencies
```txt
# Database connectivity and ORM
psycopg2-binary>=2.9.7
sqlalchemy>=2.0.23
alembic>=1.12.0
redis>=5.0.0
```

### Visualization Dependencies
```txt
# Data visualization and dashboards
plotly>=5.17.0
dash>=2.14.0
matplotlib>=3.7.0
seaborn>=0.12.0
kaleido>=0.2.1  # For static image export
```

### Testing Dependencies
```txt
# Testing and quality assurance
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
pytest-mock>=3.11.0
httpx>=0.25.0  # For FastAPI testing
```

### Development Dependencies
```txt
# Development and code quality
black>=23.0.0
flake8>=6.0.0
isort>=5.12.0
mypy>=1.5.0
pre-commit>=3.4.0
```

### Production Dependencies
```txt
# Production deployment and monitoring
gunicorn>=21.2.0
celery>=5.3.0
prometheus-client>=0.17.0
sentry-sdk>=1.32.0
```

## 🚀 Installation Guide

### Step 1: System Setup

#### Windows Setup
```powershell
# Install Python from python.org or Microsoft Store
# Install Git from git-scm.com
# Install Docker Desktop from docker.com

# Install PostgreSQL
winget install PostgreSQL.PostgreSQL

# Install Redis (using Chocolatey)
choco install redis-64

# Verify installations
python --version
git --version
docker --version
psql --version
redis-cli --version
```

#### macOS Setup
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required packages
brew install python@3.9
brew install git
brew install postgresql@14
brew install redis
brew install --cask docker

# Start services
brew services start postgresql@14
brew services start redis

# Verify installations
python3 --version
git --version
docker --version
psql --version
redis-cli --version
```

#### Ubuntu/Debian Setup
```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3.9 python3.9-pip python3.9-venv

# Install Git
sudo apt install git

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Install Redis
sudo apt install redis-server

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose

# Verify installations
python3 --version
git --version
docker --version
psql --version
redis-cli --version
```

### Step 2: Project Setup

#### Clone and Setup Project
```bash
# Clone the repository
git clone <your-repo-url>
cd Aspect-based-Sentimental-Analysis

# Create virtual environment
python -m venv absa_env

# Activate virtual environment
# Windows:
absa_env\Scripts\activate
# macOS/Linux:
source absa_env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install core dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

#### Environment Configuration
```bash
# Create environment configuration file
cp .env.example .env

# Edit .env file with your settings
# Database URLs, API keys, etc.
```

### Step 3: Database Setup

#### PostgreSQL Setup
```bash
# Start PostgreSQL service (if not already running)
# Windows: Start from Services or pgAdmin
# macOS: brew services start postgresql
# Linux: sudo systemctl start postgresql

# Create database and user
sudo -u postgres psql

# In PostgreSQL shell:
CREATE DATABASE absa_db;
CREATE USER absa_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE absa_db TO absa_user;
\q
```

#### Redis Setup
```bash
# Start Redis service
# Windows: Start from Services or redis-server.exe
# macOS: brew services start redis
# Linux: sudo systemctl start redis

# Test Redis connection
redis-cli ping
# Should return: PONG
```

### Step 4: Development Tools Setup

#### IDE Configuration
```bash
# VS Code extensions (recommended)
code --install-extension ms-python.python
code --install-extension ms-python.flake8
code --install-extension ms-python.black-formatter
code --install-extension bradlc.vscode-tailwindcss

# PyCharm plugins (if using PyCharm)
# - Python
# - Database Tools and SQL
- Docker
# - Requirements
```

#### Git Hooks Setup
```bash
# Install pre-commit hooks
pre-commit install

# Run pre-commit on all files (optional)
pre-commit run --all-files
```

## 🔧 Configuration Files

### Environment Variables (.env)
```bash
# Database Configuration
DATABASE_URL=postgresql://absa_user:your_password@localhost:5432/absa_db
REDIS_URL=redis://localhost:6379

# API Configuration
SECRET_KEY=your-secret-key-here
API_VERSION=v1
DEBUG=True

# NLP Model Configuration
STANZA_DOWNLOAD_METHOD=default
NLTK_DATA_PATH=./nltk_data

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=./logs/absa.log

# External Services (optional)
SENTRY_DSN=your-sentry-dsn
PROMETHEUS_PORT=8090
```

### Docker Environment (.env.docker)
```bash
# Docker-specific configuration
POSTGRES_DB=absa_db
POSTGRES_USER=absa_user
POSTGRES_PASSWORD=docker_password

# Container networking
API_HOST=0.0.0.0
API_PORT=8000
STREAMLIT_PORT=8501

# Resource limits
MEMORY_LIMIT=2g
CPU_LIMIT=1.0
```

## 🧪 Verification & Testing

### Verify Core Installation
```bash
# Test Python environment
python -c "import sys; print(f'Python {sys.version}')"

# Test core dependencies
python -c "import pandas, numpy, nltk, stanza; print('Core dependencies OK')"

# Test web frameworks
python -c "import streamlit, fastapi; print('Web frameworks OK')"

# Test database connectivity
python -c "import psycopg2; print('PostgreSQL driver OK')"
python -c "import redis; print('Redis driver OK')"
```

### Run Initial Tests
```bash
# Run existing project tests
python -m pytest tests/ -v

# Test ABSA core functionality
python absa_main.py --test

# Test web interface (basic)
streamlit run streamlit_app/app.py --server.port 8502
```

### Performance Baseline
```bash
# Run performance tests
python -m pytest tests/performance/ -v

# Memory usage test
python -c "
import psutil
import os
process = psutil.Process(os.getpid())
print(f'Memory usage: {process.memory_info().rss / 1024 / 1024:.2f} MB')
"
```

## 🐳 Docker Setup (Optional)

### Quick Docker Test
```bash
# Build and run with Docker Compose
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🚨 Troubleshooting

### Common Issues

#### NLP Model Download Issues
```bash
# Manual NLTK data download
python -c "
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('vader_lexicon')
"

# Manual Stanza model download
python -c "
import stanza
stanza.download('en')
"
```

#### Database Connection Issues
```bash
# Check PostgreSQL status
# Windows: Check Services
# macOS: brew services list | grep postgresql
# Linux: sudo systemctl status postgresql

# Reset PostgreSQL password
sudo -u postgres psql
\password postgres
```

#### Port Conflicts
```bash
# Check port usage
# Windows: netstat -an | findstr :8000
# macOS/Linux: lsof -i :8000

# Kill process on port
# Windows: taskkill /PID <pid> /F
# macOS/Linux: kill -9 <pid>
```

### Performance Issues
- **Slow Model Loading**: Increase available RAM or use SSD storage
- **High Memory Usage**: Monitor with `htop` or Task Manager, consider memory limits
- **Slow Database Queries**: Check database indexing and query optimization

### Development Issues
- **Import Errors**: Verify PYTHONPATH and virtual environment activation
- **Package Conflicts**: Use fresh virtual environment or conda environment
- **Version Mismatches**: Check requirements.txt for compatible versions

## 📊 Resource Monitoring

### System Monitoring Commands
```bash
# CPU and Memory usage
htop  # Linux/macOS
# Windows: Task Manager

# Disk usage
df -h  # Linux/macOS
# Windows: dir

# Network monitoring
netstat -an | grep :8000

# Docker resource usage
docker stats
```

### Application Monitoring
```bash
# Python memory profiling
pip install memory-profiler
python -m memory_profiler your_script.py

# Database monitoring
psql -c "SELECT * FROM pg_stat_activity;"

# Redis monitoring
redis-cli monitor
```

This comprehensive setup guide ensures your development environment is properly configured for all enhancement phases of the ABSA project.
