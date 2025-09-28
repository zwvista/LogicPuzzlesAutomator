import cv2
import numpy as np
import os


# 定义理想的目标尺寸
TARGET_MATCH_SIZE = (250, 250)
TARGET_W, TARGET_H = TARGET_MATCH_SIZE

def get_template_diff_in_region(large_image_path, template_path, top_left_coord, size, max_diff=0.3):
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

    w_t, h_t = template_img_4channel.shape[1], template_img_4channel.shape[0]

    # --- A. 准备模板 (无需缩放) ---
    if template_img_4channel.shape[2] == 4:
        # ... (保持原有的 BGR/Alpha 分离和背景填充逻辑) ...
        template_final_bgr = template_img_4channel[:, :, :3]
        template_mask_raw = template_img_4channel[:, :, 3]
        # ... (生成 template_final_bgr) ...
    else:
        template_final_bgr = template_img_4channel

    # --- B. 裁剪 ROI (使用用户提供的 size) ---
    x, y = top_left_coord
    w_roi, h_roi = size
    roi_bgr = large_img[y: y + h_roi, x: x + w_roi]

    # --- C. 核心修正：强制放大/缩小到目标匹配尺寸 ---

    # 1. 缩放 Template 到目标尺寸
    template_resized = cv2.resize(
        template_final_bgr,
        TARGET_MATCH_SIZE,
        interpolation=cv2.INTER_CUBIC  # 强制放大，使用 CUBIC 减少块状感
    )

    # 2. 缩放 ROI 到目标尺寸
    roi_resized = cv2.resize(
        roi_bgr,
        TARGET_MATCH_SIZE,
        interpolation=cv2.INTER_CUBIC if TARGET_W > w_roi else cv2.INTER_AREA
    )

    # 3. BGR + float32 转换
    roi_to_match = roi_resized.astype(np.float32)
    template_to_match = template_resized.astype(np.float32)

    # 3. 执行模板匹配：不再使用 mask 参数!
    method = cv2.TM_SQDIFF_NORMED
    # method = cv2.TM_CCOEFF_NORMED
    result = cv2.matchTemplate(roi_to_match, template_to_match, method)

    # 4. 处理 nan 值并获取结果
    if np.isnan(result).any():
        min_val = 1.0
    else:
        min_val = result[0][0]

    return min_val

    # # 5. 检查是否小于等于允许的最大差异值
    # if min_val <= max_diff:
    #     print(f"匹配成功：最小相似度为 {min_val:.4f} (需小于最大差异: {max_diff:.4f})")
    #     return True
    # else:
    #     print(f"匹配失败：最小相似度为 {min_val:.4f} (大于最大差异: {max_diff:.4f})")
    #     return False


# --- 运行验证 ---

LARGE_IMAGE_PATH = 'Puzzles/CoffeeAndSugar/Level_195.png'
TEMPLATE1_PATH = 'images/TileContent/cup.png'
TEMPLATE2_PATH = 'images/TileContent/cube_white.png'
rc = 11
sidelen = 1180 // rc
size = (sidelen, sidelen)
MAX_DIFFERENCE = 0.86

# --- 外部判断代码 (最终版，包含补偿逻辑) ---
PENALTY_CUP = 0.03  # 惩罚因子，强制 CUP 模板在 CUBE 区域的匹配结果变差

for r in range(0, rc):
    for c in range(0, rc):
        coord = (c * sidelen, 200 + r * sidelen)
        min_val_cup = get_template_diff_in_region(LARGE_IMAGE_PATH, TEMPLATE1_PATH, coord, size)
        min_val_cube = get_template_diff_in_region(LARGE_IMAGE_PATH, TEMPLATE2_PATH, coord, size)

        # 施加惩罚：如果 CUP 模板匹配结果更好，人为地让它变差
        adjusted_cup_val = min_val_cup + PENALTY_CUP

        # 保持 CUBE 模板差异值不变
        adjusted_cube_val = min_val_cube

        results = {
            'CUP': adjusted_cup_val,
            'CUBE': adjusted_cube_val
        }

        # 1. 找到最小值 (越低越好)
        best_match_name = min(results, key=results.get)
        min_diff = results[best_match_name]

        # 2. MAX_ALLOWABLE_DIFFERENCE = 0.99，但 0.90 已经足够宽松
        MAX_ALLOWABLE_DIFFERENCE = 0.99

        # 3. 打印原始差异值，但用调整后的值做判断
        if min_diff < MAX_ALLOWABLE_DIFFERENCE:
            # 如果是 CUP 胜出，输出其原始差异值。如果是 CUBE 胜出，输出其原始差异值。
            original_val = min_val_cup if best_match_name == 'CUP' else min_val_cube
            print(f"区域 {(r, c)} 内容是: {best_match_name} (差异: {original_val:.4f})({adjusted_cup_val:.4f},{adjusted_cube_val:.4f})")
        # else:
        #     print(f"区域 {coord} 内容是: 未知/空白 (最小差异: {min_diff:.4f})")
