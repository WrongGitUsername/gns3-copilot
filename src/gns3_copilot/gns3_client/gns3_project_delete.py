import os
from typing import Any

from dotenv import load_dotenv
from langchain.tools import BaseTool

from gns3_copilot.gns3_client import Gns3Connector, Project
from gns3_copilot.log_config import setup_tool_logger

# Configure logging
logger = setup_tool_logger("gns3_project_delete")

# Load environment variables
dotenv_loaded = load_dotenv()
if dotenv_loaded:
    logger.info(
        "GNS3ProjectDelete Tool Successfully loaded environment variables from .env file"
    )
else:
    logger.warning(
        "GNS3ProjectDelete Tool No .env file found or failed to load. Using existing environment variables."
    )


class GNS3ProjectDelete(BaseTool):
    """
    Tool to delete a GNS3 project.

    This tool connects to GNS3 server and deletes an existing project,
    optionally retrieving project details before deletion.
    """

    name: str = "delete_gns3_project"
    description: str = """
    Deletes an existing GNS3 project.

    Input parameters:
    Required:
    - project_id: The UUID of the project to delete OR
    - name: The name of the project to delete (one must be provided)

    Returns: Project deletion status and detailed information including:
    - success: Whether the operation succeeded
    - project: Deleted project details (name, project_id, status, etc.)
    - message: Status message

    Example output:
        {
            "success": true,
            "project": {
                "project_id": "ff8e059c-c33d-47f4-bc11-c7dda8a1d500",
                "name": "my_project",
                "status": "closed"
            },
            "message": "Project 'my_project' deleted successfully"
        }
    """

    def _run(self, tool_input: Any = None, run_manager: Any = None) -> dict:
        """
        Execute the project deletion operation.

        Args:
            tool_input: Dictionary containing project identifier
            run_manager: Run manager for tool execution (optional)

        Returns:
            Dictionary with operation result and deleted project details
        """
        # Log received input
        logger.info("Received input: %s", tool_input)

        try:
            # Validate input
            if not tool_input:
                return {
                    "success": False,
                    "error": "No input provided",
                }

            # Check for project identifier
            project_id = tool_input.get("project_id")
            project_name = tool_input.get("name")

            if not project_id and not project_name:
                return {
                    "success": False,
                    "error": "Missing required parameter: either 'project_id' or 'name' must be provided",
                }

            # Get environment variables
            api_version_str = os.getenv("API_VERSION")
            server_url = os.getenv("GNS3_SERVER_URL")

            if not api_version_str:
                return {
                    "success": False,
                    "error": "API_VERSION environment variable not set",
                }

            if not server_url:
                return {
                    "success": False,
                    "error": "GNS3_SERVER_URL environment variable not set",
                }

            # Create connector based on API version
            if api_version_str == "2":
                server = Gns3Connector(
                    url=server_url,
                    api_version=int(api_version_str),
                )
            elif api_version_str == "3":
                server = Gns3Connector(
                    url=server_url,
                    user=os.getenv("GNS3_SERVER_USERNAME"),
                    cred=os.getenv("GNS3_SERVER_PASSWORD"),
                    api_version=int(api_version_str),
                )
            else:
                return {
                    "success": False,
                    "error": f"Unsupported API_VERSION: {api_version_str}. Must be 2 or 3",
                }

            # Create project instance
            if project_id:
                project = Project(project_id=project_id, connector=server)
            else:
                project = Project(name=project_name, connector=server)

            # Get project information before deletion
            project.get(get_nodes=False, get_links=False, get_stats=False)

            # Verify project was found
            if not project.project_id:
                if project_name:
                    return {
                        "success": False,
                        "error": f"Project with name '{project_name}' not found",
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Project with ID '{project_id}' not found",
                    }

            # Store project details for response
            project_details = {
                "project_id": project.project_id,
                "name": project.name,
                "status": project.status,
                "path": project.path,
            }

            # Delete the project
            project.delete()

            logger.info(
                "Project deleted successfully: %s (ID: %s)",
                project.name,
                project.project_id,
            )

            # Prepare result
            result = {
                "success": True,
                "project": project_details,
                "message": f"Project '{project.name}' deleted successfully",
            }

            # Log result
            logger.info("Project deletion result: %s", result)

            # Return success with project details
            return result

        except ValueError as e:
            logger.error("Validation error deleting GNS3 project: %s", str(e))
            return {
                "success": False,
                "error": f"Validation error: {str(e)}",
            }
        except Exception as e:
            logger.error("Error deleting GNS3 project: %s", str(e))
            return {
                "success": False,
                "error": f"Failed to delete GNS3 project: {str(e)}",
            }
