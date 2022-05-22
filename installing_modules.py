import subprocess


def install_modul(package):
    """Функция по установке модулей"""
    print(f'Модуль {package} не найден')

    subprocess.Popen(f"py -m pip install {package}", shell=True).wait()

    print(f'Модуль {package} был успешно скачан')


def installing_modules():
    try:
        import cv2
    except ImportError:
        install_modul("opencv-python")

    try:
        import cvzone
    except ImportError:
        install_modul("mediapipe")
        install_modul("cvzone")

    try:
        import urllib
    except ImportError:
        install_modul('urllib3')

    try:
        import numpy as np
    except ImportError:
        install_modul('numpy')
    
    try:
        import asyncio
    except ImportError:
        install_modul('asyncio')
        
    print('Модули готовы к работе')


if __name__ == '__main__':
    installing_modules()
