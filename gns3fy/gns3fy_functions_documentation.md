# GNS3fy 函数功能分析文档

## 概述
`gns3fy.py` 文件是一个用于与 GNS3 服务器控制器 API 交互的 Python 库。该文件包含了三个主要的类：`Gns3Connector`、`Link`、`Node` 和 `Project`，以及一个装饰器函数和一些验证函数。

## 常量定义
- **NODE_TYPES**: 支持的节点类型列表（cloud, nat, ethernet_hub 等）
- **CONSOLE_TYPES**: 支持的控制台类型列表（vnc, telnet, http 等）
- **LINK_TYPES**: 支持的链路类型列表（ethernet, serial）

---

## 1. Gns3Connector 类

### 核心连接与会话管理

#### `__init__(self, url=None, user=None, cred=None, verify=False, api_version=2)`
**功能**: 初始化 GNS3 连接器
- 设置基础 URL、用户凭证、SSL 验证选项
- 创建会话对象并配置必要的参数

#### `_create_session(self)`
**功能**: 创建 requests.Session 对象
- 设置默认的 Accept 头部
- 配置身份验证信息（如果提供）

#### `http_call(self, method, url, data=None, json_data=None, headers=None, verify=False, params=None)`
**功能**: 执行 HTTP 请求操作
- 支持所有 HTTP 方法（GET, POST, PUT, DELETE 等）
- 处理数据和 JSON 数据
- 错误处理和状态检查
- 统计 API 调用次数

### 服务器信息获取

#### `get_version(self)`
**功能**: 获取 GNS3 服务器版本信息
- 返回服务器版本详细信息

### 项目管理

#### `projects_summary(self, is_print=True)`
**功能**: 获取服务器上项目的摘要信息
- 显示项目名称、ID、节点数、链路数、状态
- 可选择打印或返回元组列表

#### `get_projects(self)`
**功能**: 获取服务器上所有项目列表

#### `get_project(self, name=None, project_id=None)`
**功能**: 根据名称或 ID 检索特定项目

#### `create_project(self, **kwargs)`
**功能**: 创建新项目
- 必需参数：name

#### `delete_project(self, project_id)`
**功能**: 从服务器删除项目

### 模板管理

#### `templates_summary(self, is_print=True)`
**功能**: 获取服务器上模板的摘要信息
- 显示模板名称、ID、类型、是否内置、控制台类型、类别

#### `get_templates(self)`
**功能**: 获取服务器上定义的所有模板

#### `get_template(self, name=None, template_id=None)`
**功能**: 根据名称或 ID 检索特定模板

#### `update_template(self, name=None, template_id=None, **kwargs)`
**功能**: 更新模板属性

#### `create_template(self, **kwargs)`
**功能**: 创建新模板
- 必需参数：name, template_type
- 默认 compute_id 为 'local'

#### `delete_template(self, name=None, template_id=None)`
**功能**: 删除模板

### 节点和链路操作

#### `get_nodes(self, project_id)`
**功能**: 检索项目中定义的所有节点

#### `get_node(self, project_id, node_id)`
**功能**: 根据 ID 返回特定节点

#### `get_links(self, project_id)`
**功能**: 检索项目中定义的所有链路

#### `get_link(self, project_id, link_id)`
**功能**: 根据 ID 返回特定链路

### 计算节点管理

#### `get_computes(self)`
**功能**: 获取计算节点列表
- 返回包含 CPU/内存使用情况的字典列表

#### `get_compute(self, compute_id="local")`
**功能**: 获取特定计算节点信息

#### `get_compute_images(self, emulator, compute_id="local")`
**功能**: 获取计算节点可用的镜像列表
- 支持不同的模拟器类型（qemu, iou, docker 等）

#### `upload_compute_image(self, emulator, file_path, compute_id="local")`
**功能**: 上传镜像文件到计算节点

#### `get_compute_ports(self, compute_id="local")`
**功能**: 获取计算节点使用的端口信息

---

## 2. 装饰器函数

#### `verify_connector_and_id(f)`
**功能**: 验证连接器对象和相应对象的 ID
- 检查 Gns3Connector 是否已分配
- 检查 project_id 是否存在
- 针对 Node 和 Link 类执行特定的 ID 检查

---

## 3. Link 类

### 验证方法

#### `_valid_link_type(cls, value)`
**功能**: 验证链路类型是否有效

#### `_valid_suspend(cls, value)`
**功能**: 验证暂停状态是否为布尔值

#### `_valid_filters(cls, value)`
**功能**: 验证过滤器是否为字典类型

### 核心操作

#### `_update(self, data_dict)`
**功能**: 用字典数据更新对象属性

#### `get(self)`
**功能**: 从链路端点检索信息
- 需要 project_id, connector, link_id

#### `delete(self)`
**功能**: 从项目中删除链路端点
- 成功后将 link_id 设置为 None

#### `create(self)`
**功能**: 创建链路端点
- 需要 project_id, connector, nodes

#### `update(self, **kwargs)`
**功能**: 通过关键字参数更新链路实例属性

---

## 4. Node 类

### 验证方法

#### `_valid_node_type(cls, value)`
**功能**: 验证节点类型是否有效

#### `_valid_console_type(cls, value)`
**功能**: 验证控制台类型是否有效

#### `_valid_status(cls, value)`
**功能**: 验证节点状态是否有效（stopped, started, suspended）

### 核心操作

#### `_update(self, data_dict)`
**功能**: 用字典数据更新对象属性

#### `get(self, get_links=True)`
**功能**: 检索节点信息
- 可选择是否同时检索相关链路

#### `get_links(self)`
**功能**: 检索该节点的所有链路
- 将链路保存在 links 属性中

### 节点生命周期管理

#### `start(self)`
**功能**: 启动节点

#### `stop(self)`
**功能**: 停止节点

#### `reload(self)`
**功能**: 重新加载节点

#### `suspend(self)`
**功能**: 暂停节点

#### `update(self, **kwargs)`
**功能**: 更新节点实例属性

#### `create(self)`
**功能**: 创建节点
- 基于模板或 template_id 获取属性
- 需要 project_id, connector, compute_id（默认 "local"）

#### `delete(self)`
**功能**: 从项目中删除节点
- 成功后将 node_id 和 name 设置为 None

### 文件操作

#### `get_file(self, path)`
**功能**: 检索节点目录中的文件内容

#### `write_file(self, path, data)`
**功能**: 在指定节点文件路径放置文件内容
- 主要用于 Docker 镜像配置

---

## 5. Project 类

### 验证方法

#### `_valid_status(cls, value)`
**功能**: 验证项目状态（opened, closed）

### 核心操作

#### `_update(self, data_dict)`
**功能**: 用字典数据更新对象属性

#### `get(self, get_links=True, get_nodes=True, get_stats=True)`
**功能**: 检索项目信息
- 可选择检索链路、节点、统计信息
- 自动检索快照和绘图（如果存在）

#### `create(self)`
**功能**: 创建项目
- 需要 name 和 connector

#### `update(self, **kwargs)`
**功能**: 更新项目实例属性

#### `delete(self)`
**功能**: 从服务器删除项目
- 成功后将 project_id 和 name 设置为 None

### 项目状态管理

#### `close(self)`
**功能**: 在服务器上关闭项目

#### `open(self)`
**功能**: 在服务器上打开项目

#### `get_stats(self)`
**功能**: 检索项目统计信息

### 文件操作

#### `get_file(self, path)`
**功能**: 检索项目目录中的文件

#### `write_file(self, path, data)`
**功能**: 在项目文件路径放置文件内容

### 节点管理

#### `get_nodes(self)`
**功能**: 检索项目的所有节点

#### `get_links(self)`
**功能**: 检索项目的所有链路

#### `start_nodes(self, poll_wait_time=5)`
**功能**: 启动项目中的所有节点

#### `stop_nodes(self, poll_wait_time=5)`
**功能**: 停止项目中的所有节点

#### `reload_nodes(self, poll_wait_time=5)`
**功能**: 重新加载项目中的所有节点

#### `suspend_nodes(self, poll_wait_time=5)`
**功能**: 暂停项目中的所有节点

### 节点和链路查询

#### `nodes_summary(self, is_print=True)`
**功能**: 返回项目中节点的摘要信息
- 包含节点名称、状态、控制台端口、ID

#### `nodes_inventory(self)`
**功能**: 返回节点的清单样式字典
- 包含服务器、名称、控制台端口、类型等信息

#### `links_summary(self, is_print=True)`
**功能**: 返回项目中链路的摘要信息
- 显示连接的节点和端口信息

#### `_search_node(self, key, value)`
**功能**: 基于键值对搜索节点（内部方法）

#### `get_node(self, name=None, node_id=None)`
**功能**: 根据名称或 node_id 返回节点对象

#### `_search_link(self, key, value)`
**功能**: 基于键值对搜索链路（内部方法）

#### `get_link(self, link_id)`
**功能**: 根据 link_id 返回链路对象

### 节点和链路创建

#### `create_node(self, **kwargs)`
**功能**: 创建节点
- 需要 template 或 template_id

#### `create_link(self, node_a, port_a, node_b, port_b)`
**功能**: 创建链路
- 连接两个节点的指定端口

#### `delete_link(self, node_a, port_a, node_b, port_b)`
**功能**: 删除链路
- 根据节点和端口信息删除链路

### 快照管理

#### `get_snapshots(self)`
**功能**: 检索项目的快照列表

#### `_search_snapshot(self, key, value)`
**功能**: 基于键值对搜索快照（内部方法）

#### `get_snapshot(self, name=None, snapshot_id=None)`
**功能**: 根据名称或 snapshot_id 返回快照

#### `create_snapshot(self, name)`
**功能**: 创建项目快照

#### `delete_snapshot(self, name=None, snapshot_id=None)`
**功能**: 删除快照

#### `restore_snapshot(self, name=None, snapshot_id=None)`
**功能**: 恢复快照

### 布局和绘图

#### `arrange_nodes_circular(self, radius=120)`
**功能**: 将现有节点重新排列成圆形布局
- 自定义半径参数

#### `get_drawing(self, drawing_id=None)`
**功能**: 根据 drawing_id 返回绘图

#### `get_drawings(self)`
**功能**: 检索项目中的所有绘图

#### `create_drawing(self, svg, locked=False, x=10, y=10, z=1)`
**功能**: 创建绘图
- 需要 SVG 内容，可设置位置和锁定状态

#### `update_drawing(self, drawing_id, svg=None, locked=None, x=None, y=None, z=None)`
**功能**: 更新绘图属性

#### `delete_drawing(self, drawing_id=None)`
**功能**: 删除绘图

---

## 使用示例

### 基本连接
```python
# 创建连接器
server = Gns3Connector(url="http://localhost:3080")

# 获取版本信息
version = server.get_version()
```

### 项目操作
```python
# 创建项目
project = Project(name="my_lab", connector=server)
project.create()

# 创建节点
project.create_node(name="router1", template="vEOS")

# 创建链路
project.create_link("router1", "Ethernet0", "router2", "Ethernet0")
```

### 节点控制
```python
# 获取节点
node = project.get_node(name="router1")

# 启动节点
node.start()

# 停止节点
node.stop()
```

---

## 总结

这个库提供了与 GNS3 服务器进行完整交互的功能，包括：
- 项目和模板的完整生命周期管理
- 节点的创建、配置和控制
- 链路的创建和管理
- 快照和绘图功能
- 文件操作和配置管理

所有函数都设计为面向对象的方式，使用装饰器进行验证，确保操作的安全性和一致性。
