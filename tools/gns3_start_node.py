import json
import logging
import os
from langchain.tools import BaseTool
from tools.custom_gns3fy import Gns3Connector, Node

# Ensure log directory exists
log_dir = "log"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configure logging
logger = logging.getLogger("gns3_start_node_tool")
logger.setLevel(logging.DEBUG)

# Clear existing handlers to prevent duplicates
logger.handlers = []
file_handler = logging.FileHandler(os.path.join(log_dir, "gns3_start_node_tool.log"), mode="a")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

class GNS3StartNodeTool(BaseTool):
    """
    A LangChain tool to start a node in a GNS3 project.

    **Input**:
    A JSON object with project_id and node_id.
    Example:
        {
            "project_id": "uuid-of-project",
            "node_id": "uuid-of-node"
        }

    **Output**:
    A string starting with "Observation: " followed by a JSON object with node details and status.
    Example:
        Observation: {"node_id": "uuid-of-node", "name": "R-1", "status": "started"}
    """

    name: str = "start_gns3_node"
    description: str = """
    Starts a node in a GNS3 project. Input: JSON with project_id and node_id.
    Returns: Observation: {"node_id": "...", "name": "...", "status": "..."}
    """

    def _run(self, tool_input: str, run_manager=None) -> str:
        logger.debug("Received input: %s", tool_input)
        try:
            # Parse input JSON
            input_data = json.loads(tool_input)
            project_id = input_data.get("project_id")
            node_id = input_data.get("node_id")

            # Validate input
            if not all([project_id, node_id]):
                logger.error("Missing required fields: project_id or node_id.")
                return f"Observation: {json.dumps({'error': 'Missing required fields: project_id or node_id.'}, ensure_ascii=False)}"

            # Initialize Gns3Connector
            logger.info("Connecting to GNS3 server at http://localhost:3080...")
            gns3_server = Gns3Connector(url="http://localhost:3080")

            # Initialize Node object
            logger.info("Starting node %s in project %s...", node_id, project_id)
            node = Node(project_id=project_id, node_id=node_id, connector=gns3_server)

            # Verify node exists
            node.get()
            if not node.node_id:
                logger.error("Node %s not found in project %s.", node_id, project_id)
                return f"Observation: {json.dumps({'error': f'Node {node_id} not found in project {project_id}.'}, ensure_ascii=False)}"

            # Start the node
            node.start()
            logger.info("Node %s started successfully.", node_id)

            # Retrieve updated node information
            node.get()
            logger.debug("Node status: node_id=%s, name=%s, status=%s", 
                         node.node_id, node.name, node.status)

            # Construct node info
            node_info = {
                "node_id": node.node_id,
                "name": node.name or "N/A",
                "status": node.status or "unknown"
            }
            logger.debug("Started node: %s", json.dumps(node_info, indent=2, ensure_ascii=False))

            # Return JSON-formatted result
            return f"Observation: {json.dumps(node_info, ensure_ascii=False)}"

        except json.JSONDecodeError as e:
            logger.error("Invalid JSON input: %s", e)
            return f"Observation: {json.dumps({'error': f'Invalid JSON input: {e}'}, ensure_ascii=False)}"
        except Exception as e:
            logger.error("Failed to start node: %s", e)
            return f"Observation: {json.dumps({'error': f'Failed to start node: {str(e)}'}, ensure_ascii=False)}"

if __name__ == "__main__":
    from pprint import pprint
    test_input = json.dumps({
        "project_id": "f32ebf3d-ef8c-4910-b0d6-566ed828cd24",  # Replace with actual project UUID
        "node_id": "fbeda109-9a74-4d8c-a749-cc3847911a90"    # Replace with actual node UUID
    })
    tool = GNS3StartNodeTool()
    result = tool._run(test_input)
    if result.startswith("Observation: "):
        json_result = json.loads(result[len("Observation: "):])
        pprint(json_result)
    else:
        print("Unexpected result format:", result)