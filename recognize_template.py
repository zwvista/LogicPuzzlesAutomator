import cv2
import numpy as np
import os


def check_template_in_region_optimized(large_image_path, template_path, top_left_coord, size, max_diff=0.3):
    """
    检查大图的指定区域内是否包含带透明背景的模板图，使用 TM_SQDIFF_NORMED 方法，
    并在匹配前将模板缩放到 ROI 的大小。

    参数:
    ...
    size (tuple): 待检查区域的宽度和高度 (width, height)。
    max_diff (float): 允许的最大差异值 (0.0 到 1.0)。
    """
    if not os.path.exists(large_image_path) or not os.path.exists(template_path):
        print("错误：找不到图像文件。")
        return False

    # 1. 加载图像（带透明度）
    template_img_4channel = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    large_img = cv2.imread(large_image_path)

    if template_img_4channel is None or large_img is None:
        print("错误：无法加载图像文件。")
        return False

    w_roi, h_roi = size  # 待检查区域的宽度和高度 (114, 114)

    # --- 关键修正：根据 ROI 尺寸缩放模板 ---

    # 缩放模板到 ROI 的尺寸 (128x128 -> 114x114)
    # INTER_AREA 通常是缩小图像的首选方法
    template_resized = cv2.resize(
        template_img_4channel,
        (w_roi, h_roi),
        interpolation=cv2.INTER_AREA
    )

    # 分离 BGR 和 Alpha 通道
    if template_resized.shape[2] == 4:
        template_to_match = template_resized[:, :, :3]
        template_mask = template_resized[:, :, 3]
    else:
        template_to_match = template_resized
        template_mask = None

    # 2. 裁剪指定区域
    x, y = top_left_coord

    # 裁剪区域 (ROI)
    # 确保裁剪区域在大图范围内
    if x < 0 or y < 0 or x + w_roi > large_img.shape[1] or y + h_roi > large_img.shape[0]:
        print(f"错误：指定区域 ({x}, {y}, {w_roi}, {h_roi}) 超出大图边界。")
        return False

    roi = large_img[y: y + h_roi, x: x + w_roi]

    # 3. 执行模板匹配：使用 TM_SQDIFF_NORMED
    method = cv2.TM_SQDIFF_NORMED

    # 此时模板和 ROI 尺寸相同 (114x114)，Assertion 检查将通过
    result = cv2.matchTemplate(roi, template_to_match, method, mask=template_mask)

    # 4. 处理 nan 值 (替换为最差值 1.0)
    if np.isnan(result).any():
        result = np.nan_to_num(result, nan=1.0)

    # 5. 找到最佳匹配值 (最小值)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 6. 检查是否小于等于允许的最大差异值
    if min_val <= max_diff:
        print(f"匹配成功：最小相似度为 {min_val:.4f} (需小于最大差异: {max_diff:.4f})")
        return True
    else:
        print(f"匹配失败：最小相似度为 {min_val:.4f} (大于最大差异: {max_diff:.4f})")
        return False


# --- 运行验证 ---

# 您的路径和坐标参数 (假设路径是正确的)
LARGE_IMAGE_PATH = 'Puzzles/Landscaper/Level_036.png'
TREE_PATH = 'images/TileContent/tree.png'
FLOWER_PATH = 'images/TileContent/flower_blue.png'
size = (114, 114)

# **重要调整：** # 1. 切换到 TM_SQDIFF_NORMED，阈值 now means MAX_DIFFERENCE (越低越严格)。
# 2. 我们将 Max Difference 设为 0.3，这比之前的 0.5 严格得多 (相当于 TM_CCOEFF_NORMED 的 0.7)。
MAX_DIFFERENCE = 0.3

list_coords = [(0, 200), (114, 200), (228, 200)]  # 使用更清晰的变量名

print(f"--- 验证开始 (使用 TM_SQDIFF_NORMED, 最大差异: {MAX_DIFFERENCE}) ---")

for i, coord in enumerate(list_coords):
    print(f"\n--- 区域 {i + 1} 坐标: {coord} ---")

    # 验证树
    print("-> 验证树：")
    found_tree = check_template_in_region_optimized(
        large_image_path=LARGE_IMAGE_PATH,
        template_path=TREE_PATH,
        top_left_coord=coord,
        size=size,
        max_diff=MAX_DIFFERENCE
    )

    # 验证花
    print("-> 验证花：")
    found_flower = check_template_in_region_optimized(
        large_image_path=LARGE_IMAGE_PATH,
        template_path=FLOWER_PATH,
        top_left_coord=coord,
        size=size,
        max_diff=MAX_DIFFERENCE
    )

    print(f"区域 {coord} 结果: 树={found_tree}, 花={found_flower}")