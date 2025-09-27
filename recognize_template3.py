import cv2
import numpy as np
import os


def check_template_in_region_rgb(large_image_path, template_path, top_left_coord, size, max_diff=0.3):
    """
    检查大图的指定区域内是否包含带透明背景的模板图，使用 TM_SQDIFF_NORMED 方法。
    核心改进：在匹配前将 ROI 和模板转换为灰度图，以提高相似度。

    参数:
    ... (与原函数相同)
    """
    """
    最终且最稳定的版本：移除 cv2.matchTemplate 的 mask 参数，通过图像操作处理透明背景。
    并使用灰度图和 float32 确保计算的稳定性。
    """
    if not os.path.exists(large_image_path) or not os.path.exists(template_path):
        print("错误：找不到图像文件。")
        return False

    large_img = cv2.imread(large_image_path, cv2.IMREAD_COLOR)
    template_img_4channel = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)

    if template_img_4channel is None or large_img is None:
        print("错误：无法加载图像文件。")
        return False

    w_roi, h_roi = size

    # --- A. 缩放、提取 BGR 和 Alpha ---
    template_resized = cv2.resize(template_img_4channel, (w_roi, h_roi), interpolation=cv2.INTER_AREA)

    if template_resized.shape[2] == 4:
        template_bgr = template_resized[:, :, :3]
        template_mask_raw = template_resized[:, :, 3]

        # 1. 创建一个纯黑背景 (0, 0, 0) 的 BGR 模板
        # 背景色设置为 ROI 的背景色 (黑色)
        template_final_bgr = np.zeros_like(template_bgr)

        # 2. 使用 Alpha 掩码将模板的不透明部分复制到黑色背景上
        # cv2.split/merge 确保操作在各个通道上正确执行
        alpha_factor = template_mask_raw[:, :, np.newaxis] / 255.0
        template_final_bgr = (template_final_bgr * (1 - alpha_factor) + template_bgr * alpha_factor).astype(np.uint8)
    else:
        # 如果模板没有 Alpha 通道，直接使用 BGR
        template_final_bgr = template_resized

    # --- B. 裁剪 ROI ---
    x, y = top_left_coord
    if x < 0 or y < 0 or x + w_roi > large_img.shape[1] or y + h_roi > large_img.shape[0]:
        print(f"错误：指定区域 ({x}, {y}, {w_roi}, {h_roi}) 超出大图边界。")
        return False

    roi_bgr = large_img[y: y + h_roi, x: x + w_roi]

    # --- C. 核心优化：灰度化和强制浮点数 ---

    # 2. 强制转换为 np.float32
    roi_to_match = roi_bgr.astype(np.float32)
    template_to_match = template_final_bgr.astype(np.float32)

    # 3. 执行模板匹配：不再使用 mask 参数!
    method = cv2.TM_SQDIFF_NORMED
    result = cv2.matchTemplate(roi_to_match, template_to_match, method)

    # 4. 处理 nan 值并获取结果
    if np.isnan(result).any():
        min_val = 1.0
    else:
        min_val = result[0][0]

    # 5. 检查是否小于等于允许的最大差异值
    if min_val <= max_diff:
        print(f"匹配成功：最小相似度为 {min_val:.4f} (需小于最大差异: {max_diff:.4f})")
        return True
    else:
        print(f"匹配失败：最小相似度为 {min_val:.4f} (大于最大差异: {max_diff:.4f})")
        return False


# --- 运行验证 ---

LARGE_IMAGE_PATH = 'Puzzles/CoffeeAndSugar/Level_015.png'
TEMPLATE1_PATH = 'images/TileContent/cup.png'
TEMPLATE2_PATH = 'images/TileContent/cube_white.png'
size = (196, 196)
MAX_DIFFERENCE = 0.86
list_coords = [(0, 984), (588, 984)]

print(f"--- 验证开始 (使用 TM_SQDIFF_NORMED, 最大差异: {MAX_DIFFERENCE}) ---")

for i, coord in enumerate(list_coords):
    print(f"\n--- 区域 {i + 1} 坐标: {coord} ---")

    # 验证TEMPLATE1
    print("-> 验证TEMPLATE1：")
    found_template1 = check_template_in_region_rgb(
        large_image_path=LARGE_IMAGE_PATH,
        template_path=TEMPLATE1_PATH,
        top_left_coord=coord,
        size=size,
        max_diff=MAX_DIFFERENCE
    )

    # 验证TEMPLATE2
    print("-> 验证TEMPLATE2：")
    found_template2 = check_template_in_region_rgb(
        large_image_path=LARGE_IMAGE_PATH,
        template_path=TEMPLATE2_PATH,
        top_left_coord=coord,
        size=size,
        max_diff=MAX_DIFFERENCE
    )

    print(f"区域 {coord} 结果: TEMPLATE1={found_template1}, TEMPLATE2={found_template2}")
