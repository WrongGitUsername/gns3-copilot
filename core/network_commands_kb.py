#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络命令知识库
包含常用的网络设备命令和相关信息，用于RAG检索
"""

NETWORK_COMMANDS_KB = {
    # OSPF 相关命令
    "ospf": {
        "commands": [
            {
                "command": "show ip ospf neighbor",
                "description": "显示OSPF邻居信息",
                "purpose": "查看OSPF邻居状态、邻接关系",
                "typical_output": "邻居ID、优先级、状态、死亡时间、地址、接口",
                "platforms": ["cisco", "juniper"],
                "keywords": ["ospf", "邻居", "neighbor"]
            },
            {
                "command": "show ip ospf",
                "description": "显示OSPF进程信息",
                "purpose": "查看OSPF进程状态、路由器ID、区域信息",
                "typical_output": "路由器ID、进程ID、区域列表、LSA统计",
                "platforms": ["cisco"],
                "keywords": ["ospf", "进程", "process"]
            },
            {
                "command": "show ip ospf database",
                "description": "显示OSPF数据库",
                "purpose": "查看OSPF链路状态数据库",
                "typical_output": "LSA类型、链路ID、ADV路由器、年龄、序列号",
                "platforms": ["cisco"],
                "keywords": ["ospf", "数据库", "database", "lsa"]
            },
            {
                "command": "show ip route ospf",
                "description": "显示OSPF学习的路由",
                "purpose": "查看通过OSPF协议学习到的路由信息",
                "typical_output": "OSPF路由条目、下一跳、管理距离、度量值",
                "platforms": ["cisco"],
                "keywords": ["ospf", "路由", "route", "宣告", "advertise", "学习", "learned"]
            }
        ]
    },
    
    # BGP 相关命令
    "bgp": {
        "commands": [
            {
                "command": "show ip bgp summary",
                "description": "显示BGP会话摘要",
                "purpose": "查看BGP邻居状态、前缀计数",
                "typical_output": "邻居地址、版本、AS号、消息数、表版本、状态",
                "platforms": ["cisco", "juniper"],
                "keywords": ["bgp", "邻居", "neighbor", "summary"]
            },
            {
                "command": "show ip bgp neighbors",
                "description": "显示BGP邻居详细信息",
                "purpose": "查看BGP邻居详细状态和统计信息",
                "typical_output": "邻居详细信息、连接状态、消息统计",
                "platforms": ["cisco"],
                "keywords": ["bgp", "邻居", "neighbors", "详细"]
            }
        ]
    },
    
    # 接口相关命令
    "interface": {
        "commands": [
            {
                "command": "show ip interface brief",
                "description": "显示接口简要信息",
                "purpose": "查看接口状态、IP地址配置",
                "typical_output": "接口名、IP地址、OK状态、方法、状态、协议",
                "platforms": ["cisco"],
                "keywords": ["interface", "接口", "ip", "brief", "简要"]
            },
            {
                "command": "show interfaces",
                "description": "显示接口详细信息",
                "purpose": "查看接口详细配置和统计信息",
                "typical_output": "接口详细信息、MTU、带宽、封装、统计",
                "platforms": ["cisco", "juniper"],
                "keywords": ["interface", "接口", "详细", "统计"]
            }
        ]
    },
    
    # 路由相关命令
    "routing": {
        "commands": [
            {
                "command": "show ip route",
                "description": "显示路由表",
                "purpose": "查看IP路由表信息",
                "typical_output": "网络、下一跳、管理距离、度量值、接口",
                "platforms": ["cisco"],
                "keywords": ["route", "路由", "路由表", "routing table"]
            },
            {
                "command": "show ip route summary",
                "description": "显示路由表摘要",
                "purpose": "查看路由表统计信息",
                "typical_output": "路由总数、子网掩码分布、路由源统计",
                "platforms": ["cisco"],
                "keywords": ["route", "路由", "summary", "摘要", "统计"]
            }
        ]
    },
    
    # 系统信息命令
    "system": {
        "commands": [
            {
                "command": "show version",
                "description": "显示系统版本信息",
                "purpose": "查看设备硬件和软件版本信息",
                "typical_output": "软件版本、硬件信息、启动时间、内存信息",
                "platforms": ["cisco", "juniper"],
                "keywords": ["version", "版本", "系统", "software", "hardware"]
            },
            {
                "command": "show running-config",
                "description": "显示运行配置",
                "purpose": "查看当前运行的完整配置",
                "typical_output": "完整的设备配置文件",
                "platforms": ["cisco"],
                "keywords": ["config", "配置", "running", "运行"]
            }
        ]
    },
    
    # VLAN 相关命令
    "vlan": {
        "commands": [
            {
                "command": "show vlan brief",
                "description": "显示VLAN简要信息",
                "purpose": "查看VLAN配置和端口分配",
                "typical_output": "VLAN ID、名称、状态、端口列表",
                "platforms": ["cisco"],
                "keywords": ["vlan", "交换", "switch", "端口"]
            }
        ]
    },
    
    # STP 相关命令
    "stp": {
        "commands": [
            {
                "command": "show spanning-tree",
                "description": "显示生成树信息",
                "purpose": "查看STP状态和端口角色",
                "typical_output": "根桥ID、端口状态、端口角色、路径成本",
                "platforms": ["cisco"],
                "keywords": ["stp", "spanning", "tree", "生成树"]
            }
        ]
    }
}

def get_command_suggestions(query: str, max_results: int = 5) -> list:
    """
    基于查询获取命令建议
    
    Args:
        query: 用户查询字符串
        max_results: 最大返回结果数
    
    Returns:
        匹配的命令列表
    """
    query_lower = query.lower()
    suggestions = []
    
    for category, data in NETWORK_COMMANDS_KB.items():
        for cmd_info in data["commands"]:
            score = 0
            
            # 检查关键词匹配
            for keyword in cmd_info["keywords"]:
                if keyword.lower() in query_lower:
                    score += 2
            
            # 检查描述匹配
            if any(word in cmd_info["description"].lower() for word in query_lower.split()):
                score += 1
            
            # 检查用途匹配
            if any(word in cmd_info["purpose"].lower() for word in query_lower.split()):
                score += 1
            
            if score > 0:
                suggestions.append({
                    "command": cmd_info["command"],
                    "description": cmd_info["description"],
                    "purpose": cmd_info["purpose"],
                    "category": category,
                    "score": score
                })
    
    # 按分数排序并返回前N个结果
    suggestions.sort(key=lambda x: x["score"], reverse=True)
    return suggestions[:max_results]

def get_commands_by_category(category: str) -> list:
    """获取指定类别的所有命令"""
    if category in NETWORK_COMMANDS_KB:
        return NETWORK_COMMANDS_KB[category]["commands"]
    return []

def search_commands_by_keyword(keyword: str) -> list:
    """根据关键词搜索命令"""
    results = []
    keyword_lower = keyword.lower()
    
    for category, data in NETWORK_COMMANDS_KB.items():
        for cmd_info in data["commands"]:
            if (keyword_lower in cmd_info["command"].lower() or
                keyword_lower in cmd_info["description"].lower() or
                keyword_lower in " ".join(cmd_info["keywords"]).lower()):
                
                results.append({
                    "category": category,
                    "command": cmd_info["command"],
                    "description": cmd_info["description"],
                    "purpose": cmd_info["purpose"]
                })
    
    return results
