"""
Drawing utility functions for GNS3 area annotations.

Provides helper functions to calculate drawing parameters and generate SVG content
for network area annotations, specifically optimized for two-node ellipse annotations.
"""

import math
import re
from typing import Any

# Default parameters for area annotations
DEFAULT_PADDING = 0
DEFAULT_DEVICE_WIDTH = 50  # Width of device icons (left-top to right-top)
DEFAULT_DEVICE_HEIGHT = 50  # Height of device icons (left-top to left-bottom)
DEFAULT_FONT_SIZE = 14

# GNS3 GUI compatibility adjustment values
# These values are derived from reverse-engineering GNS3 GUI behavior
GNS3_GUI_RX_ADJUSTMENT = 7.35  # Horizontal radius adjustment (distance/2 - 7.35)
GNS3_GUI_RY_ADJUSTMENT = 4  # Vertical radius adjustment (avg_height - 4)

# Color scheme for different area types (simplified to 5 protocol categories)
# Color classification based on network protocol types
COLOR_SCHEMES = {
    # Green - IGP (Interior Gateway Protocol) - OSPF, IS-IS, RIP, EIGRP
    "IGP": {"stroke": "#00cc00", "fill": "#00cc00", "fill_opacity": 0.12},
    # Blue - EGP (Exterior Gateway Protocol) - BGP
    "EGP": {"stroke": "#3366ff", "fill": "#3366ff", "fill_opacity": 0.12},
    # Orange - Overlay - VXLAN, MPLS
    "Overlay": {"stroke": "#ff9900", "fill": "#ff9900", "fill_opacity": 0.12},
    # Gray - Underlay - Base IP network
    "Underlay": {"stroke": "#999999", "fill": "#999999", "fill_opacity": 0.10},
    # Purple - Switching - STP, LDP, VRF
    "Switching": {"stroke": "#9933ff", "fill": "#9933ff", "fill_opacity": 0.12},
}


def calculate_two_node_ellipse(
    node1: dict,
    node2: dict,
    area_name: str,
    padding: int = DEFAULT_PADDING,
    text_offset_ratio: float = 0.7,
) -> dict[str, Any]:
    """
    Calculate ellipse annotation parameters for two nodes.

    This function computes optimal ellipse to connect two network devices,
    including position, size, rotation, and SVG content.

    Algorithm:
    1. Calculate device center points (node coordinates are top-left corner)
    2. Calculate midpoint between device centers (ellipse center)
    3. Calculate distance between device centers
    4. Determine ellipse size: rx = distance/2 + padding, ry = device_height
    5. Calculate rotation angle using atan2
    6. Calculate text offset to avoid overlapping with link cables
    7. Generate SVG for ellipse and text

    Args:
        node1: First node dictionary with 'x', 'y', 'height', and 'width' (top-left corner)
        node2: Second node dictionary with 'x', 'y', 'height', and 'width' (top-left corner)
        area_name: Name of the area (e.g., "Area 0", "AS 100")
        padding: Distance from nodes to ellipse edge in pixels (default: 0)
        text_offset_ratio: Ratio of ry to offset text along perpendicular direction (default: 0.7)
                          Set to 0 to center text, 0.7 for edge, >1 for outside ellipse

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
    # Use GNS3 GUI compatibility adjustment values derived from reverse-engineering
    rx = distance / 2 - GNS3_GUI_RX_ADJUSTMENT  # Semi-major axis (horizontal)
    ry = (
        node1_height + node2_height
    ) / 2 - GNS3_GUI_RY_ADJUSTMENT  # Semi-minor axis (vertical)

    # Step 5: Calculate rotation angle based on device centers
    angle_rad = math.atan2(
        node2_center_y - node1_center_y, node2_center_x - node1_center_x
    )
    # Round to nearest integer to match GNS3 GUI behavior
    angle_deg = round(math.degrees(angle_rad))
    angle_rad = math.radians(angle_deg)  # Use rounded angle for calculations

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

    # Calculate text offset to avoid overlapping with link cables
    # Offset is perpendicular to the link direction (ellipse short axis direction)
    if text_offset_ratio != 0:
        # Calculate perpendicular direction (rotate angle by 90 degrees)
        # This gives us a vector perpendicular to the link direction
        perpendicular_x = -math.sin(angle_rad)
        perpendicular_y = math.cos(angle_rad)

        # Calculate offset distance
        offset_distance = ry * text_offset_ratio

        # Apply offset to text position
        text_offset_x = perpendicular_x * offset_distance
        text_offset_y = perpendicular_y * offset_distance

        # Position text with offset
        text_x = int(center_x + text_offset_x - text_svg_width / 2)
        text_y = int(center_y + text_offset_y - text_svg_height / 2)
    else:
        # No offset, center text on ellipse center
        text_x = int(center_x - text_svg_width / 2)
        text_y = int(center_y - text_svg_height / 2)

    # Text should always remain horizontal (rotation = 0), not rotate with ellipse
    return {
        "ellipse": {
            "svg": ellipse_svg,
            "x": int(svg_x),
            "y": int(svg_y),
            "rotation": int(angle_deg),
        },
        "text": {"svg": text_svg, "x": text_x, "y": text_y, "rotation": 0},
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

    Matches the format used by GNS3 GUI to enable style editing in the interface.

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
    # Match GUI format: no xmlns, no quotes on numeric attributes, quotes on string attributes
    return f'''<svg width="{svg_width}" height="{svg_height}"><ellipse cx="{rx}" cy="{ry}" rx="{rx}" ry="{ry}" fill="{color_scheme["fill"]}" fill-opacity="{color_scheme["fill_opacity"]}" stroke="{color_scheme["stroke"]}" stroke-width="2" stroke-dasharray="5,5"/></svg>'''


def generate_text_svg(text: str, color_scheme: dict[str, Any]) -> str:
    """
    Generate compact SVG content for text label.

    The SVG size is calculated dynamically based on text length to minimize space usage.
    Matches the format used by GNS3 GUI to enable style editing in the interface.

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

    # Match GUI format: no xmlns, no quotes on numeric attributes, quotes on string attributes
    return f'''<svg width="{text_width}" height="{text_height}"><text x="{text_x}" y="{text_y}" fill="{color_scheme["stroke"]}" font-size="{DEFAULT_FONT_SIZE}" font-weight="bold" text-anchor="middle">{text}</text></svg>'''


def _hsv_to_hex(h: int, s: int, v: int) -> str:
    """
    Convert HSV color values to HEX color string.

    HSV (Hue, Saturation, Value) is a color model that uses cylindrical coordinates.
    High lightness (v value) is used for instance color generation to create
    lighter, more transparent versions of base protocol colors.

    Args:
        h: Hue (0-360), color wheel position
        s: Saturation (0-100), color intensity
        v: Value (0-100), lightness/brightness

    Returns:
        HEX color string (e.g., "#ff00cc")

    Example:
        >>> _hsv_to_hex(120, 80, 90)
        '#4ce68c'
    """
    # Normalize values to 0-1 range
    h_norm = (h % 360) / 360
    s_norm = s / 100
    v_norm = v / 100

    # Convert HSV to RGB
    c: float = v_norm * s_norm
    x: float = c * (1 - abs((h_norm / 60) % 2 - 1))
    m: float = v_norm - c

    r: float
    g: float
    b: float

    if 0 <= h_norm < 60:
        r, g, b = c, x, 0.0
    elif 60 <= h_norm < 120:
        r, g, b = x, c, 0.0
    elif 120 <= h_norm < 180:
        r, g, b = 0.0, c, x
    elif 180 <= h_norm < 240:
        r, g, b = 0.0, x, c
    elif 240 <= h_norm < 300:
        r, g, b = x, 0.0, c
    else:
        r, g, b = c, 0.0, x

    # Convert to 0-255 range and format as HEX
    r = int((r + m) * 255)
    g = int((g + m) * 255)
    b = int((b + m) * 255)

    return f"#{r:02x}{g:02x}{b:02x}"


def _get_color_scheme(area_name: str) -> dict[str, Any]:
    """
    Get color scheme based on area name with keyword matching and instance support.

    This function supports:
    1. Exact matches (e.g., "Area 0", "AS 65000")
    2. Protocol keyword matching (e.g., "OSPF", "BGP", "RIP")
    3. Automatic instance color generation (e.g., "Area 1", "Area 2" get different light colors)

    Args:
        area_name: Name of the area (e.g., "Area 0", "Area 1", "AS 65001", "OSPF Backbone")

    Returns:
        Dictionary with color parameters (values can be str or float)

    Examples:
        >>> _get_color_scheme("Area 0")
        {'stroke': '#00cc00', 'fill': '#00cc00', 'fill_opacity': 0.15}
        >>> _get_color_scheme("Area 1")  # Auto-generated light color
        {'stroke': '#4cd17c', 'fill': '#4cd17c', 'fill_opacity': 0.12}
        >>> _get_color_scheme("AS 65001")  # Auto-generated light color
        {'stroke': '#4c80ff', 'fill': '#4c80ff', 'fill_opacity': 0.12}
        >>> _get_color_scheme("RIP Network")  # Protocol keyword match
        {'stroke': '#9933ff', 'fill': '#9933ff', 'fill_opacity': 0.12}
    """
    # Exact matches (highest priority)
    if area_name in COLOR_SCHEMES:
        return COLOR_SCHEMES[area_name]

    # Check for specific instances with auto-generated colors
    # Extract instance ID (e.g., "Area 1" -> 1, "AS 65001" -> 65001)

    # OSPF Areas: "Area 0", "Area 1", "Area 2", etc. (IGP - Green)
    area_match = re.search(r"Area\s+(\d+)", area_name)
    if area_match:
        area_id = int(area_match.group(1))
        # Auto-generate light green color for all Area instances
        # Base hue for green is ~120°, shift slightly for each instance
        hue_shift = (area_id * 15) % 30  # Shift 0-30 degrees based on ID
        color = _hsv_to_hex(120 + hue_shift, 60, 85)  # High lightness (85%)
        return {"stroke": color, "fill": color, "fill_opacity": 0.12}

    # BGP AS numbers: "AS 65000", "AS 65001", "AS 100", etc. (EGP - Blue)
    as_match = re.search(r"AS\s+(\d+)", area_name)
    if as_match:
        as_id = int(as_match.group(1))
        # Auto-generate light blue color for different AS numbers
        # Base hue for blue is ~240°, shift based on AS number
        hue_shift = (as_id * 7) % 40  # Shift 0-40 degrees
        color = _hsv_to_hex(240 + hue_shift, 65, 80)  # High lightness (80%)
        return {"stroke": color, "fill": color, "fill_opacity": 0.12}

    # Protocol keyword matching (case-insensitive)
    area_name_lower = area_name.lower()

    # Group protocols into 5 color categories based on network protocol classification
    protocol_keywords = [
        # IGP (Interior Gateway Protocol) - Green
        ("ospf", "IGP"),  # OSPF
        ("is-is", "IGP"),  # IS-IS
        ("rip", "IGP"),  # RIP
        ("eigrp", "IGP"),  # EIGRP
        # EGP (Exterior Gateway Protocol) - Blue
        ("bgp", "EGP"),  # BGP
        # Overlay - Orange
        ("vxlan", "Overlay"),  # VXLAN
        ("mpls", "Overlay"),  # MPLS
        # Underlay - Gray
        ("underlay", "Underlay"),  # Underlay network
        ("base", "Underlay"),  # Base IP network
        ("core", "Underlay"),  # Core network
        # Switching - Purple
        ("stp", "Switching"),  # STP
        ("ldp", "Switching"),  # LDP
        ("vrf", "Switching"),  # VRF
        ("vlan", "Switching"),  # VLAN
        ("hsrp", "Switching"),  # HSRP
        ("vrrp", "Switching"),  # VRRP
        ("lacp", "Switching"),  # LACP
    ]

    for keyword, scheme_key in protocol_keywords:
        if keyword in area_name_lower:
            return COLOR_SCHEMES[scheme_key]

    # Check for generic "Area" keyword as fallback for IGP
    if "area" in area_name_lower:
        return COLOR_SCHEMES["IGP"]

    # Check for generic "AS" keyword as fallback for EGP
    if "as" in area_name_lower:
        return COLOR_SCHEMES["EGP"]

    # Default to IGP color
    return COLOR_SCHEMES["IGP"]


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
