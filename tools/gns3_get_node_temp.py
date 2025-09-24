import json
import logging
from pprint import pprint
from langchain.tools import BaseTool
from tools.custom_gns3fy import Gns3Connector

# Configure logging
logger = logging.getLogger("gns3_template_tool")
logger.setLevel(logging.DEBUG)

# Prevent duplicate handlers if the module is reloaded
if not logger.handlers:
    # Log to file
    file_handler = logging.FileHandler("log/gns3_template_tool.log", mode="a")
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

class GNS3TemplateTool(BaseTool):
    """
    A LangChain tool to retrieve all available device templates from a GNS3 server.
    The tool connects to the GNS3 server and extracts the name, template_id, and template_type
    for each template.

    **Input:**
    No input is required for this tool. It connects to the GNS3 server at the default URL
    (http://localhost:3080) and retrieves all templates.

    **Output:**
    A JSON object containing a list of dictionaries, each with the name, template_id, and
    template_type of a template. Example output:
        {
            "templates": [
                {"name": "Router1", "template_id": "uuid1", "template_type": "qemu"},
                {"name": "Switch1", "template_id": "uuid2", "template_type": "ethernet_switch"}
            ]
        }
    If an error occurs, returns a JSON object with an error message.
    """

    name: str = "get_gns3_templates"
    description: str = """
    Retrieves all available device templates from a GNS3 server.
    Returns a JSON object containing a list of dictionaries, each with the name, template_id,
    and template_type of a template. No input is required.
    Example output:
        {
            "templates": [
                {"name": "Router1", "template_id": "uuid1", "template_type": "qemu"},
                {"name": "Switch1", "template_id": "uuid2", "template_type": "ethernet_switch"}
            ]
        }
    If the connection fails, returns a JSON object with an error message.
    """

    def _run(self, tool_input: str = "", run_manager=None) -> str:
        """
        Connects to the GNS3 server and retrieves a list of all available device templates.

        Args:
            tool_input (str): Optional input (not used in this tool).
            run_manager: LangChain run manager (unused).

        Returns:
            str: A JSON string containing the list of templates or an error message.
        """
        try:
            # Initialize Gns3Connector
            logger.info("Connecting to GNS3 server at http://localhost:3080...")
            gns3_server = Gns3Connector(url="http://localhost:3080")
            
            # Retrieve all available templates
            templates = gns3_server.get_templates()
            
            # Extract name, template_id, and template_type
            template_info = [
                {
                    "name": template.get("name", "N/A"),
                    "template_id": template.get("template_id", "N/A"),
                    "template_type": template.get("template_type", "N/A")
                }
                for template in templates
            ]

            # Log the retrieved templates
            logger.debug("Retrieved templates: %s", json.dumps(template_info, indent=2, ensure_ascii=False))
            
            # Return JSON-formatted result
            result_json = json.dumps({"templates": template_info}, ensure_ascii=False)
            return f"\nObservation: {result_json}\n"

        except Exception as e:
            logger.error("Failed to connect to GNS3 server or retrieve templates: %s", e)
            return json.dumps({"error": f"Failed to retrieve templates: {str(e)}"})

if __name__ == "__main__":
    # Test the tool locally
    tool = GNS3TemplateTool()
    result = tool._run("")
    print(result)