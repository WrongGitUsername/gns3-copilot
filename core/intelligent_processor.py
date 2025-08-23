#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能请求处理器
负责处理用户输入、意图分析和动作执行
增强版：集成RAG和LLM的智能命令执行系统，支持多语言适配
"""

import re
import configparser
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from langchain_core.prompts import PromptTemplate
from .gns3_agent_tools import GNS3AgentTools
from .language_adapter import get_message, get_prompt_template, language_adapter


class IntelligentProcessor:
    """智能请求处理器"""
    
    def __init__(self, tools: GNS3AgentTools, llm):
        self.tools = tools
        self.llm = llm
        self.chat_history: List[Dict[str, str]] = []
        
        # 加载RAG配置
        self.config = self._load_rag_config()
        
        # 根据配置初始化命令执行器
        self._initialize_command_executor()
    
    def _load_rag_config(self) -> configparser.ConfigParser:
        """加载RAG配置"""
        config = configparser.ConfigParser()
        config_path = Path(__file__).parent.parent / "rag_config.ini"
        
        if config_path.exists():
            config.read(config_path)
            print(get_message("rag_config_loaded"))
        else:
            if language_adapter.current_config.use_english:
                print("⚠️ RAG configuration file not found, using default settings")
            else:
                print("⚠️ 未找到RAG配置文件，使用默认设置")
            # 设置默认配置
            config['rag'] = {
                'enabled': 'false',
                'knowledge_base_path': './knowledge_base',
                'vector_store_path': './vector_store'
            }
        
        return config
    
    def _initialize_command_executor(self):
        """根据配置初始化命令执行器"""
        use_rag = self.config.getboolean('rag', 'enabled', fallback=False)
        
        if use_rag:
            try:
                # 尝试导入RAG增强执行器
                from .rag_enhanced_executor import RAGEnhancedCommandExecutor
                self.command_executor = RAGEnhancedCommandExecutor(
                    telnet_host=self.tools.telnet_host,
                    llm=self.llm,
                    use_rag=True
                )
                print(get_message("rag_executor_initialized"))
            except ImportError as e:
                if language_adapter.current_config.use_english:
                    print(f"⚠️ RAG dependencies not installed, using basic executor: {e}")
                else:
                    print(f"⚠️ RAG依赖未安装，使用基础执行器: {e}")
                self._init_base_executor()
            except Exception as e:
                if language_adapter.current_config.use_english:
                    print(f"⚠️ RAG executor initialization failed, using basic executor: {e}")
                else:
                    print(f"⚠️ RAG执行器初始化失败，使用基础执行器: {e}")
                self._init_base_executor()
        else:
            self._init_base_executor()
    
    def _init_base_executor(self):
        """初始化基础命令执行器"""
        from .intelligent_command_executor import IntelligentCommandExecutor
        self.command_executor = IntelligentCommandExecutor(
            telnet_host=self.tools.telnet_host, 
            llm=self.llm
        )
        print("📋 基础命令执行器初始化成功")
    
    def process_user_request(self, user_input: str) -> str:
        """处理用户请求"""
        user_input = user_input.strip()
        
        if not user_input:
            return "🤔 请告诉我您需要什么帮助"
        
        # 构建上下文
        context = self.tools.build_context()
        
        # 更新语言配置
        language_adapter.update_language_config(user_input)
        
        # 创建提示模板
        template_content = get_prompt_template("main_prompt")
        prompt_template = PromptTemplate.from_template(template_content)
        
        # 构建对话历史字符串
        history_str = ""
        for i, chat in enumerate(self.chat_history[-3:]):  # 只显示最近3轮对话
            history_str += f"用户{i+1}: {chat['user']}\\n助手{i+1}: {chat['assistant']}\\n\\n"
        
        # 生成提示
        prompt = prompt_template.format(
            context=context,
            user_input=user_input,
            history=history_str
        )
        
        try:
            # 使用 LLM 分析用户意图并生成响应
            print(get_message("analyzing_request"))
            response = self.llm.invoke(prompt)
            
            # 根据 LLM 的分析，执行具体操作
            action_response = self._execute_action(user_input, response)
            
            # 更新对话历史
            self.chat_history.append({
                "user": user_input,
                "assistant": action_response
            })
            
            # 保持历史记录不超过10轮
            if len(self.chat_history) > 10:
                self.chat_history = self.chat_history[-10:]
            
            return action_response
            
        except Exception as e:
            return f"❌ 处理请求失败: {e}"
    
    def _execute_action(self, user_input: str, llm_response: str) -> str:
        """根据用户输入和LLM分析执行具体操作"""
        user_input_lower = user_input.lower()
        
        # 1. 优先检查是否为网络命令查询（使用智能命令执行器）
        network_command_keywords = [
            'ospf', 'bgp', 'neighbor', 'route', 'routing', 'interface', 'vlan', 
            'stp', 'spanning', 'version', 'show', 'display',
            '邻居', '路由', '接口状态', '版本信息', '生成树', '状态'
        ]
        
        # 判断是否为网络命令查询
        is_network_command_query = any(keyword in user_input_lower for keyword in network_command_keywords)
        
        # 排除一些特定的非命令查询
        exclude_keywords = ['拓扑', '网络结构', '设备列表', '项目', '连接汇总']
        is_excluded = any(keyword in user_input_lower for keyword in exclude_keywords)
        
        if is_network_command_query and not is_excluded:
            return self._handle_network_command_query(user_input)
        
        # 2. 传统的关键词匹配（保持原有功能）
        if any(keyword in user_input_lower for keyword in ['拓扑', '网络结构', '网络拓扑', 'topology']):
            return self.tools.get_topology_info()
        
        elif any(keyword in user_input_lower for keyword in ['设备列表', '有哪些设备', '设备', 'device', 'list']):
            return self.tools.list_devices()
        
        elif any(keyword in user_input_lower for keyword in ['项目状态', '项目信息', '项目', 'project']):
            return self.tools.get_project_status()
        
        elif any(keyword in user_input_lower for keyword in ['接口', '连接', '链路', '端口', 'interface', 'connection', 'port', 'link']):
            # 检查是否指定了设备
            device_name = self.tools.extract_device_name(user_input)
            if device_name:
                return self.tools.get_interface_connections(device_name)
            elif any(keyword in user_input_lower for keyword in ['汇总', '总结', 'summary']):
                return self.tools.get_network_connections_summary()
            else:
                return self.tools.get_interface_connections()
        
        elif any(keyword in user_input_lower for keyword in ['分析', 'analyze']) and not any(keyword in user_input_lower for keyword in ['项目', 'project']):
            # 设备配置分析
            device_name = self.tools.extract_device_name(user_input)
            if device_name:
                return self._analyze_device_config(device_name)
            else:
                return "请指定要分析的设备名称，例如：'分析R-1'"
        
        elif any(keyword in user_input_lower for keyword in ['配置', 'config']):
            # 尝试提取设备名称
            device_name = self.tools.extract_device_name(user_input)
            if device_name:
                # 检查是否要求详细分析
                if any(keyword in user_input_lower for keyword in ['详细分析', '分析配置', '配置分析', 'analyze', '分析']):
                    return self._analyze_device_config(device_name)
                else:
                    return self.tools.get_device_config(device_name)
            else:
                return self.tools.list_devices() + "\\n\\n请指定要获取配置的设备名称，例如：'获取R-1的配置'"
        
        # 如果没有匹配到特定操作，返回 LLM 的通用回复
        return llm_response
    
    def _analyze_device_config(self, device_name: str) -> str:
        """获取设备完整配置并进行AI分析"""
        try:
            # 首先获取设备的完整配置
            full_config = self._get_full_device_config(device_name)
            if not full_config:
                return f"❌ 无法获取 {device_name} 的完整配置"
            
            # 构建分析提示词
            analysis_prompt = get_prompt_template("analysis_prompt", 
                                                 device_name=device_name, 
                                                 full_config=full_config)
            
            print(f"🤖 正在分析 {device_name} 配置...")
            
            # 使用LLM进行分析
            analysis_result = self.llm.invoke(analysis_prompt)
            
            if hasattr(analysis_result, 'content'):
                content = analysis_result.content
            else:
                content = str(analysis_result)
            
            # 格式化返回结果
            result = f"""🔍 {device_name} 配置分析报告
{'='*50}

{content}

📋 配置统计信息：
   - 设备名称: {device_name}
   - 配置行数: {len(full_config.splitlines())}
   - 配置大小: {len(full_config.encode('utf-8')) / 1024:.1f} KB
   - 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            return result
            
        except Exception as e:
            return f"❌ 分析 {device_name} 配置时发生错误: {e}"
    
    def _get_full_device_config(self, device_name: str) -> str:
        """获取设备的完整配置"""
        try:
            # 获取设备信息
            self.tools.update_cache()
            
            device_info = None
            device_name_lower = device_name.lower()
            
            for project_name, project_devices in self.tools.devices_cache.items():
                for device in project_devices['configurable_devices']:
                    if device['name'].lower() == device_name_lower:
                        device_info = {'device': device, 'project': project_name}
                        break
                if device_info:
                    break
            
            if not device_info:
                return None
            
            device = device_info['device']
            console_port = device.get('console')
            
            # 获取完整配置
            config = self.tools.config_manager.get_device_config(device_name, console_port)
            return config
            
        except Exception as e:
            print(f"获取 {device_name} 完整配置失败: {e}")
            return None
    
    def _handle_network_command_query(self, user_input: str) -> str:
        """处理网络命令查询（使用智能命令执行器）"""
        try:
            # 更新设备缓存
            self.tools.update_cache()
            
            # 获取所有可配置设备
            all_devices = []
            for project_name, project_devices in self.tools.devices_cache.items():
                all_devices.extend(project_devices['configurable_devices'])
            
            if not all_devices:
                return "❌ 没有找到可配置的设备"
            
            # 检查是否为多设备查询
            device_count = 0
            for device in all_devices:
                if device['name'].lower() in user_input.lower():
                    device_count += 1
            
            # 如果查询涉及多个设备，不设置target_device让系统自动识别所有设备
            # 如果只涉及一个设备，则提取目标设备名称
            target_device = None if device_count > 1 else self.tools.extract_device_name(user_input)
            
            # 使用智能命令执行器处理查询
            result = self.command_executor.execute_intelligent_query(
                user_query=user_input,
                devices_info=all_devices,
                target_device=target_device
            )
            
            return result
            
        except Exception as e:
            return f"❌ 智能命令查询处理失败: {e}"
