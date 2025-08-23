#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BGE-M3优化的RAG配置
针对网络技术文档的多语言向量检索优化
"""

import configparser
from pathlib import Path
from typing import Dict, Any
from .language_adapter import get_message, language_adapter

class BGEM3Config:
    """BGE-M3模型配置管理"""
    
    def __init__(self, config_path: str = "rag_config.ini"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> configparser.ConfigParser:
        """加载配置文件"""
        config = configparser.ConfigParser()
        
        if self.config_path.exists():
            config.read(self.config_path)
        else:
            # 创建默认的BGE-M3配置
            self._create_default_config(config)
            self._save_config(config)
        
        return config
    
    def _create_default_config(self, config: configparser.ConfigParser):
        """创建BGE-M3优化的默认配置"""
        
        # RAG基础配置
        config.add_section('rag')
        config.set('rag', 'enabled', 'true')
        config.set('rag', 'knowledge_base_path', './knowledge_base')
        config.set('rag', 'vector_store_path', './vector_store')
        config.set('rag', 'embedding_model', 'BAAI/bge-m3')
        config.set('rag', 'chunk_size', '1500')
        config.set('rag', 'chunk_overlap', '300')
        config.set('rag', 'search_results', '5')
        config.set('rag', 'max_commands_per_result', '3')
        
        # BGE-M3特有配置
        config.add_section('bge_m3')
        config.set('bge_m3', 'max_length', '8192')
        config.set('bge_m3', 'normalize_embeddings', 'true')
        config.set('bge_m3', 'batch_size', '12')
        config.set('bge_m3', 'show_progress_bar', 'true')
        config.set('bge_m3', 'device', 'cpu')
        
        # 中英文混合优化
        config.add_section('multilingual')
        config.set('multilingual', 'auto_detect_language', 'true')
        config.set('multilingual', 'english_weight', '0.6')
        config.set('multilingual', 'chinese_weight', '0.4')
        config.set('multilingual', 'technical_terms_boost', 'true')
        
        # 知识源配置
        config.add_section('knowledge_sources')
        config.set('knowledge_sources', 'rag_kb_priority', '10')
        config.set('knowledge_sources', 'base_kb_priority', '5')
        config.set('knowledge_sources', 'keyword_search_priority', '1')
        config.set('knowledge_sources', 'auto_update', 'true')
        config.set('knowledge_sources', 'supported_formats', 'pdf,txt,md,docx')
        
        # 高级配置
        config.add_section('advanced')
        config.set('advanced', 'similarity_threshold', '0.25')
        config.set('advanced', 'max_selection_tokens', '3000')
        config.set('advanced', 'enable_command_cache', 'true')
        config.set('advanced', 'cache_expiry', '300')
        config.set('advanced', 'rerank_results', 'true')
    
    def _save_config(self, config: configparser.ConfigParser):
        """保存配置到文件"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            config.write(f)
    
    def get_embedding_config(self) -> Dict[str, Any]:
        """获取嵌入模型配置"""
        return {
            'model_name': self.config.get('rag', 'embedding_model'),
            'model_kwargs': {
                'device': self.config.get('bge_m3', 'device'),
                'trust_remote_code': True
            },
            'encode_kwargs': {
                'batch_size': self.config.getint('bge_m3', 'batch_size'),
                'convert_to_tensor': True,
                'normalize_embeddings': self.config.getboolean('bge_m3', 'normalize_embeddings')
            }
        }
    
    def get_text_splitter_config(self) -> Dict[str, Any]:
        """获取文本分割器配置"""
        return {
            'chunk_size': self.config.getint('rag', 'chunk_size'),
            'chunk_overlap': self.config.getint('rag', 'chunk_overlap'),
            'separators': ["\n\n", "\n", "。", "；", ";", ".", " ", ""],
            'length_function': len,
            'is_separator_regex': False
        }
    
    def get_search_config(self) -> Dict[str, Any]:
        """获取搜索配置"""
        return {
            'k': self.config.getint('rag', 'search_results'),
            'similarity_threshold': self.config.getfloat('advanced', 'similarity_threshold'),
            'rerank': self.config.getboolean('advanced', 'rerank_results', fallback=True)
        }
    
    def optimize_for_network_docs(self):
        """针对网络技术文档的特殊优化"""
        
        # 网络技术关键词权重提升
        network_keywords = [
            'ospf', 'bgp', 'eigrp', 'rip', 'isis',
            'vlan', 'stp', 'pvst', 'rstp', 'mstp',
            'router', 'switch', 'interface', 'vrf',
            'mpls', 'vpn', 'ipsec', 'gre', 'dmvpn',
            'qos', 'acl', 'nat', 'dhcp', 'dns',
            'spanning-tree', 'port-channel', 'etherchannel',
            'hsrp', 'vrrp', 'glbp', 'bfd'
        ]
        
        # 网络命令模式
        command_patterns = [
            r'show\s+[\w\s-]+',
            r'debug\s+[\w\s-]+', 
            r'configure\s+terminal',
            r'interface\s+[\w/]+',
            r'router\s+\w+',
            r'ip\s+[\w\s-]+',
            r'no\s+[\w\s-]+',
            r'enable\s+[\w\s]*',
            r'ping\s+[\w.]+',
            r'traceroute\s+[\w.]+'
        ]
        
        return {
            'network_keywords': network_keywords,
            'command_patterns': command_patterns,
            'boost_factor': 1.5  # 关键词权重提升因子
        }

if __name__ == "__main__":
    # 创建BGE-M3优化配置
    config = BGEM3Config()
    
    print(get_message("bge_m3_config_created"))
    print(get_message("config_file_location").format(config.config_path))
    
    # 显示关键配置
    embedding_config = config.get_embedding_config()
    print(get_message("embedding_model").format(embedding_config['model_name']))
    
    text_config = config.get_text_splitter_config()
    print(get_message("document_chunk_size").format(text_config['chunk_size']))
    
    search_config = config.get_search_config()
    print(get_message("retrieval_count").format(search_config['k']))
    
    network_opt = config.optimize_for_network_docs()
    print(get_message("network_keywords_count").format(len(network_opt['network_keywords'])))
    print(get_message("command_patterns_count").format(len(network_opt['command_patterns'])))
