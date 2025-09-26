#!/bin/bash

# 进入 128 目录
cd images/128 || { echo "目录 128 不存在"; exit 1; }

# 遍历所有 .png 文件（区分大小写）
for file in *.png; do
    # 检查文件是否存在（防止无匹配时出错）
    if [[ -f "$file" ]]; then
        # 获取文件名（不含扩展名）
        filename="${file%.*}"
        # 获取扩展名
        ext="${file##*.}"
        # 重命名：添加 128_ 前缀
        mv "$file" "128_${filename}.${ext}"
        echo "已重命名: $file -> 128_${filename}.${ext}"
    fi
done

echo "✅ 所有 PNG 文件已添加 128_ 前缀"