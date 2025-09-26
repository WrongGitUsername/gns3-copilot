"""
This module provides a LangChain BaseTool to retrieve the topology of the currently open GNS3 project.
"""
import logging
from langchain_core.tools import BaseTool
from tools.custom_gns3fy import Gns3Connector, Project

# Configure logging
logger = logging.getLogger("gns3_topology_reader")
logger.setLevel(logging.DEBUG)

# File logging handler
file_handler = logging.FileHandler("log/gns3_topology_reader.log", mode="a")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Console logging handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Define LangChain tool class
class GNS3TopologyTool(BaseTool):
    name: str = "gns3_topology_reader"
    description: str = """
    Retrieves the topology of the currently open GNS3 project.
    Returns a dictionary containing the project ID, name, status, nodes, and links.
    """

    def _run(self, tool_input=None, run_manager=None) -> dict:
        """
        Synchronous method to retrieve the topology of the currently open GNS3 project.

        Args:
            tool_input : Input parameters, typically a dict or Pydantic model containing server_url.
            run_manager : Callback manager for tool run.

        Returns:
            dict: A dictionary containing the project ID, name, status, nodes, and links,
                  or an empty dict if no projects are found or no project is open,
                  or an error dictionary if an exception occurs.
        """

        try:
            server = Gns3Connector(url="http://localhost:3080/")
            projects = server.projects_summary(is_print=False)

            # Check if any projects exist
            if not projects:
                logger.warning("No projects found.")
                return {}

            # Get the ID of the opened project
            pro_id = None
            for p in projects:
                if p[4] == "opened":
                    pro_id = p[1]
                    break
            if not pro_id:
                logger.warning("No opened project found.")
                return {}

            project = Project(project_id=pro_id, connector=server)
            project.get()  # Load project details

            # Get topology JSON: includes nodes (devices), links, etc.
            topology = {
                "project_id": project.project_id,
                "name": project.name,
                "status": project.status,
                "nodes": project.nodes_inventory(),
                "links": project.links_summary(is_print=False)
            }
            logger.debug("Topology retrieved: %s", topology)
            return topology

        except Exception as e:
            logger.error(f"Error retrieving GNS3 topology: {str(e)}")
            return {"error": f"Failed to retrieve topology: {str(e)}"}

if __name__ == "__main__":
    from pprint import pprint
    # Test the tool
    tool = GNS3TopologyTool()
    result = tool._run()
    pprint(result)
