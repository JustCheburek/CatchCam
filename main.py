# встроенные файлы
import datetime  # для сохранения видео
import os

# готовые файлы
from settings import settings, colors

# установка + инициализация
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import cv2
import cvzone

# готовые файлы
from core import FaceMeshModule as FM_module
from core import FPS_module
from core import HandDetectorModule as HD_module
from core import CubesHandlingModule as CH_module
from core import ImagesHandlingModule as IH_module
from games.TouchCubes import TouchCubes
from games.CollectAllCubes import CollectAllCubes
from games.AR2048 import AR2048
from games.FallingCubes import FallingCubes


print("Создатель: https://t.me/JustCheburek")


def video_recording_func(camera):
    """Снятие видео"""
    global time_recording, recording, window_width, window_height
    time_recording += 0.05
    if time_recording > 100:
        time_recording = 0
        recording = not recording
    else:
        video_recording.write(cv2.resize(camera, (window_width, window_height)))


def return_to_menu():
    """Возврат в главное меню и сброс состояний игр"""
    global current_game
    if current_game != GAME_STATES["MENU"]:
        current_game = GAME_STATES["MENU"]
        print("Возврат в меню")
        GameCollectAllCubes.hide(cubes)
        GameFallingCubes.reset()
        for cube in cubes.values():
            TransformatorCubes.change_cube_stats_to_menu_stats(cube)


# Видео онлайн
cap = cv2.VideoCapture(settings.get("CAMERA_INDEX", 0), cv2.CAP_DSHOW)
# размеры приложения
window_width, window_height = 1280, 720
cap.set(3, window_width)
cap.set(4, window_height)

# ДЕТЕКТОРЫ
# Рук
detector_hands = None
if settings["HANDS"]:
    detector_hands = HD_module.HandDetector()
# Лица
detector_faces = None
if settings["FACE"]["turn_on"]:
    detector_faces = FM_module.FaceMeshDetector()
# ФПС
detector_FPS = FPS_module.FPS()
# Убирание фона
remove_BG = None
if settings["BG"]["turn_on"]:
    remove_BG = SelfiSegmentation()

# Окно управления (изменение размера)
cv2.namedWindow("camera", cv2.WINDOW_NORMAL)
is_fullscreen = False

# ШРИФТ
font = cv2.FONT_HERSHEY_SIMPLEX

# ВИДЕО
video_recording = ""
recording = False  # проверка на текущее видео
time_recording = 0

# СОСТОЯНИЕ ИГРЫ
GAME_STATES = {
    "MENU": "start menu",
    "TOUCH": "touch cubes",
    "COLLECT": "collect all cubes",
    "2048": "2048",
    "FALLING": "falling cubes",
}
current_game = GAME_STATES["MENU"]

# игры и начальная меню
StartMenu = CH_module.StartMenu()
GameTouchCubes = TouchCubes()
GameCollectAllCubes = CollectAllCubes()
Game2048 = AR2048()
GameFallingCubes = FallingCubes(
    window_width, window_height, difficulty=settings.get("DIFFICULTY", 3)
)

# КАРТИНКИ
# камера
cameraImg = IH_module.try_to_find_img("https://i.ibb.co/1bK4H73/camera.png")
# фон
img_BG = None
if settings["BG"]["turn_on"]:
    try:
        img_BG = IH_module.try_to_find_img(settings["BG"]["img"])
        if img_BG is not None and not isinstance(img_BG, tuple):
            # Изменение размера под размер окна
            img_BG = cv2.resize(img_BG, (window_width, window_height))
            # Если 4 канала (RGBA), конвертируем в BGR
            if img_BG.shape[2] == 4:
                img_BG = cv2.cvtColor(img_BG, cv2.COLOR_BGRA2BGR)
    except Exception:
        img_BG = tuple(settings["BG"]["COLOR"])

"""
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
"""
CubesHandling = CH_module.CubesHandling(
    window_width=window_width, window_height=window_height
)
TransformatorCubes = CH_module.TransformatorCubes()

cubes = {}

# Генерация сетки кубов 4x4 (0-15)
for i in range(16):
    row = i // 4
    col = i % 4
    cubes[i] = {
        "type": "cube",
        "orig_x": 50 + 180 * col,
        "orig_y": 20 + 180 * row,
        "w": CubesHandling.w,
        "h": CubesHandling.h,
        "cube corners": True,
    }

cubes["ready_cubes"] = {
    "type": "text",
    "x": 0,
    "y": 0,
    "text": "",
    "create_cube": False,
}

# Инициализация кубов для меню выбора игр
for i, state_name in enumerate(GAME_STATES.values()):
    if state_name == GAME_STATES["MENU"]:
        continue
    cubes[state_name] = {
        "type": "text",
        "x": 50,
        "y": 100 * i,
        "text": state_name,
        "visibility": True,
        "cube corners": True,
    }


for n_cube in cubes:
    TransformatorCubes.cube_fix(cubes[n_cube], n_cube, colors)

# Для falling cubes собираем все кончики пальцев
fingers_positions = []

while True:
    # ИЗОБРАЖЕНИЕ
    success, img = cap.read()  # чтения изображения
    if not success or img is None:
        print("Ошибка: Не удалось получить кадр с камеры.")
        cv2.waitKey(1000)  # Подождать секунду перед попыткой
        continue
    img = cv2.flip(img, 1)  # отзеркаленное изображение

    # УБИРАНИЕ ФОНА
    if settings["BG"]["turn_on"]:
        img = remove_BG.removeBG(img, img_BG, cutThreshold=settings["BG"]["threshold"])

    # ПРОВЕРКА РУК
    if settings["HANDS"]:
        # Детектор рук (возвращает список найденных рук)
        hands = detector_hands.findHands(
            img, current_game, timer=getattr(Game2048, "time_move")
        )
        if hands:
            # Обработка жеста "Сердце" двумя руками (выход в меню)
            if detector_hands.is_heart_gesture(hands):
                return_to_menu()

            for hand in hands:
                # Получаем жест и список пальцев
                gesture = detector_hands.get_gesture(hand)
                fingers = detector_hands.fingersUp(hand)

                # Координаты для курсора (центр между указательным и средним кончиками)
                idx_tip = hand["lmList"][8]
                mid_tip = hand["lmList"][12]
                x_FT, y_FT = (
                    (idx_tip[0] + mid_tip[0]) // 2,
                    (idx_tip[1] + mid_tip[1]) // 2,
                )

                # Режим: 2048 (жесты управляют игрой)
                if current_game == GAME_STATES["2048"]:
                    Game2048.play(cubes, colors, gesture)

                # Взаимодействие с кубами (через жест PINCH_2)
                for cube_id in cubes:
                    if gesture == "PINCH_2" and CubesHandling.check_cursor_in_cube(
                        (x_FT, y_FT), cubes[cube_id], cube_id, colors, current_game
                    ):
                        # Находимся в главном меню и нажали на название игры
                        if (
                            current_game == GAME_STATES["MENU"]
                            and cube_id in GAME_STATES.values()
                        ):
                            StartMenu.show(cube_id, cubes, colors)
                            current_game = cube_id  # Смена текущей игры
                            Game2048.reset()

                        # Режим: touch cubes
                        elif current_game == GAME_STATES["TOUCH"]:
                            GameTouchCubes.play(cubes, cubes[cube_id], img, colors)
                            CubesHandling.move_cube(cubes, (x_FT, y_FT), cubes[cube_id])

                        # Режим: collect all cubes
                        elif current_game == GAME_STATES["COLLECT"]:
                            GameCollectAllCubes.play(cubes)
                            CubesHandling.move_cube(cubes, (x_FT, y_FT), cubes[cube_id])

                last_cursor = cubes.get("last_cursor")
                # создание последнего курсора, если не найден
                if last_cursor is None:
                    last_cursor = cubes["last_cursor"] = {
                        "type": "cursor",
                        "w": 25,
                        "h": 25,
                    }
                # сохранение последнего курсора
                last_cursor["x"], last_cursor["y"] = (
                    x_FT - last_cursor["w"] // 2,
                    y_FT - last_cursor["h"] // 2,
                )

                # Собираем позиции всех поднятых пальцев для Falling Cubes
                for ik, finger_up in enumerate(fingers):
                    if finger_up:
                        fingers_positions.append(
                            hand["lmList"][detector_hands.tipIds[ik]][:2]
                        )

    if current_game == GAME_STATES["FALLING"]:
        GameFallingCubes.play(img, fingers_positions, colors)
    fingers_positions.clear()

    # РИСОВАНИЕ
    for n_cube in cubes:
        """Кубы"""
        cube = cubes[n_cube]
        if cube.get("visibility") is True:
            """Текст"""
            if cube["type"] == "text":
                cv2.putText(
                    img,
                    cube["text"],
                    (cube["x"] + 10, cube["y"] + 40),
                    font,
                    1,
                    cube["color_text"],
                    2,
                )

            if cube["type"] == "text_2048":
                if cube["text"] != "0":
                    x_fix_2048 = 10 * len(cube["text"])
                    cv2.putText(
                        img,
                        cube["text"],
                        (
                            cube["x"] + cube["w"] // 2 - x_fix_2048,
                            cube["y"] + cube["h"] // 2,
                        ),
                        font,
                        1,
                        cube["color_text"],
                        2,
                    )

            """Общее"""
            if cube.get("create_cube") is True:
                cv2.rectangle(
                    img,
                    (cube["x"], cube["y"]),
                    (cube["x"] + cube["w"], cube["y"] + cube["h"]),
                    colors[n_cube],
                    CubesHandling.size,
                )

            if cube.get("cube corners") is True:
                cvzone.cornerRect(
                    img, (cube["x"], cube["y"], cube["w"], cube["h"]), 1, rt=0
                )

            """Картинки"""
            if cube["type"] == "image":
                cvzone.overlayPNG(img, cube["object"], (cube["x"], cube["y"]))

    # ВИДЕО
    if recording:
        if video_recording == "":
            if not os.path.isdir("recording"):
                os.mkdir("recording")
            video_recording = cv2.VideoWriter(
                f"recording/video {datetime.datetime.today().strftime('%Y-%m-%d %H-%M-%S')}.mp4",
                cv2.VideoWriter_fourcc(*"MP4V"),
                19,
                (window_width, window_height),
            )
        img = cvzone.overlayPNG(img, cameraImg, (10, 15))
        cv2.putText(
            img, str(round(time_recording)), (10, 45), font, 1, colors["white"], 2
        )
        video_recording_func(img)

    # ЛИЦО
    if settings["FACE"]["turn_on"]:
        faces = detector_faces.findFaceMesh(img, draw=settings["FACE"]["draw_face"])

    # ФПС
    if settings["FPS_IMG"]:
        fps, img = detector_FPS.update(img, (10, 15), colors["red"], 1, 1)

    # КНОПКИ
    k = cv2.waitKey(10)
    if k == 27:  # ESC
        print("Закрытие")
        break
    elif k == 102 or k == 224:  # F
        recording = not recording
        print("Включение" if recording else "Выключение", "видео")
    elif k == 26:  # CTRL + Z (Возврат в меню)
        return_to_menu()
    elif k == 13:  # Enter (Полноэкранный режим)
        is_fullscreen = not is_fullscreen
        if is_fullscreen:
            cv2.setWindowProperty(
                "camera", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN
            )
        else:
            cv2.setWindowProperty("camera", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
        print("Полноэкранный режим:", "Включен" if is_fullscreen else "Выключен")
    elif k != -1:
        print(f"Вы нажали {k}, но такая кнопка не добавлена")

    # ПОКАЗ ОНЛАЙН КАМЕРЫ
    cv2.imshow("camera", img)

cap.release()
if video_recording != "":
    video_recording.release()

cv2.destroyAllWindows()
