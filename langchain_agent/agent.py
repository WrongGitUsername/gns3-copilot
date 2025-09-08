"""
GNS3 LangChain Agent主类
"""

import re
from typing import Dict, Any, List, Optional
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.schema import SystemMessage
from langchain_deepseek import ChatDeepSeek
from langchain.memory import ConversationBufferMemory

from langchain_agent.tools import create_gns3_tools
from langchain_agent.prompts import (
    SYSTEM_PROMPT, OSPF_ANALYSIS_PROMPT, BGP_ANALYSIS_PROMPT,
    GENERAL_NETWORK_ANALYSIS_PROMPT, ERROR_HANDLING_PROMPT
)
from langchain_agent.config import AgentConfig


class GNS3Agent:
    """GNS3网络设备运维Agent - 使用DeepSeek LLM"""
    
    def __init__(self, 
                 server_url: str = None,
                 user: str = None,
                 password: str = None,
                 api_key: str = None,
                 base_url: str = None):
        """
        初始化GNS3 Agent
        
        Args:
            server_url: GNS3服务器URL
            user: GNS3用户名
            password: GNS3密码
            api_key: DeepSeek API密钥
            base_url: DeepSeek API基础URL
        """
        self.server_url = server_url or AgentConfig.GNS3_SERVER_URL
        self.user = user or AgentConfig.GNS3_USER
        self.password = password or AgentConfig.GNS3_PASSWORD
        
        # 初始化LLM
        self.llm = self._init_llm(
            api_key=api_key or AgentConfig.DEEPSEEK_API_KEY,
            base_url=base_url or AgentConfig.DEEPSEEK_BASE_URL
        )
        
        # 创建工具
        self.tools = create_gns3_tools(
            server_url=self.server_url,
            user=self.user,
            password=self.password
        )
        
        # 创建Agent
        self.agent = self._create_agent()
        
        # 创建执行器
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            max_iterations=AgentConfig.MAX_ITERATIONS,
            verbose=True,
            handle_parsing_errors=True
        )
        
        # 初始化内存
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
    
    def _init_llm(self, api_key: str = None, base_url: str = None):
        """初始化DeepSeek LLM"""
        try:
            llm_kwargs = {
                "model": AgentConfig.LLM_MODEL,
                "temperature": AgentConfig.LLM_TEMPERATURE
            }
            
            if api_key:
                llm_kwargs["api_key"] = api_key
            if base_url:
                llm_kwargs["base_url"] = base_url
                
            return ChatDeepSeek(**llm_kwargs)
                
        except Exception as e:
            print(f"LLM初始化失败: {e}")
            print("⚠️  将在测试模式下运行，部分功能可能受限")
            
            # 创建一个简单的Mock LLM用于测试
            from unittest.mock import Mock
            mock_llm = Mock()
            mock_llm.invoke = Mock(return_value=Mock(content="这是测试模式的响应"))
            return mock_llm
    
    def _create_agent(self):
        """创建Agent"""
        from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad")
        ])
        
        return create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
    
    def query(self, user_input: str) -> Dict[str, Any]:
        """
        处理用户查询
        
        Args:
            user_input: 用户输入
            
        Returns:
            Dict: 包含分析结果的字典
        """
        try:
            # 分析用户意图
            intent = self._analyze_intent(user_input)
            
            # 执行查询
            result = self.agent_executor.invoke({
                "input": user_input,
                "chat_history": self.memory.chat_memory.messages
            })
            
            # 保存到内存
            self.memory.save_context(
                {"input": user_input},
                {"output": result["output"]}
            )
            
            # 格式化输出
            formatted_result = self._format_result(result, intent)
            
            return {
                "success": True,
                "intent": intent,
                "result": formatted_result,
                "raw_output": result
            }
            
        except Exception as e:
            error_result = self._handle_error(e, user_input)
            return {
                "success": False,
                "error": str(e),
                "result": error_result
            }
    
    def _analyze_intent(self, user_input: str) -> Dict[str, Any]:
        """分析用户意图"""
        intent = {
            "type": "general",
            "protocol": None,
            "device": None,
            "action": None
        }
        
        # 提取设备名称
        device_pattern = r"[rR]-?\d+|[sS][wW]-?\d+|[Rr]outer-?\d+|[Ss]witch-?\d+"
        device_match = re.search(device_pattern, user_input)
        if device_match:
            intent["device"] = device_match.group()
        
        # 检测协议类型
        protocols = {
            "ospf": ["ospf", "开放最短路径优先"],
            "bgp": ["bgp", "边界网关协议"],
            "eigrp": ["eigrp", "增强内部网关路由协议"],
            "interface": ["接口", "interface", "端口"],
            "route": ["路由", "route", "路由表"]
        }
        
        for protocol, keywords in protocols.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                intent["protocol"] = protocol
                intent["type"] = "protocol_query"
                break
        
        # 检测操作类型
        if any(word in user_input for word in ["查看", "显示", "show", "状态", "检查"]):
            intent["action"] = "show"
        elif any(word in user_input for word in ["分析", "诊断", "检测", "问题"]):
            intent["action"] = "analyze"
        
        return intent
    
    def _format_result(self, result: Dict[str, Any], intent: Dict[str, Any]) -> str:
        """格式化结果输出"""
        output = result.get("output", "")
        
        # 根据意图类型进行特殊格式化
        if intent["type"] == "protocol_query" and intent["protocol"]:
            protocol = intent["protocol"]
            device = intent.get("device", "设备")
            
            # 添加协议特定的分析
            if protocol == "ospf":
                output += self._add_ospf_insights(output)
            elif protocol == "bgp":
                output += self._add_bgp_insights(output)
        
        return output
    
    def _add_ospf_insights(self, output: str) -> str:
        """添加OSPF特定见解"""
        insights = "\n\n📊 **OSPF关键指标说明**:\n"
        insights += "- **Router ID**: OSPF路由器的唯一标识\n"
        insights += "- **Area**: OSPF区域，0为骨干区域\n"
        insights += "- **Neighbor状态**: Full表示邻接关系正常\n"
        insights += "- **LSA类型**: Type 1(Router), Type 2(Network), Type 3(Summary)等\n"
        return insights
    
    def _add_bgp_insights(self, output: str) -> str:
        """添加BGP特定见解"""
        insights = "\n\n📊 **BGP关键指标说明**:\n"
        insights += "- **AS号**: 自治系统编号\n"
        insights += "- **Neighbor状态**: Established表示邻居关系正常\n"
        insights += "- **Best Path**: 最优路径选择\n"
        insights += "- **Origin**: 路由来源(IGP/EGP/Incomplete)\n"
        return insights
    
    def _handle_error(self, error: Exception, user_input: str) -> str:
        """处理错误"""
        error_msg = str(error)
        
        if "device" in error_msg.lower() or "找不到" in error_msg:
            return f"❌ 设备查找失败: {error_msg}\n\n建议检查:\n1. 设备名称是否正确\n2. GNS3项目是否已打开\n3. 设备是否已启动"
        elif "command" in error_msg.lower() or "执行" in error_msg:
            return f"❌ 命令执行失败: {error_msg}\n\n建议检查:\n1. 设备是否在线\n2. 命令是否正确\n3. 设备是否支持该命令"
        else:
            return f"❌ 系统错误: {error_msg}\n\n请检查网络连接和GNS3服务状态"
    
    def get_available_devices(self) -> List[str]:
        """获取可用设备列表"""
        try:
            device_finder_tool = self.tools[0]  # DeviceFinderTool
            finder = device_finder_tool.device_finder
            
            devices = []
            for project in finder.project_info:
                for node in project.get('nodes', []):
                    device_name = node.get('name')
                    if device_name:
                        devices.append(device_name)
            return devices
        except:
            return []
    
    def quick_ospf_check(self, device_name: str) -> Dict[str, Any]:
        """快速OSPF状态检查"""
        ospf_query = f"帮我查看{device_name}路由器的OSPF状态，包括邻居关系和数据库信息"
        return self.query(ospf_query)
    
    def quick_bgp_check(self, device_name: str) -> Dict[str, Any]:
        """快速BGP状态检查"""
        bgp_query = f"帮我查看{device_name}路由器的BGP状态，包括邻居关系和路由信息"
        return self.query(bgp_query)
    
    def quick_interface_check(self, device_name: str) -> Dict[str, Any]:
        """快速接口状态检查"""
        interface_query = f"帮我查看{device_name}的接口状态信息"
        return self.query(interface_query)
