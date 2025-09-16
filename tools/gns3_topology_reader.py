from gns3fy import Gns3Connector, Project
import json
from pprint import pprint


def get_open_project_topology():
    server = Gns3Connector(url="http://localhost:3080")
    projects = server.projects_summary(is_print=False)

    # 检查是否有项目
    if not projects:
        print("No projects found.")
        return None

    # 获取打开的项目ID
    pro_id = None
    for p in projects:
        if p[4] == "opened":
            pro_id = p[1]
            break
    if not pro_id:
        print("No opened project found.")
        return None

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

    return topology


if __name__ == "__main__":
    topology = get_open_project_topology()
    pprint(topology)
