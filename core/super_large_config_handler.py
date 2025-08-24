#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Super large configuration file handler.

Specifically handles devices with extensive configuration information 
(such as core switches, large routers, etc.).
Uses multiple strategies to ensure complete configuration retrieval.
"""

import telnetlib
import time
import threading
import queue
import os
from datetime import datetime
from dotenv import load_dotenv
from .language_adapter import get_message, language_adapter

# Load environment variables
load_dotenv()

class LargeConfigHandler:
    """Super large configuration file handler."""
    
    def __init__(self, host, port, timeout=120):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.max_config_wait = 600  # Maximum wait 10 minutes
        
    def get_large_config_with_monitoring(self, device_name):
        """
        Get large configuration files using monitoring mechanism.
        Includes progress monitoring, timeout handling, and integrity verification.
        """
        
        print(f"🚀 启动超大配置获取: {device_name}")
        print(f"   最大等待时间: {self.max_config_wait}秒")
        print("="*60)
        
        try:
            # 建立连接
            tn = telnetlib.Telnet()
            tn.open(self.host, self.port, timeout=self.timeout)
            print(f"✅ 连接成功: {self.host}:{self.port}")
            
            # 初始化会话
            self._initialize_session(tn, device_name)
            
            # 使用多策略获取配置
            config = self._get_config_with_strategies(tn, device_name)
            
            tn.close()
            return config
            
        except Exception as e:
            print(f"❌ 超大配置获取失败: {e}")
            return ""
    
    def _initialize_session(self, tn, device_name):
        """初始化Telnet会话"""
        
        print("🔧 初始化会话...")
        
        # 等待设备响应
        time.sleep(3)
        tn.read_very_eager()
        
        # 激活会话
        tn.write(b'\r\n')
        time.sleep(2)
        tn.read_very_eager()
        
        # 进入特权模式
        tn.write(b'enable\r\n')
        time.sleep(2)
        tn.read_very_eager()
        
        # 优化终端设置
        commands = [
            b'terminal length 0\r\n',      # 禁用分页
            b'terminal width 0\r\n',       # 禁用行宽限制
            b'terminal no monitor\r\n',    # 禁用日志显示
        ]
        
        for cmd in commands:
            try:
                tn.write(cmd)
                time.sleep(1)
                tn.read_very_eager()
            except:
                pass  # 某些命令可能不支持，忽略错误
        
        print("✅ 会话初始化完成")
    
    def _get_config_with_strategies(self, tn, device_name):
        """使用多种策略获取配置"""
        
        strategies = [
            ("标准策略", self._strategy_standard),
            ("分段策略", self._strategy_chunked),
            ("极限耐心策略", self._strategy_extreme_patience)
        ]
        
        for strategy_name, strategy_func in strategies:
            print(f"\n🎯 尝试策略: {strategy_name}")
            print("-" * 40)
            
            try:
                config = strategy_func(tn, device_name)
                if self._validate_config(config):
                    print(f"✅ {strategy_name} 成功获取完整配置")
                    return config
                else:
                    print(f"⚠️ {strategy_name} 获取的配置不完整，尝试下一策略")
            except Exception as e:
                print(f"❌ {strategy_name} 失败: {e}")
                continue
        
        print("❌ 所有策略都失败了")
        return ""
    
    def _strategy_standard(self, tn, device_name):
        """标准策略：正常获取配置"""
        
        tn.write(b'show running-config\r\n')
        
        config_output = ""
        start_time = time.time()
        consecutive_empty = 0
        
        while (time.time() - start_time) < 180:  # 3分钟超时
            try:
                data = tn.read_very_eager().decode('ascii', errors='ignore')
                if data:
                    config_output += data
                    consecutive_empty = 0
                    print(f"📥 接收: {len(data)} 字符 (总计: {len(config_output)})")
                    
                    if self._check_config_end(data, device_name):
                        break
                else:
                    consecutive_empty += 1
                    if consecutive_empty > 10:
                        break
                
                time.sleep(0.5)
            except:
                break
        
        return config_output
    
    def _strategy_chunked(self, tn, device_name):
        """分段策略：分段获取配置"""
        
        print("使用分段获取策略...")
        
        # 先获取配置大小估计
        tn.write(b'show running-config | include Current\r\n')
        time.sleep(2)
        size_info = tn.read_very_eager().decode('ascii', errors='ignore')
        
        # 分段获取
        sections = [
            'version',
            'interface',
            'router',
            'access-list',
            'line'
        ]
        
        full_config = ""
        
        for section in sections:
            print(f"📦 获取 {section} 配置...")
            tn.write(f'show running-config | section {section}\r\n'.encode())
            time.sleep(3)
            
            section_config = ""
            for _ in range(20):
                data = tn.read_very_eager().decode('ascii', errors='ignore')
                if data:
                    section_config += data
                else:
                    break
                time.sleep(0.2)
            
            full_config += section_config + "\n"
        
        # 最后获取完整配置做验证
        tn.write(b'show running-config\r\n')
        time.sleep(5)
        
        complete_config = ""
        start_time = time.time()
        
        while (time.time() - start_time) < 300:
            data = tn.read_very_eager().decode('ascii', errors='ignore')
            if data:
                complete_config += data
                print(f"📥 验证获取: {len(data)} 字符")
            else:
                time.sleep(1)
                if (time.time() - start_time) > 10 and len(complete_config) > 1000:
                    break
        
        return complete_config if len(complete_config) > len(full_config) else full_config
    
    def _strategy_extreme_patience(self, tn, device_name):
        """极限耐心策略：最大等待时间获取"""
        
        print("使用极限耐心策略...")
        print(f"最大等待时间: {self.max_config_wait}秒")
        
        tn.write(b'show running-config\r\n')
        
        config_output = ""
        start_time = time.time()
        last_data_time = start_time
        
        while (time.time() - start_time) < self.max_config_wait:
            try:
                data = tn.read_very_eager().decode('ascii', errors='ignore')
                if data:
                    config_output += data
                    last_data_time = time.time()
                    print(f"📥 持续接收: {len(data)} 字符 (总计: {len(config_output):,})")
                    
                    if self._check_config_end(data, device_name):
                        print("✅ 检测到配置结束标志")
                        break
                else:
                    # 如果超过30秒没有新数据，可能已经完成
                    if (time.time() - last_data_time) > 30:
                        print("⏰ 30秒无新数据，认为传输完成")
                        break
                
                time.sleep(0.2)
            except Exception as e:
                print(f"⚠️ 读取异常: {e}")
                break
        
        elapsed = time.time() - start_time
        print(f"⏱️ 极限策略耗时: {elapsed:.2f}秒")
        
        return config_output
    
    def _check_config_end(self, data, device_name):
        """检查配置是否结束"""
        
        end_markers = [
            'end\r\n',
            f'{device_name}#',
            'R1#', 'R2#', 'R3#', 'R4#', 'R5#', 'R6#',
            'Switch#'
        ]
        
        data_lower = data.lower()
        for marker in end_markers:
            if marker.lower() in data_lower:
                return True
        return False
    
    def _validate_config(self, config):
        """验证配置完整性"""
        
        if not config or len(config) < 100:
            return False
        
        # 检查必要的配置元素
        required_elements = [
            'version',
            'hostname',
            ('interface' in config.lower() or 'Configuration' in config)
        ]
        
        for element in required_elements:
            if isinstance(element, str):
                if element not in config.lower():
                    print(f"⚠️ 缺少必要元素: {element}")
                    return False
            elif not element:
                print(f"⚠️ 配置验证失败")
                return False
        
        # 检查配置是否被截断
        if not any(end in config.lower() for end in ['end', '#']):
            print("⚠️ 配置可能被截断（缺少结束标志）")
            return False
        
        print(f"✅ 配置验证通过 ({len(config):,} 字符)")
        return True

def test_super_large_config():
    """测试超大配置处理"""
    
    print("🌟 超大配置文件处理测试")
    print("="*60)
    
    # 获取测试设备
    device_name = input("请输入设备名称 (默认R-2): ").strip() or "R-2"
    
    try:
        port = int(input("请输入console端口 (默认5006): ").strip() or "5006")
    except:
        port = 5006
    
    print(f"\n🎯 测试设备: {device_name}:{port}")
    
    # 创建处理器，从环境变量获取Telnet主机地址
    telnet_host = os.getenv("TELNET_HOST", "192.168.102.1")
    handler = LargeConfigHandler(telnet_host, port, timeout=60)
    
    # 开始测试
    start_time = time.time()
    config = handler.get_large_config_with_monitoring(device_name)
    end_time = time.time()
    
    # 结果分析
    if config:
        print(f"\n🎉 超大配置获取成功！")
        print(f"📊 配置大小: {len(config):,} 字符")
        config_lines = config.split('\n')
        print(f"📄 配置行数: {len(config_lines):,} 行")
        print(f"⏱️ 总耗时: {end_time - start_time:.2f} 秒")
        
        # 保存结果
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"/home/yueguobin/myCode/GNS3/tools/super_large_config_{device_name}_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"设备: {device_name}\n")
            f.write(f"获取时间: {datetime.now()}\n")
            f.write(f"总耗时: {end_time - start_time:.2f} 秒\n")
            f.write("="*50 + "\n")
            f.write(config)
        
        print(f"💾 配置已保存到: {filename}")
    else:
        print(f"😞 超大配置获取失败")
        print(f"⏱️ 总耗时: {end_time - start_time:.2f} 秒")

if __name__ == "__main__":
    test_super_large_config()
