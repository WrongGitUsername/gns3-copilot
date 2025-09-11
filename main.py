import logging
from models import GNS3ProjectManager
import json

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def diagnose_nodes():
    """
    连接到 GNS3 服务器，获取所有打开的项目和节点信息，
    并打印出详细的节点属性以供诊断。
    """
    logging.info("开始执行节点诊断...")
    
    try:
        # 使用在 get_open_project_info.py 中定义的 GNS3ProjectManager
        # 假设 GNS3 服务器在默认地址 http://localhost:3080 且无需认证
        manager = GNS3ProjectManager(server_url="http://localhost:3080")

        logging.info("正在获取已打开的项目信息...")
        projects_info = manager.get_open_projects_info()

        if not projects_info:
            logging.warning("未找到任何已打开的 GNS3 项目。请确保 GNS3 中有打开的项目。")
            return

        print("\n--- GNS3 节点诊断信息 ---\n")

        for project in projects_info:
            print(f"项目名称: {project['name']} (ID: {project['project_id']})")
            print("-" * 40)
            
            if not project['nodes']:
                print("  此项目中没有找到节点。")
                continue

            for node in project['nodes']:
                print(f"  节点名称: {node['name']}")
                print(f"    - 节点 ID: {node['node_id']}")
                
                # 为了获得最详细的信息，我们将节点的原始字典数据转换为格式化的 JSON 字符串
                # 这比访问单个属性更可靠，因为我们不确定哪些属性存在
                node_details_json = json.dumps(node, indent=6, ensure_ascii=False)
                print(f"    - 节点详细信息:\n{node_details_json}\n")
            
            print("-" * 40)

    except Exception as e:
        logging.error(f"诊断过程中发生错误: {e}", exc_info=True)

if __name__ == "__main__":
    diagnose_nodes()
