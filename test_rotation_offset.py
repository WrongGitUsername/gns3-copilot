#!/usr/bin/env python3
"""
Test script to verify ellipse center positioning after rotation offset fix.

This script verifies that when an SVG is rotated by GNS3 around its top-left corner,
the ellipse visual center remains at the correct position on the canvas.
"""

import math
from src.gns3_copilot.public_model.gns3_drawing_utils import calculate_two_node_ellipse


def calculate_visual_center_after_rotation(result):
    """
    Calculate where the ellipse center will be after GNS3 rotates the SVG.
    
    When GNS3 rotates an SVG around its top-left corner (x, y) by angle θ,
    a point at (svg_cx, svg_cy) within the SVG moves to:
    
    canvas_x = x + svg_cx * cos(θ) - svg_cy * sin(θ)
    canvas_y = y + svg_cx * sin(θ) + svg_cy * cos(θ)
    
    For our ellipse, svg_cx = rx and svg_cy = ry (the ellipse center within the SVG)
    
    Args:
        result: Full result dict from calculate_two_node_ellipse
    """
    x = result['ellipse']['x']
    y = result['ellipse']['y']
    rotation = result['ellipse']['rotation']
    rx = result['metadata']['rx']
    ry = result['metadata']['ry']
    
    angle_rad = math.radians(rotation)
    
    # Calculate where ellipse center will be after rotation
    visual_center_x = x + rx * math.cos(angle_rad) - ry * math.sin(angle_rad)
    visual_center_y = y + rx * math.sin(angle_rad) + ry * math.cos(angle_rad)
    
    return visual_center_x, visual_center_y


def run_tests():
    """Run tests to verify rotation offset calculations."""
    
    print("=" * 70)
    print("测试椭圆旋转后的中心位置")
    print("=" * 70)
    
    test_cases = [
        {
            "name": "水平布局 (0°)",
            "node1": {"x": 100, "y": 200, "width": 50, "height": 50},
            "node2": {"x": 300, "y": 200, "width": 50, "height": 50},
        },
        {
            "name": "垂直布局 (90°)",
            "node1": {"x": 200, "y": 100, "width": 50, "height": 50},
            "node2": {"x": 200, "y": 300, "width": 50, "height": 50},
        },
        {
            "name": "对角线布局 (45°)",
            "node1": {"x": 100, "y": 100, "width": 50, "height": 50},
            "node2": {"x": 300, "y": 300, "width": 50, "height": 50},
        },
        {
            "name": "小角度布局 (约8°)",
            "node1": {"x": -100, "y": 100, "width": 50, "height": 50},
            "node2": {"x": 300, "y": 80, "width": 50, "height": 50},
        },
        {
            "name": "负角度布局 (-45°)",
            "node1": {"x": 300, "y": 100, "width": 50, "height": 50},
            "node2": {"x": 100, "y": 300, "width": 50, "height": 50},
        },
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {test_case['name']}")
        print("-" * 70)
        
        result = calculate_two_node_ellipse(
            test_case['node1'],
            test_case['node2'],
            "Area 0"
        )
        
        expected_center_x = result['metadata']['center_x']
        expected_center_y = result['metadata']['center_y']
        angle_deg = result['metadata']['angle_deg']
        
        # Calculate where ellipse center will be after GNS3 rotation
        # Pass the full result dict to get access to metadata
        visual_center_x, visual_center_y = calculate_visual_center_after_rotation(
            result
        )
        
        # Check if visual center matches expected center
        error_x = abs(visual_center_x - expected_center_x)
        error_y = abs(visual_center_y - expected_center_y)
        total_error = math.sqrt(error_x**2 + error_y**2)
        
        print(f"期望中心位置: ({expected_center_x:.2f}, {expected_center_y:.2f})")
        print(f"旋转后视觉中心: ({visual_center_x:.2f}, {visual_center_y:.2f})")
        print(f"旋转角度: {angle_deg:.2f}°")
        print(f"位置误差: ΔX={error_x:.4f}, ΔY={error_y:.4f}, 总误差={total_error:.4f} 像素")
        
        if total_error < 2.5:  # Allow small floating point and rounding errors
            print("✅ 测试通过 - 椭圆中心位置正确")
        else:
            print("❌ 测试失败 - 椭圆中心位置偏移")
            all_passed = False
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ 所有测试通过！")
    else:
        print("❌ 部分测试失败！")
    print("=" * 70)
    
    return all_passed


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
