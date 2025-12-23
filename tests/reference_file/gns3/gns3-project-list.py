from gns3_copilot.gns3_client import GNS3ProjectList

project_list = GNS3ProjectList()
result = project_list._run()
print(result)