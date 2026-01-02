# GNS3 Drawing SVG Format Guide

This document provides a detailed explanation of the SVG format, parameters, and content structure used in GNS3 Drawing functionality.

## Table of Contents

- [Overview](#overview)
- [GNS3 Drawing Object Structure](#gns3-drawing-object-structure)
- [SVG Element Types](#svg-element-types)
  - [Rectangle (rect)](#rectangle-rect)
  - [Ellipse (ellipse)](#ellipse-ellipse)
  - [Text (text)](#text-text)
  - [Line (line)](#line-line)
- [Common SVG Attributes](#common-svg-attributes)
- [GNS3 Drawing Properties](#gns3-drawing-properties)
- [Practical Examples](#practical-examples)
- [Best Practices](#best-practices)

---

## Overview

GNS3's drawing feature allows you to add custom graphic elements to the project canvas, useful for:
- Network area division and grouping
- Adding labels and annotations
- Creating background decorations
- Enhancing topology diagram readability

All drawings are defined using SVG (Scalable Vector Graphics) format, an XML-based vector graphics format.

---

## GNS3 Drawing Object Structure

### API Response Format

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

### Field Description

| Field | Type | Required | Description |
|-------|------|-----------|--------------|
| `drawing_id` | string | Yes | Drawing unique identifier (UUID) |
| `svg` | string | Yes | SVG code containing the drawing content |
| `x` | integer | Yes | X coordinate of the drawing on the canvas |
| `y` | integer | Yes | Y coordinate of the drawing on the canvas |
| `z` | integer | Yes | Z-axis layer, controls display order (higher values appear on top) |
| `locked` | boolean | Yes | Whether the drawing is locked (cannot be edited when locked) |
| `rotation` | integer | Yes | Rotation angle (0-360 degrees) |

---

## SVG Element Types

### Rectangle (rect)

Used to create rectangular boxes, commonly for representing network areas or groups.

#### Basic Structure

```svg
<svg height="131" width="391">
  <rect fill="#ffffff" fill-opacity="1" height="131" width="391"
        stroke="#000000" stroke-width="2" stroke-dasharray="undefined"
        rx="0" ry="0" />
</svg>
```

#### Attribute Details

| Attribute | Type | Description | Common Values |
|-----------|------|-------------|---------------|
| **Canvas Attributes** |
| `width` | number | SVG canvas width | 100, 200, 391 |
| `height` | number | SVG canvas height | 100, 131 |
| **Rectangle Attributes** |
| `x` | number | Rectangle top-left X coordinate (relative to SVG) | 0, 10 |
| `y` | number | Rectangle top-left Y coordinate (relative to SVG) | 0, 30 |
| `width` | number | Rectangle width | 100, 391 |
| `height` | number | Rectangle height | 100, 131 |
| `rx` | number | X direction corner radius | 0 (sharp corners) |
| `ry` | number | Y direction corner radius | 0 (sharp corners) |

#### Practical Example

```svg
<!-- 391x131 pixel white rectangle with black border -->
<svg height="131" width="391">
  <rect fill="#ffffff" fill-opacity="1" height="131" width="391"
        stroke="#000000" stroke-width="2" stroke-dasharray="undefined"
        rx="0" ry="0" />
</svg>
```

**Use cases**: Grouping boxes, area backgrounds, boundary markers

---

### Ellipse (ellipse)

Used to create circles or ellipses, commonly for representing network areas or node groups.

#### Basic Structure

```svg
<svg height="119" width="488">
  <ellipse fill="#ffffff" fill-opacity="1" cx="244" cy="59.5"
           rx="244" ry="59.5" stroke="#000000" stroke-width="2"
           stroke-dasharray="undefined" />
</svg>
```

#### Attribute Details

| Attribute | Type | Description | Common Values |
|-----------|------|-------------|---------------|
| **Canvas Attributes** |
| `width` | number | SVG canvas width | 100, 200, 488 |
| `height` | number | SVG canvas height | 100, 119 |
| **Ellipse Attributes** |
| `cx` | number | Ellipse center X coordinate | 100, 244 |
| `cy` | number | Ellipse center Y coordinate | 50, 59.5 |
| `rx` | number | X direction radius (half-width) | 100, 244 |
| `ry` | number | Y direction radius (half-height) | 50, 59.5 |

**Note**: When `rx = ry`, the ellipse is a perfect circle.

#### Practical Example

```svg
<!-- 488x119 pixel white ellipse -->
<svg height="119" width="488">
  <ellipse fill="#ffffff" fill-opacity="1" cx="244" cy="59.5"
           rx="244" ry="59.5" stroke="#000000" stroke-width="2"
           stroke-dasharray="undefined" />
</svg>
```

**Use cases**: Circular area grouping, network area identification, background decoration

---

### Text (text)

Used for adding labels, annotations, and explanatory text.

#### Basic Structure

```svg
<svg height="100" width="100">
  <text fill="#000000" fill-opacity="1.0" font-family="Noto Sans"
        font-size="11" font-weight="bold">Area 0</text>
</svg>
```

Or (with namespace format):

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="50">
  <text x="10" y="30" font-size="14">Label 1</text>
</svg>
```

#### Attribute Details

| Attribute | Type | Description | Common Values |
|-----------|------|-------------|---------------|
| **Canvas Attributes** |
| `width` | number | SVG canvas width | 100 |
| `height` | number | SVG canvas height | 50, 100 |
| **Namespace** |
| `xmlns` | string | SVG namespace | `http://www.w3.org/2000/svg` |
| **Text Attributes** |
| `x` | number | Text starting X coordinate | 10, relative position |
| `y` | number | Text baseline Y coordinate | 30, relative position |
| `fill` | color | Text color | `#000000` (black) |
| `fill-opacity` | number | Text transparency | 0.0-1.0 |
| `font-family` | string | Font family | Noto Sans, Arial |
| `font-size` | number | Font size | 11, 14 (pixels) |
| `font-weight` | string | Font weight | normal, bold |

**Text Content**: Placed directly inside the `<text>` tag, supports both Chinese and English.

#### Practical Examples

```svg
<!-- Simple text label -->
<svg height="100" width="100">
  <text fill="#000000" fill-opacity="1.0" font-family="Noto Sans"
        font-size="11" font-weight="bold">Area 0</text>
</svg>

<!-- Text with namespace -->
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="50">
  <text x="10" y="30" font-size="14">Label 1</text>
</svg>

<!-- Chinese text (note: \n requires special handling in SVG) -->
<svg height="100" width="100">
  <text fill="#000000" fill-opacity="1.0" font-family="Noto Sans"
        font-size="11" font-weight="bold">哈哈哈\n哈和</text>
</svg>

<!-- Empty text placeholder -->
<svg height="100" width="100">
  <text fill="#000000" fill-opacity="1.0" font-family="Noto Sans"
        font-size="11" font-weight="bold"></text>
</svg>
```

**Use cases**: Area labels, device names, network annotations, explanatory text

**Important Notes**:
- Line break `\n` does not automatically wrap in pure SVG, use `<tspan>` elements instead
- GNS3 may have special handling for line breaks
- Chinese characters require UTF-8 encoding support

---

### Line (line)

Used to create straight lines, useful for connecting elements or dividing areas.

#### Basic Structure

```svg
<svg height="0" width="100">
  <line stroke="#000000" stroke-width="2" x1="0" x2="200"
        y1="0" y2="0" stroke-dasharray="none" />
</svg>
```

#### Attribute Details

| Attribute | Type | Description | Common Values |
|-----------|------|-------------|---------------|
| **Canvas Attributes** |
| `width` | number | SVG canvas width | 100 |
| `height` | number | SVG canvas height | 0 (line) |
| **Line Attributes** |
| `x1` | number | Start point X coordinate | 0 |
| `y1` | number | Start point Y coordinate | 0 |
| `x2` | number | End point X coordinate | 200 |
| `y2` | number | End point Y coordinate | 0 |

#### Practical Example

```svg
<!-- Horizontal black line, 2 pixels wide -->
<svg height="0" width="100">
  <line stroke="#000000" stroke-width="2" x1="0" x2="200"
        y1="0" y2="0" stroke-dasharray="none" />
</svg>
```

**Use cases**: Dividing lines, connection indicators, boundary markers

---

## Common SVG Attributes

All SVG elements support the following common attributes:

### Fill Attributes

| Attribute | Type | Description | Common Values |
|-----------|------|-------------|---------------|
| `fill` | color | Fill color | `#ffffff` (white), `#ff0000` (red) |
| `fill-opacity` | number | Fill transparency | 0.0 (transparent) - 1.0 (opaque) |

### Stroke Attributes

| Attribute | Type | Description | Common Values |
|-----------|------|-------------|---------------|
| `stroke` | color | Stroke color | `#000000` (black), `#cccccc` (gray) |
| `stroke-width` | number | Stroke width | 1, 2, 3 (pixels) |
| `stroke-dasharray` | string/array | Dashed line style | `none`, `undefined`, `5,5` |

**stroke-dasharray Explanation**:
- `none`: No dashed line (solid)
- `undefined`: Solid line (GNS3 default)
- `5,5`: 5 pixels solid, 5 pixels blank
- `10,5,2,5`: Custom dash pattern

---

## GNS3 Drawing Properties

### Coordinate System

- **X Coordinate**: Horizontal position, can be positive or negative
- **Y Coordinate**: Vertical position, can be positive or negative
- **Z Coordinate**: Layer level, higher values appear on top

**Example**:
```json
{
  "x": -376,   // Left offset
  "y": -381,   // Top offset
  "z": 1        // First layer
}
```

#### Important: Node Coordinate Reference Point

**Critical Discovery**: In GNS3, node coordinates (`node.x`, `node.y`) represent the **top-left corner** of the node icon, NOT the center point.

**Implications for Drawing Placement**:

When creating drawings that should align with or reference nodes (e.g., area annotations around devices):

1. **Node Position**: The coordinate returned by GNS3 API is the top-left corner of the node's icon
2. **Center Point Calculation**: To calculate the center point of a node, use:
   ```python
   node_center_x = node.x + (node_width / 2)
   node_center_y = node.y + (node_height / 2)
   ```
3. **Device Dimensions**: Typical router/device icons are approximately 60-80 pixels in width and height
4. **Drawing Alignment**: When creating area annotations that should encompass devices, calculations should use the device's center point, not the top-left corner

**Example**:
```python
# If node is at (100, 200) and device is 70x70 pixels
node_x = 100  # Top-left corner
node_y = 200  # Top-left corner
device_width = 70
device_height = 70

# Calculate center point
center_x = node_x + (device_width / 2)  # = 135
center_y = node_y + (device_height / 2)  # = 235
```

**Testing**: To verify node coordinate reference points in your GNS3 setup, create small test markers (e.g., 10x10 rectangles) at node positions and observe where they appear relative to the node icon.

### Lock Status

- `locked: true`: Drawing is locked, cannot be edited or moved
- `locked: false`: Drawing is editable

### Rotation Angle

- Unit: Degrees (0-360)
- 0: No rotation
- 90: Clockwise 90 degrees
- 180: 180 degrees rotation
- -90: Counter-clockwise 90 degrees

---

## Practical Examples

### Example 1: Creating Area Grouping

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

**Description**: Create a 391×131 pixel white rectangular box for marking "Area 0".

---

### Example 2: Adding Area Label

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

**Description**: Add "Area 0" label within the area.

---

### Example 3: Rotated Label

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

**Description**: Label displayed with 90-degree rotation.

---

### Example 4: Circular Grouping

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

**Description**: Use ellipse to create circular grouping area.

---

### Example 5: Chinese Annotation

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

**Description**: Add Chinese annotation (note the handling of line breaks).

---

## Best Practices

### 1. Size Planning

- **Rectangular boxes**: Use standard sizes (e.g., 200×100, 300×150) for easier alignment
- **Text areas**: Reserve sufficient space (at least 100×50) for text content
- **Elliptical areas**: Ensure reasonable aspect ratios, avoid being too flat

### 2. Color Selection

- **Background fill**: Use light colors (`#ffffff`, `#f0f0f0`) to enhance readability
- **Border stroke**: Use dark colors (`#000000`, `#333333`) for clear boundary identification
- **Text color**: Create contrast with background (white background with black text, dark background with white text)

### 3. Layer Management

- **Bottom layer (z=0)**: Background decorations, dividing lines
- **Middle layer (z=1)**: Area boxes, labels
- **Top layer (z=2+)**: Important annotations, highlighted elements

### 4. Coordinate Alignment

- Use grid alignment (GNS3 default 50-pixel grid)
- Maintain consistent element spacing (at least 20 pixels recommended)
- Reserve sufficient space for nodes and connections

### 5. Text Typography

- **Font size**: Titles 14-16px, normal text 11-12px
- **Font selection**: Use common fonts (Noto Sans, Arial) for compatibility
- **Multi-line text**: Use `<tspan>` or split into multiple text elements

### 6. Performance Optimization

- Avoid overly complex SVG code
- Use simple geometric shapes instead of complex paths
- Limit the number of on-screen drawings (recommended < 20)

---

## FAQ

### Q1: How to create rounded rectangles?

Set `rx` and `ry` attributes:

```svg
<rect rx="10" ry="10" ... />
```

### Q2: How to create dashed borders?

Set `stroke-dasharray`:

```svg
<rect stroke-dasharray="5,5" ... />
```

### Q3: How to wrap text?

Use `<tspan>` elements:

```svg
<svg height="100" width="100">
  <text x="10" y="30">
    <tspan x="10" dy="0">First line</tspan>
    <tspan x="10" dy="20">Second line</tspan>
  </text>
</svg>
```

### Q4: How to change colors?

Use hexadecimal color codes:
- `#ffffff`: White
- `#000000`: Black
- `#ff0000`: Red
- `#00ff00`: Green
- `#0000ff`: Blue

### Q5: How to rotate drawings?

Set `rotation` attribute (unit: degrees):
- `rotation: 0`: No rotation
- `rotation: 90`: Clockwise 90 degrees
- `rotation: -90`: Counter-clockwise 90 degrees

---

## Related Resources

- [SVG Specification (W3C)](https://www.w3.org/TR/SVG/)
- [MDN SVG Documentation](https://developer.mozilla.org/en-US/docs/Web/SVG)
- [GNS3 Official Documentation](https://docs.gns3.com/)
- [GNS3 API Documentation](https://api.gns3.net/)

---

**Document Version**: 1.0  
**Last Updated**: 2025-01-02  
**Maintained by**: GNS3 Copilot Team
