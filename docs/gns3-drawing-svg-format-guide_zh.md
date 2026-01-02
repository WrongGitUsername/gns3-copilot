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

**对绘图位置的影响**：

当创建需要与设备对齐或引用设备的绘图时（例如围绕设备的区域标注）：

1. **设备位置**：GNS3 API 返回的坐标是设备图标的左上角
2. **中心点计算**：要计算设备的中心点，使用以下公式：
   ```python
   node_center_x = node.x + (node_width / 2)
   node_center_y = node.y + (node_height / 2)
   ```
3. **设备尺寸**：典型的路由器/设备图标大约为 60-80 像素宽和高
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

### 锁定状态

- `locked: true`：绘图被锁定，无法编辑或移动
- `locked: false`：绘图可编辑

### 旋转角度

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
