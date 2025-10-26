import os
import string
from itertools import pairwise, groupby
from pathlib import Path
from typing import Self, Callable

import cv2
import easyocr
import numpy as np

from Puzzles.puzzle_snapshot_automator import take_snapshot_puzzle


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
        threshold: int = 15
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


def to_base_36(
        s: str
) -> str:
    """
    将表示 0~35 的数字字符串转换为对应的36进制字符（大写）
    无效输入返回原字符串
    """
    try:
        num = int(s)
        return s if num < 10 else chr(ord('A') + num - 10)
    except ValueError:
        return s  # 非数字字符串也返回原值


def get_template_img_4channel_list(*paths: str) -> list[np.ndarray]:
    return [cv2.imread(path, cv2.IMREAD_UNCHANGED) for path in paths]


def get_level_str_from_matrix(
        matrix: list[list[str]],
        elem_func: Callable[[str], str] = lambda s: s,
) -> str:
    return '\n'.join(''.join(elem_func(s) for s in row) + '`' for row in matrix)


def format_matrix_with_walls(
        matrix: list[list[str]],
        walls: tuple[set[tuple[int, int]], set[tuple[int, int]]]
) -> str:
    rows, cols = len(matrix), len(matrix[0])
    row_walls, col_walls = walls
    lines = []
    for r in range(rows + 1):
        line = []
        for c in range(cols + 1):
            line.append(' ')
            if c == cols: break
            line.append('-' if (r, c) in row_walls else ' ')
        lines.append(''.join(line) + '`')
        if r == rows: break
        digits = matrix[r]
        line = []
        for c in range(cols + 1):
            line.append('|' if (r, c) in col_walls else ' ')
            if c == cols: break
            line.append(digits[c])
        lines.append(''.join(line) + '`')
    result = '\n'.join(lines)
    return result


class PuzzleAnalyzer:

    def __init__(
            self: Self,
            level_count: int,
            level_to_cell_count: list[tuple[int, int]],
            puzzle_name: str | None = None,
    ):
        self.puzzle_name = puzzle_name or os.path.split(os.getcwd())[-1]
        self.level_count = level_count
        self._reader = None
        # large_img_bgr (np.ndarray): 使用 cv2.imread 读取的图像数组。
        self.large_img_bgr = None
        self.large_img_rgb = None
        self.level_str = ''
        self.attr_str = ''
        self.current_level = 0
        self.cell_count = 0
        self.cell_length = 0

        self.levels_to_cell_count: list[tuple[int, int, int]] = []
        for (l1, c1), (l2, c2) in pairwise(level_to_cell_count):
            self.levels_to_cell_count.append((l1, l2 - 1, c1))
        self.levels_to_cell_count.append((l2, self.level_count, c2))
        pass

    @property
    def reader(self):
        self._reader = self._reader or easyocr.Reader(['en'])
        return self._reader

    def take_snapshot(
            self: Self,
            app_series_no: int = 1,
            start_level: int = 1,
            end_level: int | None = None,
            need_page_screenshot: bool = True,
            need_level_screenshot: bool = True
    ) -> None:
        end_level = end_level or self.level_count
        take_snapshot_puzzle(app_series_no, self.puzzle_name, start_level, end_level, need_page_screenshot, need_level_screenshot)


    def get_cell_count(self: Self, level: int) -> int:
        return next(count for start, end, count in self.levels_to_cell_count if start <= level <= end)


    def analyze_horizontal_line(
            self: Self,
            y_coord: int,
            start_x: int,
            end_x: int,
            tweak=None
    ) -> list[PixelStreak]:
        """
        分析图像中指定的一行像素，并将连续的像素块信息存储到 PixelStreak 对象列表中。

        参数:
        y_coord (int): 要分析的像素行的Y坐标。
        start_x (int): 分析的起始X坐标。
        end_x (int): 分析的结束X坐标。

        返回:
        list: 一个包含 PixelStreak 对象实例的列表。
              如果发生错误，返回 None。
        """
        try:
            height, width, _ = self.large_img_bgr.shape
            if not (0 <= y_coord < height and 0 <= start_x <= end_x < width):
                print(f"错误：请求的坐标范围超出了图像尺寸 ({width}x{height})。")
                return None

            results = []

            current_streak_color = None
            current_streak_count = 0
            current_streak_start_x = start_x

            for x in range(start_x, end_x + 1):
                b, g, r = self.large_img_bgr[y_coord, x]
                current_pixel_color = int(b), int(g), int(r)

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

        except Exception as e:
            print(f"发生了未知错误: {e}")
            return None


    def analyze_vertical_line(
            self: Self,
            x_coord: int,
            start_y: int,
            end_y: int,
            tweak=None
    ) -> list[PixelStreak]:
        """
        分析图像中指定的一列像素，并将连续的像素块信息存储到 PixelStreak 对象列表中。

        参数:
        x_coord (int): 要分析的像素列的X坐标。
        start_y (int): 分析的起始Y坐标。
        end_y (int): 分析的结束Y坐标。

        返回:
        list: 一个包含 PixelStreak 对象实例的列表。
              如果发生错误，返回 None。
        """
        try:
            height, width, _ = self.large_img_bgr.shape
            if not (0 <= x_coord < width and 0 <= start_y <= end_y < height):
                print(f"错误：请求的坐标范围超出了图像尺寸 ({width}x{height})。")
                return None

            results = []

            current_streak_color = None
            current_streak_count = 0
            current_streak_start_y = start_y

            for y in range(start_y, end_y + 1):
                b, g, r = self.large_img_bgr[y, x_coord]
                current_pixel_color = int(b), int(g), int(r)

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

        except Exception as e:
            print(f"发生了未知错误: {e}")
            return None


    def get_grid_lines_by_cell_count(
            self: Self,
            cell_count: int,
            start_x: int = 0,
            start_y: int = 200,
    ) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        self.cell_length = 1180 // cell_count
        def get_grid_lines_by_cell_count2(start_position: int) -> list[tuple[int, int]]:
            result = []
            position = start_position
            for i in range(cell_count):
                result.append((position, self.cell_length))
                position += self.cell_length
            return result
        return get_grid_lines_by_cell_count2(start_x), get_grid_lines_by_cell_count2(start_y)


    def recognize_grid_lines(self: Self) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
        yoffset = 198
        roi = self.large_img_bgr[yoffset:1385, 0:1182]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150)
        linesP = cv2.HoughLinesP(
            edges,
            1,
            np.pi / 180,
            500,
            minLineLength=500,
            maxLineGap=300
        )
        y_list = []
        x_list = []
        if linesP is not None:
            for line in linesP:
                x1, y1, x2, y2 = line[0]
                y1 += yoffset
                y2 += yoffset
                if abs(y2 - y1) < 10:  # horizontal
                    y_list.append(int((y1 + y2) / 2))
                elif abs(x2 - x1) < 10:  # vertical
                    x_list.append(int((x1 + x2) / 2))

        y_list = sorted(set(y_list))
        x_list = sorted(set(x_list))
        y_list2 = []
        x_list2 = []
        for idx, y in enumerate(y_list):
            if idx == 0 or y - y_list[idx - 1] > 10:
                y_list2.append(y)
        for idx, x in enumerate(x_list):
            if idx == 0 or x - x_list[idx - 1] > 10:
                x_list2.append(x)
        if (1181 - x_list2[-1]) > 100:
            x_list2.append(1181)

        processed_vertical_lines = []
        for idx, y in enumerate(y_list2):
            if idx < len(y_list2) - 1:
                processed_vertical_lines.append((y, y_list2[idx + 1] - y))
        processed_horizontal_lines = []
        for idx, x in enumerate(x_list2):
            if idx < len(x_list2) - 1:
                processed_horizontal_lines.append((x, x_list2[idx + 1] - x))
        return processed_horizontal_lines, processed_vertical_lines


    def recognize_text(
            self: Self,
            x: int,
            y: int,
            w: int,
            h: int,
            allowlist=None,
            get_roi_large: Callable[[np.ndarray], np.ndarray] = None,
    ):
        roi = self.large_img_rgb[y:y + h, x:x + w]
        roi_large = get_roi_large(roi) if get_roi_large else roi
        output = self.reader.readtext(roi_large, allowlist=allowlist)
        return output[0] if output else None


    def get_scale_for_digit_recognition(self: Self, w: int) -> float:
        return .5 if w > 220 else 1 if w > 180 else 2 if w > 130 else 3


    def recognize_digit(self: Self, x: int, y: int, w: int, h: int) -> str | None:
        roi = self.large_img_rgb[y:y + h, x:x + w]
        scale = self.get_scale_for_digit_recognition(w)
        roi_large = cv2.resize(roi, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        output = self.reader.readtext(roi_large, allowlist=string.digits)
        if not output:
            return None
        else:
            _, text, prob = output[0]
            if text == "22":
                if prob < 0.99:
                    text = "2"
            # elif text == "7":
            #     if prob < 0.35:
            #         text = "1"
            return text


    def recognize_digits(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                horizontal_line_results = self.analyze_horizontal_line(y_coord=y + h // 2, start_x=x + 10, end_x=x+w - 10)
                if len(horizontal_line_results) == 1:
                    ch = ' '
                else:
                    ch = self.recognize_digit(x, y, w, h) or ' '
                row_result.append(ch)
            result.append(row_result)
        return result


    def recognize_blocks(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]],
            is_block: Callable[[tuple[int, int, int]], bool]
    ) -> set[tuple[int, int]]:
        result = set()
        for row_idx, (y, h) in enumerate(vertical_line_list):
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                color = self.large_img_bgr[y + 20, x + 20]
                if is_block(color):
                    result.add((row_idx, col_idx))
        return result


    def recognize_walls(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
        row_walls = set()
        col_walls = set()
        for col_idx, (x, w) in enumerate(horizontal_line_list):
            vertical_line_results = self.analyze_vertical_line(x_coord=x+15, start_y=200, end_y=1380)
            processed_column_grid = process_pixel_short_results(vertical_line_results, is_horizontal=False)
            for row_idx, (y, h) in enumerate(processed_column_grid):
                if row_idx == 0 or row_idx == len(processed_column_grid) - 1 or h > 4:
                    row_walls.add((row_idx, col_idx))

        for row_idx, (y, h) in enumerate(vertical_line_list):
            horizontal_line_results = self.analyze_horizontal_line(y_coord=y+15, start_x=0, end_x=1180)
            processed_line_grid = process_pixel_short_results(horizontal_line_results, is_horizontal=True)
            for col_idx, (x, w) in enumerate(processed_line_grid):
                if col_idx == 0 or col_idx == len(processed_line_grid) - 1 or w > 4:
                    col_walls.add((row_idx, col_idx))

        return row_walls, col_walls


    def get_template_diff_in_region(
            self: Self,
            template_img_4channel: np.ndarray,
            top_left_coord: tuple[int, int],
            size: tuple[int, int],
    ) -> float:
        """
        检查大图的指定区域内是否包含带透明背景的模板图，使用 TM_SQDIFF_NORMED 方法，
        并在匹配前将模板缩放到 ROI 的大小。
        最终且最稳定的版本：移除 cv2.matchTemplate 的 mask 参数，通过图像操作处理透明背景。
        并使用灰度图和 float32 确保计算的稳定性。

        参数:
        ...
        size (tuple): 待检查区域的宽度和高度 (width, height)。
        max_diff (float): 允许的最大差异值 (0.0 到 1.0)。
        """

        if template_img_4channel is None or self.large_img_bgr is None:
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
        if x < 0 or y < 0 or x + w_roi > self.large_img_bgr.shape[1] or y + h_roi > self.large_img_bgr.shape[0]:
            print(f"错误：指定区域 ({x}, {y}, {w_roi}, {h_roi}) 超出大图边界。")
            return False

        roi_bgr = self.large_img_bgr[y: y + h_roi, x: x + w_roi]

        # --- C. 核心优化：灰度化和强制浮点数 ---
        # 1. 转换为灰度图
        roi_gray = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template_final_bgr, cv2.COLOR_BGR2GRAY)  # 使用处理后的模板

        # 2. 强制转换为 np.float32
        # roi_to_match = roi_gray.astype(np.float32)
        # template_to_match = template_gray.astype(np.float32)
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

        # print(f"最小相似度为 {min_val:.4f}")
        return min_val


    def get_template_index_by_diff_in_region(
            self: Self,
            template_img_4channel_list: list[np.ndarray],
            top_left_coord: tuple[int, int],
            size: tuple[int, int],
            tweak=None
    ) -> int:
        diff_list = [self.get_template_diff_in_region(
            template_img_4channel=template_img_4channel,
            top_left_coord=top_left_coord,
            size=size
        ) for template_img_4channel in template_img_4channel_list]
        if tweak:
            diff_list = tweak(diff_list)
        index = next((i for i, diff in enumerate(diff_list) if diff == min(diff_list)))
        return -1 if diff_list[index] >= 1.0 else index


    def get_level_str_from_image(self: Self) -> str:
        return ''

    def get_attr_str_from_image(self: Self) -> str:
        return ''


    def get_levels_str_from_puzzle(
            self: Self,
            start_level: int = 1,
            end_level: int | None = None,
    ) -> None:
        '''

        Args:
            start_level: 起始关卡: 从1开始
            end_level: 结束关卡号
        Returns:

        '''
        end_level = end_level or self.level_count
        with open(f"Levels.txt", "w"):
            pass
        level_image_path = os.path.expanduser(f"~/Documents/Programs/Games/100LG/Levels/{self.puzzle_name}/")
        for i in range(start_level, end_level+1):
            self.current_level = i
            self.cell_count = self.get_cell_count(self.current_level)
            # 图像信息
            image_path = f'{level_image_path}Level_{i:03d}.png'
            print("正在处理图片 " + image_path)
            self.large_img_bgr = cv2.imread(image_path, cv2.IMREAD_COLOR)
            if self.large_img_bgr is None:
                print(f"错误：无法加载图像文件。{image_path}")
                continue
            if self.reader:
                self.large_img_rgb = cv2.cvtColor(self.large_img_bgr, cv2.COLOR_BGR2RGB)
            self.level_str = self.get_level_str_from_image()
            self.attr_str = self.get_attr_str_from_image()
            node = f"""  <level id="{i}"{self.attr_str}>
    <![CDATA[
{self.level_str}
    ]]>
  </level>
"""
            with open(f"Levels.txt", "a") as text_file:
                text_file.write(node)


    def get_level_board_size_from_puzzle(self: Self) -> None:
        def recognize_digit2(scale: int, x: int, y: int, w: int, h: int) -> int | None:
            roi = self.large_img_rgb[y:y + h, x:x + w]
            roi_large = cv2.resize(roi, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            # cv2.imshow("cell", roi_large)
            # cv2.waitKey(0)
            output = self.reader.readtext(roi_large, allowlist=string.digits)
            return int(output[0][1]) if output else None

        level_image_path = os.path.expanduser(f"~/Documents/Programs/Games/100LG/Levels/{self.puzzle_name}/")
        path = Path(level_image_path)
        matching_files = list(sorted(path.rglob("Page_*.png")))
        x1, y1, x2, y2 = 40, 402, 165, 512
        level_result = []
        break_out = False
        for f in matching_files:
            print("正在处理图片 " + os.path.abspath(f))
            self.large_img_bgr = cv2.imread(f, cv2.IMREAD_COLOR)
            self.large_img_rgb = cv2.cvtColor(self.large_img_bgr, cv2.COLOR_BGR2RGB)
            for r in range(6):
                offset_y = r * 186
                for c in range(6):
                    offset_x = c * 186
                    level_no = recognize_digit2(1, x1 + offset_x, y1 + offset_y, 135, 130)
                    board_size = recognize_digit2(4, x2 + offset_x, y2 + offset_y, 40, 55)
                    if board_size:
                        level_result.append((level_no or 7, board_size))
                    else:
                        break_out = True
                        break
                if break_out: break
            if break_out: break
        result = [next(g) for _, g in groupby(level_result, key=lambda x: x[1])]
        print(f"result: {result}")
