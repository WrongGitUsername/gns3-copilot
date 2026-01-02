"""
Unit tests for GNS3 area annotation drawing tools.

Tests the drawing utility functions and area drawing tool
for calculating ellipse parameters and generating SVG content.
"""

import math

from gns3_copilot.public_model.gns3_drawing_utils import (
    calculate_two_node_ellipse,
    generate_ellipse_svg,
    generate_text_svg,
    DEFAULT_PADDING,
    DEFAULT_DEVICE_HEIGHT,
    DEFAULT_FONT_SIZE
)


class TestCalculateTwoNodeEllipse:
    """Test cases for calculate_two_node_ellipse function."""

    def test_horizontal_layout(self):
        """Test ellipse calculation for horizontal node layout."""
        # Arrange
        node1 = {"x": 100, "y": 200}
        node2 = {"x": 300, "y": 200}
        area_name = "Area 0"

        # Act
        result = calculate_two_node_ellipse(node1, node2, area_name)

        # Assert
        # Check metadata
        assert result["metadata"]["center_x"] == 200.0
        assert result["metadata"]["center_y"] == 200.0
        assert result["metadata"]["distance"] == 200.0
        assert abs(result["metadata"]["angle_deg"]) < 0.1  # Should be ~0 degrees

        # Check ellipse parameters
        expected_rx = 200.0 / 2 + DEFAULT_PADDING
        assert result["metadata"]["rx"] == expected_rx
        assert result["metadata"]["ry"] == DEFAULT_DEVICE_HEIGHT

        # Check SVG content
        assert "<svg" in result["ellipse"]["svg"]
        assert "<ellipse" in result["ellipse"]["svg"]
        assert "Area 0" in result["text"]["svg"]
        assert "<text" in result["text"]["svg"]

        # Check rotation
        assert result["ellipse"]["rotation"] == 0
        assert result["text"]["rotation"] == 0

        print("✅ test_horizontal_layout passed")

    def test_vertical_layout(self):
        """Test ellipse calculation for vertical node layout."""
        # Arrange
        node1 = {"x": 200, "y": 100}
        node2 = {"x": 200, "y": 300}
        area_name = "Area 1"

        # Act
        result = calculate_two_node_ellipse(node1, node2, area_name)

        # Assert
        # Check metadata
        assert result["metadata"]["center_x"] == 200.0
        assert result["metadata"]["center_y"] == 200.0
        assert result["metadata"]["distance"] == 200.0
        assert abs(result["metadata"]["angle_deg"] - 90.0) < 0.1  # Should be ~90 degrees

        # Check ellipse parameters
        expected_rx = 200.0 / 2 + DEFAULT_PADDING
        assert result["metadata"]["rx"] == expected_rx
        assert result["metadata"]["ry"] == DEFAULT_DEVICE_HEIGHT

        # Check SVG content
        assert "<svg" in result["ellipse"]["svg"]
        assert "<ellipse" in result["ellipse"]["svg"]
        assert "Area 1" in result["text"]["svg"]

        # Check rotation
        assert result["ellipse"]["rotation"] == 90
        assert result["text"]["rotation"] == 90

        print("✅ test_vertical_layout passed")

    def test_diagonal_layout(self):
        """Test ellipse calculation for diagonal node layout."""
        # Arrange
        node1 = {"x": 100, "y": 100}
        node2 = {"x": 300, "y": 300}
        area_name = "Area 0"

        # Act
        result = calculate_two_node_ellipse(node1, node2, area_name)

        # Assert
        # Check metadata
        assert result["metadata"]["center_x"] == 200.0
        assert result["metadata"]["center_y"] == 200.0
        assert abs(result["metadata"]["distance"] - 282.84) < 0.1  # sqrt(200^2 + 200^2)
        assert abs(result["metadata"]["angle_deg"] - 45.0) < 0.1  # Should be ~45 degrees

        # Check ellipse parameters
        expected_distance = math.sqrt(200**2 + 200**2)
        expected_rx = expected_distance / 2 + DEFAULT_PADDING
        assert abs(result["metadata"]["rx"] - expected_rx) < 0.1
        assert result["metadata"]["ry"] == DEFAULT_DEVICE_HEIGHT

        # Check SVG content
        assert "<svg" in result["ellipse"]["svg"]
        assert "<ellipse" in result["ellipse"]["svg"]

        # Check rotation
        assert result["ellipse"]["rotation"] == 45
        assert result["text"]["rotation"] == 45

        print("✅ test_diagonal_layout passed")

    def test_custom_padding(self):
        """Test ellipse calculation with custom padding."""
        # Arrange
        node1 = {"x": 100, "y": 200}
        node2 = {"x": 300, "y": 200}
        area_name = "Area 0"
        custom_padding = 50

        # Act
        result = calculate_two_node_ellipse(
            node1, node2, area_name, padding=custom_padding
        )

        # Assert
        # Check that custom padding is used
        expected_rx = 200.0 / 2 + custom_padding
        assert result["metadata"]["rx"] == expected_rx

        print("✅ test_custom_padding passed")

    def test_custom_device_height(self):
        """Test ellipse calculation with custom device height."""
        # Arrange
        node1 = {"x": 100, "y": 200}
        node2 = {"x": 300, "y": 200}
        area_name = "Area 0"
        custom_height = 120

        # Act
        result = calculate_two_node_ellipse(
            node1, node2, area_name, device_height=custom_height
        )

        # Assert
        # Check that custom height is used
        assert result["metadata"]["ry"] == custom_height

        print("✅ test_custom_device_height passed")

    def test_color_scheme_area0(self):
        """Test color scheme for Area 0 (should be green)."""
        # Arrange
        node1 = {"x": 100, "y": 200}
        node2 = {"x": 300, "y": 200}
        area_name = "Area 0"

        # Act
        result = calculate_two_node_ellipse(node1, node2, area_name)

        # Assert
        # Check for green color (#00cc00)
        assert "#00cc00" in result["ellipse"]["svg"]
        assert "#00cc00" in result["text"]["svg"]

        print("✅ test_color_scheme_area0 passed")

    def test_color_scheme_other_area(self):
        """Test color scheme for other areas (should be blue)."""
        # Arrange
        node1 = {"x": 100, "y": 200}
        node2 = {"x": 300, "y": 200}
        area_name = "Area 1"

        # Act
        result = calculate_two_node_ellipse(node1, node2, area_name)

        # Assert
        # Check for blue color (#3366ff)
        assert "#3366ff" in result["ellipse"]["svg"]
        assert "#3366ff" in result["text"]["svg"]

        print("✅ test_color_scheme_other_area passed")

    def test_color_scheme_default(self):
        """Test color scheme for non-OSPF areas (should be gray)."""
        # Arrange
        node1 = {"x": 100, "y": 200}
        node2 = {"x": 300, "y": 200}
        area_name = "EIGRP AS 100"

        # Act
        result = calculate_two_node_ellipse(node1, node2, area_name)

        # Assert
        # Check for gray color (#999999)
        assert "#999999" in result["ellipse"]["svg"]
        assert "#999999" in result["text"]["svg"]

        print("✅ test_color_scheme_default passed")

    def test_svg_structure_ellipse(self):
        """Test that generated ellipse SVG has correct structure."""
        # Arrange
        node1 = {"x": 100, "y": 200}
        node2 = {"x": 300, "y": 200}
        area_name = "Area 0"

        # Act
        result = calculate_two_node_ellipse(node1, node2, area_name)
        svg = result["ellipse"]["svg"]

        # Assert
        # Check SVG structure
        assert svg.startswith('<svg')
        assert svg.endswith('</svg>')
        assert 'xmlns="http://www.w3.org/2000/svg"' in svg
        assert '<ellipse' in svg
        assert 'fill-opacity="0.15"' in svg
        assert 'stroke-width="2"' in svg
        assert 'stroke-dasharray="5,5"' in svg

        print("✅ test_svg_structure_ellipse passed")

    def test_svg_structure_text(self):
        """Test that generated text SVG has correct structure."""
        # Arrange
        node1 = {"x": 100, "y": 200}
        node2 = {"x": 300, "y": 200}
        area_name = "Area 0"

        # Act
        result = calculate_two_node_ellipse(node1, node2, area_name)
        svg = result["text"]["svg"]

        # Assert
        # Check SVG structure
        assert svg.startswith('<svg')
        assert svg.endswith('</svg>')
        assert 'xmlns="http://www.w3.org/2000/svg"' in svg
        assert '<text' in svg
        assert 'font-size="14"' in svg
        assert 'font-weight="bold"' in svg
        assert 'text-anchor="middle"' in svg

        print("✅ test_svg_structure_text passed")


def run_all_tests():
    """Run all unit tests."""
    print("=" * 80)
    print("Running GNS3 Area Drawing Unit Tests")
    print("=" * 80)

    test_class = TestCalculateTwoNodeEllipse()

    # Run all tests
    test_class.test_horizontal_layout()
    test_class.test_vertical_layout()
    test_class.test_diagonal_layout()
    test_class.test_custom_padding()
    test_class.test_custom_device_height()
    test_class.test_color_scheme_area0()
    test_class.test_color_scheme_other_area()
    test_class.test_color_scheme_default()
    test_class.test_svg_structure_ellipse()
    test_class.test_svg_structure_text()

    print("=" * 80)
    print("✅ All unit tests passed!")
    print("=" * 80)


if __name__ == "__main__":
    run_all_tests()
