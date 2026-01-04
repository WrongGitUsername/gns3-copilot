# GNS3 Drawing SVG Format Guide

This document explains the SVG format and business-style color scheme used in GNS3 drawing functionality.

## Table of Contents

- [Overview](#overview)
- [Color Scheme (Business Professional)](#color-scheme-business-professional)
- [SVG Element Types](#svg-element-types)
- [GNS3 Drawing Object Structure](#gns3-drawing-object-structure)
- [Practical Examples](#practical-examples)
- [Best Practices](#best-practices)

---

## Overview

GNS3 drawing functionality allows adding custom graphic elements to the project canvas for network area division, label annotation, and topology visualization. All drawings are defined using SVG format.

### Core Features

1. **Coordinate System**: Drawing and node coordinates represent **top-left corner** positions
2. **Rotation Center**: Rotation is around the top-left corner
3. **Device Dimensions**: Devices are typically 60×60 pixels, actual sizes from API
4. **Link Connection**: Links connect to device center points

---

## Color Scheme (Business Professional)

GNS3 Copilot uses a **functionality-based color design** rather than protocol-based color stacking, maintaining a minimalist business style.

### Color Scheme Table

| Color | Semantics | Keywords | Usage |
|-------|-----------|----------|--------|
| `#1B4F72` | Core/Backbone | BGP, AS, AREA 0, BACKBONE, CORE | BGP AS, OSPF Area 0, IS-IS Backbone |
| `#A9CCE3` | Normal Areas | AREA, LEVEL, OSPF, IS-IS, RIP, EIGRP | OSPF normal areas, IS-IS Level-1 |
| `#7D3C98` | Logical Isolation | VRF, VLAN, MSTP, VXLAN, MPLS | VRF, VLAN, MPLS VPN |
| `#808B96` | Management | MGMT, OOB, MANAGEMENT, INFRA | Management network, Out-of-band |
| `#D68910` | High Availability | VRRP, HSRP, HA, STACK, M-LAG, GLBP | VRRP virtual gateway, device stacking |
| `#943126` | External/Boundary | INET, OUT, EXTERNAL, INTERNET, DMZ | Internet egress, DMZ zone |
| `#1D8348` | Security/Trusted | TRUST, SECURE, SAFE, DATA CENTER, SECURITY, VPN, IPSEC | Trusted zone, data center, IPsec VPN |
| `#16A085` | Cloud/Tunnel | GRE, IPSEC, VPN, TUNNEL, CLOUD, AWS, AZURE | GRE tunnel, cloud providers |

### Visual Style

- **Fill Opacity**: `fill-opacity="0.8"` for appropriate transparency
- **No Border Design**: No `stroke` borders, maintaining simplicity
- **Text Color**: Use same color as fill for readability
- **Rounded Ellipses**: Use ellipses instead of rectangles for softer visual effect

### Automatic Color Mapping

The tool automatically selects colors based on keywords in `area_name`:

```python
# Pseudocode example
def get_color(area_name):
    label = area_name.upper()
    if "AREA 0" in label or "BGP" in label or "AS " in label:
        return "#1B4F72"  # Core domain
    elif "VRF" in label or "VLAN" in label:
        return "#7D3C98"  # Logical isolation
    elif "VRRP" in label or "HA" in label:
        return "#D68910"  # High availability
    # ... more rules
    return "#808B96"  # Default gray
```

---

## SVG Element Types

### Ellipse

Used to create circular or elliptical area annotations.

#### Basic Structure

```svg
<svg height="100" width="200">
  <ellipse cx="100" cy="50" rx="100" ry="50"
           fill="#1B4F72" fill-opacity="0.8" />
</svg>
```

#### Attribute Description

| Attribute | Type | Description |
|-----------|------|-------------|
| `width`, `height` | number | SVG canvas size |
| `cx`, `cy` | number | Ellipse center coordinates |
| `rx`, `ry` | number | Ellipse radius (half-width, half-height) |
| `fill` | color | Fill color (HEX format) |
| `fill-opacity` | number | Opacity (0.0-1.0) |

**Usage**: Network area grouping, logical domain annotation

---

### Text

Used to add labels and annotations.

#### Basic Structure

```svg
<svg height="50" width="200">
  <text font-family="TypeWriter" font-size="12" font-weight="bold"
        fill="#1B4F72" text-anchor="middle" x="100" y="30">
    Area 0
  </text>
</svg>
```

#### Attribute Description

| Attribute | Type | Description |
|-----------|------|-------------|
| `font-family` | string | Font family (recommended: TypeWriter) |
| `font-size` | number | Font size (pixels) |
| `font-weight` | string | Font weight (bold, normal) |
| `fill` | color | Text color |
| `text-anchor` | string | Text alignment (middle, start, end) |
| `x`, `y` | number | Text position coordinates |

**Usage**: Area labels, device names, network annotations

---

### Rectangle

Used to create rectangular boxes (less commonly used).

#### Basic Structure

```svg
<svg height="100" width="200">
  <rect x="0" y="0" width="200" height="100"
        fill="#1B4F72" fill-opacity="0.8" />
</svg>
```

**Usage**: Grouping boxes, boundary markers

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

| Field | Type | Description |
|-------|------|-------------|
| `drawing_id` | string | Drawing unique identifier (UUID) |
| `svg` | string | SVG code |
| `x`, `y` | integer | Canvas position coordinates (top-left) |
| `z` | integer | Z-axis layer (higher values appear on top) |
| `locked` | boolean | Whether locked |
| `rotation` | integer | Rotation angle (0-360 degrees) |

---

## Practical Examples

### Example 1: Core Domain Annotation (Deep Blue)

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

**Description**: Create a 400×100 pixel deep blue ellipse to mark BGP AS or OSPF Area 0.

---

### Example 2: Normal Area Annotation (Light Blue)

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

**Description**: Light blue ellipse for marking OSPF normal areas.

---

### Example 3: Logical Isolation Annotation (Purple)

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

**Description**: Purple ellipse for marking VRF or VLAN.

---

### Example 4: High Availability Annotation (Orange)

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

**Description**: Orange ellipse for marking VRRP virtual gateway or device stacking.

---

### Example 5: External Boundary Annotation (Red)

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

**Description**: Red ellipse for marking Internet egress or DMZ zone.

---

## Best Practices

### 1. Color Selection

- Choose colors based on network logical functionality, not protocol types
- Maintain color consistency: use same color for same logical domains
- Refer to color scheme table, avoid arbitrary color selection

### 2. Shape Usage

- Prioritize ellipses (softer visual effect)
- Avoid rectangular borders (maintain simplicity)
- Use only fills, no strokes (no borders)

### 3. Layer Management

- `z=0`: Background decorations
- `z=1`: Normal annotations
- `z=2`: Important annotations (display priority)

### 4. Size Planning

- Ellipse width: Typically 1.1-1.2× device spacing
- Ellipse height: Typically 80-120 pixels
- Text area: Reserve at least 100×30 pixels

### 5. Text Typography

- **Font size**: 12 pixels (default)
- **Font family**: TypeWriter (recommended)
- **Font weight**: bold
- **Text alignment**: middle (centered)

---

## Related Resources

- [SVG Specification (W3C)](https://www.w3.org/TR/SVG/)
- [MDN SVG Documentation](https://developer.mozilla.org/en-US/docs/Web/SVG)
- [GNS3 Official Documentation](https://docs.gns3.com/)

---

**Document Version**: 2.0  
**Last Updated**: 2026-01-04  
**Maintained by**: GNS3 Copilot Team
