print('Создатель: https://t.me/JustCheburek в телеге, JustCheburek#9928 в дискорде')
import datetime  # для сохранения видео
import os
import installing_modules
from settings import settings

installing_modules.installing_modules()

from cvzone.SelfiSegmentationModule import SelfiSegmentation
import cv2
import cvzone
import FaceMeshModule as FM_module
import FPS_module
import HandDetectorModule as HD_module
import CubesHandlingModule as CH_module
import ImagesHandlingModule as IH_module


def video_recording_func(camera):
    """Снятие видео"""
    global time_recording, recording, window_width, window_height
    time_recording += 0.05
    if time_recording > 100:
        time_recording = 0
        recording = not recording
    else:
        video_recording.write(cv2.resize(camera, (window_width, window_height)))


# Видео онлайн
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# размеры приложения
window_width, window_height = 1280, 720
cap.set(3, window_width)
cap.set(4, window_height)

# ДЕТЕКТОРЫ
# Рук
detector_hands = None
if settings['HANDS']:
    detector_hands = HD_module.HandDetector()
# Лица
detector_faces = None
if settings['FACE']['turn_on']:
    detector_faces = FM_module.FaceMeshDetector()
# ФПС
detector_FPS = FPS_module.FPS()
# Убирание фона
remove_BG = None
if settings['BG']['turn_on']:
    remove_BG = SelfiSegmentation()

# ШРИФТ
font = cv2.FONT_HERSHEY_SIMPLEX

# ВИДЕО
video_recording = ''
recording = False  # проверка на текущее видео
time_recording = 0

# ЦВЕТА в BGR (blue green red)
colors = {
    'red': (0, 0, 255),
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'green': (0, 255, 0),
    'blue': (255, 0, 0)
}

# МЕНЮ
menu = {
    'now': 'start menu',
    'menus': (
        'start menu',
        'settings menu',
        'touch cubes',
        'collect all cubes',
        '2048'),
}

# игры
GameTouchCubes = CH_module.GameTouchCubes()
GameCollectAllCubes = CH_module.GameCollectAllCubes()
Game2048 = CH_module.Game2048()

# КАРТИНКИ
# камера
cameraImg = IH_module.try_to_find_img('https://i.ibb.co/1bK4H73/camera.png', 'images/camera.png')
# фон
img_BG = None
if settings['BG']['turn_on']:
    img_BG = IH_module.try_to_find_img(settings['BG']['urlImg'], settings['BG']['pathImg'])
    if img_BG is False:
        img_BG = tuple(settings['BG']['COLOR'])

'''
Кубы, настройки:
type
x, y, w, h (orig_x, orig_y для кубов, где x, y определяются автоматически)
visibility (по умол - None)
moving (по умол - None)
cube corners (по умол - None)
text, color_text (для type - text)
color_unpressed (по умол - colors['black']), 
color_pressed (по умол - colors['red'])
create_cube (по умол - True)
'''
CubesHandling = CH_module.CubesHandling(window_width=window_width, window_height=window_height)
TransformatorCubes = CH_module.TransformatorCubes()

'''
4: {'type': 'cube', 'orig_x': 50, 'orig_y': 250, 'w': CubesHandling.w, 'h': CubesHandling.h, 'cube corners': True},
5: {'type': 'cube', 'orig_x': 300, 'orig_y': 250, 'w': CubesHandling.w, 'h': CubesHandling.h, 'cube corners': True},
6: {'type': 'cube', 'orig_x': 580, 'orig_y': 250, 'w': CubesHandling.w, 'h': CubesHandling.h, 'cube corners': True},
7: {'type': 'cube', 'orig_x': 850, 'orig_y': 250, 'w': CubesHandling.w, 'h': CubesHandling.h, 'cube corners': True},
8: {'type': 'cube', 'orig_x': 50, 'orig_y': 470, 'w': CubesHandling.w, 'h': CubesHandling.h, 'cube corners': True},
9: {'type': 'cube', 'orig_x': 300, 'orig_y': 470, 'w': CubesHandling.w, 'h': CubesHandling.h, 'cube corners': True},
10: {'type': 'cube', 'orig_x': 580, 'orig_y': 470, 'w': CubesHandling.w, 'h': CubesHandling.h,
     'cube corners': True},
11: {'type': 'cube', 'orig_x': 850, 'orig_y': 470, 'w': CubesHandling.w, 'h': CubesHandling.h,
     'cube corners': True},
'''

cubes = {
    0: {'type': 'cube', 'orig_x': 50, 'orig_y': 30, 'w': CubesHandling.w, 'h': CubesHandling.h, 'cube corners': True},
    1: {'type': 'cube', 'orig_x': 300, 'orig_y': 30, 'w': CubesHandling.w, 'h': CubesHandling.h, 'cube corners': True},
    2: {'type': 'cube', 'orig_x': 580, 'orig_y': 30, 'w': CubesHandling.w, 'h': CubesHandling.h, 'cube corners': True},
    3: {'type': 'cube', 'orig_x': 850, 'orig_y': 30, 'w': CubesHandling.w, 'h': CubesHandling.h, 'cube corners': True},

    # обязательно
    menu['menus'][1]: {
        'type': 'text', 'x': 100, 'y': 100, 'text': menu['menus'][1], 'visibility': True, 'cube corners': True
    },
    menu['menus'][2]: {
        'type': 'text', 'x': 400, 'y': 100, 'text': menu['menus'][2], 'visibility': True, 'cube corners': True
    },
    menu['menus'][3]: {
        'type': 'text', 'x': 650, 'y': 100, 'text': menu['menus'][3], 'visibility': True, 'cube corners': True
    },
    menu['menus'][4]: {
        'type': 'text', 'x': 1000, 'y': 100, 'text': menu['menus'][4], 'visibility': True, 'cube corners': True
    },
    'ready_cubes': {
        'type': 'text', 'x': 0, 'y': 0, 'text': '', 'create_cube': False
    },
}

for n_cube in cubes:
    TransformatorCubes.cube_fix(cubes[n_cube], n_cube, colors)

while True:
    # ИЗОБРАЖЕНИЕ
    success, img = cap.read()  # чтения изображения
    img = cv2.flip(img, 1)  # отзеркаленное изображение

    # УБИРАНИЕ ФОНА
    if settings['BG']['turn_on']:
        img = remove_BG.removeBG(img, img_BG, threshold=settings.settings['BG']['threshold'])

    # ПРОВЕРКА РУК
    if settings['HANDS']:
        hands = detector_hands.findHands(img, menu, timer=getattr(Game2048, 'time_move'))  # детектор рук
        if hands:
            for hand in hands:
                index_finger = hand['lmList'][8]
                middle_finger = hand['lmList'][12]
                index_finger_BP = hand['lmList'][5]  # расшифровка BP - BOTTOM POINT
                middle_finger_BP = hand['lmList'][9]  # расшифровка BP - BOTTOM POINT
                bottom_point = hand['lmList'][0]

                # расшифровка: l - длина (length), c - координаты (coords), FT - fingertip (кончики пальцев)
                l_FT, c_FT = detector_hands.findDistance((index_finger[0], index_finger[1]),
                                                         (middle_finger[0], middle_finger[1]))
                x_FT, y_FT = c_FT[4], c_FT[5]

                # расшифровка: l - длина (length), c - координаты (coords), BP - BOTTOM POINT
                _, c_BP = detector_hands.findDistance((index_finger_BP[0], index_finger_BP[1]),
                                                      (middle_finger_BP[0], middle_finger_BP[1]))
                x_BP, y_BP = c_BP[4], c_BP[5]

                fingers = detector_hands.fingersUp(hand)

                for cube in cubes:
                    if l_FT < 35 and CubesHandling.check_cursor_in_cube(
                            (x_FT, y_FT), cubes[cube], cube, colors, menu['now']) or menu['now'] == '2048':
                        # Start menu
                        if menu['now'] == menu['menus'][0] and cube in menu['menus']:
                            # суть игры
                            essence = None

                            if cube == menu['menus'][1]:  # проверка нажатия на текст
                                menu['now'] = menu['menus'][1]  # смена игры
                                essence = 'можно настроить всё под себя'

                            if cube == menu['menus'][2]:  # проверка нажатия на текст
                                menu['now'] = menu['menus'][2]  # смена игры
                                essence = 'суть проста - её нет)'

                            elif cube == menu['menus'][3]:  # проверка нажатия на текст
                                menu['now'] = menu['menus'][3]  # смена игры
                                essence = 'собрать все кубы в друг друга'

                            elif cube == menu['menus'][4]:
                                menu['now'] = menu['menus'][4]  # смена игры
                                essence = 'собрать куб 2048'

                            print(f'Режим - {menu["now"]}, суть проста - {essence}, чтобы вернуться жми - CTRL + Z')

                            for n_cube in cubes:
                                TransformatorCubes.change_cube_stats_to_game_stats(cubes[n_cube], n_cube, menu['now'],
                                                                                   colors)

                        # Настройки
                        if menu['now'] == menu['menus'][1]:
                            print(settings)

                        # touch cubes
                        if menu['now'] == menu['menus'][2]:
                            GameTouchCubes.play(cubes, cubes[cube], img, colors)
                            CubesHandling.move_cube(cubes, (x_FT, y_FT), cubes[cube])

                        # collect all cubes
                        elif menu['now'] == menu['menus'][3]:
                            GameCollectAllCubes.play(cubes)
                            CubesHandling.move_cube(cubes, (x_FT, y_FT), cubes[cube])

                        # 2048
                        elif menu['now'] == menu['menus'][4]:
                            Game2048.play(fingers, (x_FT, y_FT), (x_BP, y_BP))

                last_cursor = cubes.get('last_cursor')
                # создание последнего курсора, если не найден
                if last_cursor is None:
                    last_cursor = cubes['last_cursor'] = {'type': 'cursor', 'w': 25, 'h': 25}
                # сохранение последнего курсора
                last_cursor['x'], last_cursor['y'] = \
                    x_FT - last_cursor['w'] // 2, y_FT - last_cursor['h'] // 2

    # РИСОВАНИЕ
    for n_cube in cubes:
        """Кубы"""
        cube = cubes[n_cube]
        if cube.get('visibility') is True:
            """Текст"""
            if cube['type'] == 'text':
                cv2.putText(img, cube['text'],
                            (cube['x'] + 10, cube['y'] + 40),
                            font, 1, cube['color_text'], 2)

            """Общее"""
            if cube.get('create_cube') is True:
                cv2.rectangle(img, (cube['x'], cube['y']),
                              (cube['x'] + cube['w'], cube['y'] + cube['h']),
                              colors[n_cube], CubesHandling.size)

            if cube.get('cube corners') is True:
                cvzone.cornerRect(img, (cube['x'], cube['y'], cube['w'], cube['h']),
                                  1, rt=0)

            """Картинки"""
            if cube['type'] == 'image':
                cvzone.overlayPNG(img, cube['object'],
                                  (cube['x'], cube['y']))

    # ВИДЕО
    if recording:
        if video_recording == '':
            if not os.path.isdir('recording'):
                os.mkdir('recording')
            video_recording = cv2.VideoWriter(
                f'recording/video {datetime.datetime.today().strftime("%Y-%m-%d %H-%M-%S")}.mp4',
                cv2.VideoWriter_fourcc(*'MP4V'), 19, (window_width, window_height))
        img = cvzone.overlayPNG(img, cameraImg,
                                (10, 15))
        cv2.putText(img, str(round(time_recording)),
                    (10, 45),
                    font, 1, colors['white'], 2)
        video_recording_func(img)

    # ЛИЦО
    if settings['FACE']['turn_on']:
        faces = detector_faces.findFaceMesh(img, draw=settings.settings['FACE']['draw_face'])

    # ФПС
    if settings['FPS_IMG']:
        fps, img = detector_FPS.update(img, (10, 15), colors['red'], 1, 1)

    # КНОПКИ
    k = cv2.waitKey(10)
    if k == 27:  # ESC
        print('Закрытие')
        break
    elif k == 102 or k == 224:  # F
        recording = not recording
        print('Включение' if recording else 'Выключение', 'видео')
    elif k == 26:  # CTRL + Z
        if menu['now'] != menu['menus'][0]:
            menu['now'] = menu['menus'][0]
            print('Возращение')
            cubes['ready_cubes']['visibility'] = False
            cubes['ready_cubes']['text'] = ''
            for n_cube2 in cubes.values():
                TransformatorCubes.change_cube_stats_to_menu_stats(n_cube2)
        else:
            print('Вы уже в главном меню')
    elif k == 9:
        print('Инфа о кубах и меню:', cubes, menu, sep='\n')
    elif k != -1:
        print(f'Вы нажали {k}, но такая кнопка не добавлена')

    # ПОКАЗ ОНЛАЙН КАМЕРЫ
    cv2.imshow('camera', img)

cap.release()
if video_recording != '':
    video_recording.release()

cv2.destroyAllWindows()
