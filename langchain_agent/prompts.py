"""
LangChain Agent提示模板
"""

from langchain.prompts import PromptTemplate, ChatPromptTemplate

# 系统提示模板
SYSTEM_PROMPT = """你是一个专业的网络设备运维助手，专门帮助用户分析和查询GNS3网络设备的状态。

你有以下工具可以使用：
1. find_device: 根据设备名称查找设备的project_id和node_id
2. execute_commands: 在指定设备上执行网络命令

你的任务是：
1. 理解用户的查询意图（例如查看OSPF状态、BGP邻居等）
2. 找到目标设备
3. 执行相应的网络命令
4. 分析命令输出并生成易懂的分析报告

重要规则：
- 始终先使用find_device工具查找设备
- 根据用户查询选择合适的网络命令
- 分析命令输出时要关注关键状态信息
- 用中文回复，语言要专业但易懂
- 如果发现问题，要明确指出并给出建议

支持的网络协议查询：OSPF、BGP、EIGRP、接口状态、路由表等。
"""

# OSPF分析专用提示
OSPF_ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["device_name", "command_outputs"],
    template="""
基于以下OSPF命令输出，为设备 {device_name} 生成详细的OSPF状态分析报告：

命令输出：
{command_outputs}

请分析以下方面：
1. **OSPF进程状态**: 是否正常运行，Router ID是什么
2. **邻居关系**: 有哪些OSPF邻居，状态是否正常
3. **LSA数据库**: 数据库是否完整，是否有异常LSA
4. **路由信息**: OSPF学习到的路由数量和主要路由
5. **潜在问题**: 发现的任何异常或需要关注的问题
6. **建议**: 针对发现的问题给出运维建议

请用中文回复，格式要清晰易读。
"""
)

# BGP分析专用提示
BGP_ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["device_name", "command_outputs"],
    template="""
基于以下BGP命令输出，为设备 {device_name} 生成详细的BGP状态分析报告：

命令输出：
{command_outputs}

请分析以下方面：
1. **BGP进程状态**: Router ID和AS号
2. **邻居状态**: BGP邻居关系和状态
3. **路由表**: BGP路由数量和主要路由前缀
4. **路径选择**: 最佳路径选择情况
5. **潜在问题**: 邻居down、路由异常等问题
6. **建议**: 针对发现的问题给出运维建议

请用中文回复，格式要清晰易读。
"""
)

# 通用网络分析提示
GENERAL_NETWORK_ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["device_name", "protocol", "command_outputs"],
    template="""
基于以下{protocol}命令输出，为设备 {device_name} 生成分析报告：

命令输出：
{command_outputs}

请提供：
1. **状态总结**: 当前{protocol}的整体状态
2. **关键信息**: 提取的重要配置和状态信息
3. **异常检测**: 发现的任何异常或警告
4. **运维建议**: 基于当前状态的建议

请用中文回复，格式要清晰易读。
"""
)

# 错误处理提示
ERROR_HANDLING_PROMPT = PromptTemplate(
    input_variables=["error_type", "error_message", "device_name"],
    template="""
在查询设备 {device_name} 时遇到了错误：

错误类型: {error_type}
错误信息: {error_message}

请分析可能的原因：
1. **设备连接问题**: 设备是否在线，网络是否可达
2. **权限问题**: 是否有足够的权限执行命令
3. **命令问题**: 命令是否正确，设备是否支持
4. **配置问题**: 设备配置是否正确

建议的解决方案：
1. 检查设备连接状态
2. 验证设备名称是否正确
3. 确认GNS3项目状态
4. 检查设备是否已启动

请用中文回复。
"""
)

# 设备查找提示
DEVICE_SEARCH_PROMPT = PromptTemplate(
    input_variables=["device_name", "available_devices"],
    template="""
无法找到设备 "{device_name}"。

当前项目中可用的设备有：
{available_devices}

可能的原因：
1. 设备名称拼写错误
2. 设备不在当前打开的项目中
3. 设备尚未创建或已删除

建议：
- 检查设备名称拼写
- 确认设备在GNS3项目中
- 使用上述可用设备名称之一

请用中文回复。
"""
)
