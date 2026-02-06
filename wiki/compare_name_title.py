import re


def transform_name(name):
    # 逻辑：在非首字母的大写字母或数字前插入空格
    # 使用正则：查找 [非起始位置] 且 [大写字母或数字] 的位置进行替换
    return re.sub(r'(?<!^)([A-Z])', r' \1', name)


def process_markdown_table(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 提取表头、分隔线和内容行
    # 假设表格前两行是 Header 和 Separator
    header = lines[0].strip()
    separator = lines[1].strip()
    rows = lines[2:]

    output_rows = []
    # 新表头
    new_header = "| Name | Transformed Name | Original Title | Processed Title (for comparison) |"
    new_separator = "|:---|:---|:---|:---|"

    for row in rows:
        if not row.strip() or '|' not in row:
            continue

        # 分割列并去除前导后置空格
        cols = [c.strip() for c in row.split('|')]
        # col[0] 是表格前的空白, col[1] 是 Name, col[2] 是 Title
        if len(cols) < 3:
            continue

        name = cols[1]
        original_title = cols[2]

        # 1. 生成 Transformed Name
        transformed_name = transform_name(name)

        # 2. 生成用于比较的 Title (若原 Title 为空则取原始 Name)
        comparison_title = original_title if original_title else name

        # 3. 严格比对 (大小写敏感、标点敏感、空格敏感)
        if transformed_name != comparison_title:
            output_rows.append(f"| {name} | {transformed_name} | {original_title} | {comparison_title} |")

    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_header + "\n")
        f.write(new_separator + "\n")
        for r in output_rows:
            f.write(r + "\n")


if __name__ == "__main__":
    # 请确保同级目录下有 input.txt
    process_markdown_table('puzzle_table.txt', 'compare_name_title_output.txt')
    print("处理完成！请查看 output.txt")