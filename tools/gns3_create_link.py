import json
import logging
from pprint import pprint
from langchain.tools import BaseTool
from tools.custom_gns3fy import Gns3Connector, Link

# Configure logging
logger = logging.getLogger("gns3_link_tool")
logger.setLevel(logging.DEBUG)

# Prevent duplicate handlers if the module is reloaded
if not logger.handlers:
    file_handler = logging.FileHandler("log/gns3_link_tool.log", mode="a")
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

class GNS3LinkTool(BaseTool):
    """
    A LangChain tool to create a link between two nodes in a GNS3 project.

    **Input**:
    A JSON object with project_id, node_id1, port1, node_id2, port2.
    Example:
        {
            "project_id": "uuid-of-project",
            "node_id1": "uuid-of-node1",
            "port1": "Ethernet0/0",
            "node_id2": "uuid-of-node2",
            "port2": "Ethernet0/0"
        }

    **Output**:
    A string starting with "Observation: " followed by a JSON object with link details.
    Example:
        Observation: {"link_id": "uuid-of-link", "node_id1": "uuid-of-node1", "port1": "Ethernet0/0", "node_id2": "uuid-of-node2", "port2": "Ethernet0/0"}
    """

    name: str = "create_gns3_link"
    description: str = """
    Creates a link between two GNS3 nodes. Input: JSON with project_id, node_id1, port1, node_id2, port2.
    Returns: Observation: {"link_id": "...", "node_id1": "...", "port1": "...", "node_id2": "...", "port2": "..."}
    """

    def _run(self, tool_input: str, run_manager=None) -> str:
        """
        Creates a link between two nodes in a GNS3 project.

        Args:
            tool_input (str): A JSON string with project_id, node_id1, port1, node_id2, port2.
            run_manager: LangChain run manager (unused).

        Returns:
            str: A string starting with "Observation: " followed by a JSON object with link details or an error message.
        """
        try:
            # Parse input JSON
            input_data = json.loads(tool_input)
            project_id = input_data.get("project_id")
            node_id1 = input_data.get("node_id1")
            port1 = input_data.get("port1")
            node_id2 = input_data.get("node_id2")
            port2 = input_data.get("port2")

            # Validate input
            if not all([project_id, node_id1, port1, node_id2, port2]):
                logger.error("Missing required fields: project_id, node_id1, port1, node_id2, or port2.")
                return f"Observation: {json.dumps({'error': 'Missing required fields: project_id, node_id1, port1, node_id2, or port2.'}, ensure_ascii=False)}"

            # Initialize Gns3Connector
            logger.info("Connecting to GNS3 server at http://localhost:3080...")
            gns3_server = Gns3Connector(url="http://localhost:3080")

            # Get node details to validate ports and extract adapter/port numbers
            logger.info("Validating ports for nodes %s and %s...", node_id1, node_id2)
            node1 = gns3_server.get_node(project_id=project_id, node_id=node_id1)
            node2 = gns3_server.get_node(project_id=project_id, node_id=node_id2)
            if not node1 or not node2:
                logger.error("Node not found: %s or %s.", node_id1, node_id2)
                return f"Observation: {json.dumps({'error': f'Node not found: {node_id1 or node_id2}.'}, ensure_ascii=False)}"

            # Find port1 in node1's ports
            port1_info = next((port for port in node1.get("ports", []) if port.get("name") == port1), None)
            if not port1_info:
                logger.error("Port %s not found on node %s.", port1, node_id1)
                return f"Observation: {json.dumps({'error': f'Port {port1} not found on node {node_id1}.'}, ensure_ascii=False)}"

            # Find port2 in node2's ports
            port2_info = next((port for port in node2.get("ports", []) if port.get("name") == port2), None)
            if not port2_info:
                logger.error("Port %s not found on node %s.", port2, node_id2)
                return f"Observation: {json.dumps({'error': f'Port {port2} not found on node {node_id2}.'}, ensure_ascii=False)}"

            # Create link
            logger.info("Creating link between node %s (%s) and node %s (%s) in project %s...", 
                        node_id1, port1, node_id2, port2, project_id)
            link = Link(
                project_id=project_id,
                connector=gns3_server,
                nodes=[
                    {
                        "node_id": node_id1,
                        "adapter_number": port1_info.get("adapter_number", 0),
                        "port_number": port1_info.get("port_number", 0),
                        "label": {"text": port1}
                    },
                    {
                        "node_id": node_id2,
                        "adapter_number": port2_info.get("adapter_number", 0),
                        "port_number": port2_info.get("port_number", 0),
                        "label": {"text": port2}
                    }
                ]
            )
            link.create()

            # Retrieve link details
            link.get()
            link_info = {
                "link_id": link.link_id,
                "node_id1": node_id1,
                "port1": port1,
                "node_id2": node_id2,
                "port2": port2
            }

            # Log the created link details
            logger.debug("Created link: %s", json.dumps(link_info, indent=2, ensure_ascii=False))

            # Return JSON-formatted result with Observation prefix
            return f"Observation: {json.dumps(link_info, ensure_ascii=False)}"

        except json.JSONDecodeError as e:
            logger.error("Invalid JSON input: %s", e)
            return f"Observation: {json.dumps({'error': f'Invalid JSON input: {e}'}, ensure_ascii=False)}"
        except Exception as e:
            logger.error("Failed to create link: %s", e)
            return f"Observation: {json.dumps({'error': f'Failed to create link: {str(e)}'}, ensure_ascii=False)}"

if __name__ == "__main__":
    # Test the tool locally
    test_input = json.dumps({
        "project_id": "your-project-uuid",  # Replace with actual project UUID
        "node_id1": "your-node1-uuid",     # Replace with actual node1 UUID
        "port1": "Ethernet0/0",
        "node_id2": "your-node2-uuid",     # Replace with actual node2 UUID
        "port2": "Ethernet0/0"
    })
    tool = GNS3LinkTool()
    result = tool._run(test_input)
    if result.startswith("Observation: "):
        json_result = json.loads(result[len("Observation: "):])
        pprint(json_result)
    else:
        print("Unexpected result format:", result)