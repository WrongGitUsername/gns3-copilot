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

## GNS3 Coordinate System and Drawing Calculations

### 1. Coordinate System Definition

GNS3 canvas uses a centered origin coordinate system:

- **Origin Position**: Canvas center is at (0, 0)
- **Y-Axis Direction**: Down is positive (+), up is negative (-)
- **X-Axis Direction**: Right is positive (+), left is negative (-)

```
        Y-
         ↑
         |
    X- ←─┼──→ X+
         |
         ↓
        Y+
```

### 2. Device Node Coordinates

- **Coordinate Definition**: Device nodes use top-left corner coordinates
- **Default Dimensions**: 60×60 pixels
- **Actual Dimensions**: Obtain accurate width and height values through API interface
- **SVG Coordinates**: SVG format drawings also use top-left corner coordinates

### 3. Rotation Behavior

- **Rotation Center**: GNS3 drawing rotation uses the top-left corner coordinates as the center of rotation
- **Rotation Angle**: 0-360 degrees, clockwise direction is positive
- **Impact Range**: Rotation affects the actual display position of the drawing on the canvas

---

## Connection Drawing Implementation Details

### Scenario Description

Draw connection graphics between two device nodes (such as connection annotations, area coverage, etc.).

### Implementation Steps

#### Step 1: Get Device Information

Obtain information for two device nodes through API interface:
- Device node coordinates (top-left corner)
- Device node width (width)
- Device node height (height)

#### Step 2: Calculate Device Center Points

Calculate the center point coordinates for each device based on the top-left corner coordinates and dimensions:

```
center_x = x + width / 2
center_y = y + height / 2
```

#### Step 3: Calculate Distance and Angle Between Center Points

```
dx = center_x2 - center_x1
dy = center_y2 - center_y1

# Calculate distance (straight-line distance)
distance = sqrt(dx² + dy²)

# Calculate horizontal angle (radians)
angle_rad = atan2(dy, dx)

# Convert to degrees
angle_deg = angle_rad * (180 / π)
```

#### Step 4: Determine Drawing Dimensions

Determine the size of the SVG drawing based on calculated results:

- **Drawing Length/Width**: Use the distance between the two device center points
- **Drawing Height/Width**: Use the maximum of the two device node widths or heights

```
drawing_length = distance
drawing_height = max(height1, height2)
```

#### Step 5: Calculate Drawing Position (Considering Rotation)

Important: You must first calculate the distance and angle, then calculate the drawing top-left position, and finally apply rotation.

**Calculation Method**:

1. **Calculate unrotated drawing top-left position**:

```
# Start from the first device center point
drawing_x = center_x1
drawing_y = center_y1 - (drawing_height / 2)
```

2. **Consider the impact of rotation angle**:

Since rotation is centered on the top-left corner, the actual position of the rotated graphics will change. Coordinate transformation is needed:

```
# Actual top-left position after rotation (optional, adjust according to specific needs)
rotated_x = drawing_x + (drawing_length / 2) * cos(angle_rad) - (drawing_height / 2) * sin(angle_rad) - (drawing_length / 2)
rotated_y = drawing_y + (drawing_length / 2) * sin(angle_rad) + (drawing_height / 2) * cos(angle_rad) - (drawing_height / 2)
```

3. **Set rotation parameters**:

```
rotation = angle_deg  # Rotation angle
```

### Implementation Example

```python
import math

def calculate_drawing_params(node1, node2, extra_height=20):
    """
    Calculate drawing parameters for connecting two devices
    
    Args:
        node1: First device node object (containing x, y, width, height)
        node2: Second device node object (containing x, y, width, height)
        extra_height: Extra height (pixels) for accommodating annotation text, etc.
    
    Returns:
        dict: Drawing parameters including x, y, width, height, rotation
    """
    # Step 1: Get device information
    x1, y1 = node1['x'], node1['y']
    w1, h1 = node1.get('width', 60), node1.get('height', 60)
    
    x2, y2 = node2['x'], node2['y']
    w2, h2 = node2.get('width', 60), node2.get('height', 60)
    
    # Step 2: Calculate device center points
    cx1 = x1 + w1 / 2
    cy1 = y1 + h1 / 2
    
    cx2 = x2 + w2 / 2
    cy2 = y2 + h2 / 2
    
    # Step 3: Calculate distance and angle
    dx = cx2 - cx1
    dy = cy2 - cy1
    
    distance = math.sqrt(dx ** 2 + dy ** 2)
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    
    # Step 4: Determine drawing dimensions
    drawing_width = distance
    drawing_height = max(h1, h2) + extra_height
    
    # Step 5: Calculate drawing position (start from first device center point)
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

### Important Notes

1. **Rotation Order**: Must first calculate distance and angle, determine drawing dimensions and position, and finally apply rotation
2. **Coordinate Transformation**: Rotation affects the actual display position of the graphics, requiring coordinate adjustment based on rotation angle
3. **Edge Cases**:
   - When two devices overlap, distance is 0, requiring special handling
   - When angle is close to 0° or 90°, pay attention to numerical precision
4. **SVG Drawing**: When drawing within SVG, coordinates are relative to the SVG canvas and do not need to consider rotation

### Best Practices

1. **Use Integer Coordinates**: It is recommended to use integer values for final returned coordinates and dimensions
2. **Reserve Margins**: Add extra space (e.g., 20 pixels) to the drawing height for displaying annotation text
3. **Angle Normalization**: Limit angles to the 0-360 degree range
4. **Error Handling**: When distance is too small (e.g., < 10 pixels), return default values or prompt the user

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

**Document Version**: 2.1  
**Last Updated**: 2026-01-04  
**Maintained by**: GNS3 Copilot Team
