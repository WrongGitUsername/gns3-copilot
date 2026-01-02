"""
GNS3 area annotation drawing tool for creating visual area markers.

This tool creates visual annotations (ellipses) for network devices to represent
groupings such as OSPF areas, EIGRP AS numbers, or other protocol-defined regions.
Currently supports two-node ellipse annotations.
"""

import json
from typing import Any

from dotenv import load_dotenv
from langchain.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForToolRun

from gns3_copilot.gns3_client import (
    GNS3GetNodesTool,
    Project,
    get_gns3_connector,
)
from gns3_copilot.log_config import setup_tool_logger
from gns3_copilot.public_model.gns3_drawing_utils import calculate_two_node_ellipse

# Configure logging
logger = setup_tool_logger("gns3_create_area_drawing")

# Load environment variables
dotenv_loaded = load_dotenv()
if dotenv_loaded:
    logger.info(
        "GNS3CreateAreaDrawingTool Successfully loaded environment variables from .env file"
    )
else:
    logger.warning(
        "GNS3CreateAreaDrawingTool No .env file found or failed to load. "
        "Using existing environment variables."
    )


class GNS3CreateAreaDrawingTool(BaseTool):
    """
    A LangChain tool to create visual area annotations for network devices.

    Creates ellipse annotations that connect two network devices, automatically
    calculating optimal position, size, and rotation based on node coordinates.

    **Input:**
    A JSON object containing the project_id, area_name, and node_names.

    Example input:
        {
            "project_id": "uuid-of-project",
            "area_name": "Area 0",
            "node_names": ["R-1", "R-2"]
        }

    **Output:**
    A dictionary containing the creation results:
        {
            "project_id": "uuid-of-project",
            "area_name": "Area 0",
            "node_count": 2,
            "shape_type": "ellipse",
            "created_drawings": [
                {
                    "drawing_id": "uuid-of-drawing1",
                    "type": "ellipse",
                    "status": "success"
                },
                {
                    "drawing_id": "uuid-of-drawing2",
                    "type": "text",
                    "status": "success"
                }
            ],
            "total_drawings": 2,
            "successful_drawings": 2,
            "failed_drawings": 0
        }

    **Note:** Currently supports exactly 2 nodes. For more nodes, please use multiple calls
    or wait for multi-node support in future versions.
    """

    name: str = "create_gns3_area_drawing"
    description: str = """
    Creates a visual ellipse annotation for exactly TWO network devices to show area grouping.

    Use this tool when:
    - Configuring OSPF, EIGRP, BGP, or other routing protocols
    - Multiple devices belong to the same area or group
    - Users request area grouping or visual annotation

    Input parameters:
    - project_id (required): GNS3 project UUID
    - area_name (required): Area/group name (e.g., "Area 0", "AS 100")
    - node_names (required): List of exactly 2 node names (e.g., ["R-1", "R-2"])

    The tool automatically:
    - Gets node coordinates from the project topology
    - Calculates optimal ellipse to connect the two devices
    - Determines perfect size and position
    - Calculates rotation angle based on node alignment
    - Chooses appropriate colors (green for Area 0, blue for other areas)
    - Generates professional SVG graphics
    - Creates both the ellipse shape and area label text

    Example usage:
        User: "Configure OSPF area 0 on R-1 and R-2"
        → Call: create_gns3_area_drawing(project_id="xxx", area_name="Area 0", node_names=["R-1", "R-2"])

    Returns creation results including drawing IDs and status.
    """

    def _run(
        self,
        tool_input: str,
        run_manager: CallbackManagerForToolRun | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Creates a visual area annotation for network devices.

        Args:
            tool_input: A JSON string containing project_id, area_name, and node_names.
            run_manager: LangChain run manager (unused).

        Returns:
            dict: A dictionary with creation results or an error message.
        """
        # Log received input
        logger.info("Received input: %s", tool_input)

        try:
            # Parse input JSON
            input_data = json.loads(tool_input)
            project_id = input_data.get("project_id")
            area_name = input_data.get("area_name")
            node_names = input_data.get("node_names", [])

            # Validate input
            if not project_id:
                logger.error("Invalid input: Missing project_id.")
                return {"error": "Missing project_id."}

            if not area_name:
                logger.error("Invalid input: Missing area_name.")
                return {"error": "Missing area_name."}

            if not isinstance(node_names, list) or len(node_names) == 0:
                logger.error("Invalid input: node_names must be a non-empty array.")
                return {"error": "node_names must be a non-empty array."}

            # Validate: currently only supports exactly 2 nodes
            if len(node_names) != 2:
                logger.error(
                    "Invalid input: This version only supports exactly 2 nodes, got %d.",
                    len(node_names),
                )
                return {
                    "error": f"This version only supports exactly 2 nodes, got {len(node_names)}. "
                    "Please provide exactly 2 node names."
                }

            # Initialize Gns3Connector using factory function
            logger.info("Connecting to GNS3 server...")
            gns3_server = get_gns3_connector()

            if gns3_server is None:
                logger.error("Failed to create GNS3 connector")
                return {
                    "error": "Failed to connect to GNS3 server. Please check your configuration."
                }

            # Initialize Project object for drawing creation
            logger.info("Initializing project for drawing creation...")
            project = Project(project_id=project_id, connector=gns3_server)
            project.get()  # Load project details

            # Get node information using GNS3GetNodesTool to retrieve complete node data
            # including height, width, coordinates, etc.
            logger.info(
                "Retrieving node information for project %s...",
                project_id,
            )
            get_nodes_tool = GNS3GetNodesTool()
            nodes_result = get_nodes_tool._run(json.dumps({"project_id": project_id}))

            # Check if node retrieval was successful
            if "error" in nodes_result:
                logger.error("Failed to retrieve nodes: %s", nodes_result["error"])
                return {"error": f"Failed to retrieve nodes: {nodes_result['error']}"}

            # Build a dictionary mapping node names to their complete information
            nodes_dict = {node["name"]: node for node in nodes_result.get("nodes", [])}

            # Retrieve the two nodes
            node1_name = node_names[0]
            node2_name = node_names[1]

            if node1_name not in nodes_dict:
                logger.error("Node %s not found in project", node1_name)
                return {"error": f"Node '{node1_name}' not found in project topology."}

            if node2_name not in nodes_dict:
                logger.error("Node %s not found in project", node2_name)
                return {"error": f"Node '{node2_name}' not found in project topology."}

            # Get complete node information (includes x, y, height, width, etc.)
            node1 = nodes_dict[node1_name]
            node2 = nodes_dict[node2_name]

            logger.info(
                "Found nodes: %s at (%d, %d, size: %dx%d), %s at (%d, %d, size: %dx%d)",
                node1_name,
                node1["x"],
                node1["y"],
                node1.get("width", "N/A"),
                node1.get("height", "N/A"),
                node2_name,
                node2["x"],
                node2["y"],
                node2.get("width", "N/A"),
                node2.get("height", "N/A"),
            )

            # Calculate ellipse parameters using utility function
            # The function now uses actual node dimensions from the retrieved data
            logger.info(
                "Calculating ellipse parameters using actual node dimensions..."
            )
            ellipse_result = calculate_two_node_ellipse(node1, node2, area_name)

            logger.info(
                "Ellipse calculated: center=(%.2f, %.2f), distance=%.2f, angle=%.2f°, ry=%.2f",
                ellipse_result["metadata"]["center_x"],
                ellipse_result["metadata"]["center_y"],
                ellipse_result["metadata"]["distance"],
                ellipse_result["metadata"]["angle_deg"],
                ellipse_result["metadata"]["ry"],
            )

            # Prepare drawings for creation
            # Ensure all coordinates are integers as required by GNS3 API
            drawings = [
                {
                    "svg": ellipse_result["ellipse"]["svg"],
                    "x": int(ellipse_result["ellipse"]["x"]),
                    "y": int(ellipse_result["ellipse"]["y"]),
                    "z": 1,
                    "locked": False,
                    "rotation": int(ellipse_result["ellipse"]["rotation"]),
                },
                {
                    "svg": ellipse_result["text"]["svg"],
                    "x": int(ellipse_result["text"]["x"]),
                    "y": int(ellipse_result["text"]["y"]),
                    "z": 2,
                    "locked": False,
                    "rotation": int(ellipse_result["text"]["rotation"]),
                },
            ]

            # Create drawings using Project method
            logger.info(
                "Creating %d drawings in project %s...", len(drawings), project_id
            )
            results: list[dict[str, Any]] = []

            for i, drawing_data in enumerate(drawings):
                try:
                    drawing_type = "ellipse" if i == 0 else "text"
                    logger.info(
                        "Creating drawing %d/%d: %s at (%d, %d) with rotation %d°...",
                        i + 1,
                        len(drawings),
                        drawing_type,
                        drawing_data["x"],
                        drawing_data["y"],
                        drawing_data["rotation"],
                    )

                    result = project.create_drawing(
                        svg=drawing_data["svg"],
                        x=drawing_data["x"],
                        y=drawing_data["y"],
                        z=drawing_data["z"],
                        locked=drawing_data["locked"],
                        rotation=drawing_data["rotation"],
                    )

                    drawing_info = {
                        "drawing_id": result.get("drawing_id"),
                        "type": drawing_type,
                        "status": "success",
                    }

                    results.append(drawing_info)
                    logger.debug(
                        "Successfully created drawing %d: %s",
                        i + 1,
                        json.dumps(drawing_info, indent=2, ensure_ascii=False),
                    )

                except Exception as e:
                    error_info = {
                        "type": "ellipse" if i == 0 else "text",
                        "error": f"Drawing {i + 1} creation failed: {str(e)}",
                        "status": "failed",
                    }
                    results.append(error_info)
                    logger.error("Failed to create drawing %d: %s", i + 1, e)

            # Calculate summary statistics
            successful_drawings = len(
                [r for r in results if r.get("status") == "success"]
            )
            failed_drawings = len([r for r in results if r.get("status") == "failed"])

            # Prepare final result
            final_result = {
                "project_id": project_id,
                "area_name": area_name,
                "node_count": len(node_names),
                "nodes": node_names,
                "shape_type": "ellipse",
                "created_drawings": results,
                "total_drawings": len(drawings),
                "successful_drawings": successful_drawings,
                "failed_drawings": failed_drawings,
            }

            # Log the final result
            logger.info(
                "Area annotation creation completed: %d successful, %d failed out of %d total drawings.",
                successful_drawings,
                failed_drawings,
                len(drawings),
            )
            logger.debug(
                "Final result: %s",
                json.dumps(final_result, indent=2, ensure_ascii=False),
            )

            # Return JSON-formatted result
            return final_result

        except json.JSONDecodeError as e:
            logger.error("Invalid JSON input: %s", e)
            return {"error": f"Invalid JSON input: {e}"}
        except Exception as e:
            logger.error("Failed to process area annotation request: %s", e)
            return {"error": f"Failed to process area annotation request: {str(e)}"}


if __name__ == "__main__":
    # Test the tool locally
    from pprint import pprint

    test_input = json.dumps(
        {
            "project_id": "0c0fde25-6ead-4413-a283-ea8fd2324291",  # Replace with actual project UUID
            "area_name": "Area 0",
            "node_names": ["R-1", "R-2"],
        }
    )

    tool = GNS3CreateAreaDrawingTool()
    result = tool._run(test_input)
    pprint(result)


"""
example output:
{
    'area_name': 'Area 0',
    'created_drawings': [
        {'drawing_id': 'uuid-of-drawing1', 'status': 'success', 'type': 'ellipse'},
        {'drawing_id': 'uuid-of-drawing2', 'status': 'success', 'type': 'text'}
    ],
    'failed_drawings': 0,
    'node_count': 2,
    'nodes': ['R-1', 'R-2'],
    'project_id': '2245149a-71c8-4387-9d1f-441a683ef7e7',
    'shape_type': 'ellipse',
    'successful_drawings': 2,
    'total_drawings': 2
}
"""
