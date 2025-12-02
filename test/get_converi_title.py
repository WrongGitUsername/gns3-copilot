from agent import langgraph_checkpointer

thread_id = "8dde49d7-9b44-405e-9f47-825dc1a5784b"

config = {"configurable": {"thread_id": thread_id}}


# print(langgraph_checkpointer.get(config).get("channel_values").get("conversation_title"))
print(langgraph_checkpointer.get(config))
"""
{
    "v": 4,
    "ts": "2025-12-02T14:07:51.077201+00:00",
    "id": "1f0cf884-9e59-6e19-8001-8c84607229ec",
    "channel_values": {
        "messages": [
            HumanMessage(
                content="hello, what's your name? can you help me ?",
                additional_kwargs={},
                response_metadata={},
            ),
            AIMessage(
                content="Hello! I'm a network automation assistant. I don't have a personal name, but I'm here to help you with network automation tasks. \n\nI can assist you with:\n- Checking network device status (interfaces, OSPF, routing, etc.)\n- Configuring network devices (creating interfaces, configuring routing, etc.)\n- Managing GNS3 topology (creating nodes, connecting devices, etc.)\n- Performing network diagnostics and troubleshooting\n\nWhat would you like me to help you with today? For example, I can:\n1. Check the current GNS3 topology\n2. Execute commands on network devices\n3. Configure network devices\n4. Create or modify GNS3 nodes and links\n5. Troubleshoot network connectivity issues\n\nPlease let me know what specific task you need assistance with!",
                additional_kwargs={},
                response_metadata={
                    "finish_reason": "stop",
                    "model_name": "deepseek-chat",
                    "system_fingerprint": "fp_eaab8d114b_prod0820_fp8_kvcache",
                    "model_provider": "deepseek",
                },
                id="lc_run--219671c9-1a33-49a7-ad78-80f0b603c8c4",
                usage_metadata={
                    "input_tokens": 3504,
                    "output_tokens": 162,
                    "total_tokens": 3666,
                    "input_token_details": {"cache_read": 3456},
                    "output_token_details": {},
                },
            ),
        ],
        "llm_calls": 1,
        "conversation_title": "hello, what's your name? can you help me ?",
    },
    "channel_versions": {
        "__start__": "00000000000000000000000000000002.0.540354711446884",
        "messages": "00000000000000000000000000000003.0.6912742072495311",
        "conversation_title": "00000000000000000000000000000002.0.540354711446884",
        "branch:to:llm_call": "00000000000000000000000000000003.0.6912742072495311",
        "llm_calls": "00000000000000000000000000000003.0.6912742072495311",
    },
    "versions_seen": {
        "__input__": {},
        "__start__": {
            "__start__": "00000000000000000000000000000001.0.3640472566956888"
        },
        "llm_call": {
            "branch:to:llm_call": "00000000000000000000000000000002.0.540354711446884"
        },
    },
    "updated_channels": ["llm_calls", "messages"],
}
"""

"""
{
    "v": 4,
    "ts": "2025-12-02T14:47:47.858404+00:00",
    "id": "1f0cf8dd-e7d6-67de-8004-d1d36b50a42e",
    "channel_values": {
        "messages": [
            HumanMessage(
                content="你能做些什么？", additional_kwargs={}, response_metadata={}
            ),
            AIMessage(
                content="我可以帮助您完成以下网络自动化任务：\n\n## 网络设备管理\n- **状态检查**：查看设备状态（接口、OSPF、路由表、版本信息等）\n- **配置管理**：配置网络设备（创建接口、配置路由协议、设置IP地址等）\n- **故障诊断**：进行网络故障排查和问题分析\n\n## GNS3拓扑管理\n- **拓扑发现**：读取当前GNS3项目的拓扑结构\n- **设备创建**：在GNS3中创建新的网络节点\n- **连接管理**：在设备之间创建网络连接\n- **设备启动**：启动GNS3中的网络设备\n\n## 网络测试与验证\n- **连通性测试**：使用ping、traceroute等命令测试网络连通性\n- **协议验证**：检查OSPF、BGP等路由协议状态\n- **性能监控**：查看接口统计信息和设备性能\n\n## 支持的设备类型\n- **路由器/交换机**：Cisco IOS设备\n- **VPCS设备**：虚拟PC终端\n- **Linux设备**：Linux服务器和主机\n\n## 典型工作流程\n1. **信息收集**：首先了解网络拓扑结构\n2. **状态检查**：查看设备当前配置和状态\n3. **配置修改**：按需进行配置更改\n4. **验证测试**：确认配置生效并测试连通性\n\n## 安全注意事项\n- 我会先查看当前状态再进行配置\n- 避免执行危险操作（如重启、擦除配置等）\n- 配置后会进行验证测试\n\n您有什么具体的网络任务需要帮助吗？比如：\n- 检查某个网络的连通性\n- 配置路由协议\n- 创建GNS3拓扑\n- 诊断网络故障\n- 测试网络性能",
                additional_kwargs={},
                response_metadata={
                    "finish_reason": "stop",
                    "model_name": "deepseek-chat",
                    "system_fingerprint": "fp_eaab8d114b_prod0820_fp8_kvcache",
                    "model_provider": "deepseek",
                },
                id="lc_run--b290bbd3-9b8a-4b48-8458-d85ae60694d4",
                usage_metadata={
                    "input_tokens": 3496,
                    "output_tokens": 378,
                    "total_tokens": 3874,
                    "input_token_details": {"cache_read": 3456},
                    "output_token_details": {},
                },
            ),
            HumanMessage(
                content="看起来不错。你是否足够可以处理一些网络故障，比如协议故障、不同协议兼容故障。",
                additional_kwargs={},
                response_metadata={},
            ),
            AIMessage(
                content="是的，我完全有能力处理各种网络故障，包括协议故障和不同协议兼容性问题。让我详细说明我的故障处理能力：\n\n## 协议故障处理能力\n\n### 1. **路由协议故障**\n- **OSPF故障**：邻居关系建立失败、区域配置错误、网络类型不匹配\n- **BGP故障**：对等体建立失败、路由传播问题、AS路径配置错误\n- **EIGRP故障**：邻居关系、度量计算、路由重分发问题\n- **RIP故障**：版本兼容性、路由更新问题\n\n### 2. **二层协议故障**\n- **STP故障**：根桥选举、端口状态、环路检测\n- **VLAN故障**：VLAN间路由、Trunk配置、VTP同步问题\n- **EtherChannel故障**：捆绑接口、负载均衡、协议协商\n\n### 3. **协议兼容性问题**\n- **IPv4/IPv6双栈**：地址分配、路由协议支持\n- **不同厂商设备互操作**：协议实现差异\n- **协议版本兼容**：OSPFv2/v3、RIPv1/v2、BGP版本\n\n## 故障诊断方法论\n\n### 分层诊断方法：\n1. **物理层**：接口状态、线缆连接、物理错误统计\n2. **数据链路层**：MAC地址学习、VLAN配置、STP状态\n3. **网络层**：IP地址配置、路由表、协议邻居状态\n4. **传输层**：TCP/UDP连接、端口状态\n5. **应用层**：协议特定问题\n\n### 具体诊断流程：\n```\n1. 信息收集 → 2. 拓扑分析 → 3. 基础连通性测试 → \n4. 协议状态检查 → 5. 配置验证 → 6. 问题隔离 → \n7. 解决方案实施 → 8. 验证测试\n```\n\n## 可执行的故障诊断操作\n\n### 1. **信息收集阶段**\n```bash\n# 查看设备基本信息\nshow version\nshow running-config\nshow interfaces status\nshow ip interface brief\n\n# 查看协议状态\nshow ip ospf neighbor\nshow ip bgp summary\nshow ip eigrp neighbors\nshow spanning-tree\n```\n\n### 2. **协议特定诊断**\n```bash\n# OSPF诊断\nshow ip ospf interface\nshow ip ospf database\ndebug ip ospf adjacencies\n\n# BGP诊断\nshow ip bgp neighbors\nshow ip bgp\ndebug ip bgp updates\n\n# VLAN/STP诊断\nshow vlan\nshow spanning-tree detail\nshow interface trunk\n```\n\n### 3. **兼容性检查**\n```bash\n# 协议版本检查\nshow ip protocols\nshow ipv6 protocols\n\n# 接口兼容性\nshow interfaces\nshow controllers\n```\n\n## 实际故障处理案例\n\n### 案例1：OSPF邻居建立失败\n**可能原因**：\n- 接口IP地址不在同一网段\n- OSPF区域配置不一致\n- 网络类型不匹配\n- 认证配置错误\n\n**诊断步骤**：\n1. 检查接口IP地址和掩码\n2. 验证OSPF区域配置\n3. 检查网络类型（广播/点对点）\n4. 查看认证配置\n\n### 案例2：VLAN间路由故障\n**可能原因**：\n- SVI接口未启用\n- VLAN数据库不一致\n- 路由协议未通告\n- ACL阻止流量\n\n**诊断步骤**：\n1. 检查SVI接口状态\n2. 验证VLAN配置\n3. 查看路由表\n4. 检查ACL配置\n\n### 案例3：BGP路由未传播\n**可能原因**：\n- 对等体状态异常\n- 路由策略过滤\n- AS路径限制\n- 下一跳不可达\n\n**诊断步骤**：\n1. 检查BGP对等体状态\n2. 查看路由策略\n3. 验证AS路径配置\n4. 检查下一跳可达性\n\n## 工具支持\n\n我可以使用以下工具进行故障诊断：\n- **`execute_multiple_device_commands`**：同时查看多个设备状态\n- **`gns3_topology_reader`**：分析网络拓扑结构\n- **配置命令工具**：修复配置问题\n- **连通性测试工具**：验证修复效果\n\n## 优势特点\n\n1. **系统性**：遵循标准网络故障诊断流程\n2. **全面性**：覆盖从物理层到应用层的所有问题\n3. **效率性**：可同时检查多个设备状态\n4. **准确性**：基于实际设备输出进行分析\n\n如果您有具体的网络故障需要处理，我可以立即开始诊断。请提供：\n1. 故障现象描述\n2. 网络拓扑信息\n3. 受影响的设备\n4. 故障发生时间\n\n或者，如果您想测试我的能力，我们可以模拟一个故障场景进行诊断练习。",
                additional_kwargs={},
                response_metadata={
                    "finish_reason": "stop",
                    "model_name": "deepseek-chat",
                    "system_fingerprint": "fp_eaab8d114b_prod0820_fp8_kvcache",
                    "model_provider": "deepseek",
                },
                id="lc_run--3815be56-f31e-43e0-9fd8-575cdccc715b",
                usage_metadata={
                    "input_tokens": 3898,
                    "output_tokens": 1053,
                    "total_tokens": 4951,
                    "input_token_details": {"cache_read": 3840},
                    "output_token_details": {},
                },
            ),
        ],
        "llm_calls": 2,
        "conversation_title": "看起来不错。你是否足够可以处理一些网络故障，比如协议故障、不同协议兼容故障。",
    },
    "channel_versions": {
        "__start__": "00000000000000000000000000000005.0.336669370089266",
        "messages": "00000000000000000000000000000006.0.5669162995023462",
        "conversation_title": "00000000000000000000000000000005.0.336669370089266",
        "branch:to:llm_call": "00000000000000000000000000000006.0.5669162995023462",
        "llm_calls": "00000000000000000000000000000006.0.5669162995023462",
    },
    "versions_seen": {
        "__input__": {},
        "__start__": {
            "__start__": "00000000000000000000000000000004.0.8572049663074744"
        },
        "llm_call": {
            "branch:to:llm_call": "00000000000000000000000000000005.0.336669370089266"
        },
    },
    "updated_channels": ["llm_calls", "messages"],
}
"""