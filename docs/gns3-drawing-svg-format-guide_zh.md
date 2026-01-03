# GNS3 绘图 SVG 格式指南

本文档详细说明 GNS3 绘图（Drawing）功能中使用的 SVG 格式、参数和内容结构。

## 目录

- [概述](#概述)
- [GNS3 绘图对象结构](#gns3-绘图对象结构)
- [SVG 元素类型](#svg-元素类型)
  - [矩形 (rect)](#矩形-rect)
  - [椭圆 (ellipse)](#椭圆-ellipse)
  - [文本 (text)](#文本-text)
  - [线条 (line)](#线条-line)
- [通用 SVG 属性](#通用-svg-属性)
- [GNS3 绘图属性](#gns3-绘图属性)
  - [坐标系统](#坐标系统)
  - [设备坐标参考点](#重要设备坐标参考点)
  - [设备节点连接点](#设备节点连接点)
  - [线缆连接方式](#线缆连接方式)
  - [绘图位置计算方法](#绘图位置计算方法)
  - [锁定状态](#锁定状态)
  - [旋转角度](#旋转角度)
- [实际应用示例](#实际应用示例)
- [最佳实践](#最佳实践)

---

## 概述

GNS3 的绘图功能允许在项目画布上添加自定义图形元素，用于：
- 网络区域划分和分组
- 添加标签和注释
- 创建背景装饰
- 增强拓扑图的可读性

所有绘图都使用 SVG（Scalable Vector Graphics）格式定义，这是一种基于 XML 的矢量图形格式。

**⚠️ 重要提示**：在使用 GNS3 绘图功能时，请注意以下关键概念：

1. **坐标系统**：绘图和设备的坐标都表示**左上角**位置（详见 [GNS3 绘图属性 - 坐标系统](#gns3-绘图属性)）
2. **旋转中心**：旋转是以左上角为中心，而非图形中心（详见 [旋转角度](#旋转角度)）
3. **设备尺寸**：设备一般尺寸为 60 像素，但实际尺寸需从 gns3-server-api 接口获取（详见 [设备坐标参考点](#重要设备坐标参考点)）
4. **线缆连接**：线缆在绘图层面连接到设备的**中心点**，而非端口位置（详见 [线缆连接方式](#线缆连接方式)）
5. **连接点位**：设备有 8 个连接点，位于设备外部向内 10 像素处（详见 [设备节点连接点](#设备节点连接点)）
6. **位置计算**：创建连接线时需精确计算坐标（详见 [绘图位置计算方法](#绘图位置计算方法)）

---

## GNS3 绘图对象结构

### API 返回格式

```json
{
  "project_id": "UUID",
  "total_drawings": 8,
  "drawings": [
    {
      "drawing_id": "UUID",
      "svg": "...",
      "x": -376,
      "y": -381,
      "z": 1,
      "locked": false,
      "rotation": 0
    }
  ]
}
```

### 字段说明

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `drawing_id` | string | 是 | 绘图唯一标识符（UUID） |
| `svg` | string | 是 | SVG 代码，包含绘图内容 |
| `x` | integer | 是 | 绘图在画布上的 X 坐标 |
| `y` | integer | 是 | 绘图在画布上的 Y 坐标 |
| `z` | integer | 是 | Z 轴层级，控制显示顺序（数值越大越靠前） |
| `locked` | boolean | 是 | 是否锁定绘图（锁定后无法编辑） |
| `rotation` | integer | 是 | 旋转角度（0-360 度） |

---

## SVG 元素类型

### 矩形 (rect)

用于创建矩形框，常用于表示网络区域或分组。

#### 基本结构

```svg
<svg height="131" width="391">
  <rect fill="#ffffff" fill-opacity="1" height="131" width="391"
        stroke="#000000" stroke-width="2" stroke-dasharray="undefined"
        rx="0" ry="0" />
</svg>
```

#### 属性详解

| 属性 | 类型 | 说明 | 常见值 |
|------|------|------|---------|
| **画布属性** |
| `width` | number | SVG 画布宽度 | 100, 200, 391 |
| `height` | number | SVG 画布高度 | 100, 131 |
| **矩形属性** |
| `x` | number | 矩形左上角 X 坐标（相对于 SVG） | 0, 10 |
| `y` | number | 矩形左上角 Y 坐标（相对于 SVG） | 0, 30 |
| `width` | number | 矩形宽度 | 100, 391 |
| `height` | number | 矩形高度 | 100, 131 |
| `rx` | number | X 方向圆角半径 | 0（直角） |
| `ry` | number | Y 方向圆角半径 | 0（直角） |

#### 实际示例

```svg
<!-- 391x131 像素的白色矩形，黑色边框 -->
<svg height="131" width="391">
  <rect fill="#ffffff" fill-opacity="1" height="131" width="391"
        stroke="#000000" stroke-width="2" stroke-dasharray="undefined"
        rx="0" ry="0" />
</svg>
```

**用途**：分组框、区域背景、边界标记

---

### 椭圆 (ellipse)

用于创建圆形或椭圆形，常用于表示网络区域或节点分组。

#### 基本结构

```svg
<svg height="119" width="488">
  <ellipse fill="#ffffff" fill-opacity="1" cx="244" cy="59.5"
           rx="244" ry="59.5" stroke="#000000" stroke-width="2"
           stroke-dasharray="undefined" />
</svg>
```

#### 属性详解

| 属性 | 类型 | 说明 | 常见值 |
|------|------|------|---------|
| **画布属性** |
| `width` | number | SVG 画布宽度 | 100, 200, 488 |
| `height` | number | SVG 画布高度 | 100, 119 |
| **椭圆属性** |
| `cx` | number | 椭圆中心 X 坐标 | 100, 244 |
| `cy` | number | 椭圆中心 Y 坐标 | 50, 59.5 |
| `rx` | number | X 方向半径（半宽） | 100, 244 |
| `ry` | number | Y 方向半径（半高） | 50, 59.5 |

**注意**：当 `rx = ry` 时，椭圆为正圆。

#### 实际示例

```svg
<!-- 488x119 像素的白色椭圆 -->
<svg height="119" width="488">
  <ellipse fill="#ffffff" fill-opacity="1" cx="244" cy="59.5"
           rx="244" ry="59.5" stroke="#000000" stroke-width="2"
           stroke-dasharray="undefined" />
</svg>
```

**用途**：圆形区域分组、网络区域标识、背景装饰

---

### 文本 (text)

用于添加标签、注释和说明文字。

#### 基本结构

```svg
<svg height="100" width="100">
  <text fill="#000000" fill-opacity="1.0" font-family="Noto Sans"
        font-size="11" font-weight="bold">Area 0</text>
</svg>
```

或（带命名空间的格式）：

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="50">
  <text x="10" y="30" font-size="14">Label 1</text>
</svg>
```

#### 属性详解

| 属性 | 类型 | 说明 | 常见值 |
|------|------|------|---------|
| **画布属性** |
| `width` | number | SVG 画布宽度 | 100 |
| `height` | number | SVG 画布高度 | 50, 100 |
| **命名空间** |
| `xmlns` | string | SVG 命名空间 | `http://www.w3.org/2000/svg` |
| **文本属性** |
| `x` | number | 文本起始 X 坐标 | 10, 相对位置 |
| `y` | number | 文本基线 Y 坐标 | 30, 相对位置 |
| `fill` | color | 文本颜色 | `#000000`（黑色） |
| `fill-opacity` | number | 文本透明度 | 0.0-1.0 |
| `font-family` | string | 字体家族 | Noto Sans, Arial |
| `font-size` | number | 字体大小 | 11, 14（像素） |
| `font-weight` | string | 字体粗细 | normal, bold |

**文本内容**：直接放在 `<text>` 标签内，支持中文和英文。

#### 实际示例

```svg
<!-- 简单文本标签 -->
<svg height="100" width="100">
  <text fill="#000000" fill-opacity="1.0" font-family="Noto Sans"
        font-size="11" font-weight="bold">Area 0</text>
</svg>

<!-- 带命名空间的文本 -->
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="50">
  <text x="10" y="30" font-size="14">Label 1</text>
</svg>

<!-- 中文文本（注意：\n 在 SVG 中需要特殊处理） -->
<svg height="100" width="100">
  <text fill="#000000" fill-opacity="1.0" font-family="Noto Sans"
        font-size="11" font-weight="bold">哈哈哈\n哈和</text>
</svg>

<!-- 空文本占位符 -->
<svg height="100" width="100">
  <text fill="#000000" fill-opacity="1.0" font-family="Noto Sans"
        font-size="11" font-weight="bold"></text>
</svg>
```

**用途**：区域标签、设备名称、网络注释、说明文字

**注意事项**：
- 换行符 `\n` 在纯 SVG 中不会自动换行，需要使用 `<tspan>` 元素
- GNS3 可能对换行有特殊处理
- 中文字符需要支持 UTF-8 编码

---

### 线条 (line)

用于创建直线，可用于连接元素或分割区域。

#### 基本结构

```svg
<svg height="0" width="100">
  <line stroke="#000000" stroke-width="2" x1="0" x2="200"
        y1="0" y2="0" stroke-dasharray="none" />
</svg>
```

#### 属性详解

| 属性 | 类型 | 说明 | 常见值 |
|------|------|------|---------|
| **画布属性** |
| `width` | number | SVG 画布宽度 | 100 |
| `height` | number | SVG 画布高度 | 0（线条） |
| **线条属性** |
| `x1` | number | 起点 X 坐标 | 0 |
| `y1` | number | 起点 Y 坐标 | 0 |
| `x2` | number | 终点 X 坐标 | 200 |
| `y2` | number | 终点 Y 坐标 | 0 |

#### 实际示例

```svg
<!-- 水平黑色线，宽度 2 像素 -->
<svg height="0" width="100">
  <line stroke="#000000" stroke-width="2" x1="0" x2="200"
        y1="0" y2="0" stroke-dasharray="none" />
</svg>
```

**用途**：分割线、连接标识、边界标记

---

## 通用 SVG 属性

所有 SVG 元素都支持以下通用属性：

### 填充属性

| 属性 | 类型 | 说明 | 常见值 |
|------|------|------|---------|
| `fill` | color | 填充颜色 | `#ffffff`（白）、`#ff0000`（红） |
| `fill-opacity` | number | 填充透明度 | 0.0（透明）- 1.0（不透明） |

### 描边属性

| 属性 | 类型 | 说明 | 常见值 |
|------|------|------|---------|
| `stroke` | color | 描边颜色 | `#000000`（黑）、`#cccccc`（灰） |
| `stroke-width` | number | 描边宽度 | 1, 2, 3（像素） |
| `stroke-dasharray` | string/array | 虚线样式 | `none`、`undefined`、`5,5` |

**stroke-dasharray 说明**：
- `none`：无虚线（实线）
- `undefined`：实线（GNS3 默认）
- `5,5`：5 像素实线，5 像素空白
- `10,5,2,5`：自定义虚线模式

---

## GNS3 绘图属性

### 坐标系统

**⚠️ 重要**：GNS3 绘图的坐标（`x`, `y`）表示 SVG 图形的**左上角坐标**。

- **X 坐标**：水平位置，可为正数或负数
- **Y 坐标**：垂直位置，可为正数或负数
- **Z 坐标**：层级，数值越大显示越靠前

**示例**：
```json
{
  "x": -376,   // 左侧偏移
  "y": -381,   // 上方偏移
  "z": 1        // 第一层级
}
```

#### 重要：设备坐标参考点

**关键发现**：在 GNS3 中，设备坐标（`node.x`, `node.y`）表示设备图标的**左上角**，而不是中心点。

**⚠️ 重要**：设备节点的坐标同样为左上角，一般设备为 60 像素的矩形，但**实际尺寸应以从 gns3-server-api 接口获取的数据为准**。

**对绘图位置的影响**：

当创建需要与设备对齐或引用设备的绘图时（例如围绕设备的区域标注）：

1. **设备位置**：GNS3 API 返回的坐标是设备图标的左上角
2. **中心点计算**：要计算设备的中心点，使用以下公式：
   ```python
   node_center_x = node.x + (node_width / 2)
   node_center_y = node.y + (node_height / 2)
   ```
3. **设备尺寸**：
   - 一般设备：通常为 60 像素的矩形
   - 实际尺寸：**必须从 gns3-server-api 接口获取的节点数据为准**（`node.width`, `node.height`）
4. **绘图对齐**：创建应该包含设备的区域标注时，计算应该使用设备的中心点，而不是左上角

**示例**：
```python
# 如果设备在 (100, 200)，设备大小为 70x70 像素
node_x = 100  # 左上角
node_y = 200  # 左上角
device_width = 70
device_height = 70

# 计算中心点
center_x = node_x + (device_width / 2)  # = 135
center_y = node_y + (device_height / 2)  # = 235
```

**测试方法**：要验证您的 GNS3 设置中的设备坐标参考点，可以在设备位置创建小的测试标记（例如 10x10 像素的矩形），观察它们相对于设备图标出现在什么位置。

#### 设备节点连接点

**⚠️ 重要**：GNS3 设备节点有 8 个连接点位，用于创建连接线。

**连接点位置**：
- 连接点位于**设备节点外部向内 10 个像素的位置**
- 8 个点位均匀分布在设备的四个边：
  - 上边：2 个点位（左、右）
  - 下边：2 个点位（左、右）
  - 左边：2 个点位（上、下）
  - 右边：2 个点位（上、下）

**连接点示意图**：

```
  上边点1 ──────── 上边点2
  │                   │
左上点               右上点
  │                   │
  │       设备        │
  │                   │
左下点               右下点
  │                   │
  下边点1 ──────── 下边点2
```

**获取连接点位置**：
连接点的具体坐标需要通过 GNS3 API 获取，或根据设备位置和尺寸计算：
- 向内 10 像素意味着连接点在设备边框内部 10 像素处
- 可用于精确定位连接线的起点和终点

#### 线缆连接方式

**⚠️ 重要发现**：根据 GNS3 web UI 源代码（`gns3/items/link_item.py`）分析，**线缆在绘图层面是连接到设备的中心点，而不是连接到具体的端口位置**。

**核心代码分析**：

在 `gns3/items/link_item.py` 的 `adjust()` 方法中（第 427-455 行），关键代码如下：

```python
self.prepareGeometryChange()
source_rect = self._source_item.boundingRect()
self.source = self.mapFromItem(
    self._source_item, 
    source_rect.width() / 2.0, 
    source_rect.height() / 2.0
)

if not self._adding_flag:
    destination_rect = self._destination_item.boundingRect()
    self.destination = self.mapFromItem(
        self._destination_item, 
        destination_rect.width() / 2.0, 
        destination_rect.height() / 2.0
    )
```

**关键要点**：

1. **连线起点**：源设备节点的中心点（`width/2.0, height/2.0`）
2. **连线终点**：目标设备节点的中心点（`width/2.0, height/2.0`）
3. **连接方式**：GNS3 的线缆绘制使用**中心到中心**的连接方式

**端口的作用**：

虽然线缆在图形上连接到设备中心点，但端口信息仍然非常重要：

- **逻辑连接（Backend）**：端口选择主要用于确定哪个适配器/端口被连接
- **端口标签**：GNS3 可以显示端口名称标签（通过 `_draw_port_labels` 方法）
- **标签位置**：端口标签是额外的显示元素，不影响连线的实际连接点位置
- **图形表现**：在图形界面上，连线始终从一个设备的中心画到另一个设备的中心

**多连线处理**：

当两个设备之间有多条连线时，GNS3 会进行特殊处理：

```python
# _computeMultiLink() 方法会应用偏移量
# 让多条连线并排显示，避免重叠
```

- **偏移量计算**：多条连线时会计算并应用偏移量
- **并排显示**：连线会并排排列，保持清晰可读
- **基础连接点**：即使有多条连线，基础连接点仍然是设备的中心点

**对绘图的影响**：

了解线缆连接方式对创建自定义绘图非常重要：

1. **连线可视化**：当创建与设备连线相关的标注或绘图时，应考虑连线从设备中心发出
2. **端口标注**：如果需要标注端口信息，应在设备中心附近或端口标签位置添加
3. **多连线场景**：处理多连线设备时，需要考虑连线的偏移显示效果
4. **视觉效果**：理解中心到中心的连接方式有助于创建更协调的视觉布局

**实际应用**：

```python
# 计算设备中心点（连线连接点）
def get_device_center(node):
    center_x = node.x + (node.width / 2)
    center_y = node.y + (node.height / 2)
    return center_x, center_y

# 示例：在连线附近添加标注
node1_center = get_device_center(node1)
node2_center = get_device_center(node2)

# 连线中点（适合放置标注）
midpoint_x = (node1_center[0] + node2_center[0]) / 2
midpoint_y = (node1_center[1] + node2_center[1]) / 2
```

**数据来源说明**：

本节信息基于 GNS3 web UI 源代码分析得出：
- 源文件：`gns3/items/link_item.py`
- 分析方法：代码审查和关键逻辑提取
- 适用版本：GNS3 web UI 最新版本
- 可靠性：基于实际实现代码，准确反映 GNS3 的行为

#### 绘图位置计算方法

**⚠️ 重要**：当需要在设备之间创建连接线或绘图时，需要精确计算 SVG 坐标。

**计算公式**：

```
SVG 坐标 = 设备间距离 + 设备相邻最近的内部点位的距离 + 设备高度
```

**详细说明**：

1. **设备间距离**：两个设备中心点或左上角之间的距离
2. **设备相邻最近的内部点位的距离**：从设备边框向内 10 像素的连接点位置
3. **设备高度**：设备的高度（需要从 gns3-server-api 获取）

**计算示例**：

假设有两个设备 R-1 和 R-2：
- R-1 位置：(100, 200)，宽度 60，高度 60
- R-2 位置：(400, 200)，宽度 60，高度 60

**步骤 1：计算设备间距离**
```python
# 水平距离
horizontal_distance = R2_x - R1_x = 400 - 100 = 300
```

**步骤 2：找到相邻最近的连接点**
- R-1 右侧连接点：x = 100 + 60 - 10 = 150
- R-2 左侧连接点：x = 400 + 10 = 410

**步骤 3：计算 SVG 坐标**
```python
# 如果创建从 R-1 到 R-2 的连接线
svg_x = R1_x  # 从 R-1 左上角开始
svg_y = R1_y
svg_width = horizontal_distance + 10 + device_height  # 距离 + 内部点位 + 高度
```

**逐步更新方法**：

**⚠️ 实用建议**：可以先在 R-1 附近创建一个绘图内容，然后使用更新的方法依次调整：

1. **初始创建**：在 R-1 附近创建绘图（小尺寸测试）
2. **第一次更新**：调整绘图位置，使其靠近 R-2
3. **第二次更新**：调整绘图高度，使其与设备高度相同
4. **第三次更新**：精确定位，使绘图靠近最近的 8 个连接点中的合适点位

这种方法可以逐步验证每次更新的效果，避免一次性计算错误。

### 锁定状态

- `locked: true`：绘图被锁定，无法编辑或移动
- `locked: false`：绘图可编辑

### 旋转角度

**⚠️ 重要**：旋转是以**左上角坐标为中心**进行旋转的，而不是以图形中心点旋转。

- 单位：度数（0-360）
- 0：无旋转
- 90：顺时针旋转 90 度
- 180：旋转 180 度
- -90：逆时针旋转 90 度

---

## 实际应用示例

### 示例 1：创建区域分组

```json
{
  "project_id": "2245149a-71c8-4387-9d1f-441a683ef7e7",
  "drawings": [
    {
      "svg": "<svg height=\"131\" width=\"391\"><rect fill=\"#ffffff\" fill-opacity=\"1\" height=\"131\" width=\"391\" stroke=\"#000000\" stroke-width=\"2\" stroke-dasharray=\"undefined\" rx=\"0\" ry=\"0\" /></svg>",
      "x": -376,
      "y": -381,
      "z": 1,
      "locked": false,
      "rotation": 0
    }
  ]
}
```

**说明**：创建 391×131 像素的白色矩形框，用于标记 "Area 0" 区域。

---

### 示例 2：添加区域标签

```json
{
  "drawings": [
    {
      "svg": "<svg height=\"100\" width=\"100\"><text fill=\"#000000\" fill-opacity=\"1.0\" font-family=\"Noto Sans\" font-size=\"11\" font-weight=\"bold\">Area 0</text></svg>",
      "x": -573,
      "y": -272,
      "z": 1,
      "locked": false,
      "rotation": 0
    }
  ]
}
```

**说明**：在区域内添加 "Area 0" 标签。

---

### 示例 3：旋转的标签

```json
{
  "drawings": [
    {
      "svg": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"100\" height=\"50\"><text x=\"10\" y=\"30\" font-size=\"14\">Label 2</text></svg>",
      "x": 166,
      "y": -253,
      "z": 1,
      "locked": false,
      "rotation": 90
    }
  ]
}
```

**说明**：标签旋转 90 度显示。

---

### 示例 4：圆形分组

```json
{
  "drawings": [
    {
      "svg": "<svg height=\"119\" width=\"488\"><ellipse fill=\"#ffffff\" fill-opacity=\"1\" cx=\"244\" cy=\"59.5\" rx=\"244\" ry=\"59.5\" stroke=\"#000000\" stroke-width=\"2\" stroke-dasharray=\"undefined\" /></svg>",
      "x": -891,
      "y": 66,
      "z": 1,
      "locked": false,
      "rotation": 0
    }
  ]
}
```

**说明**：使用椭圆创建圆形分组区域。

---

### 示例 5：中文注释

```json
{
  "drawings": [
    {
      "svg": "<svg height=\"100\" width=\"100\"><text fill=\"#000000\" fill-opacity=\"1.0\" font-family=\"Noto Sans\" font-size=\"11\" font-weight=\"bold\">哈哈哈\\n哈和</text></svg>",
      "x": -596,
      "y": -43,
      "z": 1,
      "locked": false,
      "rotation": 0
    }
  ]
}
```

**说明**：添加中文注释（注意换行符的处理）。

---

## 最佳实践

### 1. 尺寸规划

- **矩形框**：建议使用标准尺寸（如 200×100, 300×150）便于对齐
- **文本区域**：预留足够空间（至少 100×50）容纳文字
- **椭圆区域**：确保宽高比合理，避免过于扁平

### 2. 颜色选择

- **背景填充**：使用浅色（`#ffffff`, `#f0f0f0`）增强可读性
- **边框描边**：使用深色（`#000000`, `#333333`）清晰标识边界
- **文字颜色**：与背景形成对比（白底黑字，深底白字）

### 3. 图层管理

- **底层（z=0）**：背景装饰、分隔线
- **中层（z=1）**：区域框、标签
- **顶层（z=2+）**：重要注释、高亮元素

### 4. 坐标对齐

- 使用网格对齐（GNS3 默认 50 像素网格）
- 保持元素间距一致（建议至少 20 像素间隔）
- 预留足够空间给节点和连接线

### 5. 文字排版

- **字体大小**：标题 14-16px，普通文字 11-12px
- **字体选择**：使用通用字体（Noto Sans, Arial）确保兼容性
- **多行文本**：使用 `<tspan>` 或拆分为多个文本元素

### 6. 性能优化

- 避免过度复杂的 SVG 代码
- 使用简单的几何形状而非复杂路径
- 限制同屏绘图数量（建议 < 20 个）

### 7. 逐步更新绘图方法

**⚠️ 实用技巧**：当创建与多个设备相关的复杂绘图时，推荐使用逐步更新方法：

1. **初始创建**：在第一个设备（如 R-1）附近创建绘图
   - 使用小尺寸或简化版本进行测试
   - 验证基本位置和显示效果

2. **第一次更新**：调整位置使其靠近第二个设备（如 R-2）
   - 移动绘图使其跨越到第二个设备附近
   - 确保绘图能够覆盖两个设备之间的区域

3. **第二次更新**：调整尺寸使其与设备高度相同
   - 根据设备的实际高度调整绘图的尺寸
   - 确保绘图与设备视觉上协调一致

4. **第三次更新**：精确定位到最近的连接点
   - 将绘图移动到靠近设备的 8 个连接点中的合适点位
   - 确保连接线或标注与设备的连接点对齐

**优势**：
- 每次更新都可以验证效果
- 避免一次性计算导致的错误
- 便于调试和调整
- 可以逐步微调位置和尺寸

---

## 常见问题

### Q1: 如何创建带圆角的矩形？

设置 `rx` 和 `ry` 属性：

```svg
<rect rx="10" ry="10" ... />
```

### Q2: 如何创建虚线边框？

设置 `stroke-dasharray`：

```svg
<rect stroke-dasharray="5,5" ... />
```

### Q3: 文本如何换行？

使用 `<tspan>` 元素：

```svg
<svg height="100" width="100">
  <text x="10" y="30">
    <tspan x="10" dy="0">第一行</tspan>
    <tspan x="10" dy="20">第二行</tspan>
  </text>
</svg>
```

### Q4: 如何更改颜色？

使用十六进制颜色代码：
- `#ffffff`：白色
- `#000000`：黑色
- `#ff0000`：红色
- `#00ff00`：绿色
- `#0000ff`：蓝色

### Q5: 如何旋转绘图？

设置 `rotation` 属性（单位：度数）：
- `rotation: 0`：无旋转
- `rotation: 90`：顺时针 90 度
- `rotation: -90`：逆时针 90 度

---

## 相关资源

- [SVG 规范（W3C）](https://www.w3.org/TR/SVG/)
- [MDN SVG 文档](https://developer.mozilla.org/en-US/docs/Web/SVG)
- [GNS3 官方文档](https://docs.gns3.com/)
- [GNS3 API 文档](https://api.gns3.net/)

---

**文档版本**：1.0  
**最后更新**：2025-01-02  
**维护者**：GNS3 Copilot Team
