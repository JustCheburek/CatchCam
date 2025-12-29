from urllib.request import urlopen
import numpy as np
import os
import cv2


def try_to_find_img(url, path):
    if not os.path.exists('images'):
        os.mkdir('images')

    if not os.path.exists(path):
        resourceImg = urlopen(url).read()
        with open(path, 'wb') as outImg:
            outImg.write(resourceImg)
            outImg.close()

    if os.path.exists(path):
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        return img

    print(f'У вас нет картинки ({path}), и кажется не удалось её распознать с интернета ({url}), поместите её в папку images')

    return False
