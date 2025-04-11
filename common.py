import math, time, cv2
import os
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=os.cpu_count())

# 耗时装饰器
def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        # print(f"[timer]{func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper

# 计算颜色相似度，默认小于150的算相似颜色
def is_color_similar(rgb_actual, rgb_target, threshold=80):
    distance = math.sqrt(sum((c1 - c2)**2 for c1, c2 in zip(rgb_actual, rgb_target)))
    print(distance)
    return distance <= threshold

# 模版匹配，模版和实际匹配特征的图片大小要完全一致, 阈值越小越相似
@timer
def match(target, template, threshold=0.01):
    result = cv2.matchTemplate(target, template, cv2.TM_SQDIFF_NORMED)
    return cv2.minMaxLoc(result)[0] < threshold

if __name__ == '__main__':
    print(is_color_similar((0, 221, 255), (120, 230, 0)))