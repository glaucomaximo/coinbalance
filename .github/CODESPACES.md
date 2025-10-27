# GitHub Codespaces Configuration

## Development Environment

### Container Configuration
- **Base Image**: `mcr.microsoft.com/devcontainers/python:3.11`
- **Features**: Git, Docker, Node.js
- **Extensions**: Python, Docker, GitLens

### Environment Setup
- **Python**: 3.11+
- **Node.js**: 18+
- **Docker**: Latest
- **Git**: Latest

## Pre-installed Tools

### Development Tools
- **Python**: Python 3.11+
- **pip**: Latest
- **poetry**: Latest
- **black**: Code formatter
- **flake8**: Linter
- **pytest**: Testing framework

### System Tools
- **git**: Version control
- **curl**: HTTP client
- **wget**: Download tool
- **jq**: JSON processor
- **yq**: YAML processor

### Database Tools
- **sqlite3**: SQLite client
- **postgresql-client**: PostgreSQL client
- **mysql-client**: MySQL client

## VS Code Extensions

### Python Development
- **Python**: Official Python extension
- **Pylance**: Python language server
- **Python Debugger**: Debugging support
- **Python Test Explorer**: Test discovery

### Code Quality
- **Black Formatter**: Code formatting
- **Flake8**: Linting
- **isort**: Import sorting
- **Bandit**: Security linting

### Git Integration
- **GitLens**: Git supercharged
- **Git Graph**: Visualize git history
- **GitHub Pull Requests**: PR management
- **GitHub Issues**: Issue management

### Docker Support
- **Docker**: Docker support
- **Docker Compose**: Compose support
- **Remote Containers**: Container development

### Markdown Support
- **Markdown All in One**: Markdown support
- **Markdown Preview**: Preview support
- **Markdown Lint**: Linting

## Environment Variables

### Development
- `PYTHONPATH`: Python path
- `PYTHON_ENV`: Environment
- `DEBUG`: Debug mode
- `LOG_LEVEL`: Log level

### Database
- `DATABASE_URL`: Database connection
- `REDIS_URL`: Redis connection
- `CACHE_URL`: Cache connection

### Security
- `JWT_SECRET_KEY`: JWT secret
- `COINBALANCE_MASTER_KEY`: Master key
- `ENCRYPTION_KEY`: Encryption key

## Port Forwarding

### Application Ports
- **8001**: Main application
- **8000**: Development server
- **3000**: Frontend development
- **5432**: PostgreSQL
- **6379**: Redis

### Debug Ports
- **5678**: Python debugger
- **9229**: Node.js debugger
- **8080**: Debug server

## Customization

### Shell Configuration
- **Bash**: Custom bashrc
- **Zsh**: Custom zshrc
- **Fish**: Custom config

### Editor Configuration
- **VS Code**: Custom settings
- **Vim**: Custom vimrc
- **Emacs**: Custom config

### Git Configuration
- **User**: Git user
- **Email**: Git email
- **Aliases**: Git aliases
- **Hooks**: Git hooks

## Quick Start

### 1. Open Codespace
```bash
# Click "Code" -> "Codespaces" -> "Create codespace"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Setup Environment
```bash
cp env.example .env
# Edit .env with your settings
```

### 4. Run Application
```bash
python main.py --port 8001 --reload
```

### 5. Access Application
- **Main App**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs
- **Health Check**: http://localhost:8001/health

## Development Workflow

### 1. Create Branch
```bash
git checkout -b feature/new-feature
```

### 2. Make Changes
```bash
# Edit code
# Run tests
pytest
# Format code
black src/
# Lint code
flake8 src/
```

### 3. Commit Changes
```bash
git add .
git commit -m "feat: add new feature"
```

### 4. Push Changes
```bash
git push origin feature/new-feature
```

### 5. Create PR
```bash
# Create PR on GitHub
# Request reviews
# Address feedback
```

## Testing

### Unit Tests
```bash
pytest tests/unit/ -v
```

### Integration Tests
```bash
pytest tests/integration/ -v
```

### E2E Tests
```bash
pytest tests/e2e/ -v
```

### Performance Tests
```bash
pytest tests/performance/ -v --benchmark-only
```

## Debugging

### Python Debugging
```bash
# Set breakpoints in VS Code
# Use debugger
# Step through code
```

### API Debugging
```bash
# Use Postman/Insomnia
# Check logs
# Monitor requests
```

### Database Debugging
```bash
# Connect to database
# Check queries
# Monitor performance
```

## Performance

### Optimization
- **Caching**: Enable caching
- **Compression**: Enable compression
- **CDN**: Use CDN
- **Database**: Optimize queries

### Monitoring
- **Metrics**: Monitor metrics
- **Logs**: Check logs
- **Performance**: Monitor performance
- **Errors**: Track errors

## Security

### Best Practices
- **Secrets**: Use secrets
- **Permissions**: Minimal permissions
- **Validation**: Validate inputs
- **Sanitization**: Sanitize outputs

### Tools
- **Bandit**: Security linting
- **Safety**: Dependency scanning
- **Semgrep**: Security scanning
- **OWASP ZAP**: Security testing

## Troubleshooting

### Common Issues
- **Port Conflicts**: Change ports
- **Permission Errors**: Check permissions
- **Dependency Issues**: Update dependencies
- **Environment Issues**: Check environment

### Debugging
- **Logs**: Check logs
- **Environment**: Verify environment
- **Dependencies**: Check dependencies
- **Configuration**: Verify config

### Support
- **Documentation**: Check docs
- **Community**: Ask community
- **Issues**: Create issue
- **Support**: Contact support

## Best Practices

### Development
- **Code Quality**: Maintain quality
- **Testing**: Write tests
- **Documentation**: Document code
- **Security**: Follow security practices

### Collaboration
- **Communication**: Clear communication
- **Code Review**: Thorough reviews
- **Documentation**: Keep docs updated
- **Feedback**: Provide feedback

### Maintenance
- **Updates**: Regular updates
- **Monitoring**: Continuous monitoring
- **Performance**: Optimize performance
- **Security**: Maintain security

## Future Improvements

### Planned Features
- **AI Integration**: AI-powered development
- **Advanced Debugging**: Advanced debugging tools
- **Performance Optimization**: Performance improvements
- **Security Enhancements**: Security improvements

### Research
- **Development Tools**: Tool research
- **Workflow Optimization**: Workflow research
- **Security Research**: Security research
- **Best Practices**: Best practices development