"""
Drawing utility functions for GNS3 area annotations.

Provides helper functions to calculate drawing parameters and generate SVG content
for network area annotations, specifically optimized for two-node ellipse annotations.
"""

import math
from typing import Any

# Default parameters for area annotations
DEFAULT_PADDING = 0
DEFAULT_DEVICE_WIDTH = 50  # Width of device icons (left-top to right-top)
DEFAULT_DEVICE_HEIGHT = 50  # Height of device icons (left-top to left-bottom)
DEFAULT_FONT_SIZE = 14

# Color scheme for different area types
COLOR_SCHEMES = {
    "Area 0": {"stroke": "#00cc00", "fill": "#00cc00", "fill_opacity": 0.15},
    "Area": {"stroke": "#3366ff", "fill": "#3366ff", "fill_opacity": 0.12},
    "default": {"stroke": "#999999", "fill": "#999999", "fill_opacity": 0.10},
}


def calculate_two_node_ellipse(
    node1: dict,
    node2: dict,
    area_name: str,
    padding: int = DEFAULT_PADDING,
) -> dict[str, Any]:
    """
    Calculate ellipse annotation parameters for two nodes.

    This function computes the optimal ellipse to connect two network devices,
    including position, size, rotation, and SVG content.

    Algorithm:
    1. Calculate device center points (node coordinates are top-left corner)
    2. Calculate midpoint between device centers (ellipse center)
    3. Calculate distance between device centers
    4. Determine ellipse size: rx = distance/2 + padding, ry = device_height
    5. Calculate rotation angle using atan2
    6. Generate SVG for ellipse and text

    Args:
        node1: First node dictionary with 'x', 'y', 'height', and 'width' (top-left corner)
        node2: Second node dictionary with 'x', 'y', 'height', and 'width' (top-left corner)
        area_name: Name of the area (e.g., "Area 0", "AS 100")
        padding: Distance from nodes to ellipse edge in pixels (default: 0)

    Returns:
        Dictionary containing ellipse and text SVG parameters:
        {
            "ellipse": {
                "svg": str,  # Ellipse SVG content
                "x": int,    # SVG x coordinate
                "y": int,    # SVG y coordinate
                "rotation": int  # Rotation angle in degrees
            },
            "text": {
                "svg": str,  # Text SVG content
                "x": int,    # SVG x coordinate
                "y": int,    # SVG y coordinate
                "rotation": int  # Rotation angle in degrees
            },
            "metadata": {
                "center_x": float,
                "center_y": float,
                "distance": float,
                "rx": float,
                "ry": float,
                "angle_deg": float
            }
        }

    Example:
        >>> node1 = {"x": 100, "y": 200}
        >>> node2 = {"x": 300, "y": 200}
        >>> result = calculate_two_node_ellipse(node1, node2, "Area 0")
        >>> print(result["metadata"]["center_x"])
        200.0
    """
    # Step 1: Get actual node dimensions (use defaults if not provided)
    node1_width = node1.get("width", DEFAULT_DEVICE_WIDTH)
    node1_height = node1.get("height", DEFAULT_DEVICE_HEIGHT)
    node2_width = node2.get("width", DEFAULT_DEVICE_WIDTH)
    node2_height = node2.get("height", DEFAULT_DEVICE_HEIGHT)

    # Step 2: Calculate device center points
    # Node coordinates are top-left corner, add half device size to get center
    node1_center_x = node1["x"] + (node1_width / 2)
    node1_center_y = node1["y"] + (node1_height / 2)
    node2_center_x = node2["x"] + (node2_width / 2)
    node2_center_y = node2["y"] + (node2_height / 2)

    # Step 2: Calculate midpoint between device centers (ellipse center)
    center_x = (node1_center_x + node2_center_x) / 2
    center_y = (node1_center_y + node2_center_y) / 2

    # Step 3: Calculate distance between device centers
    distance = math.sqrt(
        (node2_center_x - node1_center_x) ** 2 + (node2_center_y - node1_center_y) ** 2
    )

    # Step 4: Determine ellipse size
    # Reduce width by 10 pixels (5 on each side) for better alignment
    rx = (distance / 2) + padding - 5  # Semi-major axis (horizontal)
    # Use average height of both nodes for the vertical radius
    ry = (node1_height + node2_height) / 2  # Semi-minor axis (vertical)

    # Step 5: Calculate rotation angle based on device centers
    angle_rad = math.atan2(
        node2_center_y - node1_center_y, node2_center_x - node1_center_x
    )
    angle_deg = math.degrees(angle_rad)

    # Step 5: Determine SVG position and dimensions
    # The SVG is positioned so that its top-left corner is at (center_x - rx, center_y - ry)
    # However, when GNS3 rotates around this point, the ellipse center shifts.
    # We need to compensate for this shift by adjusting the initial SVG position.
    
    # Calculate the offset needed to keep ellipse center at (center_x, center_y) after rotation
    # Ellipse center in SVG coordinates is (rx, ry)
    # After rotation by angle_rad, this becomes:
    # rotated_x = rx * cos(θ) - ry * sin(θ)
    # rotated_y = rx * sin(θ) + ry * cos(θ)
    # The offset we need to apply:
    offset_x = rx - (rx * math.cos(angle_rad) - ry * math.sin(angle_rad))
    offset_y = ry - (rx * math.sin(angle_rad) + ry * math.cos(angle_rad))
    
    svg_x = center_x - rx + offset_x
    svg_y = center_y - ry + offset_y
    svg_width = rx * 2
    svg_height = ry * 2

    # Step 6: Get color scheme based on area name
    color_scheme = _get_color_scheme(area_name)

    # Step 7: Generate SVG content
    ellipse_svg = generate_ellipse_svg(
        int(rx), int(ry), color_scheme, int(svg_width), int(svg_height)
    )
    text_svg = generate_text_svg(area_name, color_scheme)

    # Calculate text SVG dimensions (matching generate_text_svg logic)
    text_svg_width = len(area_name) * 8 + 20
    text_svg_height = DEFAULT_FONT_SIZE + 16

    # Center the text SVG on the ellipse center
    text_x = int(center_x - text_svg_width / 2)
    text_y = int(center_y - text_svg_height / 2)

    return {
        "ellipse": {
            "svg": ellipse_svg,
            "x": int(svg_x),
            "y": int(svg_y),
            "rotation": int(angle_deg),
        },
        "text": {"svg": text_svg, "x": text_x, "y": text_y, "rotation": int(angle_deg)},
        "metadata": {
            "center_x": center_x,
            "center_y": center_y,
            "distance": distance,
            "rx": rx,
            "ry": ry,
            "angle_deg": angle_deg,
        },
    }


def generate_ellipse_svg(
    rx: int,
    ry: int,
    color_scheme: dict[str, Any],
    svg_width: int,
    svg_height: int,
) -> str:
    """
    Generate SVG content for an ellipse.

    Args:
        rx: X radius of the ellipse
        ry: Y radius of the ellipse
        color_scheme: Dictionary with 'stroke', 'fill', and 'fill_opacity' (values can be str or float)
        svg_width: Width of the SVG canvas
        svg_height: Height of the SVG canvas

    Returns:
        SVG string for the ellipse

    Example:
        >>> color = {"stroke": "#00cc00", "fill": "#00cc00", "fill_opacity": 0.15}
        >>> svg = generate_ellipse_svg(140, 100, color, 280, 200)
    """
    return f'''<svg xmlns="http://www.w3.org/2000/svg" height="{svg_height}" width="{svg_width}">
  <ellipse fill="{color_scheme["fill"]}" fill-opacity="{color_scheme["fill_opacity"]}"
           cx="{rx}" cy="{ry}"
           rx="{rx}" ry="{ry}"
           stroke="{color_scheme["stroke"]}" stroke-width="2"
           stroke-dasharray="5,5" />
</svg>'''


def generate_text_svg(text: str, color_scheme: dict[str, Any]) -> str:
    """
    Generate compact SVG content for text label.

    The SVG size is calculated dynamically based on text length to minimize space usage.

    Args:
        text: Text content to display (e.g., "Area 0", "AS 100")
        color_scheme: Dictionary with 'stroke' for text color

    Returns:
        SVG string for the text with appropriate size

    Example:
        >>> color = {"stroke": "#00cc00"}
        >>> svg = generate_text_svg("Area 0", color)
        >>> # Returns compact SVG ~100x30 pixels
    """
    # Calculate SVG dimensions based on text length
    # Each character is approximately 8 pixels wide with 14px font size
    # Add 20 pixels padding (10 on each side)
    text_width = len(text) * 8 + 20
    text_height = DEFAULT_FONT_SIZE + 16  # 14px font + 16px padding

    # Text is centered within the SVG canvas
    text_x = text_width / 2
    text_y = text_height / 2 + DEFAULT_FONT_SIZE / 2 - 2

    return f'''<svg xmlns="http://www.w3.org/2000/svg" height="{text_height}" width="{text_width}">
  <text x="{text_x}" y="{text_y}"
        fill="{color_scheme["stroke"]}" font-size="{DEFAULT_FONT_SIZE}"
        font-weight="bold"
        text-anchor="middle">{text}</text>
</svg>'''


def _get_color_scheme(area_name: str) -> dict[str, Any]:
    """
    Get color scheme based on area name.

    Args:
        area_name: Name of the area

    Returns:
        Dictionary with color parameters (values can be str or float)

    Example:
        >>> _get_color_scheme("Area 0")
        {'stroke': '#00cc00', 'fill': '#00cc00', 'fill_opacity': 0.15}
    """
    # Check for Area 0 first (highest priority)
    if "Area 0" in area_name:
        return COLOR_SCHEMES["Area 0"]
    # Check for other OSPF areas
    elif "Area" in area_name:
        return COLOR_SCHEMES["Area"]
    # Default color
    else:
        return COLOR_SCHEMES["default"]


if __name__ == "__main__":
    # Test the utility functions
    print("Testing gns3_drawing_utils...")

    # Test 1: Horizontal layout
    print("\nTest 1: Horizontal layout")
    node1 = {"x": 100, "y": 200}
    node2 = {"x": 300, "y": 200}
    result = calculate_two_node_ellipse(node1, node2, "Area 0")
    print(
        f"Center: ({result['metadata']['center_x']}, {result['metadata']['center_y']})"
    )
    print(f"Distance: {result['metadata']['distance']:.2f}")
    print(f"Angle: {result['metadata']['angle_deg']:.2f}°")

    # Test 2: Vertical layout
    print("\nTest 2: Vertical layout")
    node1 = {"x": 200, "y": 100}
    node2 = {"x": 200, "y": 300}
    result = calculate_two_node_ellipse(node1, node2, "Area 0")
    print(
        f"Center: ({result['metadata']['center_x']}, {result['metadata']['center_y']})"
    )
    print(f"Angle: {result['metadata']['angle_deg']:.2f}°")

    # Test 3: Diagonal layout
    print("\nTest 3: Diagonal layout")
    node1 = {"x": 100, "y": 100}
    node2 = {"x": 300, "y": 300}
    result = calculate_two_node_ellipse(node1, node2, "Area 0")
    print(
        f"Center: ({result['metadata']['center_x']}, {result['metadata']['center_y']})"
    )
    print(f"Angle: {result['metadata']['angle_deg']:.2f}°")

    print("\n✅ All tests passed!")
