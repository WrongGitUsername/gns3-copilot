"""
Comprehensive test suite for gns3_adjust_layout module
Tests GNS3AdjustLayoutTool which adjusts GNS3 node layouts

Test Coverage:
1. TestGNS3AdjustLayoutBasic
   - Tool initialization
   - Tool name and description validation

2. TestGNS3AdjustLayoutSuccess
   - Successful layout adjustment with auto_spacing
   - Return value validation
   - Optional parameters handling

3. TestGNS3AdjustLayoutInputValidation
   - Missing tool_input
   - Missing project_id parameter
   - Invalid parameter types

4. TestGNS3AdjustLayoutEnvironmentValidation
   - Missing API_VERSION
   - Missing GNS3_SERVER_URL

5. TestGNS3AdjustLayoutOperations
   - Layout adjustment with default parameters
   - Layout adjustment with custom parameters
   - Node position updates

6. TestGNS3AdjustLayoutErrorHandling
   - Network connection errors
   - GNS3 server errors
   - Exception handling and logging

7. TestGNS3AdjustLayoutReturnFormat
   - Success response format
   - Error response format
   - Adjusted nodes in response
"""

import os
import pytest
from unittest.mock import Mock, patch, MagicMock

# Import module to test
from gns3_copilot.gns3_client import GNS3AdjustLayoutTool


class TestGNS3AdjustLayoutBasic:
    """Basic tests for GNS3AdjustLayoutTool initialization"""

    def test_tool_initialization(self):
        """Test tool initialization"""
        tool = GNS3AdjustLayoutTool()
        
        assert tool.name == "gns3_adjust_layout"
        assert tool is not None

    def test_tool_name(self):
        """Test tool name"""
        tool = GNS3AdjustLayoutTool()
        assert tool.name == "gns3_adjust_layout"

    def test_tool_description(self):
        """Test tool description contains key information"""
        tool = GNS3AdjustLayoutTool()
        
        description = tool.description
        assert "auto_spacing" in description.lower()
        assert "adjust" in description.lower()
        assert "layout" in description.lower()
        assert "project_id" in description.lower()
        assert "min_distance" in description.lower()


class TestGNS3AdjustLayoutSuccess:
    """Tests for successful layout adjustment operations"""

    @patch.dict(os.environ, {
        "API_VERSION": "2",
        "GNS3_SERVER_URL": "http://localhost:3080"
    })
    @patch('gns3_copilot.public_model.gns3_layout_utils.auto_spacing_layout')
    @patch('gns3_copilot.gns3_client.custom_gns3fy.Project')
    @patch('gns3_copilot.gns3_client.connector_factory.get_gns3_connector')
    def test_success_with_default_params(self, mock_get_connector, mock_project_class, mock_auto_spacing):
        """Test successful layout adjustment with default parameters"""
        # Mock connector
        mock_connector = Mock()
        mock_connector.base_url = "http://localhost:3080/v2"
        mock_get_connector.return_value = mock_connector
        
        # Mock project with nodes
        mock_project = Mock()
        mock_project.project_id = "project1"
        mock_project.nodes = [
            Mock(node_id="node1", name="router1", x=0, y=0, width=80, height=50),
            Mock(node_id="node2", name="router2", x=100, y=100, width=80, height=50),
        ]
        mock_project_class.return_value = mock_project
        
        # Mock auto_spacing result
        mock_auto_spacing.return_value = [
            {"node_id": "node1", "x": 0, "y": 0},
            {"node_id": "node2", "x": 150, "y": 0},
        ]
        
        tool = GNS3AdjustLayoutTool()
        result = tool._run(project_id="project1")
        
        assert result["status"] == "success"
        assert result["project_id"] == "project1"
        assert result["layout_type"] == "auto_spacing"
        assert result["total_nodes"] == 2
        assert len(result["adjusted_nodes"]) == 2
        assert "Successfully adjusted" in result["message"]
        mock_auto_spacing.assert_called_once()

    @patch.dict(os.environ, {
        "API_VERSION": "2",
        "GNS3_SERVER_URL": "http://localhost:3080"
    })
    @patch('gns3_copilot.public_model.gns3_layout_utils.auto_spacing_layout')
    @patch('gns3_copilot.gns3_client.custom_gns3fy.Project')
    @patch('gns3_copilot.gns3_client.connector_factory.get_gns3_connector')
    def test_success_with_custom_params(self, mock_get_connector, mock_project_class, mock_auto_spacing):
        """Test successful layout adjustment with custom parameters"""
        # Mock connector
        mock_connector = Mock()
        mock_connector.base_url = "http://localhost:3080/v2"
        mock_get_connector.return_value = mock_connector
        
        # Mock project
        mock_project = Mock()
        mock_project.project_id = "project1"
        mock_project.nodes = [Mock(node_id="node1", name="router1", x=0, y=0, width=80, height=50)]
        mock_project_class.return_value = mock_project
        
        # Mock auto_spacing result
        mock_auto_spacing.return_value = [{"node_id": "node1", "x": 0, "y": 0}]
        
        tool = GNS3AdjustLayoutTool()
        result = tool._run(project_id="project1", min_distance=200, max_iterations=50)
        
        assert result["status"] == "success"
        mock_auto_spacing.assert_called_once()
        
        # Verify parameters were passed correctly
        call_args = mock_auto_spacing.call_args
        assert call_args[1]["min_distance"] == 200
        assert call_args[1]["max_iterations"] == 50

    @patch.dict(os.environ, {
        "API_VERSION": "2",
        "GNS3_SERVER_URL": "http://localhost:3080"
    })
    @patch('gns3_copilot.public_model.gns3_layout_utils.auto_spacing_layout')
    @patch('gns3_copilot.gns3_client.custom_gns3fy.Project')
    @patch('gns3_copilot.gns3_client.connector_factory.get_gns3_connector')
    def test_no_nodes_in_project(self, mock_get_connector, mock_project_class, mock_auto_spacing):
        """Test handling of project with no nodes"""
        # Mock connector
        mock_connector = Mock()
        mock_connector.base_url = "http://localhost:3080/v2"
        mock_get_connector.return_value = mock_connector
        
        # Mock project with no nodes
        mock_project = Mock()
        mock_project.project_id = "project1"
        mock_project.nodes = []
        mock_project_class.return_value = mock_project
        
        tool = GNS3AdjustLayoutTool()
        result = tool._run(project_id="project1")
        
        assert result["status"] == "success"
        assert result["total_nodes"] == 0
        assert len(result["adjusted_nodes"]) == 0
        assert "No nodes found in project" in result["message"]
        mock_auto_spacing.assert_not_called()

    @patch.dict(os.environ, {
        "API_VERSION": "2",
        "GNS3_SERVER_URL": "http://localhost:3080"
    })
    @patch('gns3_copilot.public_model.gns3_layout_utils.auto_spacing_layout')
    @patch('gns3_copilot.gns3_client.custom_gns3fy.Project')
    @patch('gns3_copilot.gns3_client.connector_factory.get_gns3_connector')
    def test_return_value_validation(self, mock_get_connector, mock_project_class, mock_auto_spacing):
        """Test return value structure is correct"""
        # Mock connector
        mock_connector = Mock()
        mock_connector.base_url = "http://localhost:3080/v2"
        mock_get_connector.return_value = mock_connector
        
        # Mock project
        mock_project = Mock()
        mock_project.project_id = "project1"
        mock_project.nodes = [Mock(node_id="node1", name="router1", x=0, y=0, width=80, height=50)]
        mock_project_class.return_value = mock_project
        
        # Mock auto_spacing result
        mock_auto_spacing.return_value = [{"node_id": "node1", "x": 0, "y": 0}]
        
        tool = GNS3AdjustLayoutTool()
        result = tool._run(project_id="project1")
        
        # Verify response structure
        assert "project_id" in result
        assert "layout_type" in result
        assert "total_nodes" in result
        assert "adjusted_nodes" in result
        assert "status" in result
        assert "message" in result
        assert isinstance(result["status"], str)
        assert isinstance(result["total_nodes"], int)
        assert isinstance(result["adjusted_nodes"], list)
        assert isinstance(result["message"], str)


class TestGNS3AdjustLayoutInputValidation:
    """Tests for input validation"""

    def test_missing_project_id(self):
        """Test missing project_id parameter"""
        tool = GNS3AdjustLayoutTool()
        result = tool._run(min_distance=150)
        
        # Should handle gracefully
        assert "status" in result
        assert result["status"] == "error"

    def test_invalid_project_id_type(self):
        """Test project_id parameter is not a string"""
        tool = GNS3AdjustLayoutTool()
        result = tool._run(project_id=123)
        
        # Should handle gracefully
        assert "status" in result
        assert result["status"] == "error"

    @patch.dict(os.environ, {
        "API_VERSION": "2",
        "GNS3_SERVER_URL": "http://localhost:3080"
    })
    def test_valid_min_distance(self):
        """Test valid min_distance parameter"""
        tool = GNS3AdjustLayoutTool()
        
        with patch('gns3_copilot.public_model.gns3_layout_utils.auto_spacing_layout') as mock_auto_spacing:
            with patch('gns3_copilot.gns3_client.custom_gns3fy.Project') as mock_project_class:
                with patch('gns3_copilot.gns3_client.connector_factory.get_gns3_connector') as mock_get_connector:
                    # Mock connector
                    mock_connector = Mock()
                    mock_connector.base_url = "http://localhost:3080/v2"
                    mock_get_connector.return_value = mock_connector
                    
                    # Mock project
                    mock_project = Mock()
                    mock_project.project_id = "project1"
                    mock_project.nodes = [Mock(node_id="node1", name="router1", x=0, y=0, width=80, height=50)]
                    mock_project_class.return_value = mock_project
                    
                    # Mock auto_spacing result
                    mock_auto_spacing.return_value = [{"node_id": "node1", "x": 0, "y": 0}]
                    
                    result = tool._run(project_id="project1", min_distance=200)
                    
                    assert result["status"] == "success"

    @patch.dict(os.environ, {
        "API_VERSION": "2",
        "GNS3_SERVER_URL": "http://localhost:3080"
    })
    def test_valid_max_iterations(self):
        """Test valid max_iterations parameter"""
        tool = GNS3AdjustLayoutTool()
        
        with patch('gns3_copilot.public_model.gns3_layout_utils.auto_spacing_layout') as mock_auto_spacing:
            with patch('gns3_copilot.gns3_client.custom_gns3fy.Project') as mock_project_class:
                with patch('gns3_copilot.gns3_client.connector_factory.get_gns3_connector') as mock_get_connector:
                    # Mock connector
                    mock_connector = Mock()
                    mock_connector.base_url = "http://localhost:3080/v2"
                    mock_get_connector.return_value = mock_connector
                    
                    # Mock project
                    mock_project = Mock()
                    mock_project.project_id = "project1"
                    mock_project.nodes = [Mock(node_id="node1", name="router1", x=0, y=0, width=80, height=50)]
                    mock_project_class.return_value = mock_project
                    
                    # Mock auto_spacing result
                    mock_auto_spacing.return_value = [{"node_id": "node1", "x": 0, "y": 0}]
                    
                    result = tool._run(project_id="project1", max_iterations=200)
                    
                    assert result["status"] == "success"


class TestGNS3AdjustLayoutEnvironmentValidation:
    """Tests for environment variable validation"""

    def test_missing_api_version(self):
        """Test missing API_VERSION environment variable"""
        tool = GNS3AdjustLayoutTool()
        
        with patch.dict(os.environ, {}, clear=True):
            result = tool._run(project_id="project1")
            
            assert result["status"] == "error"
            assert "Failed to connect to GNS3 server" in result["message"]

    def test_missing_server_url(self):
        """Test missing GNS3_SERVER_URL environment variable"""
        tool = GNS3AdjustLayoutTool()
        
        with patch.dict(os.environ, {
            "API_VERSION": "2"
        }, clear=True):
            result = tool._run(project_id="project1")
            
            assert result["status"] == "error"
            assert "Failed to connect to GNS3 server" in result["message"]

    @patch.dict(os.environ, {
        "API_VERSION": "2",
        "GNS3_SERVER_URL": "http://localhost:3080"
    })
    def test_valid_environment(self):
        """Test valid environment variables"""
        tool = GNS3AdjustLayoutTool()
        
        with patch('gns3_copilot.public_model.gns3_layout_utils.auto_spacing_layout') as mock_auto_spacing:
            with patch('gns3_copilot.gns3_client.custom_gns3fy.Project') as mock_project_class:
                with patch('gns3_copilot.gns3_client.connector_factory.get_gns3_connector') as mock_get_connector:
                    # Mock connector
                    mock_connector = Mock()
                    mock_connector.base_url = "http://localhost:3080/v2"
                    mock_get_connector.return_value = mock_connector
                    
                    # Mock project
                    mock_project = Mock()
                    mock_project.project_id = "project1"
                    mock_project.nodes = [Mock(node_id="node1", name="router1", x=0, y=0, width=80, height=50)]
                    mock_project_class.return_value = mock_project
                    
                    # Mock auto_spacing result
                    mock_auto_spacing.return_value = [{"node_id": "node1", "x": 0, "y": 0}]
                    
                    result = tool._run(project_id="project1")
                    
                    assert "status" in result


class TestGNS3AdjustLayoutOperations:
    """Tests for layout-specific operations"""

    @patch.dict(os.environ, {
        "API_VERSION": "2",
        "GNS3_SERVER_URL": "http://localhost:3080"
    })
    @patch('gns3_copilot.public_model.gns3_layout_utils.auto_spacing_layout')
    @patch('gns3_copilot.gns3_client.custom_gns3fy.Project')
    @patch('gns3_copilot.gns3_client.connector_factory.get_gns3_connector')
    def test_auto_spacing_layout_called(self, mock_get_connector, mock_project_class, mock_auto_spacing):
        """Test that auto_spacing_layout is called"""
        # Mock connector
        mock_connector = Mock()
        mock_connector.base_url = "http://localhost:3080/v2"
        mock_get_connector.return_value = mock_connector
        
        # Mock project
        mock_project = Mock()
        mock_project.project_id = "project1"
        
        # Create mock nodes with actual attribute values
        mock_node1 = Mock()
        mock_node1.node_id = "node1"
        mock_node1.name = "router1"
        mock_node1.x = 0
        mock_node1.y = 0
        mock_node1.width = 80
        mock_node1.height = 50
        
        mock_node2 = Mock()
        mock_node2.node_id = "node2"
        mock_node2.name = "router2"
        mock_node2.x = 100
        mock_node2.y = 100
        mock_node2.width = 80
        mock_node2.height = 50
        
        mock_project.nodes = [mock_node1, mock_node2]
        mock_project_class.return_value = mock_project
        
        # Mock auto_spacing result
        mock_auto_spacing.return_value = [
            {"node_id": "node1", "x": 0, "y": 0},
            {"node_id": "node2", "x": 150, "y": 0},
        ]
        
        tool = GNS3AdjustLayoutTool()
        tool._run(project_id="project1")
        
        # Verify auto_spacing_layout was called
        mock_auto_spacing.assert_called_once()
        
        # Verify node data was prepared correctly
        call_args = mock_auto_spacing.call_args
        assert len(call_args[0][0]) == 2  # Two nodes
        assert call_args[0][0][0]["node_id"] == "node1"
        assert call_args[0][0][0]["name"] == "router1"
        assert call_args[0][0][1]["node_id"] == "node2"
        assert call_args[0][0][1]["name"] == "router2"

    @patch.dict(os.environ, {
        "API_VERSION": "2",
        "GNS3_SERVER_URL": "http://localhost:3080"
    })
    @patch('gns3_copilot.public_model.gns3_layout_utils.auto_spacing_layout')
    @patch('gns3_copilot.gns3_client.custom_gns3fy.Project')
    @patch('gns3_copilot.gns3_client.connector_factory.get_gns3_connector')
    def test_node_positions_updated(self, mock_get_connector, mock_project_class, mock_auto_spacing):
        """Test that node positions are updated correctly"""
        # Mock connector
        mock_connector = Mock()
        mock_connector.base_url = "http://localhost:3080/v2"
        mock_get_connector.return_value = mock_connector
        
        # Mock project
        mock_node1 = Mock(node_id="node1", name="router1", x=0, y=0, width=80, height=50)
        mock_node2 = Mock(node_id="node2", name="router2", x=100, y=100, width=80, height=50)
        mock_project = Mock()
        mock_project.project_id = "project1"
        mock_project.nodes = [mock_node1, mock_node2]
        mock_project_class.return_value = mock_project
        
        # Mock auto_spacing result with new positions
        mock_auto_spacing.return_value = [
            {"node_id": "node1", "x": 0, "y": 0},
            {"node_id": "node2", "x": 200, "y": 50},
        ]
        
        tool = GNS3AdjustLayoutTool()
        tool._run(project_id="project1")
        
        # Verify node.update was called for each node
        mock_node1.update.assert_called_once_with(x=0, y=0)
        mock_node2.update.assert_called_once_with(x=200, y=50)

    @patch.dict(os.environ, {
        "API_VERSION": "2",
        "GNS3_SERVER_URL": "http://localhost:3080"
    })
    @patch('gns3_copilot.public_model.gns3_layout_utils.auto_spacing_layout')
    @patch('gns3_copilot.gns3_client.custom_gns3fy.Project')
    @patch('gns3_copilot.gns3_client.connector_factory.get_gns3_connector')
    def test_multiple_nodes_adjusted(self, mock_get_connector, mock_project_class, mock_auto_spacing):
        """Test that multiple nodes are adjusted correctly"""
        # Mock connector
        mock_connector = Mock()
        mock_connector.base_url = "http://localhost:3080/v2"
        mock_get_connector.return_value = mock_connector
        
        # Mock project with 5 nodes
        mock_nodes = [
            Mock(node_id=f"node{i}", name=f"router{i}", x=i*100, y=i*100, width=80, height=50)
            for i in range(5)
        ]
        mock_project = Mock()
        mock_project.project_id = "project1"
        mock_project.nodes = mock_nodes
        mock_project_class.return_value = mock_project
        
        # Mock auto_spacing result
        mock_auto_spacing.return_value = [
            {"node_id": f"node{i}", "x": i*150, "y": 0}
            for i in range(5)
        ]
        
        tool = GNS3AdjustLayoutTool()
        result = tool._run(project_id="project1")
        
        assert result["total_nodes"] == 5
        assert len(result["adjusted_nodes"]) == 5
        
        # Verify all nodes were updated
        for node in mock_nodes:
            node.update.assert_called_once()


class TestGNS3AdjustLayoutErrorHandling:
    """Tests for error handling"""

    @patch.dict(os.environ, {
        "API_VERSION": "2",
        "GNS3_SERVER_URL": "http://localhost:3080"
    })
    def test_network_connection_error(self):
        """Test handling of network connection errors"""
        tool = GNS3AdjustLayoutTool()
        
        with patch('gns3_copilot.gns3_client.connector_factory.get_gns3_connector') as mock_get_connector:
            # Mock connector to return None (connection failed)
            mock_get_connector.return_value = None
            
            result = tool._run(project_id="project1")
            
            assert result["status"] == "error"
            assert "Failed to connect to GNS3 server" in result["message"]

    @patch.dict(os.environ, {
        "API_VERSION": "2",
        "GNS3_SERVER_URL": "http://localhost:3080"
    })
    @patch('gns3_copilot.gns3_client.custom_gns3fy.Project')
    @patch('gns3_copilot.gns3_client.connector_factory.get_gns3_connector')
    def test_auto_spacing_layout_error(self, mock_get_connector, mock_project_class):
        """Test handling of auto_spacing_layout errors"""
        # Mock connector
        mock_connector = Mock()
        mock_connector.base_url = "http://localhost:3080/v2"
        mock_get_connector.return_value = mock_connector
        
        # Mock project
        mock_project = Mock()
        mock_project.project_id = "project1"
        mock_project.nodes = [Mock(node_id="node1", name="router1", x=0, y=0, width=80, height=50)]
        mock_project_class.return_value = mock_project
        
        tool = GNS3AdjustLayoutTool()
        
        with patch('gns3_copilot.public_model.gns3_layout_utils.auto_spacing_layout') as mock_auto_spacing:
            # Mock auto_spacing to raise an error
            mock_auto_spacing.side_effect = Exception("Layout algorithm error")
            
            result = tool._run(project_id="project1")
            
            assert result["status"] == "error"
            assert "Error adjusting layout" in result["message"]

    @patch.dict(os.environ, {
        "API_VERSION": "2",
        "GNS3_SERVER_URL": "http://localhost:3080"
    })
    @patch('gns3_copilot.gns3_client.custom_gns3fy.Project')
    @patch('gns3_copilot.gns3_client.connector_factory.get_gns3_connector')
    def test_project_get_error(self, mock_get_connector, mock_project_class):
        """Test handling of project.get() errors"""
        # Mock connector
        mock_connector = Mock()
        mock_connector.base_url = "http://localhost:3080/v2"
        mock_get_connector.return_value = mock_connector
        
        # Mock project to raise error on get
        mock_project = Mock()
        mock_project.get.side_effect = Exception("Project get error")
        mock_project_class.return_value = mock_project
        
        tool = GNS3AdjustLayoutTool()
        result = tool._run(project_id="project1")
        
        assert result["status"] == "error"
        assert "Error adjusting layout" in result["message"]

    @patch.dict(os.environ, {
        "API_VERSION": "2",
        "GNS3_SERVER_URL": "http://localhost:3080"
    })
    def test_exception_logging(self):
        """Test that exceptions are logged"""
        tool = GNS3AdjustLayoutTool()
        
        with patch('gns3_copilot.gns3_client.connector_factory.get_gns3_connector') as mock_get_connector:
            mock_get_connector.return_value = None
            
            result = tool._run(project_id="project1")
            
            # Should return error without crashing
            assert "status" in result
            assert result["status"] == "error"


class TestGNS3AdjustLayoutReturnFormat:
    """Tests for return format validation"""

    @patch.dict(os.environ, {
        "API_VERSION": "2",
        "GNS3_SERVER_URL": "http://localhost:3080"
    })
    @patch('gns3_copilot.public_model.gns3_layout_utils.auto_spacing_layout')
    @patch('gns3_copilot.gns3_client.custom_gns3fy.Project')
    @patch('gns3_copilot.gns3_client.connector_factory.get_gns3_connector')
    def test_success_response_format(self, mock_get_connector, mock_project_class, mock_auto_spacing):
        """Test success response has correct format"""
        # Mock connector
        mock_connector = Mock()
        mock_connector.base_url = "http://localhost:3080/v2"
        mock_get_connector.return_value = mock_connector
        
        # Mock project
        mock_project = Mock()
        mock_project.project_id = "project1"
        mock_project.nodes = [
            Mock(node_id="node1", name="router1", x=0, y=0, width=80, height=50),
            Mock(node_id="node2", name="router2", x=100, y=100, width=80, height=50),
        ]
        mock_project_class.return_value = mock_project
        
        # Mock auto_spacing result
        mock_auto_spacing.return_value = [
            {"node_id": "node1", "x": 0, "y": 0},
            {"node_id": "node2", "x": 150, "y": 0},
        ]
        
        tool = GNS3AdjustLayoutTool()
        result = tool._run(project_id="project1")
        
        # Verify all required fields
        assert "project_id" in result
        assert "layout_type" in result
        assert "total_nodes" in result
        assert "adjusted_nodes" in result
        assert "status" in result
        assert "message" in result
        assert result["status"] == "success"
        
        # Verify adjusted nodes structure
        assert len(result["adjusted_nodes"]) == 2
        assert "node_id" in result["adjusted_nodes"][0]
        assert "name" in result["adjusted_nodes"][0]
        assert "x" in result["adjusted_nodes"][0]
        assert "y" in result["adjusted_nodes"][0]

    @patch.dict(os.environ, {
        "API_VERSION": "2",
        "GNS3_SERVER_URL": "http://localhost:3080"
    })
    def test_error_response_format(self):
        """Test error response has correct format"""
        tool = GNS3AdjustLayoutTool()
        
        with patch.dict(os.environ, {}, clear=True):
            result = tool._run(project_id="project1")
            
            # Verify error format
            assert "status" in result
            assert result["status"] == "error"
            assert "message" in result
            assert isinstance(result["message"], str)

    @patch.dict(os.environ, {
        "API_VERSION": "2",
        "GNS3_SERVER_URL": "http://localhost:3080"
    })
    @patch('gns3_copilot.public_model.gns3_layout_utils.auto_spacing_layout')
    @patch('gns3_copilot.gns3_client.custom_gns3fy.Project')
    @patch('gns3_copilot.gns3_client.connector_factory.get_gns3_connector')
    def test_adjusted_nodes_content(self, mock_get_connector, mock_project_class, mock_auto_spacing):
        """Test that adjusted nodes contain correct information"""
        # Mock connector
        mock_connector = Mock()
        mock_connector.base_url = "http://localhost:3080/v2"
        mock_get_connector.return_value = mock_connector
        
        # Mock project with properly configured mock nodes
        # Use side_effect to make update() actually modify the attributes
        mock_node1 = Mock()
        mock_node1.node_id = "node1"
        mock_node1.name = "router1"
        mock_node1.x = 0
        mock_node1.y = 0
        mock_node1.width = 80
        mock_node1.height = 50
        
        # Make update() actually modify x and y
        def update_node1(**kwargs):
            if 'x' in kwargs:
                mock_node1.x = kwargs['x']
            if 'y' in kwargs:
                mock_node1.y = kwargs['y']
        mock_node1.update = Mock(side_effect=update_node1)
        
        mock_node2 = Mock()
        mock_node2.node_id = "node2"
        mock_node2.name = "router2"
        mock_node2.x = 100
        mock_node2.y = 100
        mock_node2.width = 80
        mock_node2.height = 50
        
        # Make update() actually modify x and y
        def update_node2(**kwargs):
            if 'x' in kwargs:
                mock_node2.x = kwargs['x']
            if 'y' in kwargs:
                mock_node2.y = kwargs['y']
        mock_node2.update = Mock(side_effect=update_node2)
        
        mock_project = Mock()
        mock_project.project_id = "project1"
        mock_project.nodes = [mock_node1, mock_node2]
        mock_project_class.return_value = mock_project
        
        # Mock auto_spacing result
        mock_auto_spacing.return_value = [
            {"node_id": "node1", "x": 10, "y": 20},
            {"node_id": "node2", "x": 160, "y": 20},
        ]
        
        tool = GNS3AdjustLayoutTool()
        result = tool._run(project_id="project1")
        
        # Verify adjusted nodes content
        assert result["adjusted_nodes"][0]["node_id"] == "node1"
        assert result["adjusted_nodes"][0]["name"] == "router1"
        assert result["adjusted_nodes"][0]["x"] == 10
        assert result["adjusted_nodes"][0]["y"] == 20
        assert result["adjusted_nodes"][1]["node_id"] == "node2"
        assert result["adjusted_nodes"][1]["name"] == "router2"
        assert result["adjusted_nodes"][1]["x"] == 160
        assert result["adjusted_nodes"][1]["y"] == 20

    @patch.dict(os.environ, {
        "API_VERSION": "2",
        "GNS3_SERVER_URL": "http://localhost:3080"
    })
    @patch('gns3_copilot.public_model.gns3_layout_utils.auto_spacing_layout')
    @patch('gns3_copilot.gns3_client.custom_gns3fy.Project')
    @patch('gns3_copilot.gns3_client.connector_factory.get_gns3_connector')
    def test_message_content(self, mock_get_connector, mock_project_class, mock_auto_spacing):
        """Test that message contains useful information"""
        # Mock connector
        mock_connector = Mock()
        mock_connector.base_url = "http://localhost:3080/v2"
        mock_get_connector.return_value = mock_connector
        
        # Mock project
        mock_project = Mock()
        mock_project.project_id = "project1"
        mock_project.nodes = [Mock(node_id="node1", name="router1", x=0, y=0, width=80, height=50)]
        mock_project_class.return_value = mock_project
        
        # Mock auto_spacing result
        mock_auto_spacing.return_value = [{"node_id": "node1", "x": 0, "y": 0}]
        
        tool = GNS3AdjustLayoutTool()
        result = tool._run(project_id="project1")
        
        # Verify message contains useful information
        assert "Successfully adjusted" in result["message"]
        assert "1" in result["message"]  # Number of nodes
        assert "auto_spacing" in result["message"]
