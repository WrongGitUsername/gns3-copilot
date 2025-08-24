#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Network commands knowledge base.

Contains commonly used network device commands and related information for RAG retrieval.
"""

NETWORK_COMMANDS_KB = {
    # OSPF related commands (OSPFv2)
    "ospf": {
        "commands": [
            {
                "command": "show ip ospf neighbor",
                "description": "Display OSPF neighbor information",
                "purpose": "View OSPF neighbor status and adjacency relationships",
                "typical_output": "Neighbor ID, priority, status, dead time, address, interface",
                "platforms": ["cisco", "juniper"],
                "keywords": ["ospf", "邻居", "neighbor"]
            },
            {
                "command": "show ip ospf",
                "description": "Display OSPF process information",
                "purpose": "View OSPF process status, router ID, area information",
                "typical_output": "Router ID, process ID, area list, LSA statistics",
                "platforms": ["cisco"],
                "keywords": ["ospf", "进程", "process"]
            },
            {
                "command": "show ip ospf database",
                "description": "Display OSPF database",
                "purpose": "View OSPF link state database",
                "typical_output": "LSA type, link ID, ADV router, age, sequence number",
                "platforms": ["cisco"],
                "keywords": ["ospf", "数据库", "database", "lsa"]
            },
            {
                "command": "show ip route ospf",
                "description": "Display OSPF learned routes",
                "purpose": "View route information learned through OSPF protocol",
                "typical_output": "OSPF route entries, next hop, administrative distance, metric",
                "platforms": ["cisco"],
                "keywords": ["ospf", "路由", "route", "宣告", "advertise", "学习", "learned"]
            },
            {
                "command": "show ip ospf interface",
                "description": "显示OSPF接口信息",
                "purpose": "查看OSPF接口配置和状态",
                "typical_output": "接口名、区域、进程ID、路由器ID、网络类型、开销",
                "platforms": ["cisco"],
                "keywords": ["ospf", "接口", "interface", "area", "cost"]
            },
            {
                "command": "show ip ospf border-routers",
                "description": "显示OSPF边界路由器",
                "purpose": "查看ABR和ASBR信息",
                "typical_output": "边界路由器ID、路径开销、区域",
                "platforms": ["cisco"],
                "keywords": ["ospf", "边界", "border", "abr", "asbr"]
            },
            {
                "command": "show ip ospf virtual-links",
                "description": "显示OSPF虚链路",
                "purpose": "查看虚链路状态和配置",
                "typical_output": "虚链路ID、邻居、过境区域、状态",
                "platforms": ["cisco"],
                "keywords": ["ospf", "虚链路", "virtual", "link"]
            },
            {
                "command": "debug ip ospf adj",
                "description": "调试OSPF邻接关系",
                "purpose": "实时查看OSPF邻接关系建立过程",
                "typical_output": "邻接状态变化、Hello包、DBD交换",
                "platforms": ["cisco"],
                "keywords": ["ospf", "debug", "调试", "邻接", "adjacency"]
            }
        ]
    },

    # OSPFv3 (IPv6) related commands
    "ospfv3": {
        "commands": [
            {
                "command": "show ipv6 ospf neighbor",
                "description": "显示OSPFv3邻居信息",
                "purpose": "查看IPv6 OSPF邻居状态和邻接关系",
                "typical_output": "邻居ID、优先级、状态、死亡时间、接口ID",
                "platforms": ["cisco"],
                "keywords": ["ospfv3", "ipv6", "邻居", "neighbor"]
            },
            {
                "command": "show ipv6 ospf",
                "description": "显示OSPFv3进程信息",
                "purpose": "查看IPv6 OSPF进程状态和路由器ID",
                "typical_output": "路由器ID、进程ID、区域列表、LSA统计",
                "platforms": ["cisco"],
                "keywords": ["ospfv3", "ipv6", "进程", "process"]
            },
            {
                "command": "show ipv6 ospf database",
                "description": "显示OSPFv3数据库",
                "purpose": "查看IPv6 OSPF链路状态数据库",
                "typical_output": "LSA类型、链路ID、通告路由器、老化时间",
                "platforms": ["cisco"],
                "keywords": ["ospfv3", "ipv6", "数据库", "database", "lsa"]
            },
            {
                "command": "show ipv6 route ospf",
                "description": "显示OSPFv3学习的路由",
                "purpose": "查看通过IPv6 OSPF协议学习的路由信息",
                "typical_output": "IPv6路由条目、下一跳、管理距离、度量值",
                "platforms": ["cisco"],
                "keywords": ["ospfv3", "ipv6", "路由", "route"]
            },
            {
                "command": "show ipv6 ospf interface",
                "description": "显示OSPFv3接口信息",
                "purpose": "查看IPv6 OSPF接口配置和状态",
                "typical_output": "接口ID、区域、进程ID、网络类型、开销",
                "platforms": ["cisco"],
                "keywords": ["ospfv3", "ipv6", "接口", "interface"]
            }
        ]
    },
    
    # BGP related commands
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
            },
            {
                "command": "show ip bgp",
                "description": "显示BGP路由表",
                "purpose": "查看BGP路由表信息",
                "typical_output": "网络、下一跳、度量值、本地优先级、权重、路径",
                "platforms": ["cisco"],
                "keywords": ["bgp", "路由", "table", "表"]
            },
            {
                "command": "show ip bgp regexp",
                "description": "根据正则表达式显示BGP路由",
                "purpose": "使用正则表达式过滤BGP路由",
                "typical_output": "匹配AS路径的BGP路由",
                "platforms": ["cisco"],
                "keywords": ["bgp", "regexp", "正则", "as-path", "过滤"]
            },
            {
                "command": "show ip bgp community",
                "description": "显示BGP团体属性",
                "purpose": "查看具有特定团体属性的BGP路由",
                "typical_output": "带有指定团体属性的BGP路由",
                "platforms": ["cisco"],
                "keywords": ["bgp", "community", "团体", "属性"]
            },
            {
                "command": "show ip bgp dampening",
                "description": "显示BGP路由抑制",
                "purpose": "查看BGP路由抑制信息",
                "typical_output": "被抑制的路由、惩罚值、剩余时间",
                "platforms": ["cisco"],
                "keywords": ["bgp", "dampening", "抑制", "flap"]
            },
            {
                "command": "show ip bgp flap-statistics",
                "description": "显示BGP震荡统计",
                "purpose": "查看BGP路由震荡统计信息",
                "typical_output": "网络、震荡次数、持续时间",
                "platforms": ["cisco"],
                "keywords": ["bgp", "flap", "震荡", "统计"]
            },
            {
                "command": "show ip bgp peer-group",
                "description": "显示BGP对等体组",
                "purpose": "查看BGP对等体组配置",
                "typical_output": "对等体组名称、成员、配置",
                "platforms": ["cisco"],
                "keywords": ["bgp", "peer", "group", "对等体", "组"]
            },
            {
                "command": "show ipv6 bgp summary",
                "description": "显示IPv6 BGP摘要",
                "purpose": "查看IPv6 BGP邻居状态",
                "typical_output": "IPv6邻居、AS号、状态、前缀数",
                "platforms": ["cisco"],
                "keywords": ["bgp", "ipv6", "summary", "摘要"]
            },
            {
                "command": "clear ip bgp",
                "description": "重置BGP会话",
                "purpose": "软重置或硬重置BGP会话",
                "typical_output": "BGP会话重置确认",
                "platforms": ["cisco"],
                "keywords": ["bgp", "clear", "重置", "reset"]
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
            },
            {
                "command": "show interfaces status",
                "description": "显示接口状态",
                "purpose": "查看接口端口状态、VLAN、双工模式、速度",
                "typical_output": "端口名称、状态、VLAN、双工、速度、类型",
                "platforms": ["cisco"],
                "keywords": ["interface", "接口", "状态", "status", "port"]
            },
            {
                "command": "show interfaces trunk",
                "description": "显示中继接口信息",
                "purpose": "查看中继端口配置和VLAN信息",
                "typical_output": "端口、模式、封装、状态、原生VLAN、允许VLAN",
                "platforms": ["cisco"],
                "keywords": ["interface", "接口", "trunk", "中继", "vlan"]
            },
            {
                "command": "show interfaces counters",
                "description": "显示接口计数器",
                "purpose": "查看接口流量统计和错误计数",
                "typical_output": "端口、输入/输出包数、字节数、错误数",
                "platforms": ["cisco"],
                "keywords": ["interface", "接口", "counters", "计数器", "统计"]
            },
            {
                "command": "show interfaces description",
                "description": "显示接口描述",
                "purpose": "查看接口描述信息和状态",
                "typical_output": "接口名称、状态、协议、描述",
                "platforms": ["cisco"],
                "keywords": ["interface", "接口", "description", "描述"]
            },
            {
                "command": "show interfaces switchport",
                "description": "显示交换端口信息",
                "purpose": "查看交换端口模式和VLAN配置",
                "typical_output": "管理VLAN、操作模式、接入VLAN、中继VLAN",
                "platforms": ["cisco"],
                "keywords": ["interface", "接口", "switchport", "交换", "vlan"]
            },
            {
                "command": "show ip interface",
                "description": "显示IP接口详细信息",
                "purpose": "查看接口IP配置、访问列表、帮助器地址",
                "typical_output": "IP地址、子网掩码、访问组、代理ARP状态",
                "platforms": ["cisco"],
                "keywords": ["interface", "接口", "ip", "详细", "acl"]
            },
            {
                "command": "show ipv6 interface",
                "description": "显示IPv6接口信息",
                "purpose": "查看接口IPv6配置和地址",
                "typical_output": "IPv6地址、链路本地地址、ND状态、MTU",
                "platforms": ["cisco"],
                "keywords": ["interface", "接口", "ipv6", "地址"]
            },
            {
                "command": "show interfaces summary",
                "description": "显示接口摘要统计",
                "purpose": "查看接口数量和类型统计",
                "typical_output": "接口总数、管理状态、协议状态统计",
                "platforms": ["cisco"],
                "keywords": ["interface", "接口", "summary", "摘要", "统计"]
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
            },
            {
                "command": "show ip route connected",
                "description": "显示直连路由",
                "purpose": "查看直接连接的网络路由",
                "typical_output": "直连网络、接口、管理距离",
                "platforms": ["cisco"],
                "keywords": ["route", "路由", "connected", "直连"]
            },
            {
                "command": "show ip route static",
                "description": "显示静态路由",
                "purpose": "查看手动配置的静态路由",
                "typical_output": "静态路由网络、下一跳、管理距离",
                "platforms": ["cisco"],
                "keywords": ["route", "路由", "static", "静态"]
            },
            {
                "command": "show ipv6 route",
                "description": "显示IPv6路由表",
                "purpose": "查看IPv6路由表信息",
                "typical_output": "IPv6网络、下一跳、管理距离、度量值",
                "platforms": ["cisco"],
                "keywords": ["route", "路由", "ipv6", "routing table"]
            },
            {
                "command": "show ipv6 route summary",
                "description": "显示IPv6路由摘要",
                "purpose": "查看IPv6路由表统计信息",
                "typical_output": "IPv6路由总数、路由源统计",
                "platforms": ["cisco"],
                "keywords": ["route", "路由", "ipv6", "summary", "摘要"]
            },
            {
                "command": "show ip protocols",
                "description": "显示IP路由协议",
                "purpose": "查看启用的路由协议和配置",
                "typical_output": "路由协议、网络、管理距离、定时器",
                "platforms": ["cisco"],
                "keywords": ["route", "路由", "protocols", "协议"]
            },
            {
                "command": "show ip route longer-prefixes",
                "description": "显示更长前缀路由",
                "purpose": "查看指定网络的更具体路由",
                "typical_output": "匹配网络的更长前缀路由条目",
                "platforms": ["cisco"],
                "keywords": ["route", "路由", "prefix", "前缀"]
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
            },
            {
                "command": "show startup-config",
                "description": "显示启动配置",
                "purpose": "查看保存在NVRAM中的启动配置",
                "typical_output": "保存的启动配置文件",
                "platforms": ["cisco"],
                "keywords": ["config", "配置", "startup", "启动", "nvram"]
            },
            {
                "command": "show tech-support",
                "description": "显示技术支持信息",
                "purpose": "收集完整的系统信息用于故障排除",
                "typical_output": "版本、配置、日志、接口状态等综合信息",
                "platforms": ["cisco"],
                "keywords": ["tech", "support", "技术", "支持", "故障"]
            },
            {
                "command": "show inventory",
                "description": "显示硬件清单",
                "purpose": "查看设备硬件组件和序列号",
                "typical_output": "硬件名称、产品ID、版本ID、序列号",
                "platforms": ["cisco"],
                "keywords": ["inventory", "硬件", "清单", "serial", "序列号"]
            },
            {
                "command": "show environment",
                "description": "显示环境状态",
                "purpose": "查看设备温度、电源、风扇状态",
                "typical_output": "温度传感器、电源状态、风扇状态",
                "platforms": ["cisco"],
                "keywords": ["environment", "环境", "温度", "电源", "风扇"]
            },
            {
                "command": "show memory",
                "description": "显示内存使用情况",
                "purpose": "查看系统内存使用统计",
                "typical_output": "总内存、已用内存、空闲内存、内存池",
                "platforms": ["cisco"],
                "keywords": ["memory", "内存", "使用", "统计"]
            },
            {
                "command": "show processes",
                "description": "显示系统进程",
                "purpose": "查看系统运行的进程和CPU使用率",
                "typical_output": "进程ID、CPU使用率、内存使用、进程名",
                "platforms": ["cisco"],
                "keywords": ["processes", "进程", "cpu", "usage"]
            },
            {
                "command": "show processes cpu",
                "description": "显示CPU使用情况",
                "purpose": "查看CPU使用率和进程统计",
                "typical_output": "CPU使用率、中断、进程CPU使用排名",
                "platforms": ["cisco"],
                "keywords": ["processes", "cpu", "使用率", "统计"]
            },
            {
                "command": "show clock",
                "description": "显示系统时间",
                "purpose": "查看当前系统时间和日期",
                "typical_output": "当前时间、日期、时区",
                "platforms": ["cisco"],
                "keywords": ["clock", "时间", "日期", "time"]
            },
            {
                "command": "show users",
                "description": "显示已登录用户",
                "purpose": "查看当前登录的用户会话",
                "typical_output": "用户名、线路、登录时间、空闲时间",
                "platforms": ["cisco"],
                "keywords": ["users", "用户", "登录", "会话"]
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
            },
            {
                "command": "show vlan",
                "description": "显示VLAN详细信息",
                "purpose": "查看VLAN详细配置信息",
                "typical_output": "VLAN ID、名称、状态、类型、MTU、端口列表",
                "platforms": ["cisco"],
                "keywords": ["vlan", "详细", "配置", "信息"]
            },
            {
                "command": "show vlan id",
                "description": "显示指定VLAN信息",
                "purpose": "查看特定VLAN的详细信息",
                "typical_output": "指定VLAN的配置和端口信息",
                "platforms": ["cisco"],
                "keywords": ["vlan", "id", "指定", "特定"]
            },
            {
                "command": "show vlan name",
                "description": "显示指定名称的VLAN",
                "purpose": "根据VLAN名称查看信息",
                "typical_output": "指定名称VLAN的详细信息",
                "platforms": ["cisco"],
                "keywords": ["vlan", "name", "名称", "指定"]
            },
            {
                "command": "show vlan summary",
                "description": "显示VLAN摘要统计",
                "purpose": "查看VLAN数量和类型统计",
                "typical_output": "VLAN总数、活跃数、暂停数",
                "platforms": ["cisco"],
                "keywords": ["vlan", "summary", "摘要", "统计"]
            },
            {
                "command": "show vtp status",
                "description": "显示VTP状态",
                "purpose": "查看VLAN中继协议状态",
                "typical_output": "VTP版本、模式、域名、修订号",
                "platforms": ["cisco"],
                "keywords": ["vtp", "status", "状态", "中继", "协议"]
            },
            {
                "command": "show vtp password",
                "description": "显示VTP密码配置",
                "purpose": "查看VTP域密码设置",
                "typical_output": "VTP密码配置状态",
                "platforms": ["cisco"],
                "keywords": ["vtp", "password", "密码", "域"]
            },
            {
                "command": "show interfaces vlan",
                "description": "显示VLAN接口信息",
                "purpose": "查看VLAN接口配置和状态",
                "typical_output": "VLAN接口IP、状态、协议",
                "platforms": ["cisco"],
                "keywords": ["vlan", "interface", "接口", "配置"]
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
    },
    
    # ARP 相关命令
    "arp": {
        "commands": [
            {
                "command": "show arp",
                "description": "显示ARP表",
                "purpose": "查看IP到MAC地址的映射关系",
                "typical_output": "协议、地址、年龄、硬件地址、类型、接口",
                "platforms": ["cisco"],
                "keywords": ["arp", "地址解析", "mac", "ip", "映射"]
            },
            {
                "command": "show ip arp",
                "description": "显示IP ARP表",
                "purpose": "查看IP ARP缓存表",
                "typical_output": "协议、地址、年龄、硬件地址、类型、接口",
                "platforms": ["cisco"],
                "keywords": ["arp", "ip", "地址解析", "缓存"]
            },
            {
                "command": "show arp statistics",
                "description": "显示ARP统计信息",
                "purpose": "查看ARP请求、回复、超时等统计",
                "typical_output": "ARP请求数、回复数、失败数、超时数",
                "platforms": ["cisco"],
                "keywords": ["arp", "统计", "statistics", "请求", "回复"]
            },
            {
                "command": "clear arp",
                "description": "清除ARP表",
                "purpose": "清除ARP缓存表条目",
                "typical_output": "命令执行结果",
                "platforms": ["cisco"],
                "keywords": ["arp", "清除", "clear", "缓存"]
            }
        ]
    },
    
    # MAC 地址表相关命令
    "mac": {
        "commands": [
            {
                "command": "show mac address-table",
                "description": "显示MAC地址表",
                "purpose": "查看交换机的MAC地址表",
                "typical_output": "VLAN、MAC地址、类型、端口",
                "platforms": ["cisco"],
                "keywords": ["mac", "地址表", "address", "table", "交换"]
            },
            {
                "command": "show mac address-table dynamic",
                "description": "显示动态MAC地址表",
                "purpose": "查看动态学习的MAC地址",
                "typical_output": "VLAN、MAC地址、端口、老化时间",
                "platforms": ["cisco"],
                "keywords": ["mac", "dynamic", "动态", "学习"]
            },
            {
                "command": "show mac address-table static",
                "description": "显示静态MAC地址表",
                "purpose": "查看静态配置的MAC地址",
                "typical_output": "VLAN、MAC地址、端口、类型",
                "platforms": ["cisco"],
                "keywords": ["mac", "static", "静态", "配置"]
            },
            {
                "command": "show mac address-table aging-time",
                "description": "显示MAC地址老化时间",
                "purpose": "查看MAC地址表老化时间配置",
                "typical_output": "全局老化时间、VLAN老化时间",
                "platforms": ["cisco"],
                "keywords": ["mac", "aging", "老化", "时间"]
            },
            {
                "command": "show mac address-table count",
                "description": "显示MAC地址表计数",
                "purpose": "查看MAC地址表条目数量统计",
                "typical_output": "动态条目数、静态条目数、总数",
                "platforms": ["cisco"],
                "keywords": ["mac", "count", "计数", "统计", "数量"]
            },
            {
                "command": "clear mac address-table dynamic",
                "description": "清除动态MAC地址表",
                "purpose": "清除动态学习的MAC地址条目",
                "typical_output": "命令执行结果",
                "platforms": ["cisco"],
                "keywords": ["mac", "clear", "清除", "dynamic", "动态"]
            }
        ]
    },
    
    # IPv6 相关命令
    "ipv6": {
        "commands": [
            {
                "command": "show ipv6 interface brief",
                "description": "显示IPv6接口简要信息",
                "purpose": "查看IPv6接口状态和地址",
                "typical_output": "接口、IPv6地址、状态、协议",
                "platforms": ["cisco"],
                "keywords": ["ipv6", "interface", "接口", "地址", "brief"]
            },
            {
                "command": "show ipv6 neighbors",
                "description": "显示IPv6邻居发现表",
                "purpose": "查看IPv6邻居发现缓存",
                "typical_output": "IPv6地址、年龄、链路层地址、状态、接口",
                "platforms": ["cisco"],
                "keywords": ["ipv6", "neighbors", "邻居", "发现", "nd"]
            },
            {
                "command": "show ipv6 route summary",
                "description": "显示IPv6路由摘要",
                "purpose": "查看IPv6路由表统计信息",
                "typical_output": "路由总数、路由源统计、内存使用",
                "platforms": ["cisco"],
                "keywords": ["ipv6", "route", "路由", "summary", "摘要"]
            },
            {
                "command": "show ipv6 protocols",
                "description": "显示IPv6路由协议",
                "purpose": "查看启用的IPv6路由协议",
                "typical_output": "路由协议、接口、管理距离",
                "platforms": ["cisco"],
                "keywords": ["ipv6", "protocols", "协议", "路由"]
            },
            {
                "command": "show ipv6 access-list",
                "description": "显示IPv6访问控制列表",
                "purpose": "查看IPv6 ACL配置",
                "typical_output": "ACL名称、序列号、规则、匹配统计",
                "platforms": ["cisco"],
                "keywords": ["ipv6", "access", "list", "acl", "访问控制"]
            },
            {
                "command": "show ipv6 traffic",
                "description": "显示IPv6流量统计",
                "purpose": "查看IPv6协议流量统计信息",
                "typical_output": "接收包数、发送包数、错误数、丢弃数",
                "platforms": ["cisco"],
                "keywords": ["ipv6", "traffic", "流量", "统计", "packets"]
            },
            {
                "command": "ping ipv6",
                "description": "IPv6 ping测试",
                "purpose": "测试IPv6网络连通性",
                "typical_output": "ping统计、往返时间、丢包率",
                "platforms": ["cisco"],
                "keywords": ["ipv6", "ping", "测试", "连通性"]
            },
            {
                "command": "traceroute ipv6",
                "description": "IPv6路由跟踪",
                "purpose": "跟踪到IPv6目标的路径",
                "typical_output": "跳数、IPv6地址、往返时间",
                "platforms": ["cisco"],
                "keywords": ["ipv6", "traceroute", "路由", "跟踪", "路径"]
            }
        ]
    },
    
    # 配置管理命令
    "config": {
        "commands": [
            {
                "command": "show running-config interface",
                "description": "显示接口运行配置",
                "purpose": "查看指定接口的配置",
                "typical_output": "接口配置命令和参数",
                "platforms": ["cisco"],
                "keywords": ["config", "配置", "interface", "接口", "running"]
            },
            {
                "command": "show startup-config",
                "description": "显示启动配置",
                "purpose": "查看保存的启动配置",
                "typical_output": "完整的启动配置文件",
                "platforms": ["cisco"],
                "keywords": ["config", "配置", "startup", "启动"]
            },
            {
                "command": "show running-config | section",
                "description": "显示配置片段",
                "purpose": "显示配置文件的特定部分",
                "typical_output": "匹配的配置部分",
                "platforms": ["cisco"],
                "keywords": ["config", "配置", "section", "片段", "部分"]
            },
            {
                "command": "show running-config | include",
                "description": "显示包含关键字的配置行",
                "purpose": "过滤显示包含特定关键字的配置",
                "typical_output": "包含关键字的配置行",
                "platforms": ["cisco"],
                "keywords": ["config", "配置", "include", "包含", "过滤"]
            },
            {
                "command": "show running-config | exclude",
                "description": "显示排除关键字的配置行",
                "purpose": "过滤显示不包含特定关键字的配置",
                "typical_output": "不包含关键字的配置行",
                "platforms": ["cisco"],
                "keywords": ["config", "配置", "exclude", "排除", "过滤"]
            },
            {
                "command": "show running-config | begin",
                "description": "从指定行开始显示配置",
                "purpose": "从匹配的行开始显示配置",
                "typical_output": "从匹配行开始的配置内容",
                "platforms": ["cisco"],
                "keywords": ["config", "配置", "begin", "开始", "匹配"]
            },
            {
                "command": "show archive",
                "description": "显示配置存档",
                "purpose": "查看配置文件的存档历史",
                "typical_output": "存档文件列表、时间戳、大小",
                "platforms": ["cisco"],
                "keywords": ["config", "配置", "archive", "存档", "历史"]
            },
            {
                "command": "show configuration sessions",
                "description": "显示配置会话",
                "purpose": "查看当前的配置会话",
                "typical_output": "会话ID、用户、状态、时间",
                "platforms": ["cisco"],
                "keywords": ["config", "配置", "sessions", "会话"]
            }
        ]
    },
    
    # 日志和监控命令
    "logging": {
        "commands": [
            {
                "command": "show logging",
                "description": "显示系统日志",
                "purpose": "查看系统日志信息",
                "typical_output": "日志级别、日志消息、时间戳",
                "platforms": ["cisco"],
                "keywords": ["logging", "日志", "系统", "消息"]
            },
            {
                "command": "show logging summary",
                "description": "显示日志摘要",
                "purpose": "查看日志统计信息",
                "typical_output": "日志级别统计、消息数量",
                "platforms": ["cisco"],
                "keywords": ["logging", "日志", "summary", "摘要", "统计"]
            },
            {
                "command": "show snmp",
                "description": "显示SNMP信息",
                "purpose": "查看SNMP配置和统计",
                "typical_output": "SNMP版本、团体字符串、统计信息",
                "platforms": ["cisco"],
                "keywords": ["snmp", "监控", "管理", "统计"]
            },
            {
                "command": "show snmp community",
                "description": "显示SNMP团体字符串",
                "purpose": "查看SNMP团体字符串配置",
                "typical_output": "团体字符串、访问权限、ACL",
                "platforms": ["cisco"],
                "keywords": ["snmp", "community", "团体", "字符串"]
            },
            {
                "command": "debug all",
                "description": "启用所有调试",
                "purpose": "启用所有调试输出(谨慎使用)",
                "typical_output": "调试状态确认",
                "platforms": ["cisco"],
                "keywords": ["debug", "调试", "all", "所有"]
            },
            {
                "command": "undebug all",
                "description": "关闭所有调试",
                "purpose": "关闭所有调试输出",
                "typical_output": "调试状态确认",
                "platforms": ["cisco"],
                "keywords": ["debug", "调试", "undebug", "关闭"]
            },
            {
                "command": "show debugging",
                "description": "显示调试状态",
                "purpose": "查看当前启用的调试选项",
                "typical_output": "启用的调试选项列表",
                "platforms": ["cisco"],
                "keywords": ["debug", "调试", "状态", "启用"]
            }
        ]
    },
    
    # 网络诊断命令
    "diagnostics": {
        "commands": [
            {
                "command": "ping",
                "description": "网络连通性测试",
                "purpose": "测试到目标主机的网络连通性",
                "typical_output": "ping统计、往返时间、成功率",
                "platforms": ["cisco"],
                "keywords": ["ping", "测试", "连通性", "网络"]
            },
            {
                "command": "traceroute",
                "description": "路由跟踪",
                "purpose": "跟踪数据包到目标的路径",
                "typical_output": "跳数、IP地址、往返时间",
                "platforms": ["cisco"],
                "keywords": ["traceroute", "路由", "跟踪", "路径"]
            },
            {
                "command": "telnet",
                "description": "Telnet连接测试",
                "purpose": "测试到远程主机的telnet连接",
                "typical_output": "连接状态、远程主机响应",
                "platforms": ["cisco"],
                "keywords": ["telnet", "连接", "测试", "远程"]
            },
            {
                "command": "show cdp neighbors",
                "description": "显示CDP邻居",
                "purpose": "查看通过CDP发现的邻居设备",
                "typical_output": "设备ID、本地接口、保持时间、能力、平台、端口ID",
                "platforms": ["cisco"],
                "keywords": ["cdp", "neighbors", "邻居", "发现"]
            },
            {
                "command": "show cdp neighbors detail",
                "description": "显示CDP邻居详细信息",
                "purpose": "查看CDP邻居的详细信息",
                "typical_output": "设备详细信息、IP地址、软件版本、VTP域",
                "platforms": ["cisco"],
                "keywords": ["cdp", "neighbors", "detail", "邻居", "详细"]
            },
            {
                "command": "show lldp neighbors",
                "description": "显示LLDP邻居",
                "purpose": "查看通过LLDP发现的邻居设备",
                "typical_output": "设备ID、本地接口、保持时间、系统名称",
                "platforms": ["cisco"],
                "keywords": ["lldp", "neighbors", "邻居", "发现"]
            },
            {
                "command": "show ip nbar protocol-discovery",
                "description": "显示NBAR协议发现",
                "purpose": "查看网络流量的协议分布",
                "typical_output": "协议、输入包/字节、输出包/字节",
                "platforms": ["cisco"],
                "keywords": ["nbar", "protocol", "协议", "发现", "流量"]
            }
        ]
    },
    
    # 安全相关命令
    "security": {
        "commands": [
            {
                "command": "show access-lists",
                "description": "显示访问控制列表",
                "purpose": "查看ACL配置和匹配统计",
                "typical_output": "ACL编号/名称、规则、匹配次数",
                "platforms": ["cisco"],
                "keywords": ["access", "list", "acl", "访问控制", "安全"]
            },
            {
                "command": "show ip access-lists",
                "description": "显示IP访问控制列表",
                "purpose": "查看IP ACL配置",
                "typical_output": "标准/扩展ACL、规则、匹配统计",
                "platforms": ["cisco"],
                "keywords": ["access", "list", "ip", "acl", "访问控制"]
            },
            {
                "command": "show crypto isakmp sa",
                "description": "显示ISAKMP安全关联",
                "purpose": "查看IKE阶段1的安全关联",
                "typical_output": "目标、源、状态、加密、哈希、认证、生命周期",
                "platforms": ["cisco"],
                "keywords": ["crypto", "isakmp", "ike", "vpn", "安全"]
            },
            {
                "command": "show crypto ipsec sa",
                "description": "显示IPSec安全关联",
                "purpose": "查看IKE阶段2的安全关联",
                "typical_output": "接口、流、源/目标、协议、加密包数",
                "platforms": ["cisco"],
                "keywords": ["crypto", "ipsec", "vpn", "安全", "加密"]
            },
            {
                "command": "show crypto map",
                "description": "显示加密映射",
                "purpose": "查看crypto map配置",
                "typical_output": "crypto map名称、序列号、ACL、对等体",
                "platforms": ["cisco"],
                "keywords": ["crypto", "map", "加密", "映射", "vpn"]
            },
            {
                "command": "show port-security",
                "description": "显示端口安全",
                "purpose": "查看端口安全配置和状态",
                "typical_output": "端口、状态、最大MAC数、当前MAC数、违规动作",
                "platforms": ["cisco"],
                "keywords": ["port", "security", "端口", "安全", "mac"]
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
