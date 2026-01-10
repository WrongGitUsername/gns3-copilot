# Technical Documentation

This section contains technical specifications and implementation details for GNS3 Copilot.

## Available Documentation

### GNS3 Drawing SVG Format
- [GNS3 Drawing SVG Format Guide (English)](gns3-drawing-svg-format-guide.md) - SVG drawing format specification
- [GNS3 绘图 SVG 格式指南 (中文)](gns3-drawing-svg-format-guide_zh.md) - SVG 绘图格式规范

## Technical Overview

### GNS3 Drawing Format

GNS3 uses SVG (Scalable Vector Graphics) for rendering network topology diagrams. Understanding the SVG format is essential for:

- **Automatic Topology Generation**: Programmatically creating visual representations of network topologies
- **Drawing Area Management**: Creating visual areas for organizing topology components (e.g., OSPF area circles)
- **Topology Visualization**: Rendering network diagrams in the GNS3 Web UI

### SVG Drawing Components

GNS3 drawings support the following SVG elements:

| Element | Usage |
|---------|-------|
| `<rect>` | Rectangular areas and zones |
| `<circle>` | Circular areas (e.g., OSPF areas) |
| `<line>` | Connection lines and annotations |
| `<path>` | Complex shapes and routes |
| `<text>` | Labels and annotations |

### GNS3 Drawing API

GNS3 provides REST API endpoints for managing drawings:

- **Create Drawing**: `POST /v2/projects/{project_id}/drawings`
- **Update Drawing**: `PUT /v2/projects/{project_id}/drawings/{drawing_id}`
- **Delete Drawing**: `DELETE /v2/projects/{project_id}/drawings/{drawing_id}`
- **Get Drawings**: `GET /v2/projects/{project_id}/drawings`

### Example: Creating a Circle Drawing

```json
{
  "type": "ellipse",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 200,
  "rotation": 0,
  "svg": "<svg width='200' height='200'><ellipse cx='100' cy='100' rx='100' ry='100' style='fill:none;stroke:#ff0000;stroke-width:2'/></svg>"
}
```

## Related Resources

- [GNS3 API Documentation](https://api.gns3.net/)
- [SVG Specification](https://www.w3.org/TR/SVG/)
- [Project Documentation](https://yueguobin.github.io/gns3-copilot/)