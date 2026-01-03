"""
Test script to verify GNS3 node coordinate reference point.

This script creates small test rectangles at node positions to determine
whether GNS3 uses center, top-left, or other reference points for node coordinates.

Note: This is a standalone test script, not a pytest test file.
Run it directly with: python test_node_coordinate_reference.py
"""

# Prevent pytest from collecting this as a test file
__test__ = False

import json
from dotenv import load_dotenv
from gns3_copilot.gns3_client import Project, get_gns3_connector
from gns3_copilot.log_config import setup_tool_logger

# Configure logging
logger = setup_tool_logger("test_node_coordinate_reference")

# Load environment variables
load_dotenv()


def test_node_coordinate_reference(project_id: str, node_names: list[str]):
    """
    Test node coordinate reference points by creating test rectangles.

    For each node, creates three test markers:
    1. A 10x10 red rectangle at the node's (x, y) position
    2. A 5x5 blue circle 20 pixels to the right
    3. A 5x5 green circle 20 pixels below

    This helps visualize where the (x, y) coordinate is located relative to the node.
    """
    # Initialize Gns3Connector
    logger.info("Connecting to GNS3 server...")
    gns3_server = get_gns3_connector()

    if gns3_server is None:
        logger.error("Failed to create GNS3 connector")
        return {"error": "Failed to connect to GNS3 server"}

    # Get project topology
    logger.info("Retrieving topology for project %s...", project_id)
    project = Project(project_id=project_id, connector=gns3_server)
    project.get()

    # Get nodes inventory
    nodes_inventory = project.nodes_inventory()

    results = []

    for node_name in node_names:
        if node_name not in nodes_inventory:
            logger.warning("Node %s not found in project", node_name)
            continue

        node = nodes_inventory[node_name]
        x, y = node["x"], node["y"]

        logger.info(
            "Node %s at (%d, %d) - Creating test markers...", node_name, x, y
        )

        # Create test markers for this node
        test_drawings = []

        # Marker 1: Red rectangle at (x, y) - the reference point
        test_drawings.append({
            "svg": f'<svg xmlns="http://www.w3.org/2000/svg" height="10" width="10">\n  <rect fill="#ff0000" height="10" width="10" x="0" y="0" />\n</svg>',
            "x": x,
            "y": y,
            "z": 10,
            "locked": False,
            "rotation": 0,
            "description": f"Red square at ({x}, {y}) for {node_name}"
        })

        # Marker 2: Blue circle 20px to the right
        test_drawings.append({
            "svg": f'<svg xmlns="http://www.w3.org/2000/svg" height="10" width="10">\n  <circle cx="5" cy="5" fill="#0000ff" r="5" />\n</svg>',
            "x": x + 50,
            "y": y,
            "z": 10,
            "locked": False,
            "rotation": 0,
            "description": f"Blue circle at ({x + 50}, {y}) for {node_name}"
        })

        # Marker 3: Green circle 20px below
        test_drawings.append({
            "svg": f'<svg xmlns="http://www.w3.org/2000/svg" height="10" width="10">\n  <circle cx="5" cy="5" fill="#00ff00" r="5" />\n</svg>',
            "x": x,
            "y": y + 50,
            "z": 10,
            "locked": False,
            "rotation": 0,
            "description": f"Green circle at ({x}, {y + 50}) for {node_name}"
        })

        # Create the drawings
        for i, drawing_data in enumerate(test_drawings):
            try:
                logger.info(f"Creating marker {i+1}: {drawing_data['description']}")
                result = project.create_drawing(
                    svg=drawing_data["svg"],
                    x=drawing_data["x"],
                    y=drawing_data["y"],
                    z=drawing_data["z"],
                    locked=drawing_data["locked"],
                    rotation=drawing_data["rotation"],
                )

                results.append({
                    "node": node_name,
                    "marker_type": ["Red square (x,y)", "Blue circle (x+20,y)", "Green circle (x,y+20)"][i],
                    "drawing_id": result.get("drawing_id"),
                    "position": f"({drawing_data['x']}, {drawing_data['y']})",
                    "status": "success"
                })

            except Exception as e:
                logger.error(f"Failed to create marker {i+1}: {e}")
                results.append({
                    "node": node_name,
                    "marker_type": ["Red square (x,y)", "Blue circle (x+20,y)", "Green circle (x,y+20)"][i],
                    "status": "failed",
                    "error": str(e)
                })

    return {
        "project_id": project_id,
        "nodes_tested": node_names,
        "markers_created": len([r for r in results if r.get("status") == "success"]),
        "results": results
    }


if __name__ == "__main__":
    from pprint import pprint

    # Test with your project and nodes
    test_input = {
        "project_id": "0c0fde25-6ead-4413-a283-ea8fd2324291",
        "node_names": ["R-1", "R-2"]
    }

    print("Testing GNS3 node coordinate reference points...")
    print(f"Project ID: {test_input['project_id']}")
    print(f"Nodes to test: {test_input['node_names']}")
    print("\nCreating test markers...\n")

    result = test_node_coordinate_reference(
        project_id=test_input["project_id"],
        node_names=test_input["node_names"]
    )

    print("\n" + "="*80)
    print("Test Results:")
    print("="*80)
    pprint(result)

    print("\n" + "="*80)
    print("Interpretation:")
    print("="*80)
    print("If the RED square appears:")
    print("  - In the center of the node → (x, y) is the center point")
    print("  - At the top-left corner of the node → (x, y) is the top-left corner")
    print("  - At the bottom-right corner of the node → (x, y) is the bottom-right corner")
    print("\nThe blue and green circles help verify the coordinate system direction.")
