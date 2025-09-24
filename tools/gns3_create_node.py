import json
import logging
from pprint import pprint
from langchain.tools import BaseTool
from tools.custom_gns3fy import Gns3Connector, Node

# Configure logging
logger = logging.getLogger("gns3_create_node_tool")
logger.setLevel(logging.DEBUG)

# Prevent duplicate handlers if the module is reloaded
if not logger.handlers:
    # Log to file
    file_handler = logging.FileHandler("log/gns3_create_node_tool.log", mode="a")
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Log to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

class GNS3CreateNodeTool(BaseTool):
    """
    A LangChain tool to create a node in a GNS3 project using a specified template and coordinates.

    **Input:**
    A JSON object containing the template_id, x and y coordinates, and project_id.
    Example input:
        {
            "project_id": "uuid-of-project",
            "template_id": "uuid-of-template",
            "x": 100,
            "y": -200
        }

    **Output:**
    A JSON object containing the created node's details (node_id, name, x, y).
    Example output:
        {
            "node_id": "uuid-of-node",
            "name": "NodeName",
        }
    If an error occurs, returns a JSON object with an error message.
    """

    name: str = "create_gns3_node"
    description: str = """
    Creates a node in a GNS3 project using a specified template and coordinates.
    Input is a JSON object with project_id, template_id(default use IOSv templates),
     x, and y coordinates.
    Example input:
        {
            "project_id": "uuid-of-project",
            "template_id": "uuid-of-template",
            "x": 100,
            "y": -200
        }
    Returns a JSON object with the created node's details (node_id, name, x, y).
    If the operation fails, returns a JSON object with an error message.
    """

    def _run(self, tool_input: str, run_manager=None) -> str:
        """
        Creates a node in a GNS3 project using the provided template_id and coordinates.

        Args:
            tool_input (str): A JSON string containing project_id, template_id, x, and y.
            run_manager: LangChain run manager (unused).

        Returns:
            str: A JSON string with the created node's details or an error message.
        """
        try:
            # Parse input JSON
            input_data = json.loads(tool_input)
            project_id = input_data.get("project_id")
            template_id = input_data.get("template_id")
            x = input_data.get("x")
            y = input_data.get("y")

            # Validate input
            if not all([project_id, template_id, isinstance(x, (int, float)), isinstance(y, (int, float))]):
                logger.error("Invalid input: Missing or invalid project_id, template_id, x, or y.")
                return json.dumps({"error": "Missing or invalid project_id, template_id, x, or y."})

            # Initialize Gns3Connector
            logger.info("Connecting to GNS3 server at http://localhost:3080...")
            gns3_server = Gns3Connector(url="http://localhost:3080")

            # Create node
            logger.info("Creating node in project %s with template %s at coordinates (%s, %s)...", 
                        project_id, template_id, x, y)
            node = Node(
                project_id=project_id,
                template_id=template_id,
                x=x,
                y=y,
                connector=gns3_server
            )
            node.create()

            # Retrieve node details
            node.get()
            node_info = {
                "node_id": node.node_id,
                "name": node.name,
                #"x": node.x,
                #"y": node.y
            }

            # Log the created node details
            logger.debug("Created node: %s", json.dumps(node_info, indent=2, ensure_ascii=False))

            # Return JSON-formatted result
            result_json = json.dumps(node_info, ensure_ascii=False)
            return f"\nObservation: {result_json}\n"

        except json.JSONDecodeError as e:
            logger.error("Invalid JSON input: %s", e)
            return json.dumps({"error": f"Invalid JSON input: {e}"})
        except Exception as e:
            logger.error("Failed to create node: %s", e)
            return json.dumps({"error": f"Failed to create node: {str(e)}"})

if __name__ == "__main__":
    # Test the tool locally
    test_input = json.dumps({
        "project_id": "your-project-uuid",  # Replace with actual project UUID
        "template_id": "your-template-uuid",  # Replace with actual template UUID
        "x": 100,
        "y": -200
    })
    tool = GNS3CreateNodeTool()
    result = tool._run(test_input)
    print(result)