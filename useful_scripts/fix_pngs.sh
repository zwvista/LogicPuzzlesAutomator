#!/bin/bash

# 定义输入和输出目录
INPUT_DIR="../images/TileContent2"
OUTPUT_DIR="../images/TileContent2_fixed"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 遍历所有 .png 文件（不递归子目录）
for file in "$INPUT_DIR"/*.png; do
    # 检查文件是否存在（防止空匹配）
    if [ -f "$file" ]; then
        # 获取文件名（不含路径）
        filename=$(basename "$file")
        # 输出路径
        output_file="$OUTPUT_DIR/$filename"
        # 使用 sips 转换为标准 PNG
        sips -s format png "$file" --out "$output_file" >/dev/null
        # 检查是否成功
        if [ $? -eq 0 ]; then
            echo "✅ 已修复: $filename"
        else
            echo "❌ 失败: $filename"
        fi
    fi
done

echo "✅ 所有图像已处理，修复后的图像保存在: $OUTPUT_DIR"