"""
This module retrieves the topology of the currently open GNS3 project.
"""
import logging
from pprint import pprint
from gns3fy import Gns3Connector, Project

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

def get_open_project_topology():
    """
    Retrieves the topology of the currently open GNS3 project.

    Returns:
        dict: A dictionary containing the project ID, name, status, nodes, and links.
        None: If no projects are found or no project is open.
    """
    server = Gns3Connector(url="http://localhost:3080")
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


if __name__ == "__main__":
    topo = get_open_project_topology()
    pprint(topo)
