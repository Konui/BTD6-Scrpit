import torch
from paddleocr import PaddleOCR

from common import timer


class OCR():
    def __init__(self):
        self.model = PaddleOCR(lang="ch", use_angle_cls=False)

    @timer
    def recognition(self, img):
        result = []
        output  = self.model.ocr(img)
        if output[0]:
            for res in output[0]:
                if res[1][1] > 0.8:
                    result.append(res[1][0])
        return result

if __name__ == '__main__':
    ocr = OCR()
    recognition = ocr.recognition("img/game.png")
    print(recognition)
