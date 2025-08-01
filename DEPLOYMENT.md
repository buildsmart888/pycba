# 🚀 PyCBA Deployment Guide

## Quick Start (Windows)

### Option 1: One-Click Deployment (Recommended)
```batch
# Just double-click this file!
deploy.bat
```

### Option 2: Manual Docker Deployment
```batch
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop application
docker-compose down
```

### Option 3: Local Development
```batch
# Activate virtual environment
.venv\Scripts\activate

# Run Streamlit app
streamlit run advanced_app.py
```

## 🌐 Cloud Deployment Options

### Streamlit Cloud (Free)
1. Push code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Deploy automatically!

### Heroku
```bash
# Install Heroku CLI
# Create Procfile:
web: streamlit run advanced_app.py --server.port=$PORT --server.address=0.0.0.0

# Deploy
heroku create your-app-name
git push heroku main
```

### Railway
1. Connect GitHub repo to [Railway](https://railway.app)
2. Add environment variables
3. Deploy automatically!

### DigitalOcean App Platform
1. Create app from GitHub repo
2. Set Python environment
3. Configure run command: `streamlit run advanced_app.py`

## 🐳 Docker Production Deployment

### Build Production Image
```bash
docker build -t pycba-app:latest .
```

### Run in Production
```bash
docker run -d \
  --name pycba-production \
  -p 8501:8501 \
  --restart unless-stopped \
  pycba-app:latest
```

### Docker Swarm (Multiple Servers)
```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml pycba-stack
```

### Kubernetes
```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pycba-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: pycba-app
  template:
    metadata:
      labels:
        app: pycba-app
    spec:
      containers:
      - name: pycba-app
        image: pycba-app:latest
        ports:
        - containerPort: 8501
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi" 
            cpu: "1000m"
```

## 🔧 Configuration

### Environment Variables
- `PYTHONPATH`: Set to `/app/src` in production
- `STREAMLIT_SERVER_PORT`: Port for Streamlit (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Server address (default: 0.0.0.0)

### Performance Tuning
- **Memory**: Minimum 512MB RAM recommended
- **CPU**: Single core sufficient for small loads
- **Storage**: ~100MB for application

## 🔍 Monitoring & Health Checks

### Health Check Endpoint
```
GET http://your-app:8501/_stcore/health
```

### Docker Health Check
```bash
# Check container health
docker ps
docker logs pycba-app
```

### Application Metrics
- Response time monitoring
- Memory usage tracking
- Error rate monitoring

## 🔒 Security Considerations

### Production Checklist
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure firewall rules
- [ ] Set up authentication if needed
- [ ] Regular security updates
- [ ] Backup strategy
- [ ] Monitor logs for security events

### SSL/TLS Setup (nginx)
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📊 Scaling

### Horizontal Scaling
- Use load balancer (nginx, HAProxy)
- Deploy multiple instances
- Session state management

### Vertical Scaling
- Increase container resources
- Optimize Python code
- Use caching strategies

## 🐛 Troubleshooting

### Common Issues
1. **Port already in use**: Change port in config
2. **Memory errors**: Increase container memory limit
3. **Python path issues**: Verify PYTHONPATH setting
4. **Permission errors**: Check file permissions

### Debugging Commands
```bash
# View container logs
docker logs pycba-app

# Access container shell
docker exec -it pycba-app /bin/bash

# Check running processes
docker ps -a

# Monitor resources
docker stats pycba-app
```

## 📝 Maintenance

### Regular Tasks
- Update dependencies
- Monitor performance
- Backup data
- Review logs
- Security patches

### Updates
```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

---

## 🎯 Success Indicators

✅ **Application loads at http://localhost:8501**  
✅ **All diagrams render correctly**  
✅ **Calculations are accurate**  
✅ **No error messages in logs**  
✅ **Responsive UI on different screen sizes**

---

**Need help?** Check the [troubleshooting section](#troubleshooting) or create an issue on GitHub.
