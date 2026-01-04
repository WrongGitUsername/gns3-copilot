"""
Unit tests for GNS3 layout utility functions.

Tests() layout algorithms in gns3_layout_utils.py:
- auto_spacing_layout
- calculate_distance
- get_node_center
- is_point_on_line_segment
"""

import math

import pytest

from gns3_copilot.public_model.gns3_layout_utils import (
    auto_spacing_layout,
    calculate_distance,
    get_node_center,
    is_point_on_line_segment,
)


class TestCalculateDistance:
    """Test cases for calculate_distance function."""

    def test_horizontal_distance(self):
        """Test distance calculation for horizontal nodes."""
        node1 = {"x": 100, "y": 200}
        node2 = {"x": 300, "y": 200}
        assert calculate_distance(node1, node2) == 200.0

    def test_vertical_distance(self):
        """Test distance calculation for vertical nodes."""
        node1 = {"x": 200, "y": 100}
        node2 = {"x": 200, "y": 300}
        assert calculate_distance(node1, node2) == 200.0

    def test_diagonal_distance(self):
        """Test distance calculation for diagonal nodes."""
        node1 = {"x": 0, "y": 0}
        node2 = {"x": 300, "y": 400}
        expected = math.sqrt(300**2 + 400**2)
        assert pytest.approx(calculate_distance(node1, node2), 0.01) == expected

    def test_zero_distance(self):
        """Test distance calculation for same position."""
        node1 = {"x": 100, "y": 200}
        node2 = {"x": 100, "y": 200}
        assert calculate_distance(node1, node2) == 0.0


class TestGetNodeCenter:
    """Test cases for get_node_center function."""

    def test_center_with_dimensions(self):
        """Test center calculation with explicit dimensions."""
        node = {"x": 100, "y": 200, "width": 50, "height": 50}
        center = get_node_center(node)
        assert center == (125.0, 225.0)

    def test_center_with_default_dimensions(self):
        """Test center calculation with default dimensions."""
        node = {"x": 100, "y": 200}
        center = get_node_center(node)
        # Default dimensions are 50x50
        assert center == (125.0, 225.0)

    def test_center_at_origin(self):
        """Test center calculation at origin."""
        node = {"x": 0, "y": 0, "width": 100, "height": 100}
        center = get_node_center(node)
        assert center == (50.0, 50.0)


class TestIsPointOnLineSegment:
    """Test cases for is_point_on_line_segment function."""

    def test_point_on_horizontal_line(self):
        """Test point exactly on horizontal line."""
        point = (150, 200)
        line_start = (100, 200)
        line_end = (200, 200)
        assert is_point_on_line_segment(point, line_start, line_end) is True

    def test_point_off_horizontal_line(self):
        """Test point off horizontal line."""
        point = (150, 250)
        line_start = (100, 200)
        line_end = (200, 200)
        assert is_point_on_line_segment(point, line_start, line_end) is False

    def test_point_near_horizontal_line(self):
        """Test point near horizontal line within tolerance."""
        point = (150, 205)
        line_start = (100, 200)
        line_end = (200, 200)
        # Within default tolerance of 10.0
        assert is_point_on_line_segment(point, line_start, line_end) is True

    def test_point_outside_line_bounds(self):
        """Test point on line extension but outside segment."""
        point = (250, 200)
        line_start = (100, 200)
        line_end = (200, 200)
        assert is_point_on_line_segment(point, line_start, line_end) is False

    def test_point_on_vertical_line(self):
        """Test point on vertical line."""
        point = (200, 150)
        line_start = (200, 100)
        line_end = (200, 200)
        assert is_point_on_line_segment(point, line_start, line_end) is True


class TestAutoSpacingLayout:
    """Test cases for auto_spacing_layout function."""

    def test_empty_nodes(self):
        """Test with empty node list."""
        nodes = []
        result = auto_spacing_layout(nodes)
        assert result == []

    def test_single_node(self):
        """Test with single node (should remain unchanged)."""
        nodes = [
            {
                "x": 100,
                "y": 200,
                "width": 50,
                "height": 50,
                "node_id": "1",
                "name": "r1",
            }
        ]
        result = auto_spacing_layout(nodes)
        assert len(result) == 1
        assert result[0]["x"] == nodes[0]["x"]
        assert result[0]["y"] == nodes[0]["y"]

    def test_overlapping_nodes(self):
        """Test with overlapping nodes."""
        nodes = [
            {
                "x": 100,
                "y": 200,
                "width": 50,
                "height": 50,
                "node_id": "1",
                "name": "r1",
            },
            {
                "x": 110,
                "y": 210,
                "width": 50,
                "height": 50,
                "node_id": "2",
                "name": "r2",
            },
        ]
        min_distance = 150
        result = auto_spacing_layout(
            nodes, min_distance=min_distance, max_iterations=50
        )

        # Nodes should be moved apart
        original_dist = calculate_distance(nodes[0], nodes[1])
        new_dist = calculate_distance(result[0], result[1])

        assert new_dist > original_dist
        assert new_dist >= min_distance - 10  # Allow small tolerance

    def test_well_spaced_nodes(self):
        """Test with nodes already well spaced (should remain unchanged)."""
        nodes = [
            {
                "x": 100,
                "y": 200,
                "width": 50,
                "height": 50,
                "node_id": "1",
                "name": "r1",
            },
            {
                "x": 400,
                "y": 200,
                "width": 50,
                "height": 50,
                "node_id": "2",
                "name": "r2",
            },
        ]
        min_distance = 150
        result = auto_spacing_layout(
            nodes, min_distance=min_distance, max_iterations=50
        )

        # Nodes are already spaced, should not move much
        original_dist = calculate_distance(nodes[0], nodes[1])
        new_dist = calculate_distance(result[0], result[1])

        assert abs(new_dist - original_dist) < 10  # Small movement only

    def test_original_unchanged(self):
        """Test that original nodes are not modified."""
        nodes = [
            {
                "x": 100,
                "y": 200,
                "width": 50,
                "height": 50,
                "node_id": "1",
                "name": "r1",
            },
            {
                "x": 110,
                "y": 210,
                "width": 50,
                "height": 50,
                "node_id": "2",
                "name": "r2",
            },
        ]
        original_x = nodes[0]["x"]
        original_y = nodes[0]["y"]

        auto_spacing_layout(nodes, min_distance=150, max_iterations=10)

        # Original should be unchanged
        assert nodes[0]["x"] == original_x
        assert nodes[0]["y"] == original_y


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
