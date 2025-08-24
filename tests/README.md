# 🧪 Test Documentation / 测试文档

This directory contains test files for validating the enhanced features of the GNS3 Intelligent Agent.

本目录包含用于验证GNS3智能代理增强功能的测试文件。

## 📋 Test Files Overview / 测试文件概览

| Test File | Purpose | 测试目的 |
|-----------|---------|----------|
| **test_connectivity_analysis.py** | Connectivity analysis validation | 连通性分析验证 |
| **test_english_connectivity.py** | English-mode connectivity testing | 英文模式连通性测试 |
| **test_english_analysis.py** | English language adaptation testing | 英文语言适配测试 |
| **test_main_connectivity.py** | Main application connectivity testing | 主应用连通性测试 |
| **test_enhanced_executor.py** | Enhanced executor functionality testing | 增强执行器功能测试 |

## 🔍 Test Descriptions / 测试描述

### test_connectivity_analysis.py
**Purpose / 目的**: Tests the intelligent connectivity analysis feature
- ✅ Device IP discovery from configurations / 从配置中发现设备IP
- ✅ Ping command analysis and execution / Ping命令分析和执行
- ✅ Connectivity report generation / 连通性报告生成

### test_english_connectivity.py  
**Purpose / 目的**: Validates English-only output for connectivity queries
- ✅ English input detection / 英文输入检测
- ✅ English-only response verification / 纯英文响应验证
- ✅ No Chinese text in English mode / 英文模式下无中文文本

### test_english_analysis.py
**Purpose / 目的**: Comprehensive English language adaptation testing
- ✅ Language detection accuracy / 语言检测准确性
- ✅ Message template validation / 消息模板验证
- ✅ LLM prompt template consistency / LLM提示模板一致性

### test_main_connectivity.py
**Purpose / 目的**: End-to-end connectivity testing through main application
- ✅ Full system integration / 完整系统集成
- ✅ Real device communication / 真实设备通信
- ✅ Complete workflow validation / 完整工作流验证

### test_enhanced_executor.py
**Purpose / 目的**: Enhanced executor feature validation
- ✅ RAG-enhanced command execution / RAG增强命令执行
- ✅ Device configuration analysis / 设备配置分析
- ✅ Advanced query processing / 高级查询处理

## 🚀 Running Tests / 运行测试

### Prerequisites / 前提条件
```bash
# Ensure GNS3 project is running / 确保GNS3项目正在运行
# Configure environment variables / 配置环境变量
# Install dependencies / 安装依赖项
pip install -r requirements.txt
```

### Individual Test Execution / 单独测试执行
```bash
# Test connectivity analysis / 测试连通性分析
python tests/test_connectivity_analysis.py

# Test English mode / 测试英文模式
python tests/test_english_connectivity.py

# Test language adaptation / 测试语言适配
python tests/test_english_analysis.py

# Test main application / 测试主应用
python tests/test_main_connectivity.py

# Test enhanced executor / 测试增强执行器
python tests/test_enhanced_executor.py
```

### Batch Test Execution / 批量测试执行
```bash
# Run all tests / 运行所有测试
cd tests/
for test in test_*.py; do
    echo "Running $test..."
    python "$test"
    echo "---"
done
```

## 📊 Test Results Interpretation / 测试结果解释

### Success Indicators / 成功指标
- ✅ **Language Detection**: Correct language identification / 正确的语言识别
- ✅ **Response Consistency**: Matching input-output language / 输入输出语言匹配
- ✅ **Device Discovery**: Real IP addresses from configs / 从配置获取真实IP地址
- ✅ **Command Execution**: Successful device communication / 成功的设备通信
- ✅ **Error Handling**: Graceful failure management / 优雅的错误处理

### Failure Indicators / 失败指标
- ❌ **Language Mismatch**: Chinese text in English mode / 英文模式出现中文
- ❌ **Fake IPs**: Using hardcoded/irrelevant IP addresses / 使用硬编码/无关IP地址
- ❌ **Connection Errors**: Unable to reach GNS3 devices / 无法连接GNS3设备
- ❌ **Execution Failures**: Command validation or execution errors / 命令验证或执行错误

## 🛠️ Troubleshooting / 故障排除

### Common Issues / 常见问题

1. **GNS3 Connection Errors / GNS3连接错误**
   ```bash
   # Check GNS3 server status / 检查GNS3服务器状态
   curl http://192.168.101.1:3080/v2/version
   
   # Verify project is running / 验证项目正在运行
   curl http://192.168.101.1:3080/v2/projects
   ```

2. **Environment Configuration / 环境配置**
   ```bash
   # Check environment variables / 检查环境变量
   echo $GNS3_SERVER_URL
   echo $TELNET_HOST
   
   # Verify API keys / 验证API密钥
   echo $DEEPSEEK_API_KEY
   ```

3. **Language Detection Issues / 语言检测问题**
   ```python
   # Test language detector manually / 手动测试语言检测器
   from core.language_adapter import LanguageDetector
   detector = LanguageDetector()
   print(detector.detect_language("ping from R1 to R2"))
   ```

## 📝 Test Development Guidelines / 测试开发指南

### Adding New Tests / 添加新测试
1. **File Naming**: Use `test_<feature>.py` convention / 使用 `test_<功能>.py` 命名约定
2. **Documentation**: Include clear test purpose and expected outcomes / 包含清晰的测试目的和预期结果
3. **Error Handling**: Test both success and failure scenarios / 测试成功和失败场景
4. **Language Testing**: Validate both English and Chinese modes / 验证英文和中文模式

### Test Structure / 测试结构
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test Description: Brief description of what this test validates
测试描述: 此测试验证的内容简述
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test implementation
# 测试实现
```

---

## 📄 Related Documentation / 相关文档

- **[📖 Main README](../README.md)** - Project overview / 项目概览
- **[🔧 Core Modules](../core/README.md)** - Technical documentation / 技术文档
- **[🌍 Language System](../README_LANGUAGE.md)** - Language adaptation guide / 语言适配指南
- **[📚 RAG System](../README_RAG.md)** - RAG configuration / RAG配置

---

<div align="center">

**🧪 Testing ensures reliability and quality! / 测试确保可靠性和质量！**

</div>
