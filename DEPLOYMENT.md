# 部署指南

本文档提供了肺结核耐药性预测系统的详细部署指南。

## 目录

- [本地部署](#本地部署)
- [Docker部署](#docker部署)
- [生产环境部署](#生产环境部署)
- [云平台部署](#云平台部署)
- [故障排除](#故障排除)

## 本地部署

### 前提条件

- Python 3.8 或更高版本
- pip 包管理器
- Git（可选）

### 步骤

1. **克隆或下载项目**
   ```bash
   git clone <repository-url>
   cd tuberculosis-prediction
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **启动应用**
   ```bash
   python app.py
   ```

5. **访问应用**
   打开浏览器访问 `http://localhost:5000`

## Docker部署

### 使用Docker Compose（推荐）

1. **确保已安装Docker和Docker Compose**

2. **启动服务**
   ```bash
   # 仅启动应用
   docker-compose up -d
   
   # 启动应用和Nginx（生产环境）
   docker-compose --profile production up -d
   ```

3. **查看日志**
   ```bash
   docker-compose logs -f
   ```

4. **停止服务**
   ```bash
   docker-compose down
   ```

### 使用Docker（手动）

1. **构建镜像**
   ```bash
   docker build -t tuberculosis-prediction .
   ```

2. **运行容器**
   ```bash
   docker run -d -p 5000:5000 --name tb-app tuberculosis-prediction
   ```

## 生产环境部署

### 使用Nginx + Gunicorn

1. **安装Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **创建Gunicorn配置文件**
   ```python
   # gunicorn.conf.py
   bind = "127.0.0.1:5000"
   workers = 4
   worker_class = "sync"
   worker_connections = 1000
   timeout = 30
   keepalive = 2
   max_requests = 1000
   max_requests_jitter = 100
   preload_app = True
   ```

3. **启动Gunicorn**
   ```bash
   gunicorn -c gunicorn.conf.py app:app
   ```

4. **配置Nginx**
   使用提供的 `nginx.conf` 文件配置Nginx反向代理

### 使用Systemd服务

1. **创建服务文件**
   ```ini
   # /etc/systemd/system/tuberculosis-prediction.service
   [Unit]
   Description=Tuberculosis Prediction Web Application
   After=network.target
   
   [Service]
   Type=exec
   User=www-data
   Group=www-data
   WorkingDirectory=/path/to/tuberculosis-prediction
   Environment=PATH=/path/to/tuberculosis-prediction/venv/bin
   ExecStart=/path/to/tuberculosis-prediction/venv/bin/gunicorn -c gunicorn.conf.py app:app
   ExecReload=/bin/kill -s HUP $MAINPID
   Restart=always
   RestartSec=3
   
   [Install]
   WantedBy=multi-user.target
   ```

2. **启用并启动服务**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable tuberculosis-prediction
   sudo systemctl start tuberculosis-prediction
   ```

## 云平台部署

### Heroku

1. **创建Procfile**
   ```
   web: gunicorn app:app
   ```

2. **部署到Heroku**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### AWS EC2

1. **启动EC2实例**（推荐使用Ubuntu 20.04 LTS）

2. **安装Docker**
   ```bash
   sudo apt update
   sudo apt install docker.io docker-compose
   sudo usermod -aG docker $USER
   ```

3. **部署应用**
   ```bash
   git clone <repository-url>
   cd tuberculosis-prediction
   docker-compose --profile production up -d
   ```

4. **配置安全组**
   - 开放端口80（HTTP）
   - 开放端口443（HTTPS，如果使用SSL）
   - 限制SSH访问（端口22）

### Google Cloud Platform

1. **使用Cloud Run**
   ```bash
   gcloud run deploy tuberculosis-prediction \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

## 环境变量配置

创建 `.env` 文件配置环境变量：

```env
# Flask配置
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here

# 服务器配置
HOST=0.0.0.0
PORT=5000

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=app.log

# 安全配置
CSRF_ENABLED=True
WTF_CSRF_TIME_LIMIT=3600
```

## 性能优化

### 缓存配置

1. **Redis缓存**（可选）
   ```bash
   pip install redis flask-caching
   ```

2. **静态文件缓存**
   配置Nginx缓存静态资源

### 监控和日志

1. **应用监控**
   - 使用Prometheus + Grafana
   - 集成健康检查端点

2. **日志管理**
   - 配置日志轮转
   - 使用ELK Stack（可选）

## 安全配置

### SSL/TLS配置

1. **获取SSL证书**
   ```bash
   # 使用Let's Encrypt
   sudo certbot --nginx -d your-domain.com
   ```

2. **配置HTTPS重定向**
   更新Nginx配置以强制HTTPS

### 防火墙配置

```bash
# Ubuntu UFW
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 查找占用端口的进程
   lsof -i :5000
   # 或者
   netstat -tulpn | grep 5000
   ```

2. **依赖安装失败**
   ```bash
   # 升级pip
   pip install --upgrade pip
   # 清理缓存
   pip cache purge
   ```

3. **模型文件缺失**
   确保所有 `.pkl` 文件都在项目目录中

4. **内存不足**
   - 增加服务器内存
   - 减少Gunicorn worker数量
   - 使用模型量化技术

### 日志查看

```bash
# Docker日志
docker-compose logs -f tuberculosis-prediction

# Systemd日志
sudo journalctl -u tuberculosis-prediction -f

# 应用日志
tail -f app.log
```

### 性能调优

1. **数据库优化**（如果使用数据库）
   - 添加索引
   - 优化查询
   - 使用连接池

2. **应用优化**
   - 启用Gzip压缩
   - 优化静态资源
   - 使用CDN

## 备份和恢复

### 备份策略

1. **代码备份**
   使用Git版本控制

2. **模型文件备份**
   ```bash
   # 创建备份
   tar -czf models-backup-$(date +%Y%m%d).tar.gz *.pkl
   ```

3. **配置文件备份**
   定期备份配置文件和环境变量

### 恢复流程

1. **从备份恢复**
   ```bash
   # 恢复模型文件
   tar -xzf models-backup-YYYYMMDD.tar.gz
   ```

2. **重新部署**
   按照部署步骤重新部署应用

## 联系支持

如果在部署过程中遇到问题，请：

1. 查看本文档的故障排除部分
2. 检查GitHub Issues
3. 创建新的Issue并提供详细的错误信息

---

**注意**: 在生产环境中部署时，请确保遵循安全最佳实践，包括定期更新依赖、使用强密码、配置防火墙等。