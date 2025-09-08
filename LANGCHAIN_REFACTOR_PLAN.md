
## 🚀 LangChain Workflow 

### 目标架构
```
用户输入 → Intent Classification Chain → Router Chain → Tool Execution Chain → Response Generation Chain → 多语言输出
```

## 📦 重构实施计划

### Phase 1: 基础Tools转换
将现有功能转换为LangChain Tools

### Phase 2: Chain架构设计
构建主要的处理链条

### Phase 3: Agent集成
使用LangChain Agent进行智能路由

### Phase 4: LCEL优化
使用LangChain Expression Language简化流程

## 🛠️ 具体实施方案

### 1. Tools重构

#### 1.1 将GNS3AgentTools转换为LangChain Tools
```python
from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class TopologyQueryInput(BaseModel):
    """拓扑查询输入"""
    include_details: bool = Field(default=False, description="是否包含详细信息")

class TopologyTool(BaseTool):
    name = "get_topology"
    description = "获取GNS3网络拓扑信息，包括设备和连接"
    args_schema: Type[BaseModel] = TopologyQueryInput
    
    def _run(self, include_details: bool = False) -> str:
        # 实现拓扑获取逻辑
        pass
```

#### 1.2 网络命令执行工具
```python
class NetworkCommandInput(BaseModel):
    device_name: str = Field(description="目标设备名称")
    command: str = Field(description="要执行的网络命令")

class NetworkCommandTool(BaseTool):
    name = "execute_network_command"
    description = "在指定设备上执行网络命令"
    args_schema: Type[BaseModel] = NetworkCommandInput
    
    def _run(self, device_name: str, command: str) -> str:
        # 执行网络命令逻辑
        pass
```

### 2. Chain架构设计

#### 2.1 意图分类Chain
```python
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel

class IntentClassification(BaseModel):
    intent: str = Field(description="用户意图类型")
    confidence: float = Field(description="置信度")
    entities: Dict[str, str] = Field(description="提取的实体")

intent_prompt = PromptTemplate(
    template="""分析用户输入，确定意图类型：
    
用户输入: {user_input}

可能的意图类型:
- topology_query: 查询网络拓扑
- device_config: 设备配置相关
- network_command: 执行网络命令
- connectivity_test: 连通性测试
- analysis_request: 分析请求

返回JSON格式的分类结果。

{format_instructions}
""",
    input_variables=["user_input"],
    partial_variables={"format_instructions": PydanticOutputParser(pydantic_object=IntentClassification).get_format_instructions()}
)

intent_chain = LLMChain(
    llm=llm,
    prompt=intent_prompt,
    output_parser=PydanticOutputParser(pydantic_object=IntentClassification)
)
```

#### 2.2 路由Chain
```python
from langchain.chains.router import MultiRouteChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.chains.router.multi_route_prompt import MULTI_ROUTE_PROMPT

# 定义不同意图的处理链
topology_chain = LLMChain(llm=llm, prompt=topology_prompt)
config_chain = LLMChain(llm=llm, prompt=config_prompt)
command_chain = LLMChain(llm=llm, prompt=command_prompt)

destination_chains = {
    "topology": topology_chain,
    "config": config_chain,
    "command": command_chain
}

router_chain = LLMRouterChain.from_llm(llm, MULTI_ROUTE_PROMPT)
chain = MultiRouteChain(
    router_chain=router_chain,
    destination_chains=destination_chains,
    default_chain=topology_chain
)
```

### 3. Agent架构

#### 3.1 自定义Agent
```python
from langchain.agents import Tool, AgentExecutor, BaseMultiActionAgent
from langchain.schema import AgentAction, AgentFinish

class GNS3Agent(BaseMultiActionAgent):
    tools: List[Tool]
    llm: BaseLanguageModel
    
    def plan(self, intermediate_steps, **kwargs):
        # 智能规划执行步骤
        user_input = kwargs.get("input", "")
        
        # 使用LLM分析需要执行的工具序列
        planning_prompt = f"""
        用户请求: {user_input}
        
        可用工具: {[tool.name for tool in self.tools]}
        
        请规划执行步骤...
        """
        
        # 返回要执行的动作列表
        return actions
```

#### 3.2 RAG增强Agent
```python
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferWindowMemory

# 初始化工具列表
tools = [
    TopologyTool(),
    NetworkCommandTool(),
    DeviceConfigTool(),
    ConnectivityTestTool()
]

# 添加RAG工具
if use_rag:
    tools.append(RAGSearchTool())

# 初始化记忆
memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    k=5,
    return_messages=True
)

# 创建Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    memory=memory,
    verbose=True
)
```

### 4. LCEL优化方案

#### 4.1 使用LCEL简化链式调用
```python
from langchain.schema.runnable import RunnableParallel, RunnableSequence

# 并行处理多个查询
parallel_chain = RunnableParallel({
    "intent": intent_classification_chain,
    "entities": entity_extraction_chain,
    "context": context_retrieval_chain
})

# 序列处理
main_chain = (
    parallel_chain
    | route_to_appropriate_handler
    | execute_tools
    | generate_response
    | format_output
)

# 使用
result = main_chain.invoke({"input": user_input})
```

#### 4.2 条件路由
```python
from langchain.schema.runnable import RunnableBranch

def route_based_on_intent(inputs):
    intent = inputs["intent"]["intent"]
    if intent == "topology_query":
        return topology_handler
    elif intent == "network_command":
        return command_handler
    else:
        return default_handler

routing_chain = RunnableBranch(
    (lambda x: x["intent"]["intent"] == "topology_query", topology_handler),
    (lambda x: x["intent"]["intent"] == "network_command", command_handler),
    default_handler
)
```

## 🔧 重构实施步骤

### Step 1: 创建新的工具模块
1. 创建 `tools/` 目录
2. 实现 LangChain Tool 类
3. 保持向后兼容

### Step 2: 重构处理器
1. 创建 `chains/` 目录
2. 实现各种处理链
3. 替换硬编码逻辑

### Step 3: Agent集成
1. 创建主Agent类
2. 集成工具和链
3. 添加智能路由

### Step 4: 测试和优化
1. 单元测试
2. 集成测试
3. 性能优化

## 📊 预期收益

### 灵活性提升
- 动态添加新工具
- 可配置的处理流程
- 更好的错误处理

### 可维护性改善
- 模块化设计
- 清晰的职责分离
- 标准化的接口

### 功能增强
- 智能意图识别
- 自动工具选择
- 上下文记忆

### 扩展性
- 支持插件架构
- 易于添加新的LLM
- 可配置的工作流

## ⚠️ 注意事项

1. **保持向后兼容**: 在重构过程中保持现有API的兼容性
2. **渐进式迁移**: 分模块逐步重构，避免大爆炸式更改
3. **性能考虑**: LangChain可能引入额外开销，需要监控性能
4. **错误处理**: 确保新架构有完善的错误处理机制
5. **测试覆盖**: 重构时要保证测试覆盖率

## 🎯 实施优先级

### 高优先级
1. Tools重构 (基础设施)
2. 意图分类Chain (核心功能)
3. 基本Agent (用户接口)

### 中优先级
1. RAG增强
2. 记忆系统
3. 多轮对话

### 低优先级
1. LCEL优化
2. 高级Agent功能
3. 性能优化

这个重构方案将大大提高系统的灵活性和可维护性，同时充分利用LangChain生态系统的强大功能。
