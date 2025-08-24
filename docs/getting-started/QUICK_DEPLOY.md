# 🚀 Quick Deployment Guide / 快速部署指南

## 🎯 5-Minute Setup / 5分钟快速设置

### Prerequisites Check / 环境检查
```bash
# Check Python version / 检查Python版本
python3 --version  # Should be 3.8+

# Check GPU availability (optional) / 检查GPU可用性（可选）
nvidia-smi

# Check GNS3 server / 检查GNS3服务器
curl http://YOUR_GNS3_SERVER:3080/v2/version
```

### Step 1: Clone & Setup / 步骤1：克隆和设置
```bash
# Clone repository / 克隆仓库
git clone <your-repository-url>
cd GNS3/tools

# Create virtual environment / 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

# Install dependencies / 安装依赖
pip install -r requirements.txt
```

### Step 2: Environment Configuration / 步骤2：环境配置
```bash
# Copy environment template / 复制环境模板
cp .env.example .env

# Edit configuration / 编辑配置
nano .env
```

**Required Settings / 必需设置:**
```bash
# GNS3 Configuration / GNS3配置
GNS3_SERVER_URL=http://192.168.101.1:3080
TELNET_HOST=192.168.102.1

# LLM Configuration / LLM配置
DEEPSEEK_API_KEY=your_deepseek_api_key_here
# or / 或者
OLLAMA_BASE_URL=http://localhost:11434

# RAG Configuration / RAG配置
USE_RAG=true
```

### Step 3: Initialize RAG System / 步骤3：初始化RAG系统
```bash
# Quick setup (recommended) / 快速设置（推荐）
python setup_rag.py --all

# Or step by step / 或者分步执行
python setup_rag.py --install
python setup_rag.py --init
python setup_rag.py --enable
```

### Step 4: Add Knowledge Base / 步骤4：添加知识库
```bash
# Create knowledge base directory / 创建知识库目录
mkdir -p knowledge_base

# Add your network documentation / 添加网络文档
cp /path/to/your/network-docs/* knowledge_base/

# Supported formats / 支持的格式
# - PDF files (*.pdf)
# - Text files (*.txt)
# - Markdown files (*.md)
# - Word documents (*.docx)
```

### Step 5: Launch Application / 步骤5：启动应用
```bash
# Start the intelligent agent / 启动智能代理
python main.py
```

## 🔧 Configuration Options / 配置选项

### Basic Configuration / 基础配置
```ini
# .env file
GNS3_SERVER_URL=http://192.168.101.1:3080
TELNET_HOST=192.168.102.1
TELNET_PORT=23

# LLM Provider Selection / LLM提供商选择
DEFAULT_LLM=deepseek  # or 'ollama', 'openai'
DEEPSEEK_API_KEY=your_key
OLLAMA_BASE_URL=http://localhost:11434

# RAG Settings / RAG设置
USE_RAG=true
KNOWLEDGE_BASE_PATH=./knowledge_base
VECTOR_STORE_PATH=./vector_store
```

### Advanced Configuration / 高级配置
```ini
# rag_config.ini
[embeddings]
model_name = BAAI/bge-m3
device = cuda
max_length = 8192
batch_size = 32

[vector_store]
chunk_size = 1000
chunk_overlap = 200
search_k = 5

[llm]
temperature = 0.1
max_tokens = 1024
```

## 🐳 Docker Deployment / Docker部署

### Quick Docker Setup / 快速Docker设置
```bash
# Build Docker image / 构建Docker镜像
docker build -t gns3-intelligent-agent .

# Run with environment file / 使用环境文件运行
docker run -d \
  --name gns3-agent \
  --env-file .env \
  -v $(pwd)/knowledge_base:/app/knowledge_base \
  -v $(pwd)/vector_store:/app/vector_store \
  gns3-intelligent-agent
```

### Docker Compose / Docker Compose
```yaml
# docker-compose.yml
version: '3.8'
services:
  gns3-agent:
    build: .
    container_name: gns3-intelligent-agent
    env_file: .env
    volumes:
      - ./knowledge_base:/app/knowledge_base
      - ./vector_store:/app/vector_store
      - ./device_configs:/app/device_configs
    ports:
      - "8080:8080"
    restart: unless-stopped
    
  # Optional: Add Redis for caching / 可选：添加Redis缓存
  redis:
    image: redis:alpine
    container_name: redis-cache
    ports:
      - "6379:6379"
```

## ☁️ Cloud Deployment / 云部署

### AWS EC2 Setup / AWS EC2设置
```bash
# Instance requirements / 实例要求
# - Type: t3.large or better / 类型：t3.large或更好
# - Storage: 20GB+ EBS / 存储：20GB+ EBS
# - Security Group: Allow port 22, 8080 / 安全组：允许端口22, 8080

# Install dependencies / 安装依赖
sudo apt update
sudo apt install python3 python3-pip python3-venv git

# Setup application / 设置应用
git clone <repository>
cd GNS3/tools
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Google Cloud Platform / 谷歌云平台
```bash
# Use Compute Engine / 使用计算引擎
gcloud compute instances create gns3-agent \
  --machine-type=n1-standard-4 \
  --boot-disk-size=20GB \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --tags=gns3-agent

# Setup firewall / 设置防火墙
gcloud compute firewall-rules create allow-gns3-agent \
  --allow=tcp:8080 \
  --target-tags=gns3-agent
```

## 🔍 Troubleshooting / 故障排除

### Common Issues / 常见问题

#### Issue: "CUDA not available" / 问题："CUDA不可用"
```bash
# Solution 1: Install CUDA toolkit / 解决方案1：安装CUDA工具包
# Visit: https://developer.nvidia.com/cuda-downloads

# Solution 2: Use CPU mode / 解决方案2：使用CPU模式
# Edit rag_config.ini:
[embeddings]
device = cpu
```

#### Issue: "GNS3 connection failed" / 问题："GNS3连接失败"
```bash
# Check GNS3 server status / 检查GNS3服务器状态
curl http://YOUR_GNS3_SERVER:3080/v2/version

# Verify network connectivity / 验证网络连接
ping YOUR_GNS3_SERVER

# Check firewall settings / 检查防火墙设置
sudo ufw status
```

#### Issue: "LLM model not found" / 问题："LLM模型未找到"
```bash
# For Ollama / 对于Ollama
ollama pull llama3.1
ollama list

# For DeepSeek / 对于DeepSeek
# Verify API key in .env file / 验证.env文件中的API密钥
echo $DEEPSEEK_API_KEY
```

#### Issue: "Vector store initialization failed" / 问题："向量存储初始化失败"
```bash
# Clear existing vector store / 清除现有向量存储
rm -rf vector_store/*

# Rebuild vector store / 重建向量存储
python setup_rag.py --rebuild
```

### Debug Mode / 调试模式
```bash
# Enable debug logging / 启用调试日志
export DEBUG=true
python main.py

# Check logs / 检查日志
tail -f logs/gns3_agent.log
```

## 📊 Performance Tuning / 性能调优

### GPU Optimization / GPU优化
```ini
# rag_config.ini
[embeddings]
device = cuda
batch_size = 64  # Increase for more GPU memory
max_length = 8192
```

### Memory Optimization / 内存优化
```ini
[vector_store]
chunk_size = 500  # Reduce for less memory usage
search_k = 3     # Reduce search results
```

### CPU Optimization / CPU优化
```bash
# Set environment variables / 设置环境变量
export OMP_NUM_THREADS=4
export MKL_NUM_THREADS=4
```

## 🔄 Update & Maintenance / 更新与维护

### Regular Updates / 定期更新
```bash
# Update repository / 更新仓库
git pull origin main

# Update dependencies / 更新依赖
pip install -r requirements.txt --upgrade

# Rebuild vector store if needed / 如需要重建向量存储
python setup_rag.py --rebuild
```

### Backup & Restore / 备份与恢复
```bash
# Backup configuration and data / 备份配置和数据
tar -czf gns3-agent-backup.tar.gz \
  .env rag_config.ini knowledge_base/ vector_store/

# Restore from backup / 从备份恢复
tar -xzf gns3-agent-backup.tar.gz
```

## 📞 Support / 技术支持

### Getting Help / 获取帮助
- **📖 Documentation**: Read full documentation in `PROJECT_OVERVIEW.md`
- **🐛 Issues**: Report bugs on GitHub Issues
- **💬 Community**: Join discussions for help
- **📧 Email**: Contact support team

### Health Check / 健康检查
```bash
# System health check / 系统健康检查
python -c "
import torch
import transformers
import langchain
print('✅ All dependencies working')
print(f'PyTorch: {torch.__version__}')
print(f'CUDA Available: {torch.cuda.is_available()}')
"
```

---

## 🎉 Success! / 成功！

If you see this interface, your deployment is successful! / 如果看到此界面，说明部署成功！

```
🌟 GNS3 Intelligent Agent v6.0
   Network device management AI agent based on LangChain + Ollama
   Refactored version - Modular design

💡 Usage examples:
   • View network topology
   • List all devices
   • Get R-1 configuration
   
💬 Start conversation (enter 'quit' or 'exit' to exit):
--------------------------------------------------
```

**Next Steps / 下一步:**
1. Try some basic commands / 尝试一些基本命令
2. Add your network documentation / 添加网络文档
3. Configure advanced settings / 配置高级设置
4. Explore all features / 探索所有功能

---

*Happy networking! / 网络管理愉快！* 🚀
