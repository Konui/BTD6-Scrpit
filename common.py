import math
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        # print(f"[timer]{func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def is_color_similar(rgb_actual, rgb_target, threshold=150):
    distance = math.sqrt(sum((c1 - c2)**2 for c1, c2 in zip(rgb_actual, rgb_target)))
    print(distance)
    return distance <= threshold

if __name__ == '__main__':
    print(is_color_similar((0, 221, 255), (120, 230, 0)))