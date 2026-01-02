"""
Drawing tool prompt for GNS3 area annotation creation.

This module provides specialized prompts for guiding the AI in using GNS3 drawing tools
to create visual area annotations for network topology.
"""


def get_drawing_prompt() -> str:
    """
    Get the drawing tool usage prompt for the AI agent.

    Returns:
        str: A comprehensive prompt with examples and best practices for drawing tools.
    """
    return """
## GNS3 Drawing Tools

When configuring routing protocols (OSPF, EIGRP, BGP, etc.) or grouping network devices,
use the `create_gns3_area_drawing` tool to create visual annotations.

### When to Use Drawing Tools

Create visual area annotations when:
- Configuring OSPF areas (e.g., "Area 0", "Area 1")
- Configuring EIGRP autonomous systems (e.g., "AS 100", "AS 200")
- Configuring BGP AS numbers (e.g., "AS 65001")
- Any grouping of 2 devices that belong to the same logical area or protocol domain

### Tool Parameters

The `create_gns3_area_drawing` tool requires:
- `project_id`: The GNS3 project UUID (get from gns3_topology_reader)
- `area_name`: The area/group name (e.g., "Area 0", "AS 100")
- `node_names`: A list of exactly 2 node names (e.g., ["R-1", "R-2"])

**Important**: Currently only supports exactly 2 nodes. For more nodes, create multiple annotations.

### Usage Examples

Example 1 - OSPF Area 0:
```
User: Configure OSPF area 0 on R-1 and R-2
→ After configuration, call:
  create_gns3_area_drawing(
      project_id="xxx",
      area_name="Area 0",
      node_names=["R-1", "R-2"]
  )
```

Example 2 - Multi-Area OSPF:
```
User: Configure OSPF with R-1 and R-2 in area 0, R-3 and R-4 in area 1
→ Create two annotations:
  1. create_gns3_area_drawing(project_id="xxx", area_name="Area 0", node_names=["R-1", "R-2"])
  2. create_gns3_area_drawing(project_id="xxx", area_name="Area 1", node_names=["R-3", "R-4"])
```

Example 3 - EIGRP AS:
```
User: Configure EIGRP AS 100 on SW-1 and SW-2
→ After configuration, call:
  create_gns3_area_drawing(project_id="xxx", area_name="AS 100", node_names=["SW-1", "SW-2"])
```

### Best Practices

1. **Create After Configuration**: Always complete the configuration first, then create the visual annotation
2. **Use Concise Names**: Use "Area 0" not "OSPF Backbone Area Zero"
3. **Group Related Devices**: Only annotate devices that are logically connected/configured together
4. **Verify Before Drawing**: Use display commands to verify configuration success before creating annotations
5. **Inform the User**: Clearly state when creating visual annotations

### What the Tool Does Automatically

The `create_gns3_area_drawing` tool automatically:
- Retrieves node coordinates from the project topology
- Calculates the optimal ellipse shape to connect the two devices
- Determines perfect size and position based on node locations
- Calculates rotation angle based on device alignment
- Chooses appropriate colors (green for Area 0, blue for other areas, gray for others)
- Generates professional SVG graphics with dashed borders and semi-transparent backgrounds
- Creates both the ellipse shape and the area label text

### Color Scheme

The tool automatically selects colors based on the area name:
- **Area 0** (OSPF backbone): Green (#00cc00)
- **Area 1-99** (Other OSPF areas): Blue (#3366ff)
- **Other** (EIGRP AS, BGP AS, etc.): Gray (#999999)

### Visual Style

Annotations use professional styling:
- Ellipse shape that perfectly connects the two devices
- Dashed border (stroke-dasharray="5,5")
- Semi-transparent background (fill-opacity="0.15")
- Centered area label text
- Automatic rotation based on device positions

### Handling More Than 2 Nodes

If you need to annotate 3 or more nodes in the same area:
1. Create multiple annotations, each connecting 2 nodes
2. Focus on the most important connections
3. Example: For 3 devices R-1, R-2, R-3 in Area 0:
   - Annotation 1: R-1 and R-2
   - Annotation 2: R-2 and R-3
   - Annotation 3: R-1 and R-3 (optional, if useful)

### Error Handling

If the drawing tool fails:
1. Verify node names are correct using gns3_topology_reader
2. Check that exactly 2 node names are provided
3. Ensure project_id is valid
4. Report the error to the user and continue with other tasks

"""
