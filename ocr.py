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

if __name__ == '__main__':
    ocr = OCR()
    img = PIL.Image.open("img/img_1.png")
    img = img.crop((250, 800, 400, 850))
    img.show()
    result = ocr.model.ocr(np.array(img))
    print(result)


