#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM模型管理器
负责不同LLM模型的初始化和切换
"""

import os
from typing import Union
from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI
from langchain_core.language_models.base import BaseLanguageModel

# 尝试导入 langchain-deepseek
try:
    from langchain_deepseek import ChatDeepSeek
    DEEPSEEK_AVAILABLE = True
except ImportError:
    DEEPSEEK_AVAILABLE = False
    print("⚠️ langchain-deepseek not installed, DeepSeek functionality unavailable")
    print("Install command: pip install langchain-deepseek")

# 导入语言适配器
try:
    from .language_adapter import get_message, language_adapter
    LANGUAGE_ADAPTER_AVAILABLE = True
except ImportError:
    LANGUAGE_ADAPTER_AVAILABLE = False


class LLMManager:
    """LLM模型管理器"""
    
    def __init__(self):
        self.current_model = None
        self.model_name = None
        self._deepseek_model_name = None  # 用于保存 DeepSeek 模型名称
        # 自动初始化 LLM
        self.init_llm()
    
    def get_current_model_info(self) -> str:
        """获取当前模型信息"""
        if not self.current_model:
            if LANGUAGE_ADAPTER_AVAILABLE:
                return get_message("model_not_initialized")
            else:
                return "Model not initialized"
        
        if isinstance(self.current_model, OllamaLLM):
            return f"Ollama: {self.current_model.model}"
        elif isinstance(self.current_model, ChatOpenAI):
            # 区分不同的 OpenAI 兼容服务
            base_url = getattr(self.current_model, 'openai_api_base', None) or getattr(self.current_model, 'base_url', None)
            if base_url and 'openrouter.ai' in str(base_url):
                return f"OpenRouter: {self.current_model.model_name}"
            elif base_url:
                return f"OpenAI兼容: {self.current_model.model_name}"
            else:
                return f"OpenAI: {self.current_model.model_name}"
        elif DEEPSEEK_AVAILABLE and isinstance(self.current_model, ChatDeepSeek):
            # 使用保存的模型名称
            model_name = self._deepseek_model_name or "deepseek-chat"
            return f"DeepSeek: {model_name}"
        else:
            return f"未知模型类型: {type(self.current_model).__name__}"
    
    def init_llm(self) -> BaseLanguageModel:
        """智能初始化LLM（根据默认配置或优先级尝试）"""
        
        # 从环境变量读取默认模型
        default_model = os.getenv("DEFAULT_LLM_MODEL", "").lower()
        
        # 解析默认模型，支持直接指定模型名称
        if "/" in default_model:  # 如 "moonshotai/kimi-k2:free"
            # 检查是否是 OpenRouter 模型
            if os.getenv("USE_OPENROUTER", "false").lower() == "true":
                if self._try_init_openrouter():
                    return self.current_model
            default_model_type = "openrouter"
        elif "deepseek" in default_model:  # 支持 "deepseek" 或 "deepseek-chat"
            default_model_type = "deepseek"
        else:
            default_model_type = default_model
        
        # 根据默认配置优先尝试指定模型
        if default_model_type == "deepseek":
            if self._try_init_deepseek():
                return self.current_model
        elif default_model_type == "openai_compatible":
            if self._try_init_openai_compatible():
                return self.current_model
        elif default_model_type == "ollama":
            if self._try_init_ollama():
                return self.current_model
        elif default_model_type == "openrouter":
            if self._try_init_openrouter():
                return self.current_model
        
        # 如果默认模型失败，按优先级尝试其他模型
        print(f"⚠️ 默认模型 '{default_model}' 初始化失败，尝试其他模型...")
        
        # 优先级1: OpenRouter
        if os.getenv("USE_OPENROUTER", "false").lower() == "true":
            if self._try_init_openrouter():
                return self.current_model
        
        # 优先级2: DeepSeek
        if os.getenv("USE_DEEPSEEK", "false").lower() == "true":
            if self._try_init_deepseek():
                return self.current_model
        
        # 优先级3: OpenAI兼容接口
        if os.getenv("USE_OPENAI_COMPATIBLE", "false").lower() == "true":
            if self._try_init_openai_compatible():
                return self.current_model
        
        # 优先级4: Ollama本地模型（最后选择）
        if self._try_init_ollama():
            return self.current_model
        
        raise Exception("❌ 无法初始化任何LLM模型")
    
    def _try_init_openrouter(self) -> bool:
        """尝试初始化 OpenRouter 模型"""
        try:
            llm = self._init_openrouter_llm()
            self.current_model = llm
            self.model_name = "OpenRouter"
            return True
        except Exception as e:
            print(f"⚠️ OpenRouter 初始化失败: {e}")
            return False
    
    def _try_init_deepseek(self) -> bool:
        """尝试初始化 DeepSeek 模型"""
        try:
            llm = self._init_deepseek_llm()
            self.current_model = llm
            self.model_name = "DeepSeek"
            return True
        except Exception as e:
            print(f"⚠️ DeepSeek 初始化失败: {e}")
            return False
    
    def _try_init_openai_compatible(self) -> bool:
        """尝试初始化 OpenAI 兼容接口"""
        try:
            llm = self._init_openai_compatible_llm()
            self.current_model = llm
            self.model_name = "OpenAI兼容"
            return True
        except Exception as e:
            print(f"⚠️ OpenAI兼容接口初始化失败: {e}")
            return False
    
    def _try_init_ollama(self) -> bool:
        """尝试初始化 Ollama 本地模型"""
        try:
            llm = self._init_ollama_llm()
            self.current_model = llm
            self.model_name = "Ollama"
            return True
        except Exception as e:
            print(f"⚠️ Ollama 初始化失败: {e}")
            return False
    
    def _init_openrouter_llm(self) -> ChatOpenAI:
        """初始化 OpenRouter 模型"""
        base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        api_key = os.getenv("OPENROUTER_API_KEY")
        model = os.getenv("OPENROUTER_MODEL") or os.getenv("DEFAULT_LLM_MODEL", "moonshotai/kimi-k2:free")
        
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY 未设置")
        
        llm = ChatOpenAI(
            base_url=base_url,
            api_key=api_key,
            model=model,
            temperature=0.1,
            max_tokens=1024,
        )
        
        # 测试连接
        test_response = llm.invoke("你好")
        print(f"🧠 OpenRouter 连接成功: {model}")
        return llm
    
    def _init_deepseek_llm(self):
        """初始化 DeepSeek 模型（使用 langchain-deepseek）"""
        if not DEEPSEEK_AVAILABLE:
            raise ImportError("langchain-deepseek 模块未安装")
        
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY 未设置")
        
        model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        
        try:
            llm = ChatDeepSeek(
                api_key=api_key,
                model=model,
                temperature=0.1,
                max_tokens=1024,
            )
            
            # 测试连接
            test_response = llm.invoke("你好")
            if LANGUAGE_ADAPTER_AVAILABLE:
                print(get_message("deepseek_connected", model))
            else:
                print(f"🧠 DeepSeek connected successfully: {model}")
            
            # 保存模型名称以备后用
            self._deepseek_model_name = model
            return llm
            
        except Exception as e:
            if LANGUAGE_ADAPTER_AVAILABLE:
                print(get_message("deepseek_init_failed", str(e)))
            else:
                print(f"❌ DeepSeek initialization failed: {e}")
            # 尝试使用更简单的参数
            try:
                llm = ChatDeepSeek(api_key=api_key)
                test_response = llm.invoke("你好")
                if LANGUAGE_ADAPTER_AVAILABLE:
                    print(get_message("deepseek_connected_default"))
                else:
                    print("🧠 DeepSeek connected successfully (using default parameters)")
                self._deepseek_model_name = "deepseek-chat"
                return llm
            except Exception as e2:
                raise Exception(f"DeepSeek initialization completely failed: {e2}")
    
    def _init_openai_compatible_llm(self) -> ChatOpenAI:
        """初始化 OpenAI 兼容接口"""
        base_url = os.getenv("OPENAI_COMPATIBLE_BASE_URL")
        api_key = os.getenv("OPENAI_COMPATIBLE_API_KEY", "dummy")
        model = os.getenv("OPENAI_COMPATIBLE_MODEL", "gpt-3.5-turbo")
        
        if not base_url:
            raise ValueError("OPENAI_COMPATIBLE_BASE_URL 未设置")
        
        llm = ChatOpenAI(
            base_url=base_url,
            api_key=api_key,
            model=model,
            temperature=0.1,
            max_tokens=1024,
        )
        
        # 测试连接
        test_response = llm.invoke("你好")
        print(f"🧠 OpenAI兼容接口连接成功: {model}")
        return llm
    
    def _init_ollama_llm(self) -> OllamaLLM:
        """初始化 Ollama 本地模型"""
        ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        ollama_model = os.getenv("OLLAMA_MODEL", "deepseek-r1:8b")
        
        llm = OllamaLLM(
            base_url=ollama_base_url,
            model=ollama_model,
            temperature=0.1,
            num_predict=1024,
            verbose=False
        )
        
        # 测试连接
        test_response = llm.invoke("你好")
        print(f"🧠 Ollama 连接成功: {ollama_model}")
        return llm
