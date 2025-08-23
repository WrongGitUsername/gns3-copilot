#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GNS3设备配置信息批量获取工具
功能：获取拓扑信息后，批量登录各设备获取配置信息
整合三个模块：get_topology_info, get_config_info, get_project_info
支持多语言适配
"""

import os
import time
from datetime import datetime
from dotenv import load_dotenv
from .language_adapter import get_message, format_device_info, format_skip_reason

# 导入自定义模块
try:
    # 当作为模块导入时使用相对导入
    from .get_topology_info import TopologyManager
    from .get_config_info import DeviceConfigManager
    from .get_project_info import ProjectInfoManager
except ImportError:
    # 当直接运行时使用绝对导入
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from core.get_topology_info import TopologyManager
    from core.get_config_info import DeviceConfigManager
    from core.get_project_info import ProjectInfoManager

# 加载环境变量
load_dotenv()

class DeviceConfigCollector:
    def __init__(self, server_url=None, telnet_host=None):
        """
        初始化配置收集器
        
        Args:
            server_url: GNS3服务器地址，如果不指定则从环境变量获取
            telnet_host: Telnet连接的主机地址，如果不指定则从环境变量获取
        """
        self.server_url = server_url or os.getenv("GNS3_SERVER_URL", "http://192.168.101.1:3080")
        self.telnet_host = telnet_host or os.getenv("TELNET_HOST", "192.168.102.1")
        
        # 初始化各个管理器
        self.topology_manager = TopologyManager(self.server_url)
        self.config_manager = DeviceConfigManager(self.telnet_host)
        self.project_manager = ProjectInfoManager(self.server_url)
        
        # 创建配置文件保存目录
        self.config_dir = "/home/yueguobin/myCode/GNS3/tools/device_configs"
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
    
    def get_topology_info(self):
        """
        获取拓扑信息和链路摘要
        使用 topology_manager 模块
        
        Returns:
            tuple: (opened_projects, topology_data)
        """
        try:
            print("使用拓扑管理器获取拓扑信息...")
            opened_projects = self.topology_manager.get_opened_projects()
            topology_data = self.topology_manager.get_all_topology_info()
            return opened_projects, topology_data
        except Exception as e:
            print(f"获取拓扑信息时发生错误: {e}")
            return [], {}
    
    def get_project_details(self):
        """
        获取项目详细信息
        使用 project_manager 模块
        
        Returns:
            dict: 项目详细信息
        """
        try:
            print("使用项目管理器获取项目详细信息...")
            return self.project_manager.get_all_opened_projects_info()
        except Exception as e:
            print(f"获取项目详细信息时发生错误: {e}")
            return {}
    
    def get_device_config(self, device_name, console_port):
        """
        获取单个设备配置信息
        使用 config_manager 模块
        
        Args:
            device_name: 设备名称
            console_port: 控制台端口
            
        Returns:
            str: 设备配置信息
        """
        try:
            return self.config_manager.get_device_config(device_name, console_port)
        except Exception as e:
            print(f"获取设备 {device_name} 配置时发生错误: {e}")
            return ""
    
    def get_multiple_devices_config(self, devices_info):
        """
        批量获取多个设备配置信息
        使用 config_manager 模块
        
        Args:
            devices_info: 设备信息列表
            
        Returns:
            dict: 设备配置信息字典
        """
        try:
            return self.config_manager.get_multiple_devices_config(devices_info)
        except Exception as e:
            print(f"批量获取设备配置时发生错误: {e}")
            return {}
    
    def filter_configurable_devices(self, nodes):
        """
        过滤出可配置的设备
        
        Args:
            nodes: 节点列表
            
        Returns:
            list: 过滤后的可配置设备列表
        """
        # 可配置的设备类型
        configurable_types = [
            'dynamips',  # Cisco路由器
            'qemu',      # QEMU虚拟机 (包括路由器、交换机)
            'vpcs',      # 虚拟PC
            'iou',       # IOU设备
            'docker',    # Docker容器
        ]
        
        # 不可配置的设备类型
        non_configurable_types = [
            'ethernet_switch',  # 以太网交换机 (内置)
            'ethernet_hub',     # 以太网集线器
            'frame_relay_switch',  # 帧中继交换机
            'atm_switch',       # ATM交换机
            'cloud',            # 云连接
            'nat',              # NAT节点
            'builtin',          # 内置设备
        ]
        
        configurable_devices = []
        skipped_devices = []
        
        for node in nodes:
            device_name = node.get('name', 'Unknown')
            # 兼容两种字段名：node_type 和 type
            device_type = node.get('node_type') or node.get('type', 'unknown')
            device_status = node.get('status', 'unknown')
            console_port = node.get('console', None)
            
            # 检查设备类型
            if device_type in non_configurable_types:
                skipped_devices.append({
                    'name': device_name,
                    'reason': get_message("device_type_not_supported").format(device_type)
                })
                continue
            
            # 检查设备状态
            if device_status != 'started':
                skipped_devices.append({
                    'name': device_name,
                    'reason': get_message("device_not_running").format(device_status)
                })
                continue
            
            # 检查控制台端口
            if console_port is None:
                skipped_devices.append({
                    'name': device_name,
                    'reason': '无控制台端口'
                })
                continue
            
            # 设备类型检查 - 只有在已知可配置类型列表中的才处理
            if device_type in configurable_types:
                configurable_devices.append(node)
            else:
                # 对于未知类型，如果有控制台端口且状态是started，也尝试获取配置
                print(f"⚠️ 未知设备类型 {device_type} ({device_name})，将尝试获取配置")
                configurable_devices.append(node)
        
        # 打印过滤结果
        print(f"\n{get_message('device_filter_results')}")
        print(get_message("configurable_devices", len(configurable_devices)))
        print(get_message("skipped_devices", len(skipped_devices)))
        
        if configurable_devices:
            print(f"\n{get_message('configurable_device_list')}")
            for device in configurable_devices:
                device_type_display = device.get('node_type') or device.get('type', 'unknown')
                print(format_device_info(device['name'], device_type_display, device['console']))
        
        if skipped_devices:
            print(f"\n{get_message('skipped_device_list')}")
            for device in skipped_devices:
                print(format_skip_reason(device['name'], device['reason']))
        
        return configurable_devices

    def save_config_to_file(self, device_name, config_content, project_name):
        """
        保存配置到文件
        
        Args:
            device_name: 设备名称
            config_content: 配置内容
            project_name: 项目名称
        """
        try:
            # 创建项目目录
            project_dir = os.path.join(self.config_dir, project_name)
            if not os.path.exists(project_dir):
                os.makedirs(project_dir)
            
            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{device_name}_{timestamp}.txt"
            filepath = os.path.join(project_dir, filename)
            
            # 保存配置
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"设备名称: {device_name}\n")
                f.write(f"获取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n")
                f.write(config_content)
            
            print(f"设备 {device_name} 的配置已保存到: {filepath}")
            
        except Exception as e:
            print(f"保存设备 {device_name} 配置文件时发生错误: {e}")
    
    def collect_configs_by_topology(self):
        """
        方法1：基于拓扑信息收集配置
        使用 topology_manager 获取拓扑信息，然后批量获取配置
        """
        print("=" * 60)
        print("方法1: 基于拓扑信息收集配置")
        print("=" * 60)
        
        # 获取拓扑信息
        opened_projects, topology_data = self.get_topology_info()
        
        if not topology_data:
            print("没有找到可用的拓扑数据。")
            return
        
        # 遍历每个项目
        for project_name, project_data in topology_data.items():
            print(f"\n正在处理项目: {project_name}")
            print("-" * 40)
            
            # 过滤出可配置的设备
            configurable_devices = self.filter_configurable_devices(project_data['nodes'])
            
            if not configurable_devices:
                print("❌ 没有找到可配置的设备")
                continue
            
            # 批量获取所有设备配置
            devices_configs = self.get_multiple_devices_config(configurable_devices)
            
            # 保存配置文件
            for device_name, config_content in devices_configs.items():
                self.save_config_to_file(device_name, config_content, project_name)
        
        print(f"\n基于拓扑信息的配置收集完成！")
    
    def collect_configs_by_project_details(self):
        """
        方法2：基于项目详细信息收集配置
        使用 project_manager 获取详细信息，然后逐个获取配置
        """
        print("=" * 60)
        print("方法2: 基于项目详细信息收集配置")
        print("=" * 60)
        
        # 获取项目详细信息
        projects_info = self.get_project_details()
        
        if not projects_info:
            print("没有找到可用的项目信息。")
            return
        
        # 遍历每个项目
        for project_name, project_details in projects_info.items():
            print(f"\n正在处理项目: {project_name}")
            print("-" * 40)
            
            # 过滤出可配置的设备
            configurable_devices = self.filter_configurable_devices(project_details['nodes'])
            
            if not configurable_devices:
                print("❌ 没有找到可配置的设备")
                continue
            
            # 逐个获取设备配置
            for node in configurable_devices:
                device_name = node['name']
                console_port = node['console']
                # 兼容两种字段名
                device_type = node.get('node_type') or node.get('type', 'unknown')
                
                print(f"\n处理设备: {device_name} ({device_type})")
                
                # 获取设备配置
                config_content = self.get_device_config(device_name, console_port)
                
                if config_content:
                    # 保存配置文件
                    self.save_config_to_file(device_name, config_content, project_name)
                    print(f"✅ 设备 {device_name} 配置获取成功")
                else:
                    print(f"❌ 设备 {device_name} 配置获取失败")
                
                # 设备间等待间隔
                time.sleep(2)
        
        print(f"\n基于项目详细信息的配置收集完成！")
    
    def collect_all_configs(self, method="topology"):
        """
        收集所有设备的配置信息
        
        Args:
            method: 收集方法，"topology" 或 "project_details"
        """
        print("开始收集所有设备配置信息...")
        print(f"使用方法: {method}")
        print("=" * 60)
        
        start_time = datetime.now()
        
        try:
            if method == "topology":
                self.collect_configs_by_topology()
            elif method == "project_details":
                self.collect_configs_by_project_details()
            else:
                print(f"不支持的方法: {method}")
                return
        
        except Exception as e:
            print(f"收集配置过程中发生错误: {e}")
        
        finally:
            end_time = datetime.now()
            duration = end_time - start_time
            
            print(f"\n{'=' * 60}")
            print("配置收集任务完成！")
            print(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"总耗时: {duration}")
            print(f"配置文件保存在: {self.config_dir}")
            print(f"{'=' * 60}")
    
    def show_summary(self):
        """
        显示收集任务摘要
        """
        print("=" * 60)
        print("GNS3设备配置批量收集工具摘要")
        print("=" * 60)
        
        # 使用拓扑管理器获取基本信息
        opened_projects, topology_data = self.get_topology_info()
        
        total_projects = len(topology_data)
        total_devices = 0
        running_devices = 0
        configurable_devices = 0
        
        for project_name, project_data in topology_data.items():
            devices = project_data['nodes']
            total_devices += len(devices)
            running_devices += len([d for d in devices if d['status'] == 'started'])
            
            # 统计可配置设备
            configurable = self.filter_configurable_devices(devices)
            configurable_devices += len(configurable)
            
            print(f"\n项目: {project_name}")
            print(f"  总设备数: {len(devices)}")
            print(f"  运行设备数: {len([d for d in devices if d['status'] == 'started'])}")
            print(f"  可配置设备数: {len(configurable)}")
            print(f"  链路数: {len(project_data['links'])}")
        
        print(f"\n总计:")
        print(f"  项目数: {total_projects}")
        print(f"  设备总数: {total_devices}")
        print(f"  运行设备数: {running_devices}")
        print(f"  可配置设备数: {configurable_devices}")
        
        return {
            'total_projects': total_projects,
            'total_devices': total_devices,
            'running_devices': running_devices,
            'configurable_devices': configurable_devices,
            'topology_data': topology_data
        }

def main():
    """
    主函数
    """
    print("GNS3设备配置信息批量获取工具")
    print("集成拓扑信息、项目信息和配置获取模块")
    print("=" * 60)
    
    try:
        # 创建配置收集器实例
        collector = DeviceConfigCollector()
        
        # 显示摘要信息
        summary = collector.show_summary()
        
        if summary['running_devices'] == 0:
            print("\n没有找到运行中的设备，程序退出。")
            return
        
        # 询问用户选择收集方法
        print(f"\n请选择配置收集方法:")
        print("1. 基于拓扑信息收集 (批量处理，速度较快)")
        print("2. 基于项目详细信息收集 (逐个处理，信息更详细)")
        print("3. 两种方法都执行")
        
        choice = input("请输入选择 (1/2/3，默认为1): ").strip()
        
        if choice == "2":
            collector.collect_all_configs("project_details")
        elif choice == "3":
            print("\n执行方法1: 基于拓扑信息收集")
            collector.collect_all_configs("topology")
            print("\n执行方法2: 基于项目详细信息收集")
            collector.collect_all_configs("project_details")
        else:
            # 默认使用拓扑信息方法
            collector.collect_all_configs("topology")
    
    except KeyboardInterrupt:
        print("\n\n用户中断操作")
    except Exception as e:
        print(f"\n程序执行过程中发生错误: {e}")

if __name__ == "__main__":
    main()
