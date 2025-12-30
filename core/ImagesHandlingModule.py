from urllib.request import urlopen
import os
import cv2


def try_to_find_img(source, path=None):
    """
    Автоопределение: если source - это URL, скачивает его.
    Если source - это путь, загружает его.
    """
    if not os.path.exists("images"):
        os.mkdir("images")

    # Если source похож на URL
    if source.startswith(("http")):
        if path is None:
            # Генерация пути из URL, если не указан
            file_name = source.split("/")[-1]
            if not file_name:
                file_name = "downloaded_img.png"
            path = os.path.join("images", file_name)

        if not os.path.exists(path):
            try:
                resourceImg = urlopen(source).read()
                with open(path, "wb") as outImg:
                    outImg.write(resourceImg)
            except Exception as e:
                print(f"Ошибка при скачивании {source}: {e}")
                return False
    else:
        # Если это не URL, значит это путь
        path = source

    if os.path.exists(path):
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if img is not None:
            return img

    print(f"Не удалось найти или загрузить картинку по пути: {path}")
    return False
