#!/usr/bin/env python3
"""
Test script to verify rectangle drawing calculations.

This script tests the calculate_two_node_rectangle function with the provided
node data to verify the calculations are correct.
"""

from src.gns3_copilot.public_model.gns3_drawing_utils import calculate_two_node_rectangle

# Test data from user
node1 = {
    "x": -407,
    "y": -259,
    "width": 60,
    "height": 60,
    "name": "R-1"
}

node2 = {
    "x": -95,
    "y": -367,
    "width": 60,
    "height": 60,
    "name": "R-5"
}

# Calculate rectangle parameters
result = calculate_two_node_rectangle(node1, node2, "Area 0")

# Print results
print("=" * 60)
print("矩形绘图参数计算结果")
print("=" * 60)

print("\n输入节点信息:")
print(f"节点1 (R-1): x={node1['x']}, y={node1['y']}, width={node1['width']}, height={node1['height']}")
print(f"节点2 (R-5): x={node2['x']}, y={node2['y']}, width={node2['width']}, height={node2['height']}")

print("\n计算结果:")
print(f"矩形宽度:  {result['metadata']['rect_width']:.2f} 像素")
print(f"矩形高度:  {result['metadata']['rect_height']:.2f} 像素")
print(f"旋转角度:  {result['metadata']['angle_deg']:.0f} 度")
print(f"中心点坐标: ({result['metadata']['center_x']:.2f}, {result['metadata']['center_y']:.2f})")

print("\nSVG绘图参数:")
print(f"SVG x坐标: {result['rectangle']['x']}")
print(f"SVG y坐标: {result['rectangle']['y']}")
print(f"SVG宽度:   {result['rectangle']['svg']}")
print(f"SVG旋转:   {result['rectangle']['rotation']} 度")

print("\n文本标签参数:")
print(f"文本 x坐标: {result['text']['x']}")
print(f"文本 y坐标: {result['text']['y']}")
print(f"文本旋转:   {result['text']['rotation']} 度")

print("\nSVG内容:")
print("矩形SVG:")
print(result['rectangle']['svg'])
print("\n文本SVG:")
print(result['text']['svg'])

print("\n" + "=" * 60)
print("验证:")
print("=" * 60)
print(f"✓ 矩形宽度 (330.16 ≈ {result['metadata']['rect_width']:.2f}): {'通过' if 329 <= result['metadata']['rect_width'] <= 331 else '失败'}")
print(f"✓ 矩形高度 (60.00 ≈ {result['metadata']['rect_height']:.2f}): {'通过' if result['metadata']['rect_height'] == 60 else '失败'}")
print(f"✓ 旋转角度 (-19° ≈ {result['metadata']['angle_deg']:.0f}°): {'通过' if result['metadata']['angle_deg'] == -19 else '失败'}")
print(f"✓ SVG x坐标 (-387 ≈ {result['rectangle']['x']}): {'通过' if -389 <= result['rectangle']['x'] <= -385 else '失败'}")
print(f"✓ SVG y坐标 (-258 ≈ {result['rectangle']['y']}): {'通过' if -260 <= result['rectangle']['y'] <= -256 else '失败'}")

print("\n计算完成!")
