"""
Test script to verify GNS3 GUI compatibility algorithm.

This script tests the new ellipse calculation algorithm using real data
from GNS3 to ensure compatibility with GNS3 GUI behavior.
"""

import math
from gns3_copilot.public_model.gns3_drawing_utils import calculate_two_node_ellipse

# Test data from user's GNS3 project
# R-4 device
node1 = {
    "x": 195,
    "y": -30,
    "width": 60,
    "height": 60,
}

# R-8 device
node2 = {
    "x": 505,
    "y": 134,
    "width": 60,
    "height": 60,
}

# Expected result from actual GNS3 GUI
expected = {
    "svg_x": 250,
    "svg_y": -43,
    "rotation": 26,
    "svg_width": 335,
    "svg_height": 112,
    "rx": 168,
    "ry": 56,
}

print("=" * 60)
print("GNS3 GUI Compatibility Test")
print("=" * 60)

# Calculate using new algorithm
result = calculate_two_node_ellipse(node1, node2, "Area 0")

# Extract calculated values
calculated = {
    "svg_x": result["ellipse"]["x"],
    "svg_y": result["ellipse"]["y"],
    "rotation": result["ellipse"]["rotation"],
    "svg_width": int(result["metadata"]["rx"] * 2),
    "svg_height": int(result["metadata"]["ry"] * 2),
    "rx": int(result["metadata"]["rx"]),
    "ry": int(result["metadata"]["ry"]),
}

print("\n1. Node Coordinates (Top-Left Corner):")
print(f"   R-4: ({node1['x']}, {node1['y']}, size: {node1['width']}x{node1['height']})")
print(f"   R-8: ({node2['x']}, {node2['y']}, size: {node2['width']}x{node2['height']})")

# Calculate node centers
node1_center_x = node1["x"] + node1["width"] / 2
node1_center_y = node1["y"] + node1["height"] / 2
node2_center_x = node2["x"] + node2["width"] / 2
node2_center_y = node2["y"] + node2["height"] / 2

print("\n2. Node Centers:")
print(f"   R-4 Center: ({node1_center_x}, {node1_center_y})")
print(f"   R-8 Center: ({node2_center_x}, {node2_center_y})")

print("\n3. Expected vs Calculated Values:")
print(f"{'Parameter':<15} {'Expected':<15} {'Calculated':<15} {'Diff':<15}")
print("-" * 60)
for key in expected:
    diff = calculated[key] - expected[key]
    print(f"{key:<15} {expected[key]:<15} {calculated[key]:<15} {diff:+.2f}")

# Calculate tolerance
tolerance = 2.5  # Allow 2.5 pixel difference for rendering

print(f"\n4. Tolerance Check (±{tolerance} pixels):")
print("-" * 60)
all_passed = True
for key in expected:
    diff = abs(calculated[key] - expected[key])
    status = "✓ PASS" if diff <= tolerance else "✗ FAIL"
    print(f"{key:<15} | Expected: {expected[key]:<10} | Got: {calculated[key]:<10} | Diff: {diff:.2f} | {status}")
    if diff > tolerance:
        all_passed = False

print("\n5. Metadata:")
print(f"   Center X: {result['metadata']['center_x']:.2f}")
print(f"   Center Y: {result['metadata']['center_y']:.2f}")
print(f"   Distance: {result['metadata']['distance']:.2f}")
print(f"   RX: {result['metadata']['rx']:.2f}")
print(f"   RY: {result['metadata']['ry']:.2f}")
print(f"   Angle: {result['metadata']['angle_deg']:.2f}°")

# Calculate what the ellipse center would be on canvas after rotation
angle_rad = math.radians(calculated["rotation"])
rotated_x = calculated["rx"] * math.cos(angle_rad) - calculated["ry"] * math.sin(angle_rad)
rotated_y = calculated["rx"] * math.sin(angle_rad) + calculated["ry"] * math.cos(angle_rad)

canvas_x = calculated["svg_x"] + rotated_x
canvas_y = calculated["svg_y"] + rotated_y

expected_center_x = (node1_center_x + node2_center_x) / 2
expected_center_y = (node1_center_y + node2_center_y) / 2

print("\n6. Ellipse Center on Canvas (After Rotation):")
print(f"   Expected: ({expected_center_x:.2f}, {expected_center_y:.2f})")
print(f"   Calculated: ({canvas_x:.2f}, {canvas_y:.2f})")
print(f"   Diff: ({canvas_x - expected_center_x:.2f}, {canvas_y - expected_center_y:.2f})")

print("\n" + "=" * 60)
if all_passed:
    print("✅ ALL TESTS PASSED - Algorithm is compatible with GNS3 GUI")
else:
    print("⚠️  SOME TESTS FAILED - Algorithm needs adjustment")
print("=" * 60)

# Additional test: Verify SVG content
print("\n7. SVG Content Preview:")
print(f"   Ellipse SVG: {result['ellipse']['svg'][:80]}...")
print(f"   Text SVG: {result['text']['svg'][:80]}...")
