def test_setup():
    # 这是一个临时测试，证明环境配置正确
    assert True


def test_package_import():
    """测试主包可以正常导入"""
    import gns3_copilot

    assert gns3_copilot.__version__ is not None
    assert gns3_copilot.__author__ == "Guobin Yue"
    assert (
        gns3_copilot.__description__
        == "AI-powered network automation assistant for GNS3"
    )


def test_main_module_import():
    """测试主模块可以正常导入"""
    from gns3_copilot.main import main

    assert callable(main)


def test_app_module_import():
    """测试应用模块可以正常导入"""
    from gns3_copilot.app import main as app_main

    assert callable(app_main)


def test_agent_module_import():
    """测试代理模块可以正常导入"""
    # 检查模块是否可以导入，而不是特定的类
    import gns3_copilot.agent.gns3_copilot

    assert gns3_copilot.agent.gns3_copilot is not None


def test_gns3_client_module_import():
    """测试GNS3客户端模块可以正常导入"""
    from gns3_copilot.gns3_client.custom_gns3fy import (
        Gns3Connector,
        Link,
        Node,
        Project,
    )
    from gns3_copilot.gns3_client.gns3_topology_reader import GNS3TopologyTool

    assert Gns3Connector is not None
    assert Node is not None
    assert Link is not None
    assert Project is not None
    assert GNS3TopologyTool is not None


def test_tools_module_import():
    """测试工具模块可以正常导入"""
    from gns3_copilot.tools_v2.gns3_create_link import GNS3LinkTool
    from gns3_copilot.tools_v2.gns3_create_node import GNS3CreateNodeTool
    from gns3_copilot.tools_v2.gns3_start_node import GNS3StartNodeTool

    assert GNS3CreateNodeTool is not None
    assert GNS3LinkTool is not None
    assert GNS3StartNodeTool is not None


def test_ui_modules_import():
    """测试UI模块可以正常导入"""
    # 检查模块是否可以导入，而不是特定的函数
    import gns3_copilot.ui_model.chat
    import gns3_copilot.ui_model.help
    import gns3_copilot.ui_model.settings

    assert gns3_copilot.ui_model.chat is not None
    assert gns3_copilot.ui_model.help is not None
    assert gns3_copilot.ui_model.settings is not None
