"""
Layout utility functions for GNS3 node positioning.

Provides helper functions to calculate optimal node positions using the
auto_spacing algorithm to solve issues like overlapping nodes, uneven spacing,
and nodes positioned on link cables.
"""

import math
from typing import Any

# Default parameters for layout algorithms
DEFAULT_MIN_DISTANCE = 150  # Minimum distance between nodes in pixels
DEFAULT_ITERATIONS = 100  # Default number of iterations

# GNS3 GUI compatibility
DEFAULT_NODE_WIDTH = 50  # Width of device icons
DEFAULT_NODE_HEIGHT = 50  # Height of device icons


def calculate_distance(node1: dict[str, Any], node2: dict[str, Any]) -> float:
    """
    Calculate Euclidean distance between two nodes.

    Args:
        node1: First node dictionary with 'x' and 'y' coordinates
        node2: Second node dictionary with 'x' and 'y' coordinates

    Returns:
        Euclidean distance between the two nodes

    Example:
        >>> node1 = {"x": 100, "y": 200}
        >>> node2 = {"x": 300, "y": 200}
        >>> calculate_distance(node1, node2)
        200.0
    """
    dx = node2["x"] - node1["x"]
    dy = node2["y"] - node1["y"]
    return math.sqrt(dx * dx + dy * dy)


def auto_spacing_layout(
    nodes: list[dict[str, Any]],
    links: list[dict[str, Any]] | None = None,
    min_distance: int = DEFAULT_MIN_DISTANCE,
    max_iterations: int = DEFAULT_ITERATIONS,
    step_size: float = 0.1,
    safety_margin: float = 20.0,
    cable_ratio: float = 0.15,
    cable_strength: float = 0.5,
) -> list[dict[str, Any]]:
    """
    Automatically adjust node positions to maintain minimum spacing and avoid cables.

    This algorithm solves issues where nodes are too close to each other,
    overlapping, or positioned on link cables. It applies repulsive
    forces between nodes that are closer than the minimum distance,
    and pushes nodes away from cables to prevent visual overlaps.

    Algorithm:
    1. For each iteration:
       a. Calculate distances between all node pairs
       b. If distance < min_distance, apply repulsive force
       c. If links provided and node is near cable, push away from cable
       d. Move nodes in the direction of the force by step_size
    2. Repeat until max_iterations or no more adjustments needed

    Args:
        nodes: List of node dictionaries with 'x', 'y', 'width', 'height', 'node_id', 'name'
        links: List of link dictionaries with 'nodes' array containing node positions
                (optional, default: None - no cable constraints applied)
        min_distance: Minimum desired distance between nodes in pixels (default: 150)
        max_iterations: Maximum number of iterations to perform (default: 100)
        step_size: Step size for node movement, 0.0-1.0 (default: 0.1)
                   Smaller values = more precise but slower convergence
        safety_margin: Additional safety margin for node labels (default: 20.0 pixels)
        cable_ratio: Ratio of min_distance for cable push distance (default: 0.15)
        cable_strength: Push strength factor for cable avoidance (default: 0.5)

    Returns:
        List of node dictionaries with updated 'x' and 'y' coordinates

    Example:
        >>> nodes = [
        ...     {"x": 100, "y": 200, "width": 50, "height": 50, "node_id": "1", "name": "r1"},
        ...     {"x": 110, "y": 210, "width": 50, "height": 50, "node_id": "2", "name": "r2"}
        ... ]
        >>> links = [
        ...     {"nodes": [{"node_id": "1", "x": 100, "y": 200}, {"node_id": "2", "x": 300, "y": 200}]}
        ... ]
        >>> adjusted = auto_spacing_layout(nodes, links=links, min_distance=150)
        >>> print(f"Distance: {calculate_distance(adjusted[0], adjusted[1]):.0f}")
        150
    """
    if not nodes:
        return nodes

    # Create a copy to avoid modifying original
    adjusted_nodes = [node.copy() for node in nodes]

    for _iteration in range(max_iterations):
        moved = False

        # Check all pairs of nodes for spacing
        for i in range(len(adjusted_nodes)):
            for j in range(i + 1, len(adjusted_nodes)):
                node1 = adjusted_nodes[i]
                node2 = adjusted_nodes[j]

                # Calculate distance between nodes
                dist = calculate_distance(node1, node2)

                # Apply repulsion if too close
                if dist < min_distance and dist > 0:
                    # Calculate direction vector from node2 to node1
                    dx = node1["x"] - node2["x"]
                    dy = node1["y"] - node2["y"]

                    # Normalize and scale by distance deficit
                    force = (min_distance - dist) / dist
                    dx *= force * step_size
                    dy *= force * step_size

                    # Move nodes apart
                    node1["x"] += dx / 2
                    node1["y"] += dy / 2
                    node2["x"] -= dx / 2
                    node2["y"] -= dy / 2

                    moved = True

        # Apply cable constraints if links are provided
        if links:
            for node in adjusted_nodes:
                for link in links:
                    # Check if node is near cable
                    if is_node_near_cable(node, link, tolerance=15.0):
                        # Push node away from cable
                        push_node_away_from_cable(
                            node,
                            link,
                            min_distance=min_distance,
                            safety_margin=safety_margin,
                            cable_ratio=cable_ratio,
                            strength=cable_strength,
                        )
                        moved = True

        # Exit early if no nodes moved
        if not moved:
            break

    return adjusted_nodes


def get_node_center(node: dict[str, Any]) -> tuple[float, float]:
    """
    Get the center point of a node.

    Args:
        node: Node dictionary with 'x', 'y', and optional 'width', 'height'

    Returns:
        Tuple of (center_x, center_y)

    Example:
        >>> node = {"x": 100, "y": 200, "width": 50, "height": 50}
        >>> get_node_center(node)
        (125.0, 225.0)
    """
    width = float(node.get("width", DEFAULT_NODE_WIDTH))
    height = float(node.get("height", DEFAULT_NODE_HEIGHT))
    center_x = float(node["x"]) + (width / 2)
    center_y = float(node["y"]) + (height / 2)
    return center_x, center_y


def distance_point_to_line(
    point: tuple[float, float],
    line_start: tuple[float, float],
    line_end: tuple[float, float],
) -> float:
    """
    Calculate the shortest distance from a point to a line segment.

    Args:
        point: Point coordinates (x, y)
        line_start: Line segment start point (x, y)
        line_end: Line segment end point (x, y)

    Returns:
        Shortest distance from point to line segment

    Example:
        >>> point = (125, 50)
        >>> line_start = (0, 0)
        >>> line_end = (250, 0)
        >>> distance_point_to_line(point, line_start, line_end)
        50.0
    """
    px, py = point
    x1, y1 = line_start
    x2, y2 = line_end

    # Calculate line segment length squared
    line_length_sq = (x2 - x1) ** 2 + (y2 - y1) ** 2

    if line_length_sq == 0:
        # Line segment is a point
        return math.sqrt((px - x1) ** 2 + (py - y1) ** 2)

    # Calculate projection parameter t
    t = ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / line_length_sq

    # Limit t to [0, 1] range (on the line segment)
    t = max(0, min(1, t))

    # Calculate projection point on the line
    projection_x = x1 + t * (x2 - x1)
    projection_y = y1 + t * (y2 - y1)

    # Calculate distance from point to projection
    distance = math.sqrt((px - projection_x) ** 2 + (py - projection_y) ** 2)

    return distance


def is_point_on_line_segment(
    point: tuple[float, float],
    line_start: tuple[float, float],
    line_end: tuple[float, float],
    tolerance: float = 10.0,
) -> bool:
    """
    Check if a point is on a line segment within a tolerance.

    This function can be used to detect if a node is positioned on
    or near a link cable.

    Args:
        point: (x, y) coordinates of point to check
        line_start: (x, y) coordinates of line segment start
        line_end: (x, y) coordinates of line segment end
        tolerance: Maximum distance from line to consider "on" the line (default: 10.0)

    Returns:
        True if point is within tolerance of line segment, False otherwise

    Example:
        >>> point = (150, 200)
        >>> line_start = (100, 200)
        >>> line_end = (200, 200)
        >>> is_point_on_line_segment(point, line_start, line_end)
        True
    """
    distance = distance_point_to_line(point, line_start, line_end)
    return distance <= tolerance


def get_node_rectangle(node: dict[str, Any]) -> tuple[float, float, float, float]:
    """
    Get the rectangular bounding box of a node.

    Calculates the four corners of the node rectangle based on its
    position and dimensions. In GNS3, (x, y) represents the
    top-left corner of the node icon.

    Args:
        node: Node dictionary with 'x', 'y', 'width', 'height'

    Returns:
        Tuple of (min_x, min_y, max_x, max_y) representing the
        rectangle boundaries

    Example:
        >>> node = {"x": 100, "y": 200, "width": 50, "height": 50}
        >>> rect = get_node_rectangle(node)
        >>> print(rect)
        (100.0, 200.0, 150.0, 250.0)
    """
    node_x = node.get("x", 0)
    node_y = node.get("y", 0)
    width = node.get("width", DEFAULT_NODE_WIDTH)
    height = node.get("height", DEFAULT_NODE_HEIGHT)

    min_x = float(node_x)
    min_y = float(node_y)
    max_x = float(node_x + width)
    max_y = float(node_y + height)

    return (min_x, min_y, max_x, max_y)


def line_intersects_rectangle(
    line_start: tuple[float, float],
    line_end: tuple[float, float],
    rect: tuple[float, float, float, float],
) -> bool:
    """
    Check if a line segment intersects with a rectangle.

    This function performs two checks:
    1. Checks if either line endpoint is inside the rectangle
    2. Checks if the line intersects any of the four rectangle edges

    Args:
        line_start: Line segment start point (x, y)
        line_end: Line segment end point (x, y)
        rect: Rectangle bounds as (min_x, min_y, max_x, max_y)

    Returns:
        True if line segment intersects rectangle, False otherwise

    Example:
        >>> line_start = (100, 225)
        >>> line_end = (150, 225)
        >>> rect = (100.0, 200.0, 150.0, 250.0)
        >>> line_intersects_rectangle(line_start, line_end, rect)
        True
    """
    x1, y1 = line_start
    x2, y2 = line_end
    min_x, min_y, max_x, max_y = rect

    # Check if either endpoint is inside the rectangle
    def point_in_rect(px: float, py: float) -> bool:
        return min_x <= px <= max_x and min_y <= py <= max_y

    if point_in_rect(x1, y1) or point_in_rect(x2, y2):
        return True

    # Check if line intersects any of the four rectangle edges
    def line_segments_intersect(x3: float, y3: float, x4: float, y4: float) -> bool:
        """Check if line (x1,y1)-(x2,y2) intersects with (x3,y3)-(x4,y4)"""

        def ccw(
            ax: float, ay: float, bx: float, by: float, cx: float, cy: float
        ) -> bool:
            return (cy - ay) * (bx - ax) > (by - ay) * (cx - ax)

        a, b, c, d = (x1, y1), (x2, y2), (x3, y3), (x4, y4)
        return ccw(a[0], a[1], c[0], c[1], d[0], d[1]) != ccw(
            b[0], b[1], c[0], c[1], d[0], d[1]
        ) and ccw(a[0], a[1], b[0], b[1], c[0], c[1]) != ccw(
            a[0], a[1], b[0], b[1], d[0], d[1]
        )

    # Check intersection with all four edges
    # Top edge: (min_x, min_y) to (max_x, min_y)
    if line_segments_intersect(min_x, min_y, max_x, min_y):
        return True
    # Right edge: (max_x, min_y) to (max_x, max_y)
    if line_segments_intersect(max_x, min_y, max_x, max_y):
        return True
    # Bottom edge: (max_x, max_y) to (min_x, max_y)
    if line_segments_intersect(max_x, max_y, min_x, max_y):
        return True
    # Left edge: (min_x, max_y) to (min_x, min_y)
    if line_segments_intersect(min_x, max_y, min_x, min_y):
        return True

    return False


def is_node_near_cable(
    node: dict[str, Any],
    link: dict[str, Any],
    tolerance: float = 15.0,
) -> bool:
    """
    Check if a node is positioned on or near a link cable.

    This function uses rectangle intersection detection to check if
    the node's bounding box intersects with the cable line segment.
    This is more accurate than checking only the center point.

    Args:
        node: Node dictionary with 'x', 'y', 'width', 'height'
        link: Link dictionary with 'nodes' array containing node information
        tolerance: Maximum distance to consider "near" the cable (default: 15.0 pixels)
                   Note: For rectangle-based detection, this is used as a fallback
                   when using center point detection

    Returns:
        True if node rectangle intersects with cable, False otherwise

    Example:
        >>> node = {"x": 125, "y": 50, "width": 50, "height": 50}
        >>> link = {
        ...     "nodes": [
        ...         {"node_id": "1", "x": 0, "y": 0},
        ...         {"node_id": "2", "x": 250, "y": 0}
        ...     ]
        ... }
        >>> is_node_near_cable(node, link)
        False
    """
    if "nodes" not in link or len(link["nodes"]) < 2:
        return False

    # Get node rectangle
    node_rect = get_node_rectangle(node)

    # Get cable endpoints (using node centers)
    node_a = link["nodes"][0]
    node_b = link["nodes"][1]

    point_a = get_node_center(node_a)
    point_b = get_node_center(node_b)

    # Check if cable line intersects node rectangle
    return line_intersects_rectangle(point_a, point_b, node_rect)


def calculate_cable_push_distance(
    node: dict[str, Any],
    min_distance: float,
    safety_margin: float = 20.0,
    cable_ratio: float = 0.15,
) -> float:
    """
    Calculate the distance a node should be pushed away from a cable.

    The push distance is calculated as:
        push_distance = (node_radius) + safety_margin + (min_distance * cable_ratio)

    This ensures:
    1. The node icon doesn't overlap with cable (node_radius)
    2. The node label doesn't overlap with cable (safety_margin)
    3. Consistency with node spacing (min_distance * cable_ratio)

    Args:
        node: Node dictionary containing 'width' and 'height'
        min_distance: Minimum distance between nodes
        safety_margin: Additional safety margin for node labels (default: 20.0 pixels)
        cable_ratio: Ratio of min_distance to add (default: 0.15)

    Returns:
        Calculated push distance in pixels

    Example:
        >>> node = {"width": 50, "height": 50}
        >>> push_dist = calculate_cable_push_distance(node, min_distance=250)
        >>> print(f"Push distance: {push_dist:.0f} pixels")
        Push distance: 83 pixels
        # (50/2) + 20 + (250 * 0.15) = 25 + 20 + 37.5 = 82.5
    """
    # Get node actual dimensions (default to 50x50)
    node_width = float(node.get("width", DEFAULT_NODE_WIDTH))
    node_height = float(node.get("height", DEFAULT_NODE_HEIGHT))

    # Calculate node radius (half of max dimension)
    node_radius = max(node_width, node_height) / 2.0

    # Calculate push distance
    # = node_radius (ensure icon doesn't overlap)
    # + safety_margin (ensure label doesn't overlap)
    # + ratio_distance (maintain consistency with node spacing)
    push_distance = node_radius + safety_margin + (min_distance * cable_ratio)

    return push_distance


def push_node_away_from_cable(
    node: dict[str, Any],
    link: dict[str, Any],
    min_distance: float,
    safety_margin: float = 20.0,
    cable_ratio: float = 0.15,
    strength: float = 0.5,
) -> None:
    """
    Push a node away from a cable along with perpendicular direction.

    This function calculates perpendicular direction to cable,
    determines which side of the cable the node is on,
    and pushes node away until it reaches to target distance.

    Args:
        node: Node dictionary with 'x', 'y', 'width', 'height'
        link: Link dictionary with 'nodes' array containing node information
        min_distance: Minimum distance between nodes
        safety_margin: Safety margin for node labels (default: 20.0 pixels)
        cable_ratio: Ratio of min_distance (default: 0.15)
        strength: Push strength factor, 0.0-1.0 (default: 0.5)
                  Lower values = more gradual movement

    Example:
        >>> node = {"x": 125, "y": 0, "width": 50, "height": 50}
        >>> link = {
        ...     "nodes": [
        ...         {"node_id": "1", "x": 0, "y": 0},
        ...         {"node_id": "2", "x": 250, "y": 0}
        ...     ]
        ... }
        >>> push_node_away_from_cable(node, link, min_distance=250)
        >>> # Node will be pushed to (125, ~83)
    """
    # Calculate target push distance
    target_distance = calculate_cable_push_distance(
        node, min_distance, safety_margin, cable_ratio
    )

    # Get cable endpoints
    node_a = link["nodes"][0]
    node_b = link["nodes"][1]

    point_a = get_node_center(node_a)
    point_b = get_node_center(node_b)

    # Calculate cable direction vector
    dx = point_b[0] - point_a[0]
    dy = point_b[1] - point_a[1]

    # Calculate perpendicular vector (normal)
    # Two possible directions: (-dy, dx) and (dy, -dx)
    normal_x = -dy
    normal_y = dx

    # Normalize
    length = math.sqrt(normal_x**2 + normal_y**2)
    if length > 0:
        normal_x /= length
        normal_y /= length

    # Get current node center
    node_center = get_node_center(node)

    # Calculate current distance to cable
    current_distance = distance_point_to_line(node_center, point_a, point_b)

    # Push node if current distance is less than target
    if current_distance < target_distance:
        # Determine which side of the cable the node is on
        # by projecting node center onto the normal vector
        # This works for all cable orientations (horizontal, vertical, diagonal)
        node_vector_x = node_center[0] - point_a[0]
        node_vector_y = node_center[1] - point_a[1]

        # Dot product to determine direction
        dot_product = node_vector_x * normal_x + node_vector_y * normal_y

        # If dot product is negative, node is in opposite direction
        # so we need to flip the normal vector
        if dot_product < 0:
            normal_x = -normal_x
            normal_y = -normal_y

        deficit = target_distance - current_distance

        # Apply push force in the correct direction
        node["x"] += normal_x * deficit * strength
        node["y"] += normal_y * deficit * strength


if __name__ == "__main__":
    # Test auto_spacing_layout
    print("Testing auto_spacing_layout...")

    nodes = [
        {"x": 100, "y": 200, "width": 50, "height": 50, "node_id": "1", "name": "r1"},
        {"x": 110, "y": 210, "width": 50, "height": 50, "node_id": "2", "name": "r2"},
    ]
    adjusted = auto_spacing_layout(nodes, min_distance=150, max_iterations=100)
    dist = calculate_distance(adjusted[0], adjusted[1])
    print(f"Original distance: {calculate_distance(nodes[0], nodes[1]):.0f}")
    print(f"Adjusted distance: {dist:.0f}")
    # Allow small margin for rounding errors
    print(f"Status: {'PASS' if dist >= 148 else 'FAIL'}\n")

    # Test diagonal cable push
    print("Testing diagonal cable push...")
    # Create a diagonal cable from (0, 0) to (200, 200)
    link = {
        "nodes": [
            {"node_id": "1", "x": 0, "y": 0, "width": 50, "height": 50},
            {"node_id": "2", "x": 200, "y": 200, "width": 50, "height": 50},
        ]
    }

    # Node positioned near the diagonal cable
    node = {"x": 95, "y": 95, "width": 50, "height": 50, "node_id": "3", "name": "r3"}

    print(f"Original node position: ({node['x']}, {node['y']})")

    # Check if node is near cable
    is_near = is_node_near_cable(node, link, tolerance=15.0)
    print(f"Node near cable: {is_near}")

    if is_near:
        # Calculate current distance to cable
        node_center = get_node_center(node)
        point_a = get_node_center(link["nodes"][0])
        point_b = get_node_center(link["nodes"][1])
        current_dist = distance_point_to_line(node_center, point_a, point_b)
        print(f"Current distance to cable: {current_dist:.1f}")

        # Push node away from cable
        push_node_away_from_cable(node, link, min_distance=200, strength=1.0)

        # Calculate new distance
        new_dist = distance_point_to_line(get_node_center(node), point_a, point_b)
        print(f"New node position: ({node['x']:.1f}, {node['y']:.1f})")
        print(f"New distance to cable: {new_dist:.1f}")

        target_dist = calculate_cable_push_distance(node, min_distance=200)
        print(f"Target distance: {target_dist:.1f}")

        # Verify node moved away from cable
        if new_dist > current_dist:
            print("Status: PASS (Node pushed away from cable)")
        else:
            print("Status: FAIL (Node not pushed correctly)")
    else:
        print("Status: SKIP (Node not near cable)")
