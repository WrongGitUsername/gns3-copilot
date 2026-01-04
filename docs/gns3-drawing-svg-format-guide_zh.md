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

**文档版本**：2.0  
**最后更新**：2026-01-04  
**维护者**：GNS3 Copilot Team
