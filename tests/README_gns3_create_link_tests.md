# GNS3 Link Creation Tool Tests

## 概述

本文档描述了 `tests/test_gns3_create_link.py` 中的测试用例，该测试文件为 `src/gns3_copilot/tools_v2/gns3_create_link.py` 模块提供全面的测试覆盖。

## 测试统计

- **总测试用例数**: 35个
- **代码覆盖率**: 99%
- **测试类别**: 8个主要测试类

## 测试结构

### 1. TestGNS3LinkToolInitialization (3个测试)
测试工具的基本初始化和属性
- `test_tool_name_and_description`: 验证工具名称和描述
- `test_tool_inheritance`: 验证继承自BaseTool
- `test_tool_attributes`: 验证必需属性存在

### 2. TestGNS3LinkToolInputValidation (9个测试)
测试输入验证逻辑
- `test_empty_input`: 空输入处理
- `test_invalid_json`: 无效JSON输入
- `test_missing_project_id`: 缺少project_id
- `test_empty_links_array`: 空链接数组
- `test_links_not_array`: 链接不是数组
- `test_missing_links_field`: 缺少links字段
- `test_link_missing_required_fields`: 链接定义缺少必需字段
- `test_link_with_none_values`: 包含None值
- `test_link_with_empty_strings`: 包含空字符串

### 3. TestGNS3LinkToolAPIVersionHandling (4个测试)
测试API版本处理
- `test_api_version_2_initialization`: API版本2初始化
- `test_api_version_3_initialization`: API版本3初始化
- `test_unsupported_api_version`: 不支持的API版本
- `test_default_api_version`: 默认API版本

### 4. TestGNS3LinkToolSuccessScenarios (3个测试)
测试成功场景
- `test_single_link_creation`: 单个链接创建
- `test_multiple_links_creation`: 多个链接创建
- `test_port_search_with_adapter_port_numbers`: 特定适配器/端口号搜索

### 5. TestGNS3LinkToolErrorHandling (6个测试)
测试错误处理
- `test_node_not_found`: 节点未找到
- `test_port_not_found`: 端口未找到
- `test_node_without_ports`: 节点无端口信息
- `test_link_creation_exception`: 链接创建异常
- `test_connector_exception`: 连接器异常
- `test_node_retrieval_exception`: 节点检索异常

### 6. TestGNS3LinkToolMixedSuccessFailure (1个测试)
测试混合成功和失败场景
- `test_mixed_success_and_failure`: 混合成功和失败的链接创建

### 7. TestGNS3LinkToolEdgeCases (5个测试)
测试边界条件
- `test_unicode_port_names`: Unicode端口名
- `test_very_long_port_names`: 超长端口名
- `test_special_characters_in_ids`: ID中的特殊字符
- `test_large_number_of_links`: 大量链接
- `test_empty_string_values`: 空字符串值

### 8. TestGNS3LinkToolIntegration (2个测试)
集成测试
- `test_complete_workflow`: 完整工作流程测试
- `test_json_parsing_edge_cases`: JSON解析边界情况

### 9. TestGNS3LinkToolLogging (2个测试)
测试日志功能
- `test_logging_on_success`: 成功操作日志
- `test_logging_on_failure`: 失败操作日志

## 测试特点

### Mock策略
- 使用`unittest.mock`模拟外部依赖
- 模拟`Gns3Connector`和`Link`类
- 使用`patch.dict`管理环境变量

### 环境变量测试
- 测试API版本2和3的配置
- 测试无效API版本处理
- 测试默认配置行为

### 错误处理覆盖
- 网络连接错误
- 数据验证错误
- JSON解析错误
- 节点和端口不存在错误

### 边界条件测试
- Unicode字符处理
- 超长字符串处理
- 大数据量处理
- 特殊字符处理

## 运行测试

### 单独运行此测试文件
```bash
python -m pytest tests/test_gns3_create_link.py -v
```

### 运行带覆盖率的测试
```bash
python -m pytest tests/test_gns3_create_link.py --cov=gns3_copilot.tools_v2.gns3_create_link --cov-report=term-missing
```

### 运行所有测试
```bash
python -m pytest tests/ -v
```

## GitHub Actions集成

此测试文件已集成到项目的CI/CD流程中（`.github/workflows/ci.yaml`），包括：
- 多Python版本测试（3.10, 3.11, 3.12, 3.13）
- 代码质量检查
- 测试覆盖率报告
- 自动化部署触发

## 测试数据

测试使用模拟数据，包括：
- 模拟节点数据（路由器、交换机等）
- 模拟端口配置
- 模拟链接创建响应
- 各种错误场景数据

## 维护说明

1. **添加新功能时**: 添加对应的测试用例
2. **修改API时**: 更新相关测试的mock配置
3. **修复bug时**: 添加回归测试
4. **性能优化时**: 确保测试覆盖率不下降

## 依赖项

- `pytest`: 测试框架
- `unittest.mock`: 模拟框架
- `json`: JSON处理
- `os`: 环境变量管理
- `pytest-cov`: 覆盖率报告（可选）
