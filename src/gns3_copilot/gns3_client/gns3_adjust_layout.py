"""
GNS3 Layout Adjustment Tool

This tool provides automatic node layout adjustment for GNS3 projects.
It addresses common issues with LLM-generated topologies where nodes may be
overlapping, too close together, or positioned on link cables.

Layout Algorithm:
- auto_spacing: Adjust spacing between nodes to prevent overlap and avoid cables
"""

import logging
from typing import Any

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class LayoutAdjustmentInput(BaseModel):
    """Input schema for GNS3 layout adjustment tool."""

    project_id: str = Field(..., description="GNS3 project ID")
    min_distance: int = Field(
        default=250,
        description="Minimum distance between nodes in pixels (default: 250)",
    )
    max_iterations: int = Field(
        default=100,
        description="Maximum iterations (default: 100)",
    )


class GNS3AdjustLayoutTool(BaseTool):
    """
    Tool for adjusting GNS3 node layout automatically.

    This tool solves common topology layout issues:
    - Nodes too close together
    - Overlapping nodes
    - Nodes positioned on link cables
    - Uneven spacing

    The tool uses the auto_spacing algorithm to adjust node positions,
    preventing overlaps and moving nodes away from link cables.

    Example usage:
        >>> tool = GNS3AdjustLayoutTool()
        >>> result = tool.run({
        ...     "project_id": "uuid-of-project",
        ...     "min_distance": 150
        ... })
    """

    name: str = "gns3_adjust_layout"
    description: str = """Adjust GNS3 node layout automatically using auto_spacing algorithm.

    This tool fixes common topology layout issues like overlapping nodes, uneven spacing,
    and nodes on link cables in LLM-generated topologies.

    The auto_spacing algorithm adjusts spacing between nodes to prevent overlap.

    Parameters:
    - project_id: GNS3 project ID (required)
    - min_distance: Minimum distance between nodes in pixels (optional, default: 150)
    - max_iterations: Maximum iterations (optional, default: 100)

    Example for fixing LLM-generated topologies:
    {"project_id": "uuid", "min_distance": 150}
    """
    args_schema: type[BaseModel] = LayoutAdjustmentInput

    def _run(self, **kwargs: Any) -> dict[str, Any]:
        """
        Execute the layout adjustment using auto_spacing algorithm.

        Args:
            **kwargs: Input parameters matching LayoutAdjustmentInput schema

        Returns:
            Dictionary containing:
            - project_id: Project ID
            - layout_type: Layout algorithm used (always "auto_spacing")
            - total_nodes: Number of nodes adjusted
            - adjusted_nodes: List of nodes with new positions
            - status: "success" or "error"
            - message: Status message
        """
        try:
            # Parse input
            project_id = kwargs.get("project_id")
            layout_type = "auto_spacing"  # Fixed to auto_spacing
            min_distance = kwargs.get("min_distance", 250)
            max_iterations = kwargs.get("max_iterations", 100)

            logger.info(f"Adjusting layout for project {project_id} using auto_spacing")

            # Get GNS3 connector
            from gns3_copilot.gns3_client.connector_factory import get_gns3_connector

            connector = get_gns3_connector()
            if connector is None:
                return {
                    "status": "error",
                    "message": "Failed to connect to GNS3 server",
                }

            # Get project
            from gns3_copilot.gns3_client.custom_gns3fy import Project

            project = Project(project_id=project_id, connector=connector)
            project.get(get_nodes=True, get_links=True)

            if not project.nodes:
                return {
                    "project_id": project_id,
                    "layout_type": layout_type,
                    "total_nodes": 0,
                    "adjusted_nodes": [],
                    "status": "success",
                    "message": "No nodes found in project",
                }

            # Prepare node data for layout algorithm
            node_data = [
                {
                    "x": node.x,
                    "y": node.y,
                    "width": node.width,
                    "height": node.height,
                    "node_id": node.node_id,
                    "name": node.name,
                }
                for node in project.nodes
            ]

            # Prepare link data for cable constraint
            link_data = []
            try:
                # Check if project.links exists and is iterable
                if project.links and hasattr(project.links, "__iter__"):
                    for link in project.links:
                        # Check if link has nodes attribute
                        if (
                            hasattr(link, "nodes")
                            and link.nodes
                            and len(link.nodes) >= 2
                        ):
                            # Get actual node positions from project nodes
                            node_a_info = None
                            node_b_info = None
                            for node in project.nodes:
                                if node.node_id == link.nodes[0].get("node_id"):
                                    node_a_info = node
                                elif node.node_id == link.nodes[1].get("node_id"):
                                    node_b_info = node

                            if node_a_info and node_b_info:
                                link_data.append(
                                    {
                                        "nodes": [
                                            {
                                                "node_id": node_a_info.node_id,
                                                "x": node_a_info.x,
                                                "y": node_a_info.y,
                                            },
                                            {
                                                "node_id": node_b_info.node_id,
                                                "x": node_b_info.x,
                                                "y": node_b_info.y,
                                            },
                                        ]
                                    }
                                )
            except (AttributeError, TypeError) as e:
                logger.warning(
                    f"Failed to prepare link data for cable constraints: {e}"
                )
                link_data = []

            # Import layout algorithm here to avoid circular import
            from gns3_copilot.public_model.gns3_layout_utils import (
                auto_spacing_layout,
            )

            # Apply auto_spacing layout algorithm with cable constraints
            logger.info(
                f"Applying auto_spacing layout with min_distance={min_distance}"
            )
            adjusted_nodes = auto_spacing_layout(
                node_data,
                links=link_data,
                min_distance=min_distance,
                max_iterations=max_iterations,
            )

            # Update node positions in GNS3
            for i, original_node in enumerate(project.nodes):
                new_position = adjusted_nodes[i]
                new_x = int(new_position["x"])
                new_y = int(new_position["y"])

                logger.debug(
                    f"Updating node {original_node.name}: "
                    f"({original_node.x}, {original_node.y}) -> ({new_x}, {new_y})"
                )

                original_node.update(x=new_x, y=new_y)

            # Prepare result
            result = {
                "project_id": project_id,
                "layout_type": layout_type,
                "total_nodes": len(project.nodes),
                "adjusted_nodes": [
                    {
                        "node_id": node.node_id,
                        "name": node.name,
                        "x": node.x,
                        "y": node.y,
                    }
                    for node in project.nodes
                ],
                "status": "success",
                "message": f"Successfully adjusted {len(project.nodes)} nodes using auto_spacing layout",
            }

            logger.info(f"Layout adjustment completed: {result['message']}")
            return result

        except Exception as e:
            logger.error(f"Error adjusting layout: {e}", exc_info=True)
            return {
                "status": "error",
                "message": f"Error adjusting layout: {str(e)}",
            }


# Create tool instance
gns3_adjust_layout_tool = GNS3AdjustLayoutTool()

# Export for LangChain
__all__ = ["gns3_adjust_layout_tool", "GNS3AdjustLayoutTool"]


if __name__ == "__main__":
    # Test the tool
    print("Testing GNS3AdjustLayoutTool...")

    # This requires a running GNS3 server with a project
    # Uncomment to test with actual GNS3 server

    tool = GNS3AdjustLayoutTool()
    result = tool.run(
        {
            "project_id": "d7fc094c-685e-4db1-ac11-5e33a1b2e066",
            "min_distance": 300,
        }
    )
    print(result)

    print("\n✅ Tool created successfully!")
    print("\nNote: To test with actual GNS3 server, uncomment the test code above.")
