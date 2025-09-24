"""
This module provides a LangChain BaseTool to retrieve the topology of the currently open GNS3 project.
"""
import logging
from langchain_core.tools import BaseTool
from tools.custom_gns3fy import Gns3Connector, Project

# 配置日志记录
logger = logging.getLogger("gns3_topology_reader")
logger.setLevel(logging.DEBUG)

# 文件日志处理
file_handler = logging.FileHandler("log/gns3_topology_reader.log", mode="a")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# 控制台日志处理
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# 将日志添加到日志记录
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 定义 LangChain 工具类
class GNS3TopologyTool(BaseTool):
    name: str = "gns3_topology_reader"
    description: str = """
    Retrieves the topology of the currently open GNS3 project.
    Returns a dictionary containing the project ID, name, status, nodes, and links.
    """

    def _run(self, tool_input = None, run_manager = None) -> dict:
        """
        Synchronous method to retrieve the topology of the currently open GNS3 project.

        Args:
            tool_input : Input parameters, typically a dict or Pydantic model containing server_url.
            run_manager : Callback manager for tool run.

        Returns:
            dict: A dictionary containing the project ID, name, status, nodes, and links.
            dict: Empty dict if no projects are found or no project is open.
        """

        try:
            server = Gns3Connector(url="http://localhost:3080/")
            projects = server.projects_summary(is_print=False)

            # 检查是否有项目
            if not projects:
                logger.warning("No projects found.")
                return {}

            # 获取打开的项目ID
            pro_id = None
            for p in projects:
                if p[4] == "opened":
                    pro_id = p[1]
                    break
            if not pro_id:
                logger.warning("No opened project found.")
                return {}

            project = Project(project_id=pro_id, connector=server)
            project.get()  # 加载项目细节

            # 获取拓扑JSON：包括节点（设备）、链接等
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
    # 测试工具
    tool = GNS3TopologyTool()
    result = tool._run()
    pprint(result)