import cv2
import numpy as np
import os


# ⚙️ 配置参数
LARGE_IMAGE_PATH = os.path.expanduser('~/Documents/Programs/Games/100LG/Landscaper/Level_002.png')  # 替换为你的大图路径
TEMPLATE_PATH = 'images/TileContent/tree.png'  # 替换为你的树模板路径（推荐透明 PNG）
