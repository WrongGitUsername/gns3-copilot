"""
GNS3 命令执行器
用于执行 GNS3 设备命令并返回完整的执行结果
"""

import sys
import os
from typing import List, Dict, Any, Optional

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.gns3_web_console import GNS3WebConsole


class GNS3CommandExecutor:
    """
    GNS3 命令执行器
    提供简化的接口来执行设备命令并获取完整结果
    """
    
    def __init__(self, server_url: str = "http://localhost:3080", 
                 user: Optional[str] = None, 
                 password: Optional[str] = None):
        """
        初始化命令执行器
        
        Args:
            server_url (str): GNS3 服务器 URL
            user (str, optional): 用户名
            password (str, optional): 密码
        """
        self.console = GNS3WebConsole(server_url=server_url, user=user, password=password)
        self.server_url = server_url
    
    def execute_multiple_commands(self, project_id: str, node_id: str, commands: List[str], 
                                timeout: int = 30) -> List[Dict[str, Any]]:
        """
        执行多个命令
        
        Args:
            project_id (str): 项目 ID
            node_id (str): 节点 ID
            commands (List[str]): 命令列表
            timeout (int): 每个命令的超时时间（秒）
            
        Returns:
            List[Dict[str, Any]]: 每个命令的执行结果
        """
        print(f"🚀 执行 {len(commands)} 个命令")
        results = self.console.execute_commands(project_id, node_id, commands, timeout)
        
        # 格式化结果
        formatted_results = []
        for i, result in enumerate(results):
            formatted_result = {
                'command_index': i + 1,
                'command': result['command'],
                'success': result['success'],
                'execution_time': result.get('execution_time', 0),
                'output': result['output'] if result['success'] else '',
                'error': result.get('error'),
                'output_lines': result['output'].split('\n') if result['success'] and result['output'] else [],
                'output_length': len(result['output']) if result['success'] and result['output'] else 0
            }
            formatted_results.append(formatted_result)
        
        return formatted_results
    
    def execute_with_detailed_output(self, project_id: str, node_id: str, commands: List[str], 
                                   timeout: int = 30, show_progress: bool = True) -> Dict[str, Any]:
        """
        执行命令并返回详细的输出信息
        
        Args:
            project_id (str): 项目 ID
            node_id (str): 节点 ID
            commands (List[str]): 命令列表
            timeout (int): 每个命令的超时时间
            show_progress (bool): 是否显示执行进度
            
        Returns:
            Dict[str, Any]: 详细的执行结果
        """
        if show_progress:
            print(f"📋 准备执行 {len(commands)} 个命令")
            print(f"🎯 目标设备: project_id={project_id[:8]}..., node_id={node_id[:8]}...")
        
        # 执行命令
        command_results = self.execute_multiple_commands(project_id, node_id, commands, timeout)
        
        # 统计信息
        total_commands = len(command_results)
        successful_commands = sum(1 for r in command_results if r['success'])
        failed_commands = total_commands - successful_commands
        total_execution_time = sum(r['execution_time'] for r in command_results)
        total_output_length = sum(r['output_length'] for r in command_results)
        
        # 汇总结果
        summary = {
            'execution_summary': {
                'total_commands': total_commands,
                'successful_commands': successful_commands,
                'failed_commands': failed_commands,
                'success_rate': f"{(successful_commands/total_commands)*100:.1f}%",
                'total_execution_time': f"{total_execution_time:.2f}s",
                'average_execution_time': f"{total_execution_time/total_commands:.2f}s",
                'total_output_length': total_output_length
            },
            'command_results': command_results,
            'failed_commands': [r for r in command_results if not r['success']],
            'all_outputs': '\n'.join([f"# 命令 {r['command_index']}: {r['command']}\n{r['output']}" 
                                    for r in command_results if r['success']])
        }
        
        if show_progress:
            self._print_execution_summary(summary)
        
        return summary
    
    def _print_execution_summary(self, summary: Dict[str, Any]):
        """打印执行摘要"""
        exec_summary = summary['execution_summary']
        
        print(f"\n📊 执行摘要:")
        print(f"   总命令数: {exec_summary['total_commands']}")
        print(f"   成功: {exec_summary['successful_commands']}")
        print(f"   失败: {exec_summary['failed_commands']}")
        print(f"   成功率: {exec_summary['success_rate']}")
        print(f"   总执行时间: {exec_summary['total_execution_time']}")
        print(f"   平均执行时间: {exec_summary['average_execution_time']}")
        print(f"   总输出长度: {exec_summary['total_output_length']} 字符")
        
        # 显示失败的命令
        if summary['failed_commands']:
            print(f"\n❌ 失败的命令:")
            for failed in summary['failed_commands']:
                print(f"   命令 {failed['command_index']}: {failed['command']} - {failed['error']}")
    
    def format_for_llm(self, results: List[Dict[str, Any]], 
                      include_metadata: bool = True,
                      max_output_length: int = 1000) -> str:
        """
        将命令执行结果格式化为适合 LLM 处理的文本
        
        Args:
            results (List[Dict[str, Any]]): 命令执行结果
            include_metadata (bool): 是否包含元数据
            max_output_length (int): 每个命令输出的最大长度
            
        Returns:
            str: 格式化后的文本
        """
        formatted_text = []
        
        if include_metadata:
            successful = sum(1 for r in results if r['success'])
            total = len(results)
            formatted_text.append(f"# 命令执行报告")
            formatted_text.append(f"- 总命令数: {total}")
            formatted_text.append(f"- 成功执行: {successful}")
            formatted_text.append(f"- 成功率: {(successful/total)*100:.1f}%")
            formatted_text.append("")
        
        for result in results:
            if result['success']:
                # 格式化成功的命令
                formatted_text.append(f"## 命令 {result['command_index']}: {result['command']}")
                formatted_text.append(f"**执行状态**: ✅ 成功")
                formatted_text.append(f"**执行时间**: {result['execution_time']:.2f}s")
                formatted_text.append("")
                formatted_text.append("**输出内容**:")
                formatted_text.append("```")
                
                # 限制输出长度
                output = result['output']
                if len(output) > max_output_length:
                    output = output[:max_output_length] + f"\n... (输出被截断，完整长度: {len(result['output'])} 字符)"
                
                formatted_text.append(output)
                formatted_text.append("```")
                formatted_text.append("")
            else:
                # 格式化失败的命令
                formatted_text.append(f"## 命令 {result['command_index']}: {result['command']}")
                formatted_text.append(f"**执行状态**: ❌ 失败")
                formatted_text.append(f"**错误信息**: {result.get('error', '未知错误')}")
                formatted_text.append("")
        
        return "\n".join(formatted_text)
    
    def get_device_info(self, project_id: str, node_id: str) -> Optional[Dict[str, Any]]:
        """
        获取设备信息
        
        Args:
            project_id (str): 项目 ID
            node_id (str): 节点 ID
            
        Returns:
            Dict[str, Any]: 设备信息
        """
        return self.console.get_device_info(project_id, node_id)


# 便捷函数
def execute_commands(project_id: str, node_id: str, commands: List[str],
                    server_url: str = "http://localhost:3080",
                    user: Optional[str] = None,
                    password: Optional[str] = None,
                    timeout: int = 30,
                    detailed: bool = True) -> Dict[str, Any]:
    """
    便捷函数：执行设备命令
    
    Args:
        project_id (str): 项目 ID
        node_id (str): 节点 ID
        commands (List[str]): 命令列表
        server_url (str): 服务器 URL
        user (str, optional): 用户名
        password (str, optional): 密码
        timeout (int): 超时时间
        detailed (bool): 是否返回详细结果
        
    Returns:
        Dict[str, Any]: 执行结果
    """
    executor = GNS3CommandExecutor(server_url=server_url, user=user, password=password)
    
    if detailed:
        return executor.execute_with_detailed_output(project_id, node_id, commands, timeout)
    else:
        results = executor.execute_multiple_commands(project_id, node_id, commands, timeout)
        return {'command_results': results}


# 使用示例
if __name__ == "__main__":
    # 创建命令执行器
    executor = GNS3CommandExecutor()
    
    # 示例项目和节点 ID（请替换为实际值）
    project_id = "f2f7ed27-7aa3-4b11-a64c-da947a2c7210"
    node_id = "770c835c-83ae-42ce-a2b9-9a88fb4d2145"
    
    # 示例：执行多个命令
    print("=" * 60)
    print("示例：执行多个命令")
    print("=" * 60)
    
    
    commands = [
        "",                        # 唤醒控制台
        "",                        # 再次唤醒
        "enable",                  # 进入特权模式
        "terminal length 0",       # 设置终端长度
        "show version",           # 显示版本信息
        "show ip interface brief", # 显示接口信息
        "show running-config"      # 显示配置
    ]
    
    detailed_result = executor.execute_with_detailed_output(project_id, node_id, commands)
    
    # 显示每个命令的详细结果
    print("\n📝 详细命令结果:")
    for result in detailed_result['command_results']:
        print(f"\n命令 {result['command_index']}: {result['command']}")
        print(f"  ✅ 成功: {result['success']}")
        print(f"  ⏱️  时间: {result['execution_time']:.2f}s")
        print(f"  📏 输出长度: {result['output_length']} 字符")
        
        if result['success'] and result['output']:
            # 显示输出的第一行和最后一行（如果有的话）
            lines = result['output_lines']
            if lines:
                print(f"  📄 首行: {lines[0][:50]}..." if len(lines[0]) > 50 else f"  📄 首行: {lines[0]}")
                if len(lines) > 1:
                    print(f"  📄 末行: {lines[-1][:50]}..." if len(lines[-1]) > 50 else f"  📄 末行: {lines[-1]}")
        elif not result['success']:
            print(f"  ❌ 错误: {result['error']}")


