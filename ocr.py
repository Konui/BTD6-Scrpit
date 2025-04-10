import PIL.Image
import numpy as np
import torch
from paddleocr import PaddleOCR

from common import timer


class OCR():
    def __init__(self):
        self.model = PaddleOCR(lang="ch", use_angle_cls=False)

    @timer
    def recognition(self, img):
        result = []
        output  = self.model.ocr(img, cls=False)
        if output[0]:
            for res in output[0]:
                if res[1][1] > 0.8:
                    result.append(res[1][0])
        return result


def is_fully_contained(ocr_bbox, target_rect):
    """
    判断OCR检测框是否完全包含在目标矩形内
    :param ocr_bbox: OCR返回的四边形坐标
    :param target_rect: 目标矩形 (x_min, y_min, x_max, y_max)
    :return: bool
    """
    ocr_x = [p[0] for p in ocr_bbox]
    ocr_y = [p[1] for p in ocr_bbox]
    t_x1, t_y1, t_x2, t_y2 = target_rect

    return (
        min(ocr_x) >= t_x1 and
        max(ocr_x) <= t_x2 and
        min(ocr_y) >= t_y1 and
        max(ocr_y) <= t_y2
    )

if __name__ == '__main__':
    ocr = OCR()
    img = PIL.Image.open("img/img_1.png")
    img = img.crop((250, 800, 400, 850))
    img.show()
    result = ocr.model.ocr(np.array(img))
    print(result)

    # t = (340, 20, 550, 70)
    # o = [[344.0, 20.0], [450.0, 20.0], [450.0, 64.0], [344.0, 64.0]]
    #
    # print(is_fully_contained(o, t))

