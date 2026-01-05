# GNS3 绘图 SVG 格式指南

本文档说明 GNS3 绘图功能中使用的 SVG 格式和商务风格颜色方案。

## 目录

- [概述](#概述)
- [颜色方案（商务专业风格）](#颜色方案商务专业风格)
- [SVG 元素类型](#svg-元素类型)
- [GNS3 绘图对象结构](#gns3-绘图对象结构)
- [实际应用示例](#实际应用示例)
- [最佳实践](#最佳实践)

---

## 概述

GNS3 绘图功能允许在项目画布上添加自定义图形元素，用于网络区域划分、标签注释和拓扑图可视化。所有绘图使用 SVG 格式定义。

### 核心特性

1. **坐标系统**：绘图和设备坐标表示**左上角**位置
2. **旋转中心**：旋转以左上角为中心
3. **设备尺寸**：设备通常为 60×60 像素，实际尺寸从 API 获取
4. **线缆连接**：线缆连接到设备中心点

---

## GNS3 坐标系统与绘图计算

### 1. 坐标系定义

GNS3 画布使用中心原点坐标系：

- **原点位置**：画布中心为 (0, 0)
- **Y 轴方向**：向下为正（+），向上为负（-）
- **X 轴方向**：向右为正（+），向左为负（-）

```
        Y-
         ↑
         |
    X- ←─┼──→ X+
         |
         ↓
        Y+
```

### 2. 设备节点坐标

- **坐标定义**：设备节点使用左上角坐标
- **默认尺寸**：60×60 像素
- **实际尺寸**：通过 API 接口获取准确的宽度和高度数值
- **SVG 坐标**：SVG 格式绘图也使用左上角坐标

### 3. 旋转行为

- **旋转中心**：GNS3 绘图旋转时以左上角坐标为圆心进行旋转
- **旋转角度**：0-360 度，顺时针方向为正
- **影响范围**：旋转会影响绘图在画布上的实际显示位置

---

## 连接绘图实现细节

### 场景描述

在两个设备节点之间绘制连接图形（如连线标注、区域覆盖等）。

### 实现步骤

#### 步骤 1：获取设备信息

通过 API 接口获取两个设备节点的信息：
- 设备节点坐标（左上角）
- 设备节点宽度（width）
- 设备节点高度（height）

#### 步骤 2：计算设备中心点

根据设备左上角坐标和尺寸，计算每个设备的中心点坐标：

```
center_x = x + width / 2
center_y = y + height / 2
```

#### 步骤 3：计算中心点之间的距离和角度

```
dx = center_x2 - center_x1
dy = center_y2 - center_y1

# 计算距离（直线距离）
distance = sqrt(dx² + dy²)

# 计算水平角度（弧度）
angle_rad = atan2(dy, dx)

# 转换为角度
angle_deg = angle_rad * (180 / π)
```

#### 步骤 4：确定绘图尺寸

根据计算结果确定 SVG 绘图的大小：

- **绘图长度/宽度**：使用两个设备中心点之间的距离
- **绘图高度/宽度**：使用两个设备节点宽度或高度的最大值

```
drawing_length = distance
drawing_height = max(height1, height2)
```

#### 步骤 5：计算绘图位置（考虑旋转）

重要：需要先计算距离和角度，然后计算绘图左上角位置，最后应用旋转。

**计算方法**：

1. **计算未旋转时的绘图左上角位置**：

```
# 从第一个设备中心点出发
drawing_x = center_x1
drawing_y = center_y1 - (drawing_height / 2)
```

2. **考虑旋转角度的影响**：

由于旋转是以左上角为圆心，旋转后图形的实际位置会发生变化。需要进行坐标变换：

```
# 旋转后的实际左上角位置（可选，根据具体需求调整）
rotated_x = drawing_x + (drawing_length / 2) * cos(angle_rad) - (drawing_height / 2) * sin(angle_rad) - (drawing_length / 2)
rotated_y = drawing_y + (drawing_length / 2) * sin(angle_rad) + (drawing_height / 2) * cos(angle_rad) - (drawing_height / 2)
```

3. **设置旋转参数**：

```
rotation = angle_deg  # 旋转角度
```

### 实现示例

```python
import math

def calculate_drawing_params(node1, node2, extra_height=20):
    """
    计算连接两个设备的绘图参数
    
    Args:
        node1: 第一个设备节点对象（包含 x, y, width, height）
        node2: 第二个设备节点对象（包含 x, y, width, height）
        extra_height: 额外高度（像素），用于容纳标注文字等
    
    Returns:
        dict: 包含 x, y, width, height, rotation 的绘图参数
    """
    # 步骤 1：获取设备信息
    x1, y1 = node1['x'], node1['y']
    w1, h1 = node1.get('width', 60), node1.get('height', 60)
    
    x2, y2 = node2['x'], node2['y']
    w2, h2 = node2.get('width', 60), node2.get('height', 60)
    
    # 步骤 2：计算设备中心点
    cx1 = x1 + w1 / 2
    cy1 = y1 + h1 / 2
    
    cx2 = x2 + w2 / 2
    cy2 = y2 + h2 / 2
    
    # 步骤 3：计算距离和角度
    dx = cx2 - cx1
    dy = cy2 - cy1
    
    distance = math.sqrt(dx ** 2 + dy ** 2)
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    
    # 步骤 4：确定绘图尺寸
    drawing_width = distance
    drawing_height = max(h1, h2) + extra_height
    
    # 步骤 5：计算绘图位置（从第一个设备中心点开始）
    drawing_x = cx1
    drawing_y = cy1 - (drawing_height / 2)
    
    return {
        'x': drawing_x,
        'y': drawing_y,
        'width': drawing_width,
        'height': drawing_height,
        'rotation': angle_deg
    }
```

### 注意事项

1. **旋转顺序**：必须先计算距离和角度，确定绘图尺寸和位置，最后应用旋转
2. **坐标变换**：旋转会影响图形的实际显示位置，需要根据旋转角度调整坐标
3. **边缘情况**：
   - 当两个设备重叠时，距离为 0，需要特殊处理
   - 当角度接近 0° 或 90° 时，注意数值精度
4. **SVG 绘图**：在 SVG 内部绘图时，坐标是相对于 SVG 画布的，不需要考虑旋转

### 最佳实践

1. **使用整数坐标**：最终返回的坐标和尺寸建议使用整数值
2. **预留边距**：在绘图高度上增加额外空间（如 20 像素），用于显示标注文字
3. **角度规范化**：将角度限制在 0-360 度范围内
4. **错误处理**：当距离过小（如 < 10 像素）时，返回默认值或提示用户

---

## 颜色方案（商务专业风格）

GNS3 Copilot 采用**按逻辑功能分类**的颜色设计，而非按协议堆砌颜色，保持简约商务风格。

### 颜色方案表

| 颜色 | 语义 | 关键词 | 用途 |
|-------|------|--------|------|
| `#1B4F72` | 核心域/骨干 | BGP, AS, AREA 0, BACKBONE, CORE | BGP AS, OSPF Area 0, IS-IS Backbone |
| `#A9CCE3` | 普通域 | AREA, LEVEL, OSPF, IS-IS, RIP, EIGRP | OSPF 普通区域, IS-IS Level-1 |
| `#7D3C98` | 逻辑隔离 | VRF, VLAN, MSTP, VXLAN, MPLS | VRF, VLAN, MPLS VPN |
| `#808B96` | 管理网络 | MGMT, OOB, MANAGEMENT, INFRA | 管理网络, 带外网络 |
| `#D68910` | 高可用 | VRRP, HSRP, HA, STACK, M-LAG, GLBP | VRRP 虚拟网关, 设备堆叠 |
| `#943126` | 外部边界 | INET, OUT, EXTERNAL, INTERNET, DMZ | Internet 出口, DMZ 区域 |
| `#1D8348` | 安全/可信域 | TRUST, SECURE, SAFE, DATA CENTER, SECURITY, VPN, IPSEC | 信任域, 数据中心, IPsec VPN |
| `#16A085` | 云/隧道 | GRE, IPSEC, VPN, TUNNEL, CLOUD, AWS, AZURE | GRE 隧道, 云服务商 |

### 视觉风格

- **填充透明度**：`fill-opacity="0.8"` 保持适当透明度
- **无边框设计**：不使用 `stroke` 边框，保持简约
- **文本颜色**：使用与填充相同的颜色，确保可读性
- **圆角椭圆**：使用椭圆而非矩形，视觉效果更柔和

### 自动颜色映射

工具会根据 `area_name` 中的关键词自动选择颜色：

```python
# 伪代码示例
def get_color(area_name):
    label = area_name.upper()
    if "AREA 0" in label or "BGP" in label or "AS " in label:
        return "#1B4F72"  # 核心域
    elif "VRF" in label or "VLAN" in label:
        return "#7D3C98"  # 逻辑隔离
    elif "VRRP" in label or "HA" in label:
        return "#D68910"  # 高可用
    # ... 更多规则
    return "#808B96"  # 默认灰色
```

---

## SVG 元素类型

### 椭圆 (ellipse)

用于创建圆形或椭圆形区域标注。

#### 基本结构

```svg
<svg height="100" width="200">
  <ellipse cx="100" cy="50" rx="100" ry="50"
           fill="#1B4F72" fill-opacity="0.8" />
</svg>
```

#### 属性说明

| 属性 | 类型 | 说明 |
|------|------|------|
| `width`, `height` | number | SVG 画布尺寸 |
| `cx`, `cy` | number | 椭圆中心坐标 |
| `rx`, `ry` | number | 椭圆半径（半宽、半高） |
| `fill` | color | 填充颜色（HEX 格式） |
| `fill-opacity` | number | 透明度（0.0-1.0） |

**用途**：网络区域分组、逻辑域标注

---

### 文本 (text)

用于添加标签和注释。

#### 基本结构

```svg
<svg height="50" width="200">
  <text font-family="TypeWriter" font-size="12" font-weight="bold"
        fill="#1B4F72" text-anchor="middle" x="100" y="30">
    Area 0
  </text>
</svg>
```

#### 属性说明

| 属性 | 类型 | 说明 |
|------|------|------|
| `font-family` | string | 字体（推荐：TypeWriter） |
| `font-size` | number | 字体大小（像素） |
| `font-weight` | string | 字体粗细（bold, normal） |
| `fill` | color | 文本颜色 |
| `text-anchor` | string | 文本对齐（middle, start, end） |
| `x`, `y` | number | 文本位置坐标 |

**用途**：区域标签、设备名称、网络注释

---

### 矩形 (rect)

用于创建矩形框（较少使用）。

#### 基本结构

```svg
<svg height="100" width="200">
  <rect x="0" y="0" width="200" height="100"
        fill="#1B4F72" fill-opacity="0.8" />
</svg>
```

**用途**：分组框、边界标记

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

| 字段 | 类型 | 说明 |
|------|------|------|
| `drawing_id` | string | 绘图唯一标识符（UUID） |
| `svg` | string | SVG 代码 |
| `x`, `y` | integer | 画布位置坐标（左上角） |
| `z` | integer | Z 轴层级（越大越靠前） |
| `locked` | boolean | 是否锁定 |
| `rotation` | integer | 旋转角度（0-360 度） |

---

## 实际应用示例

### 示例 1：核心域标注（深蓝）

```json
{
  "drawing_id": "UUID",
  "svg": "<svg height=\"100\" width=\"400\"><ellipse cx=\"200\" cy=\"50\" rx=\"200\" ry=\"50\" fill=\"#1B4F72\" fill-opacity=\"0.8\"/></svg>",
  "x": 100,
  "y": 200,
  "z": 1,
  "locked": false,
  "rotation": 0
}
```

**说明**：创建 400×100 像素的深蓝色椭圆，用于标记 BGP AS 或 OSPF Area 0。

---

### 示例 2：普通域标注（浅蓝）

```json
{
  "drawing_id": "UUID",
  "svg": "<svg height=\"100\" width=\"400\"><ellipse cx=\"200\" cy=\"50\" rx=\"200\" ry=\"50\" fill=\"#A9CCE3\" fill-opacity=\"0.8\"/></svg>",
  "x": 100,
  "y": 200,
  "z": 1,
  "locked": false,
  "rotation": 0
}
```

**说明**：浅蓝色椭圆，用于标记 OSPF 普通区域。

---

### 示例 3：逻辑隔离标注（紫色）

```json
{
  "drawing_id": "UUID",
  "svg": "<svg height=\"100\" width=\"400\"><ellipse cx=\"200\" cy=\"50\" rx=\"200\" ry=\"50\" fill=\"#7D3C98\" fill-opacity=\"0.8\"/></svg>",
  "x": 100,
  "y": 200,
  "z": 1,
  "locked": false,
  "rotation": 0
}
```

**说明**：紫色椭圆，用于标记 VRF 或 VLAN。

---

### 示例 4：高可用标注（橙色）

```json
{
  "drawing_id": "UUID",
  "svg": "<svg height=\"100\" width=\"400\"><ellipse cx=\"200\" cy=\"50\" rx=\"200\" ry=\"50\" fill=\"#D68910\" fill-opacity=\"0.8\"/></svg>",
  "x": 100,
  "y": 200,
  "z": 1,
  "locked": false,
  "rotation": 0
}
```

**说明**：橙色椭圆，用于标记 VRRP 虚拟网关或设备堆叠。

---

### 示例 5：外部边界标注（红色）

```json
{
  "drawing_id": "UUID",
  "svg": "<svg height=\"100\" width=\"400\"><ellipse cx=\"200\" cy=\"50\" rx=\"200\" ry=\"50\" fill=\"#943126\" fill-opacity=\"0.8\"/></svg>",
  "x": 100,
  "y": 200,
  "z": 1,
  "locked": false,
  "rotation": 0
}
```

**说明**：红色椭圆，用于标记 Internet 出口或 DMZ 区域。

---

## 最佳实践

### 1. 颜色选择

- 根据网络逻辑功能选择颜色，而非协议种类
- 保持颜色一致性：相同逻辑域使用相同颜色
- 参考颜色方案表，避免随意选择颜色

### 2. 形状使用

- 优先使用椭圆（柔和视觉效果）
- 避免使用矩形边框（保持简约）
- 不使用描边（stroke），仅使用填充

### 3. 图层管理

- `z=0`：背景装饰
- `z=1`：普通标注
- `z=2`：重要标注（优先显示）

### 4. 尺寸规划

- 椭圆宽度：通常为设备间距的 1.1-1.2 倍
- 椭圆高度：通常为 80-120 像素
- 文本区域：预留至少 100×30 像素

### 5. 文本排版

- **字体大小**：12 像素（默认）
- **字体家族**：TypeWriter（推荐）
- **字体粗细**：bold（加粗）
- **文本对齐**：middle（居中）

---

## 相关资源

- [SVG 规范（W3C）](https://www.w3.org/TR/SVG/)
- [MDN SVG 文档](https://developer.mozilla.org/en-US/docs/Web/SVG)
- [GNS3 官方文档](https://docs.gns3.com/)

---

**文档版本**：2.1  
**最后更新**：2026-01-04  
**维护者**：GNS3 Copilot Team
