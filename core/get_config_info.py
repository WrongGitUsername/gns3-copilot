#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设备配置信息获取模块
支持通过Telnet连接获取设备配置
增强版：支持超大配置文件和智能完成检测
"""

import telnetlib
import time
import os
from datetime import datetime
from dotenv import load_dotenv
from .language_adapter import get_message, language_adapter

# 加载环境变量
load_dotenv()

class DeviceConfigManager:
    """设备配置管理器"""
    
    def __init__(self, telnet_host=None):
        """
        初始化配置管理器
        
        Args:
            telnet_host: Telnet主机地址，如果不指定则从环境变量获取
        """
        self.telnet_host = telnet_host or os.getenv("TELNET_HOST", "192.168.102.1")
        self.configs = {}  # 存储获取的配置信息
    
    def get_device_config(self, device_name, console_port, max_wait_time=180, use_large_config_handler=False):
        """
        获取指定设备的配置信息
        增强版本：支持超大型配置文件，多策略智能处理
        
        Args:
            device_name: 设备名称
            console_port: Console端口号
            max_wait_time: 最大等待时间（秒），默认180秒
            use_large_config_handler: 是否使用超大配置处理器
        """
        print(get_message("getting_device_config").format(device_name))
        print(get_message("console_port").format(console_port))
        print(get_message("max_wait_time").format(max_wait_time))
        
        # 如果需要，使用超大配置处理器
        if use_large_config_handler:
            return self._get_large_config_with_fallback(device_name, console_port, max_wait_time)
        
        try:
            # 建立telnet连接
            tn = telnetlib.Telnet()
            tn.open(self.telnet_host, console_port, timeout=60)
            print(get_message("connected_successfully").format(self.telnet_host, console_port))
            
            # 增强的初始化连接
            self._initialize_connection(tn)
            
            # 执行show running-config命令
            print(get_message("executing_show_run"))
            tn.write(b'show running-config\r\n')
            
            # 智能等待和读取配置
            config_output = ""
            start_time = time.time()
            consecutive_empty_reads = 0
            last_output_time = start_time
            data_chunks = 0
            
            while (time.time() - start_time) < max_wait_time:
                try:
                    data = tn.read_very_eager().decode('ascii', errors='ignore')
                    if data:
                        config_output += data
                        consecutive_empty_reads = 0
                        last_output_time = time.time()
                        data_chunks += 1
                        
                        # 每100个数据块显示一次进度
                        if data_chunks % 100 == 0:
                            print(get_message("receiving_data").format(len(config_output), data_chunks))
                        
                        # 智能检测配置完成
                        if self._is_config_complete(data, device_name):
                            print(get_message("config_transfer_complete"))
                            break
                    else:
                        consecutive_empty_reads += 1
                        # 大配置文件可能有传输间隙，增加容忍度
                        if consecutive_empty_reads >= 20:  # 增加到20次
                            if (time.time() - last_output_time) > 30:  # 增加到30秒
                                print(get_message("no_new_data_timeout"))
                                break
                    
                    time.sleep(0.3)  # 稍微减少睡眠时间提高响应性
                    
                except Exception as e:
                    print(get_message("read_exception").format(e))
                    break
            
            tn.close()
            
            # 处理输出
            if config_output:
                result_config = self._process_config_output(config_output, device_name)
                elapsed_time = time.time() - start_time
                print(get_message("config_get_success").format(device_name))
                print(get_message("config_size").format(len(result_config)))
                print(get_message("config_lines").format(len(result_config.split(chr(10)))))
                print(get_message("config_get_time").format(elapsed_time))
                return result_config
            else:
                print(get_message("config_get_failed").format(device_name))
                return ""
                
        except Exception as e:
            print(get_message("config_get_error").format(device_name, e))
            # 如果普通方法失败，尝试大配置处理器
            if not use_large_config_handler:
                print(get_message("try_large_config_handler"))
                return self._get_large_config_with_fallback(device_name, console_port, max_wait_time)
            return ""
    
    def _initialize_connection(self, tn):
        """增强的连接初始化"""
        # 等待设备响应
        time.sleep(3)
        tn.read_very_eager()  # 清空缓冲区
        
        # 激活会话
        tn.write(b'\r\n')
        time.sleep(2)
        tn.read_very_eager()
        
        # 进入特权模式
        tn.write(b'enable\r\n')
        time.sleep(2)
        tn.read_very_eager()
        
        # 优化终端设置
        terminal_commands = [
            b'terminal length 0\r\n',      # 禁用分页
            b'terminal width 0\r\n',       # 禁用行宽限制
            b'terminal no monitor\r\n',    # 禁用日志显示
        ]
        
        for cmd in terminal_commands:
            try:
                tn.write(cmd)
                time.sleep(1)
                tn.read_very_eager()
            except:
                pass  # 某些命令可能不支持，忽略错误
    
    def _get_large_config_with_fallback(self, device_name, console_port, max_wait_time):
        """
        超大配置处理器，包含多种备用策略
        """
        print(get_message("large_config_mode"))
        
        strategies = [
            ("极限耐心策略", self._strategy_extreme_patience),
            ("分段获取策略", self._strategy_chunked_config),
            ("多次尝试策略", self._strategy_multiple_attempts)
        ]
        
        for strategy_name, strategy_func in strategies:
            print(get_message("trying_strategy").format(strategy_name))
            try:
                config = strategy_func(device_name, console_port, max_wait_time * 2)
                if config and len(config) > 500:  # 基本的配置长度检查
                    print(get_message("strategy_success").format(strategy_name))
                    return config
                else:
                    print(get_message("strategy_config_too_short").format(strategy_name))
            except Exception as e:
                print(get_message("strategy_failed").format(strategy_name, e))
                continue
        
        print(get_message("config_get_failed").format(device_name))
        return ""
    
    def _strategy_extreme_patience(self, device_name, console_port, max_wait_time):
        """极限耐心策略"""
        max_wait = min(max_wait_time, 600)  # 最多等待10分钟
        
        tn = telnetlib.Telnet()
        tn.open(self.telnet_host, console_port, timeout=90)
        
        self._initialize_connection(tn)
        tn.write(b'show running-config\r\n')
        
        config_output = ""
        start_time = time.time()
        last_data_time = start_time
        
        while (time.time() - start_time) < max_wait:
            try:
                data = tn.read_very_eager().decode('ascii', errors='ignore')
                if data:
                    config_output += data
                    last_data_time = time.time()
                    
                    if len(config_output) % 10000 < len(data):  # 每10KB显示一次
                        print(f"📥 已接收: {len(config_output):,} 字符")
                    
                    if self._is_config_complete(data, device_name):
                        break
                else:
                    if (time.time() - last_data_time) > 60:  # 1分钟无数据
                        print("⏰ 极限等待完成")
                        break
                
                time.sleep(0.1)
            except:
                break
        
        tn.close()
        return self._process_config_output(config_output, device_name)
    
    def _strategy_chunked_config(self, device_name, console_port, max_wait_time):
        """分段获取策略"""
        tn = telnetlib.Telnet()
        tn.open(self.telnet_host, console_port, timeout=90)
        
        self._initialize_connection(tn)
        
        # 分段获取不同部分
        sections = ['interface', 'router', 'access-list', 'ip route']
        partial_configs = []
        
        for section in sections:
            tn.write(f'show running-config | section {section}\r\n'.encode())
            time.sleep(5)
            section_data = tn.read_very_eager().decode('ascii', errors='ignore')
            partial_configs.append(section_data)
        
        # 最后获取完整配置
        tn.write(b'show running-config\r\n')
        time.sleep(10)
        
        full_config = ""
        for _ in range(100):
            data = tn.read_very_eager().decode('ascii', errors='ignore')
            if data:
                full_config += data
            else:
                break
            time.sleep(0.5)
        
        tn.close()
        return self._process_config_output(full_config, device_name)
    
    def _strategy_multiple_attempts(self, device_name, console_port, max_wait_time):
        """多次尝试策略"""
        attempts = 3
        best_config = ""
        
        for attempt in range(attempts):
            print(f"🔄 第 {attempt + 1}/{attempts} 次尝试")
            
            try:
                tn = telnetlib.Telnet()
                tn.open(self.telnet_host, console_port, timeout=60)
                
                self._initialize_connection(tn)
                tn.write(b'show running-config\r\n')
                
                config = ""
                for _ in range(200):
                    data = tn.read_very_eager().decode('ascii', errors='ignore')
                    if data:
                        config += data
                    time.sleep(0.5)
                
                tn.close()
                
                if len(config) > len(best_config):
                    best_config = config
                    
            except Exception as e:
                print(f"第 {attempt + 1} 次尝试失败: {e}")
                time.sleep(5)  # 等待5秒再试
        
        return self._process_config_output(best_config, device_name)
    
    def _process_config_output(self, config_output, device_name):
        """处理配置输出，清理不需要的内容"""
        if not config_output:
            return ""
        
        config_lines = config_output.split('\n')
        clean_config = []
        config_started = False
        
        for line in config_lines:
            line = line.strip()
            
            # 检测配置开始
            if not config_started:
                if any(marker in line for marker in ['Building configuration', 'Current configuration']):
                    config_started = True
                    continue
            
            if config_started:
                # 跳过命令回显和提示符
                if any(skip in line for skip in ['show running-config', f'{device_name}#']):
                    continue
                    
                # 检测配置结束
                if line == 'end' or (line.endswith('#') and len(line) < 20):
                    if line == 'end':
                        clean_config.append(line)
                    break
                    
                clean_config.append(line)
        
        return '\n'.join(clean_config)
    
    def _is_config_complete(self, data, device_name):
        """
        智能检测配置是否传输完成
        
        Args:
            data: 最新接收的数据
            device_name: 设备名称
        
        Returns:
            bool: 是否完成
        """
        # 检查常见的结束标志
        end_markers = [
            'end\r\n',
            'end\n',
            f'{device_name}#',
            'R1#', 'R2#', 'R3#', 'R4#', 'R5#', 'R6#',  # 常见设备提示符
            'Router#',
            'Switch#'
        ]
        
        for marker in end_markers:
            if marker in data:
                return True
        
        return False
    
    def get_multiple_devices_config(self, devices_info):
        """
        获取多个设备的配置信息
        
        Args:
            devices_info: 设备信息列表，格式: [{"name": "R-1", "console": 5004}, ...]
        
        Returns:
            dict: 设备配置字典，格式: {"设备名": "配置内容", ...}
        """
        results = {}
        total_devices = len(devices_info)
        
        print(f"开始获取 {total_devices} 个设备的配置信息")
        print("=" * 50)
        
        for i, device_info in enumerate(devices_info, 1):
            device_name = device_info.get('name', f'Device-{i}')
            console_port = device_info.get('console', 5000 + i)
            
            print(f"\n[{i}/{total_devices}] 正在处理设备: {device_name}")
            
            config = self.get_device_config(device_name, console_port)
            if config:
                results[device_name] = config
                self.configs[device_name] = config
                print(f"✅ {device_name} 配置获取成功")
            else:
                print(f"❌ {device_name} 配置获取失败")
            
            # 设备间间隔，避免并发问题
            if i < total_devices:
                print("等待 3 秒后处理下一个设备...")
                time.sleep(3)
        
        print(f"\n配置获取完成！成功: {len(results)}/{total_devices}")
        return results
    
    def save_configs_to_file(self, configs, filename=None):
        """
        将配置保存到文件
        
        Args:
            configs: 配置字典
            filename: 文件名，如果不指定则自动生成
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"/home/yueguobin/myCode/GNS3/tools/device_configs_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"设备配置信息导出\n")
                f.write(f"导出时间: {datetime.now()}\n")
                f.write(f"设备总数: {len(configs)}\n")
                f.write("=" * 60 + "\n\n")
                
                for device_name, config in configs.items():
                    f.write(f"\n{'='*20} {device_name} {'='*20}\n")
                    f.write(config)
                    f.write(f"\n{'='*50}\n")
            
            print(f"✅ 配置已保存到: {filename}")
            return filename
        except Exception as e:
            print(f"❌ 保存配置失败: {e}")
            return None

def main():
    """主函数，用于测试"""
    print("设备配置管理器测试")
    print("=" * 50)
    
    # 创建配置管理器
    config_manager = DeviceConfigManager()
    
    # 测试获取单个设备配置
    print("\n测试获取单个设备配置:")
    device_name = input("请输入设备名称 (默认 R-1): ").strip() or "R-1"
    
    try:
        port = int(input("请输入console端口 (默认 5004): ").strip() or "5004")
    except:
        port = 5004
    
    use_large = input("是否使用大配置处理器? (y/N): ").strip().lower() == 'y'
    
    config = config_manager.get_device_config(device_name, port, 
                                            max_wait_time=300, 
                                            use_large_config_handler=use_large)
    
    if config:
        print(f"\n获取到的配置预览 ({len(config)} 字符):")
        print("-" * 30)
        print(config[:500] + "..." if len(config) > 500 else config)
        
        # 保存配置
        save = input("\n是否保存配置到文件? (Y/n): ").strip().lower() != 'n'
        if save:
            config_manager.save_configs_to_file({device_name: config})

if __name__ == "__main__":
    main()
