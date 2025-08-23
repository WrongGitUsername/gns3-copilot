#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能语言适配器
根据用户输入自动检测语言并调整输出消息的语言风格
"""

import re
from typing import Dict, Optional, List
from dataclasses import dataclass

@dataclass
class LanguageConfig:
    """语言配置类"""
    use_english: bool = True  # 默认使用英文
    mixed_mode: bool = False
    tech_terms_english: bool = True

class LanguageDetector:
    """语言检测器"""
    
    def __init__(self):
        # 中文字符范围（包括中文标点）
        self.chinese_pattern = re.compile(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]')
        # 英文字母范围
        self.english_pattern = re.compile(r'[a-zA-Z]')
        
    def detect_language(self, text: str) -> LanguageConfig:
        """
        检测文本语言并返回语言配置
        
        Args:
            text: 输入文本
            
        Returns:
            LanguageConfig: 语言配置对象
        """
        if not text or not text.strip():
            return LanguageConfig()
        
        # 计算中文和英文字符数量
        chinese_chars = len(self.chinese_pattern.findall(text))
        english_chars = len(self.english_pattern.findall(text))
        total_chars = len(text.strip())
        
        # 忽略空格和标点符号
        meaningful_chars = chinese_chars + english_chars
        
        if meaningful_chars == 0:
            return LanguageConfig()
        
        chinese_ratio = chinese_chars / meaningful_chars
        english_ratio = english_chars / meaningful_chars
        
        # 语言检测逻辑 - 默认英文，只有明确包含中文时才使用中文
        if chinese_ratio > 0:
            # 包含中文字符，使用中文模式
            return LanguageConfig(use_english=False, mixed_mode=True, tech_terms_english=True)
        else:
            # 默认使用英文模式
            return LanguageConfig(use_english=True, mixed_mode=False, tech_terms_english=True)

class MessageAdapter:
    """消息适配器 - 根据语言配置调整输出消息"""
    
    def __init__(self):
        self.current_config = LanguageConfig()  # 现在默认为英文
        self.detector = LanguageDetector()
        
        # 消息模板字典
        self.messages = {
            # 系统初始化消息
            "initializing_llm": {
                "en": "🧠 Initializing LLM...",
                "zh": "🧠 初始化LLM..."
            },
            "llm_connected": {
                "en": "🧠 {} connected successfully: {}",
                "zh": "🧠 {} 连接成功: {}"
            },
            "deepseek_connected": {
                "en": "🧠 DeepSeek connected successfully: {}",
                "zh": "🧠 DeepSeek 连接成功: {}"
            },
            "deepseek_connected_default": {
                "en": "🧠 DeepSeek connected successfully (using default parameters)",
                "zh": "🧠 DeepSeek 连接成功（使用默认参数）"
            },
            "deepseek_init_failed": {
                "en": "❌ DeepSeek initialization failed: {}",
                "zh": "❌ DeepSeek 初始化失败: {}"
            },
            "model_not_initialized": {
                "en": "Model not initialized",
                "zh": "未初始化模型"
            },
            "current_model": {
                "en": "✅ Current model: {}: {}",
                "zh": "✅ 当前模型: {}: {}"
            },
            "initializing_toolset": {
                "en": "🛠️ Initializing toolset...",
                "zh": "🛠️ 初始化工具集..."
            },
            "initializing_processor": {
                "en": "🧩 Initializing intelligent processor...",
                "zh": "🧩 初始化智能处理器..."
            },
            "rag_config_loaded": {
                "en": "✅ RAG configuration loaded successfully",
                "zh": "✅ RAG配置加载成功"
            },
            "vector_store_loading": {
                "en": "📖 Loading existing vector store...",
                "zh": "📖 加载现有向量存储..."
            },
            "vector_store_loaded": {
                "en": "✅ Vector store loaded successfully",
                "zh": "✅ 向量存储加载成功"
            },
            "rag_kb_initialized": {
                "en": "✅ RAG knowledge base initialized successfully",
                "zh": "✅ RAG知识库初始化成功"
            },
            "rag_executor_initialized": {
                "en": "🧠 RAG-enhanced command executor initialized successfully",
                "zh": "🧠 RAG增强命令执行器初始化成功"
            },
            "vector_store_rebuilding": {
                "en": "🔄 Force rebuilding vector store...",
                "zh": "🔄 强制重建向量存储..."
            },
            "vector_store_rebuilt": {
                "en": "✅ Vector store rebuild completed",
                "zh": "✅ 向量存储重建完成"
            },
            "no_documents_for_vector_store": {
                "en": "❌ No documents available for building vector store",
                "zh": "❌ 没有文档可用于构建向量存储"
            },
            "loading_documents_from": {
                "en": "📚 Starting to load documents from: {}",
                "zh": "📚 开始加载文档从: {}"
            },
            "documents_loaded": {
                "en": "✅ Loaded {} documents",
                "zh": "✅ 加载了 {} 个文档"
            },
            "document_loading_error": {
                "en": "⚠️ Error loading documents: {}",
                "zh": "⚠️ 加载文档时出错: {}"
            },
            "creating_vector_embeddings": {
                "en": "🧠 Creating vector embeddings...",
                "zh": "🧠 正在创建向量嵌入..."
            },
            "vector_store_saved": {
                "en": "💾 Vector store saved to: {}",
                "zh": "💾 向量存储已保存到: {}"
            },
            "vector_store_not_found": {
                "en": "🆕 No existing vector store found, will create new one...",
                "zh": "🆕 未找到现有向量存储，将创建新的..."
            },
            "vector_store_load_failed": {
                "en": "❌ Failed to load vector store: {}",
                "zh": "❌ 加载向量存储失败: {}"
            },
            "vector_store_not_initialized": {
                "en": "❌ Vector store not initialized",
                "zh": "❌ 向量存储未初始化"
            },
            "splitting_documents": {
                "en": "🔧 Splitting documents...",
                "zh": "🔧 正在分割文档..."
            },
            "documents_split": {
                "en": "📄 Split into {} document chunks",
                "zh": "📄 分割成 {} 个文档块"
            },
            "agent_initialized": {
                "en": "✅ GNS3 intelligent agent initialization completed",
                "zh": "✅ GNS3智能代理初始化完成"
            },
            
            # 项目和设备管理
            "updating_project_info": {
                "en": "🔄 Updating project and device information...",
                "zh": "🔄 更新项目和设备信息..."
            },
            "getting_project_summary": {
                "en": "Getting project summary from server...",
                "zh": "正在获取服务器上的项目摘要..."
            },
            "found_projects": {
                "en": "Found {} open project(s):",
                "zh": "找到 {} 个打开的项目:"
            },
            "device_filter_results": {
                "en": "📊 Device filtering results:",
                "zh": "📊 设备过滤结果:"
            },
            "configurable_devices": {
                "en": "   Configurable devices: {} devices",
                "zh": "   可配置设备: {} 个"
            },
            "skipped_devices": {
                "en": "   Skipped devices: {} devices",
                "zh": "   跳过设备: {} 个"
            },
            "configurable_device_list": {
                "en": "✅ Configurable device list:",
                "zh": "✅ 可配置设备列表:"
            },
            "skipped_device_list": {
                "en": "⏭️ Skipped devices:",
                "zh": "⏭️ 跳过的设备:"
            },
            "cache_updated": {
                "en": "✅ Cache updated, found {} project(s)",
                "zh": "✅ 缓存更新完成，找到 {} 个项目"
            },
            
            # 设备配置获取
            "getting_device_config": {
                "en": "Getting configuration for {}...",
                "zh": "正在获取 {} 的配置信息..."
            },
            "console_port": {
                "en": "Console port: {}",
                "zh": "Console端口: {}"
            },
            "max_wait_time": {
                "en": "Maximum wait time: {} seconds",
                "zh": "最大等待时间: {}秒"
            },
            "connected_successfully": {
                "en": "Successfully connected to {}:{}",
                "zh": "成功连接到 {}:{}"
            },
            "executing_show_run": {
                "en": "Executing 'show running-config' command...",
                "zh": "执行 'show running-config' 命令..."
            },
            "receiving_data": {
                "en": "📥 Receiving data... {:,} characters ({} data blocks)",
                "zh": "📥 持续接收中... {:,} 字符 ({} 数据块)"
            },
            "config_transfer_complete": {
                "en": "✅ Configuration transfer detected as complete",
                "zh": "✅ 检测到配置传输完成"
            },
            "no_new_data_timeout": {
                "en": "⏰ No new data for extended period, considering transfer complete",
                "zh": "⏰ 长时间无新数据，认为传输完成"
            },
            "read_exception": {
                "en": "Exception during read process: {}",
                "zh": "读取过程中出现异常: {}"
            },
            "config_get_success": {
                "en": "✅ Successfully obtained {} configuration",
                "zh": "✅ 成功获取 {} 的配置"
            },
            "config_size": {
                "en": "📊 Configuration size: {:,} characters",
                "zh": "📊 配置大小: {:,} 字符"
            },
            "config_lines": {
                "en": "📄 Configuration lines: {:,} lines",
                "zh": "📄 配置行数: {:,} 行"
            },
            "config_get_time": {
                "en": "⏱️ Retrieval time: {:.2f} seconds",
                "zh": "⏱️ 获取耗时: {:.2f} 秒"
            },
            "config_get_failed": {
                "en": "❌ Failed to obtain {} configuration",
                "zh": "❌ 未能获取到 {} 的配置信息"
            },
            "config_get_error": {
                "en": "❌ Failed to get {} configuration: {}",
                "zh": "❌ 获取 {} 配置失败: {}"
            },
            "try_large_config_handler": {
                "en": "🔄 Trying large configuration handler...",
                "zh": "🔄 尝试使用大配置处理器..."
            },
            "large_config_mode": {
                "en": "🚀 Starting large configuration processing mode",
                "zh": "🚀 启动超大配置处理模式"
            },
            "trying_strategy": {
                "en": "🎯 Trying: {}",
                "zh": "🎯 尝试: {}"
            },
            "strategy_success": {
                "en": "✅ {} successful",
                "zh": "✅ {} 成功"
            },
            "strategy_config_too_short": {
                "en": "⚠️ {} retrieved configuration too short, trying next strategy",
                "zh": "⚠️ {} 获取的配置太短，尝试下一策略"
            },
            "strategy_failed": {
                "en": "❌ {} failed: {}",
                "zh": "❌ {} 失败: {}"
            },
            
            # 项目管理相关
            "getting_project_summary": {
                "en": "Getting project summary from server...",
                "zh": "正在获取服务器上的项目摘要..."
            },
            "no_open_projects_found": {
                "en": "No open projects found on the server.",
                "zh": "在服务器上没有找到任何处于打开状态的项目。"
            },
            "found_open_projects": {
                "en": "Found {} open project(s):",
                "zh": "找到 {} 个打开的项目:"
            },
            "get_project_summary_error": {
                "en": "Error getting project summary: {}",
                "zh": "获取项目摘要时发生错误: {}"
            },
            "get_project_details_error": {
                "en": "Error getting project {} details: {}",
                "zh": "获取项目 {} 详细信息时发生错误: {}"
            },
            "no_open_projects": {
                "en": "No open projects currently.",
                "zh": "当前没有打开的项目。"
            },
            "current_open_projects": {
                "en": "Currently open projects:",
                "zh": "当前打开的项目："
            },
            "project_name_id": {
                "en": "  - Name: {}, ID: {}",
                "zh": "  - 名称: {}, ID: {}"
            },
            "project_topology_info": {
                "en": "\n=== Project '{}' Topology Information ===",
                "zh": "\n=== 项目 '{}' 的拓扑信息 ==="
            },
            "node_list": {
                "en": "  Node list:",
                "zh": "  节点列表："
            },
            "node_details": {
                "en": "    - Name: {}, Type: {}, Status: {}, Console port: {}",
                "zh": "    - 名称: {}, 类型: {}, 状态: {}, 控制台端口: {}"
            },
            "no_nodes": {
                "en": "    No nodes.",
                "zh": "    无节点。"
            },
            "link_list": {
                "en": "  Link list:",
                "zh": "  链路列表："
            },
            "link_details": {
                "en": "    - Link ID: {}, Type: {}",
                "zh": "    - 链路ID: {}, 类型: {}"
            },
            "connection_point": {
                "en": "      Connection point: {} (adapter{}/port{})",
                "zh": "      连接点: {} (适配器{}/端口{})"
            },
            "no_links": {
                "en": "    No links.",
                "zh": "    无链路。"
            },
            "project_summary": {
                "en": "\n=== Project '{}' Summary ===",
                "zh": "\n=== 项目 '{}' 摘要 ==="
            },
            "project_id": {
                "en": "Project ID: {}",
                "zh": "项目ID: {}"
            },
            "node_count": {
                "en": "Node count: {}",
                "zh": "节点数量: {}"
            },
            "link_count": {
                "en": "Link count: {}",
                "zh": "链路数量: {}"
            },
            "node_status_stats": {
                "en": "Node status statistics:",
                "zh": "节点状态统计:"
            },
            "status_count": {
                "en": "  {}: {}",
                "zh": "  {}: {}"
            },
            
            # 命令处理
            "analyzing_request": {
                "en": "🤖 Analyzing request...",
                "zh": "🤖 正在分析请求..."
            },
            "using_rag_enhanced": {
                "en": "🧠 Using RAG-enhanced command selection...",
                "zh": "🧠 使用RAG增强的命令选择..."
            },
            "using_rag_enhanced_command_selection": {
                "en": "🧠 Using RAG-enhanced command selection...",
                "zh": "🧠 使用RAG增强的命令选择..."
            },
            "vector_store_not_initialized": {
                "en": "❌ Vector store not initialized",
                "zh": "❌ 向量存储未初始化"
            },
            "rag_returned_commands": {
                "en": "🧠 RAG knowledge base returned {} relevant commands",
                "zh": "🧠 RAG知识库返回了 {} 个相关命令"
            },
            "rag_knowledge_base_returned": {
                "en": "🧠 RAG knowledge base returned {} relevant commands",
                "zh": "🧠 RAG知识库返回了 {} 个相关命令"
            },
            "found_relevant_commands": {
                "en": "📚 Found {} relevant commands (source: RAG + base knowledge)",
                "zh": "📚 找到 {} 个相关命令（来源：RAG + 基础知识库）"
            },
            "found_relevant_commands_combined": {
                "en": "📚 Found {} relevant commands (source: RAG + base knowledge base)",
                "zh": "📚 找到 {} 个相关命令（来源：RAG + 基础知识库）"
            },
            "llm_selected_commands": {
                "en": "🤖 LLM selected commands: {}",
                "zh": "🤖 LLM选择的命令: {}"
            },
            "llm_command_selection_failed": {
                "en": "⚠️ LLM command selection failed, using default strategy: {}",
                "zh": "⚠️ LLM命令选择失败，使用默认策略: {}"
            },
            "executing_commands_on_device": {
                "en": "🔍 Executing {} commands on device {}...",
                "zh": "🔍 执行 {} 个命令在设备 {} 上..."
            },
            "executing_command": {
                "en": "  📡 Executing: {}",
                "zh": "  📡 执行: {}"
            },
            "using_cached_result": {
                "en": "  ✅ Using cached result",
                "zh": "  ✅ 使用缓存结果"
            },
            "command_prompt_detected": {
                "en": "  🎯 Command prompt detected, command execution complete",
                "zh": "  🎯 检测到命令提示符，命令执行完成"
            },
            "no_output_timeout": {
                "en": "  ⏱️ No additional output, command appears complete",
                "zh": "  ⏱️ 无新增输出，命令执行完成"
            },
            "command_execution_complete": {
                "en": "  ✅ Command execution complete, output length: {} characters",
                "zh": "  ✅ 命令执行完成，输出长度: {} 字符"
            },
            "command_execution_failed": {
                "en": "  ❌ Command execution failed: {}",
                "zh": "  ❌ 命令执行失败: {}"
            },
            
            # 设备状态相关消息
            "device_type_not_supported": {
                "en": "Device type not supported for configuration retrieval ({})",
                "zh": "设备类型不支持配置获取 ({})"
            },
            "device_not_running": {
                "en": "Device not running (status: {})",
                "zh": "设备未运行 (状态: {})"
            },
            "no_relevant_commands_found": {
                "en": "❌ No relevant network commands found for query '{}'",
                "zh": "❌ 无法找到与查询 '{}' 相关的网络命令"
            },
            "llm_no_suitable_commands": {
                "en": "❌ LLM could not select suitable commands",
                "zh": "❌ LLM未能选择到合适的命令"
            },
            
            # BGE-M3配置相关
            "bge_m3_config_created": {
                "en": "✅ BGE-M3 configuration created",
                "zh": "✅ BGE-M3配置已创建"
            },
            "config_file_location": {
                "en": "📄 Configuration file: {}",
                "zh": "📄 配置文件: {}"
            },
            "embedding_model": {
                "en": "🧠 Embedding model: {}",
                "zh": "🧠 嵌入模型: {}"
            },
            "document_chunk_size": {
                "en": "📄 Document chunk size: {}",
                "zh": "📄 文档分块大小: {}"
            },
            "retrieval_count": {
                "en": "🔍 Retrieval count: {}",
                "zh": "🔍 检索数量: {}"
            },
            "network_keywords_count": {
                "en": "🌐 Network keywords count: {}",
                "zh": "🌐 网络关键词数量: {}"
            },
            "command_patterns_count": {
                "en": "🔧 Command patterns count: {}",
                "zh": "🔧 命令模式数量: {}"
            },
            
            # 错误消息
            "error_occurred": {
                "en": "❌ Error occurred: {}",
                "zh": "❌ 发生错误: {}"
            },
            "please_retry": {
                "en": "Please retry or enter 'quit' to exit",
                "zh": "请重试或输入 'quit' 退出"
            },
            
            # 系统初始化消息
            "initializing_llm": {
                "en": "🧠 Initializing LLM...",
                "zh": "🧠 正在初始化 LLM..."
            },
            "current_model": {
                "en": "✅ Current model: {}: {}",
                "zh": "✅ 当前模型: {}: {}"
            },
            "initializing_toolset": {
                "en": "🛠 Initializing toolset...",
                "zh": "🛠 正在初始化工具集..."
            },
            "initializing_processor": {
                "en": "🧩 Initializing intelligent processor...",
                "zh": "🧩 正在初始化智能处理器..."
            },
            "agent_initialized": {
                "en": "✅ GNS3 intelligent agent initialization completed",
                "zh": "✅ GNS3智能代理初始化完成"
            },
            "app_title": {
                "en": "🌟 GNS3 Intelligent Agent v6.0",
                "zh": "🌟 GNS3 智能代理 v6.0"
            },
            "app_description": {
                "en": "   Network device management AI agent based on LangChain + Ollama",
                "zh": "   基于 LangChain + Ollama 的网络设备管理智能体"
            },
            "app_version": {
                "en": "   Refactored version - Modular design",
                "zh": "   重构版本 - 模块化设计"
            },
            "usage_examples": {
                "en": "💡 Usage examples:",
                "zh": "💡 使用示例："
            },
            "example_topology": {
                "en": "   • View network topology",
                "zh": "   • 查看网络拓扑"
            },
            "example_devices": {
                "en": "   • List all devices",
                "zh": "   • 列出所有设备"
            },
            "example_config": {
                "en": "   • Get R-1 configuration",
                "zh": "   • 获取R-1的配置"
            },
            "example_interfaces": {
                "en": "   • View R-1 interface connections",
                "zh": "   • 查看R-1的接口连接"
            },
            "example_summary": {
                "en": "   • Network connection summary",
                "zh": "   • 网络连接汇总"
            },
            "example_status": {
                "en": "   • Analyze device status",
                "zh": "   • 分析设备状态"
            },
            "example_project": {
                "en": "   • Project information",
                "zh": "   • 项目信息"
            },
            "chat_start": {
                "en": "💬 Start conversation (enter 'quit' or 'exit' to exit):",
                "zh": "💬 开始对话 (输入 'quit' 或 'exit' 退出):"
            },
            
            # 用户交互
            "user_prompt": {
                "en": "🙋 You: ",
                "zh": "🙋 您: "
            },
            "goodbye": {
                "en": "👋 Goodbye!",
                "zh": "👋 再见！"
            },
            
            # 专业术语（保持英文）
            "tech_terms": {
                "DeepSeek": "DeepSeek",
                "Ollama": "Ollama", 
                "GNS3": "GNS3",
                "RAG": "RAG",
                "LLM": "LLM",
                "BGE-M3": "BGE-M3",
                "FAISS": "FAISS",
                "OSPF": "OSPF",
                "BGP": "BGP",
                "EIGRP": "EIGRP",
                "VPN": "VPN",
                "VLAN": "VLAN"
            },
            
            # LLM 提示模板
            "main_prompt_template": {
                "en": """You are a professional network device management assistant specialized in helping users manage and analyze GNS3 network environments.

System Environment Information:
{context}

Conversation History:
{history}

User Request: {user_input}

Please analyze user requirements and execute corresponding operations. If the user wants to get device configuration but hasn't specified device name, please list devices first for user selection.

Response Requirements:
- Reply in English
- Provide clear and structured information
- For configuration analysis, provide professional network technology advice
- Maintain friendly and professional tone

Execute operations and reply:""",
                "zh": """你是一个专业的网络设备管理助手，专门帮助用户管理和分析GNS3网络环境。

系统环境信息：
{context}

对话历史：
{history}

用户请求：{user_input}

请分析用户需求并执行相应操作。如果用户要获取设备配置但没有指定设备名称，请先列出设备让用户选择。

回答要求：
- 使用中文回复
- 提供清晰、结构化的信息
- 对于配置分析，提供专业的网络技术建议
- 保持友好和专业的语气

执行操作并回复："""
            },
            
            "analysis_prompt_template": {
                "en": """Please analyze the following network device configuration in detail and provide a professional network engineer-level analysis report:

Device Name: {device_name}

Configuration Content:
{full_config}

Please analyze from the following aspects:
1. Basic device information (hostname, version, etc.)
2. Interface configuration analysis
3. Routing protocol configuration
4. Security configuration assessment
5. Potential issue identification
6. Optimization recommendations

Please provide detailed, professional, and structured analysis report.""",
                "zh": """请详细分析以下网络设备配置，并提供专业的网络工程师级别的分析报告：

设备名称: {device_name}

配置内容:
{full_config}

请从以下几个方面进行分析：
1. 设备基本信息（主机名、版本等）
2. 接口配置分析
3. 路由协议配置
4. 安全配置评估
5. 潜在问题识别
6. 优化建议

请提供详细、专业、结构化的分析报告。"""
            },
            
            "rag_command_prompt_template": {
                "en": """As a professional network engineer, please analyze user query and select the most suitable network commands.

User Query: {query}

Available Command List (from multiple knowledge sources):
{commands_str}

Notes:
- [base_kb]: Basic command knowledge base
- [rag_kb]: Network troubleshooting document RAG knowledge base  
- [keyword_search]: Keyword matching

Please select the most suitable {max_commands} commands, prioritizing:
1. Professional recommendations from RAG knowledge base
2. Command relevance and accuracy  
3. Problem-solving effectiveness

IMPORTANT CONSTRAINTS:
- Return ONLY valid network commands
- Do NOT use wildcards (* ? ...)  
- Do NOT use placeholders (x.x.x.x, ***_, ..., etc.)
- Do NOT use incomplete commands (show ip ro...)
- Commands must contain ONLY letters, numbers, spaces, hyphens, dots, and slashes
- Each command must be complete and executable

Return only commands, one per line, no other text.

Valid Examples:
show ip ospf neighbor
show ip route ospf
show running-config

Invalid Examples (DO NOT USE):
show ip route x.x.x.x
show ip ro...
show * interface
ping ***""",
                "zh": """作为专业网络工程师，请分析用户查询并选择最适合的网络命令。

用户查询: {query}

可用命令列表（包含多个知识源）:
{commands_str}

说明：
- [base_kb]: 基础命令知识库
- [rag_kb]: 网络排错文档RAG知识库  
- [keyword_search]: 关键词匹配

请选择最适合的 {max_commands} 个命令，优先考虑：
1. RAG知识库中的专业建议
2. 命令的相关性和准确性  
3. 解决问题的有效性

重要约束：
- 只返回有效的网络命令
- 不要使用通配符（* ? ...）
- 不要使用占位符（x.x.x.x, ***_, ..., 等）
- 不要使用不完整的命令（show ip ro...）
- 命令只能包含字母、数字、空格、连字符、点号和斜杠
- 每个命令必须完整且可执行

只返回命令本身，每行一个，不要其他文字。

有效示例：
show ip ospf neighbor
show ip route ospf
show running-config

无效示例（请勿使用）：
show ip route x.x.x.x
show ip ro...
show * interface
ping ***"""
            }
        }
    
    def update_language_config(self, user_input: str):
        """根据用户输入更新语言配置"""
        self.current_config = self.detector.detect_language(user_input)
    
    def get_message(self, key: str, *args, **kwargs) -> str:
        """
        获取适配语言的消息
        
        Args:
            key: 消息键
            *args: 格式化参数
            **kwargs: 关键字参数
            
        Returns:
            str: 适配后的消息
        """
        if key not in self.messages:
            return key  # 如果没有找到键，返回键本身
        
        message_dict = self.messages[key]
        
        # 选择语言
        if self.current_config.use_english:
            template = message_dict.get("en", message_dict.get("zh", key))
        else:
            template = message_dict.get("zh", message_dict.get("en", key))
        
        # 格式化消息
        try:
            if args:
                return template.format(*args)
            elif kwargs:
                return template.format(**kwargs)
            else:
                return template
        except (IndexError, KeyError):
            return template
    
    def format_device_info(self, device_name: str, device_type: str, port: int) -> str:
        """格式化设备信息"""
        if self.current_config.use_english:
            return f"   - {device_name} ({device_type}) port:{port}"
        else:
            return f"   - {device_name} ({device_type}) 端口:{port}"
    
    def format_project_info(self, name: str, project_id: str) -> str:
        """格式化项目信息"""
        if self.current_config.use_english:
            return f"  - Name: {name}, ID: {project_id}"
        else:
            return f"  - 名称: {name}, ID: {project_id}"
    
    def format_skip_reason(self, device_name: str, reason: str) -> str:
        """格式化跳过设备的原因"""
        if self.current_config.use_english:
            return f"   - {device_name}: {reason}"
        else:
            # 翻译常见的跳过原因
            reason_translations = {
                "Device not running": "设备未运行",
                "Device type not supported for configuration retrieval": "设备类型不支持配置获取",
                "stopped": "已停止",
                "ethernet_switch": "以太网交换机",
                "cloud": "云设备"
            }
            
            translated_reason = reason
            for en_text, zh_text in reason_translations.items():
                translated_reason = translated_reason.replace(en_text, zh_text)
            
            return f"   - {device_name}: {translated_reason}"
    
    def get_prompt_template(self, template_name: str, **kwargs) -> str:
        """获取适配语言的提示模板"""
        template_key = f"{template_name}_template"
        
        if template_key not in self.messages:
            return f"Template not found: {template_key}"
        
        template_dict = self.messages[template_key]
        
        # 选择语言
        if self.current_config.use_english:
            template = template_dict.get("en", template_dict.get("zh", template_key))
        else:
            template = template_dict.get("zh", template_dict.get("en", template_key))
        
        # 格式化模板
        try:
            if kwargs:
                return template.format(**kwargs)
            else:
                return template
        except (KeyError, ValueError) as e:
            return template

# 全局语言适配器实例
language_adapter = MessageAdapter()

def get_message(key: str, *args, **kwargs) -> str:
    """便捷函数：获取适配语言的消息"""
    return language_adapter.get_message(key, *args, **kwargs)

def update_language(user_input: str):
    """便捷函数：更新语言配置"""
    language_adapter.update_language_config(user_input)

def format_device_info(device_name: str, device_type: str, port: int) -> str:
    """便捷函数：格式化设备信息"""
    return language_adapter.format_device_info(device_name, device_type, port)

def format_project_info(name: str, project_id: str) -> str:
    """便捷函数：格式化项目信息"""
    return language_adapter.format_project_info(name, project_id)

def format_skip_reason(device_name: str, reason: str) -> str:
    """便捷函数：格式化跳过原因"""
    return language_adapter.format_skip_reason(device_name, reason)

def get_prompt_template(template_name: str, **kwargs) -> str:
    """便捷函数：获取提示模板"""
    return language_adapter.get_prompt_template(template_name, **kwargs)
