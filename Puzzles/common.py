import math
import os

import cv2
import easyocr
from PIL import Image
import numpy as np


class PixelStreak:
    """
    用于存储连续像素块信息的类。
    """

    def __init__(self, position, color, count):
        self.position = position
        self.color = color
        self.count = count

    def __repr__(self):
        """
        用于在打印时提供友好的表示。
        """
        return f"PixelStreak(position={self.position}, color={self.color}, count={self.count})"


def analyze_horizontal_line(
        image_path: str,
        y_coord: int,
        start_x: int,
        end_x: int,
        tweak=None
) -> list[PixelStreak]:
    """
    分析图像中指定的一行像素，并将连续的像素块信息存储到 PixelStreak 对象列表中。

    参数:
    image_path (str): 图像文件的路径。
    y_coord (int): 要分析的像素行的Y坐标。
    start_x (int): 分析的起始X坐标。
    end_x (int): 分析的结束X坐标。

    返回:
    list: 一个包含 PixelStreak 对象实例的列表。
          如果发生错误，返回 None。
    """
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            if not (0 <= y_coord < height and 0 <= start_x <= end_x < width):
                print(f"错误：请求的坐标范围超出了图像尺寸 ({width}x{height})。")
                return None

            pixels = img.load()
            results = []

            current_streak_color = None
            current_streak_count = 0
            current_streak_start_x = start_x

            for x in range(start_x, end_x + 1):
                current_pixel_color = pixels[x, y_coord]
                if tweak:
                    current_pixel_color = tweak(current_pixel_color)

                if current_streak_color is None:
                    current_streak_color = current_pixel_color
                    current_streak_count = 1
                    current_streak_start_x = x
                elif current_pixel_color == current_streak_color:
                    current_streak_count += 1
                else:
                    results.append(PixelStreak(
                        position=(current_streak_start_x, y_coord),
                        color=current_streak_color,
                        count=current_streak_count
                    ))
                    current_streak_color = current_pixel_color
                    current_streak_count = 1
                    current_streak_start_x = x

            if current_streak_count > 0:
                results.append(PixelStreak(
                    position=(current_streak_start_x, y_coord),
                    color=current_streak_color,
                    count=current_streak_count
                ))

            return results

    except FileNotFoundError:
        print(f"错误：找不到文件 '{image_path}'。请确保路径正确。")
        return None
    except Exception as e:
        print(f"发生了未知错误: {e}")
        return None


def analyze_vertical_line(
        image_path: str,
        x_coord: int,
        start_y: int,
        end_y: int,
        tweak=None
) -> list[PixelStreak]:
    """
    分析图像中指定的一列像素，并将连续的像素块信息存储到 PixelStreak 对象列表中。

    参数:
    image_path (str): 图像文件的路径。
    x_coord (int): 要分析的像素列的X坐标。
    start_y (int): 分析的起始Y坐标。
    end_y (int): 分析的结束Y坐标。

    返回:
    list: 一个包含 PixelStreak 对象实例的列表。
          如果发生错误，返回 None。
    """
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            if not (0 <= x_coord < width and 0 <= start_y <= end_y < height):
                print(f"错误：请求的坐标范围超出了图像尺寸 ({width}x{height})。")
                return None

            pixels = img.load()
            results = []

            current_streak_color = None
            current_streak_count = 0
            current_streak_start_y = start_y

            for y in range(start_y, end_y + 1):
                current_pixel_color = pixels[x_coord, y]
                if tweak:
                    current_pixel_color = tweak(current_pixel_color)

                if current_streak_color is None:
                    current_streak_color = current_pixel_color
                    current_streak_count = 1
                    current_streak_start_y = y
                elif current_pixel_color == current_streak_color:
                    current_streak_count += 1
                else:
                    results.append(PixelStreak(
                        position=(x_coord, current_streak_start_y),
                        color=current_streak_color,
                        count=current_streak_count
                    ))
                    current_streak_color = current_pixel_color
                    current_streak_count = 1
                    current_streak_start_y = y

            if current_streak_count > 0:
                results.append(PixelStreak(
                    position=(x_coord, current_streak_start_y),
                    color=current_streak_color,
                    count=current_streak_count
                ))

            return results

    except FileNotFoundError:
        print(f"错误：找不到文件 '{image_path}'。请确保路径正确。")
        return None
    except Exception as e:
        print(f"发生了未知错误: {e}")
        return None


def report_analysis_results(results: list[PixelStreak]) -> None:
    """
    打印分析结果列表。

    参数:
    results (list): 从分析函数返回的 PixelStreak 对象列表。
    """
    if results is None:
        print("无法生成报告，因为分析过程中发生了错误。")
        return

    print("--- 像素线/列分析报告 ---")
    if not results:
        print("在指定的范围内没有找到像素数据。")
        return

    for item in results:
        position = f"({item.position[0]}, {item.position[1]})"
        color_str = str(item.color)
        print(f"位置: {position:<15} 颜色: {color_str:<20} 重复次数: {item.count}")

    print("--- 报告结束 ---")


def process_pixel_long_results(
        results: list[PixelStreak],
        is_horizontal: bool,
        threshold: int = 50
) -> list[tuple[int, int]]:
    """
    筛选像素块结果，只保留重复次数超过阈值的，并返回它们的起始X坐标和长度。

    参数:
    results (list): analyze_horizontal_line 函数返回的 PixelStreak 对象列表。
    is_horizontal: True 表示处理行，False 表示处理行
    threshold (int): 重复次数的最低门槛。

    返回:
    list: 一个包含元组的列表，每个元组的格式为
    is_horizontal 为True时 (起始X坐标, 长度)
    is_horizontal False时 (起始Y坐标, 长度)。
    """
    if results is None:
        return []

    processed_list = []
    for streak in results:
        # 筛选：检查重复次数是否超过门槛
        if streak.count >= threshold:
            position = streak.position[0 if is_horizontal else 1]
            # 添加到结果列表，格式为 (起始X坐标, 长度)
            processed_list.append((position, streak.count))

    return processed_list


def process_pixel_short_results(
        results: list[PixelStreak],
        is_horizontal: bool,
        threshold: int = 10
) -> list[tuple[int, int]]:
    """
    筛选像素块结果，只保留连续一段重复次数低于阈值的，并返回它们的起始X坐标和长度。

    参数:
    results (list): analyze_horizontal_line 函数返回的 PixelStreak 对象列表。
    is_horizontal: True 表示处理行，False 表示处理行
    threshold (int): 重复次数的最低门槛。

    返回:
    list: 一个包含元组的列表，每个元组的格式为
    is_horizontal 为True时 (起始X坐标, 长度)
    is_horizontal False时 (起始Y坐标, 长度)。
    """
    if results is None:
        return []

    processed_list = []
    count = 0
    position = None
    for streak in results:
        # 筛选：检查重复次数是否超过门槛
        if streak.count <= threshold:
            # 添加到结果列表，格式为 (起始X坐标, 长度)
            count += streak.count
            if not position:
                position = streak.position[0 if is_horizontal else 1]
        else:
            processed_list.append((position, count))
            count = 0
            position = None

    processed_list.append((position, count))
    return processed_list


def normalize_lines(
        line_list: list[tuple[int, int]],
        start_position: int,
        grid_length: int = 1180
) -> list[tuple[int, int]]:
    cell_length = max(line_list, key=lambda x: x[1])[1] + 4
    cell_count = math.floor(grid_length / cell_length + .5)
    cell_length = int(grid_length / cell_count)
    position = start_position
    result = []
    for i in range(cell_count):
        result.append((position, cell_length))
        position += cell_length
    return result


def recognize_digits(
        image_path: str,
        line_list: list[tuple[int, int]],
        column_list: list[tuple[int, int]]
) -> list[list[str]]:
    """
    读取图片中多个区域的数字，不进行图像预处理。

    参数:
        image_path: 图片路径
        line_list: [(x1, w1), (x2, w2), ...] 水平列（x坐标和宽度）
        column_list: [(y1, h1), (y2, h2), ...] 垂直行（y坐标和高度）

    返回:
        二维列表，每个元素是识别出的字符或空格
    """
    # 读取图像
    img = cv2.imread(image_path)

    # 存储识别结果
    result = []

    reader = easyocr.Reader(['en'])  # 初始化，只加载英文模型
    for row_idx, (y, h) in enumerate(column_list):
        row_result = []
        for col_idx, (x, w) in enumerate(line_list):
            # 裁剪感兴趣区域(ROI)
            roi = img[y:y + h, x:x + w]
            roi_large = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

            output = reader.readtext(roi_large)
            text = ' ' if not output else output[0][1]

            # # 图像预处理（可选但推荐）
            # gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            # gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)
            # _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            #
            # # 使用 Tesseract 识别文字，这里我们假设只识别数字
            # custom_config = r'--oem 3 --psm 6 outputbase digits'
            # text = pytesseract.image_to_string(thresh, config=custom_config).strip()
            # # text = pytesseract.image_to_string(roi, config=custom_config).strip()

            # 将识别的结果添加到当前行的结果列表中
            row_result.append(text)

        # 将当前行的结果添加到最终结果列表中
        result.append(row_result)

    return result


def recognize_blocks(
        image_path:str,
        line_list: list[tuple[int, int]],
        column_list: list[tuple[int, int]],
        is_white
) -> set[tuple[int, int]]:
    result = set()
    try:
        with Image.open(image_path) as img:
            pixels = img.load()
            for row_idx, (y, h) in enumerate(column_list):
                for col_idx, (x, w) in enumerate(line_list):
                    color = pixels[x + 20, y + 20]
                    if is_white(color):
                        result.add((row_idx, col_idx))
        return result

    except FileNotFoundError:
        print(f"错误：找不到文件 '{image_path}'。请确保路径正确。")
        return None
    except Exception as e:
        print(f"发生了未知错误: {e}")
        return None


def recognize_walls(
        image_path:str,
        line_list: list[tuple[int, int]],
        column_list: list[tuple[int, int]]
) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
    row_walls = set()
    col_walls = set()
    try:
        for col_idx, (x, w) in enumerate(line_list):
            vertical_line_results = analyze_vertical_line(image_path, x_coord=x+10, start_y=200, end_y=1380)
            processed_column_grid = process_pixel_short_results(vertical_line_results, is_horizontal=False)
            for row_idx, (y, h) in enumerate(processed_column_grid):
                if row_idx == 0 or row_idx == len(processed_column_grid) - 1 or h > 4:
                    row_walls.add((row_idx, col_idx))

        for row_idx, (y, h) in enumerate(column_list):
            horizontal_line_results = analyze_horizontal_line(image_path, y_coord=y+10, start_x=0, end_x=1180)
            processed_line_grid = process_pixel_short_results(horizontal_line_results, is_horizontal=True)
            for col_idx, (x, w) in enumerate(processed_line_grid):
                if col_idx == 0 or col_idx == len(processed_line_grid) - 1 or w > 4:
                    col_walls.add((row_idx, col_idx))

        return row_walls, col_walls

    except FileNotFoundError:
        print(f"错误：找不到文件 '{image_path}'。请确保路径正确。")
        return None
    except Exception as e:
        print(f"发生了未知错误: {e}")
        return None


def check_template_in_region_optimized(
        large_image_path: str,
        template_path: str,
        top_left_coord: tuple[int, int],
        size: tuple[int, int],
        max_diff=0.3
) -> bool:
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
        # print(f"匹配成功：最小相似度为 {min_val:.4f} (需小于最大差异: {max_diff:.4f})")
        return True
    else:
        # print(f"匹配失败：最小相似度为 {min_val:.4f} (大于最大差异: {max_diff:.4f})")
        return False


def check_template_list_in_region(
        large_image_path: str,
        template_path_list: list[str],
        top_left_coord: tuple[int, int],
        size: tuple[int, int],
        max_diff=0.3
) -> int:
    return next((template_path for template_path in template_path_list if check_template_in_region_optimized(
        large_image_path, template_path, top_left_coord, size, max_diff)), -1)

def to_hex_char(s: str) -> str:
    """
    将表示 0~15 的数字字符串转换为对应的十六进制字符（大写）
    空格保持不变
    其他无效输入返回原字符串或报错（可按需调整）
    """
    if s == ' ':
        return s  # 空格不转换

    try:
        num = int(s)
        if 0 <= num <= 15:
            return format(num, 'X')  # 转为大写十六进制字符，如 'A', 'F'
        else:
            return s  # 超出范围则返回原字符串
    except ValueError:
        return s  # 非数字字符串也返回原值


def level_node_string(level: int, level_str: str) -> str:
    return f"""  <level id="{level}">
    <![CDATA[
{level_str}
    ]]>
  </level>
"""

