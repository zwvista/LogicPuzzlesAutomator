#!/bin/bash

# 定义输入和输出目录
INPUT_DIR="../../100LG/Images2/128"
OUTPUT_DIR="../../100LG/Images2/128_fixed"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 遍历所有 .png 和 .jpg 文件（不递归子目录）
for file in "$INPUT_DIR"/*.{png,jpg,jpeg}; do
    # 检查文件是否存在（防止空匹配）
    if [ -f "$file" ]; then
        # 获取文件名（不含路径）
        filename=$(basename "$file")
        # 输出路径（统一转换为 PNG）
        output_file="$OUTPUT_DIR/${filename%.*}.png"
        # 使用 sips 转换为标准 PNG
        sips -s format png "$file" --out "$output_file" >/dev/null
        # 检查是否成功
        if [ $? -eq 0 ]; then
            echo "✅ 已修复并转换为 PNG: $filename"
        else
            echo "❌ 失败: $filename"
        fi
    fi
done

echo "✅ 所有图像已处理，修复后的图像保存在: $OUTPUT_DIR"
