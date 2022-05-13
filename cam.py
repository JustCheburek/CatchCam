import datetime
import os
import installing_modules
import settings
if settings.modules_installing:
    installing_modules.installing_modules()
import cv2
import cvzone
if settings.HANDS:
    import HandDetectorModule as HD_module


def check_cursor_in_cube(
        cursor, cube, name_cube
) -> True or False:
    """Функция по проверке нажатия курсором на куб"""
    if cube.get('visibility') is True:
        cursor_x1, cursor_y1 = cursor
        if cube['x'] - w < cursor_x1 < cube['x'] + cube['w'] and cube['y'] - h < cursor_y1 < cube['y'] + cube['h']:
            colors[name_cube] = cube.get('color_pressed')
            return True
        else:
            colors[name_cube] = cube.get('color_unpressed')
            return False


def check_cubes_in_1_place() -> str and (int, int):
    x_cubes = ()
    y_cubes = ()
    all_cubes = 0
    cubes_in_1_place = 1
    success_cubes_in_1_place = False

    for cube in cubes.values():
        if cube['type'] == 'cube':
            all_cubes += 1
            if cube['x'] in x_cubes and cube['y'] in y_cubes:
                cubes_in_1_place += 1
            else:
                x_cubes += (cube['x'],)
                y_cubes += (cube['y'],)

    if len(x_cubes) == 1 and len(y_cubes) == 1:
        success_cubes_in_1_place = True

    return success_cubes_in_1_place, (cubes_in_1_place, all_cubes)


def move_cube(cursor, cube):
    """Функция по передвижению кубов"""
    if cube.get('moving') is True:
        """Движение"""
        cursor_x, cursor_y, _ = cursor
        cube['x'], cube['y'] = cursor_x - cube['w'] // 2, cursor_y - cube['h'] // 2

        """Физика кубов"""
        last_cursor_cube = cubes['last_cursor']
        if last_cursor_cube.get('x') is None or last_cursor_cube.get('y') is None:
            return
        if last_cursor_cube['x'] > cursor_x:
            for _ in range(range_prediction_cubes):
                cube['x'] -= prediction_cubes
        elif last_cursor_cube['x'] + last_cursor_cube['w'] < cursor_x:
            for _ in range(range_prediction_cubes):
                cube['x'] += prediction_cubes
        if last_cursor_cube['y'] > cursor_y:
            for _ in range(range_prediction_cubes):
                cube['y'] -= prediction_cubes
        elif last_cursor_cube['y'] + last_cursor_cube['h'] < cursor_y:
            for _ in range(range_prediction_cubes):
                cube['y'] += prediction_cubes


def cube_fix(cube, name):
    """Добавление недостающих атрибутов кубов"""
    if cube['type'] == 'text':
        textSize = cv2.getTextSize(text=cube['text'], thickness=2,
                                   fontScale=1, fontFace=cv2.FONT_HERSHEY_SIMPLEX)[0]
        cube['w'] = textSize[0] + 20
        cube['h'] = textSize[1] + 40

    if cube.get('color_unpressed') is None:
        cube['color_unpressed'] = colors['black']
    if cube.get('color_pressed') is None:
        cube['color_pressed'] = colors['red']
    if cube['type'] == 'text' and cube.get('color_text') is None:
        cube['color_text'] = colors['green']
    if cube.get('create_cube') is None:
        cube['create_cube'] = True

    colors[name] = cube['color_unpressed']


def video_recording_func(camera) -> 'запись видео':
    """Снятие видео"""
    global time_recording, recording, window_width, window_height
    time_recording += 0.05
    if time_recording > 100:
        time_recording = 0
        recording = not recording
    else:
        video_recording.write(cv2.resize(camera, (window_width, window_height)))


'''Видео онлайн'''
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# размеры приложения
window_width, window_height = 1920, 1080
cap.set(3, window_width)
cap.set(4, window_height)

'''Детектор рук'''
if settings.HANDS:
    detector = HD_module.HandDetector()

"""Предсказания"""
prediction_cubes = 5  # передвижение кубов
range_prediction_cubes = 9  # насколько передвигать

'''Видео'''
video_recording = ''
recording = False  # проверка на текущее видео
FPS = 30
time_recording = 0

'''Цвета в BGR (blue green red)'''
colors = {
    'red': (0, 0, 255),
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'green': (0, 255, 0),
    'blue': (255, 0, 0)
}

'''Картинки'''
cameraImg = cv2.imread('images/camera.png', cv2.IMREAD_UNCHANGED)
backImg = cv2.imread('images/back.png', cv2.IMREAD_UNCHANGED)

'''
Кубы, настройки:
type
x, y, w, h
visibility (по умол - None)
moving (по умол - None)
cube corners (по умол - None)
text, color_text (для type - text)
color_unpressed (по умол - colors['black']), 
color_pressed (по умол - colors['red'])
create_cube (по умол - True) 
'''
w = 200
h = 200
size = 5

cubes = {
    0: {'type': 'cube', 'x': 100, 'y': 100, 'w': w, 'h': h, 'cube corners': True},
    1: {'type': 'cube', 'x': 200, 'y': 100, 'w': w, 'h': h, 'cube corners': True},

    # обязательно
    'game 1': {
        'type': 'text', 'x': 100, 'y': 100, 'text': 'movements cubes', 'visibility': True, 'cube corners': True
    },
    'game 2': {
        'type': 'text', 'x': 100, 'y': 200, 'text': 'collect all cubes', 'visibility': True, 'cube corners': True
    },
    'backImg': {
        'type': 'image', 'x': 10, 'y': 10, 'w': 0, 'h': 0, 'object': backImg, 'visibility': True
    },
    'cameraImg': {
        'type': 'image', 'x': 10, 'y': 20 + backImg.shape[1], 'w': 0, 'h': 0, 'object': cameraImg
    },
}

for n_cube in cubes:
    cube_fix(cubes[n_cube], n_cube)

suc, result = check_cubes_in_1_place()
print(suc, result)

menu = {'now': 'start_menu',
        'menus': [
            'start_menu',
            'touch_cubes'  # game 1
        ]}

while True:
    """Изображение"""
    success, img = cap.read()  # чтения изображения
    img = cv2.flip(img, 1)  # отзеркаленное изображение

    """Проверка рук"""
    if settings.HANDS:
        hands, _ = detector.findHands(img)  # детектор рук
        if hands:
            for hand in hands:
                index_finger = hand['lmList'][8]
                middle_finger = hand['lmList'][12]
                bottom_point = hand['lmList'][0]

                l, c = detector.findDistance((index_finger[0], index_finger[1]),
                                             (middle_finger[0], middle_finger[1]))
                c_x, c_y = c[4], c[5]

                if settings.show_number_fingers:
                    fingers = detector.fingersUp(hand)
                    number_fingers = cubes.get('number fingers')
                    if number_fingers is None:
                        cubes['number fingers'] = {
                            'type': 'text', 'x': 0, 'y': 0, 'text': '', 'color_text': colors['black'],
                            'visibility': True, 'cube corners': False, 'create_cube': False
                        }
                        cube_fix(cubes.get('number fingers'), 'number fingers')
                    else:
                        cubes['number fingers']['visibility'] = True
                        number_fingers['x'] = bottom_point[0] - number_fingers['w']
                        number_fingers['y'] = bottom_point[1] - number_fingers['h'] // 2
                        number_fingers['text'] = str(sum(fingers))

                for n_cube in cubes:
                    if l < 30 and check_cursor_in_cube((c_x, c_y), cubes[n_cube], n_cube):
                        if menu['now'] == menu['menus'][0]:
                            if n_cube == 'game 1':  # проверка нажатия на текст
                                menu['now'] = menu['menus'][1]  # смена игры
                                for n_cube2 in cubes:
                                    cube2 = cubes[n_cube2]
                                    if cube2['type'] == 'cube':
                                        cube2['visibility'], cube2['moving'] = True, True
                                    elif cube2['type'] == 'text':
                                        cube2['visibility'] = False
                        elif menu['now'] == menu['menus'][1]:
                            move_cube(index_finger, cubes[n_cube])

                last_cursor = cubes.get('last_cursor')
                # создание последнего курсора, если не найден
                if last_cursor is None:
                    last_cursor = cubes['last_cursor'] = {'type': 'cursor', 'w': 25, 'h': 25}
                # сохранение последнего курсора
                last_cursor['x'], last_cursor['y'] = \
                    index_finger[0] - last_cursor['w'] // 2, index_finger[1] - last_cursor['h'] // 2

        else:
            if cubes.get('number fingers') is not None:
                cubes['number fingers']['visibility'] = False

    """Рисование"""
    for n_cube in cubes:
        """Кубы"""
        cube_ = cubes[n_cube]
        if cube_.get('visibility') is True:
            """Текст"""
            if cube_['type'] == 'text':
                cv2.putText(img, cube_['text'],
                            (cube_['x'] + 10, cube_['y'] + 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, cube_['color_text'], 2)

            """Общее"""
            if cube_.get('create_cube') is True:
                cv2.rectangle(img, (cube_['x'], cube_['y']),
                              (cube_['x'] + cube_['w'], cube_['y'] + cube_['h']),
                              colors[n_cube], size)

            if cube_.get('cube corners') is True:
                cvzone.cornerRect(img, (cube_['x'], cube_['y'], cube_['w'], cube_['h']),
                                  size, rt=0)

            """Картинки"""
            if cube_['type'] == 'image':
                img = cvzone.overlayPNG(img, cube_['object'],
                                        (cube_['x'], cube_['y']))

    """Видео"""
    if recording and settings.RECORDING:
        if video_recording == '':
            if not os.path.isdir('recording'):
                os.mkdir('recording')
            video_recording = cv2.VideoWriter(
                f'recording/video {datetime.datetime.today().strftime("%Y-%m-%d %H-%M-%S")}.mp4',
                cv2.VideoWriter_fourcc(*'MP4V'), FPS, (window_width, window_height))
        cube_cameraImg = cubes['cameraImg']
        img = cvzone.overlayPNG(img, cameraImg,
                                (cube_cameraImg['x'], cube_cameraImg['y']))
        cv2.putText(img, str(round(time_recording)),
                    (cube_cameraImg['x'], cube_cameraImg['y'] + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, colors['white'], 2)
        video_recording_func(img)

    '''Лицо'''
    if settings.FACE:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        haar_face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
        faces = haar_face_cascade.detectMultiScale(gray_img)
        if isinstance(settings.BLUR, int):
            for (x_, y_, w_, h_) in faces:
                # cv2.rectangle(img, (x_, y_), (x_ + w_, y_ + h_), colors['white'], 1)
                img[y_:y_ + h_, x_:x_ + w_] = cv2.medianBlur(img[y_:y_ + h_, x_:x_ + w_], settings.BLUR)

    cv2.imshow('camera', img)

    """Кнопки"""
    k = cv2.waitKey(10)
    if k == 27:
        print('Закрытие')
        break
    elif k == 102:
        recording = not recording
        print('Включение' if recording else 'Выключение', 'видео')

cap.release()
if video_recording != '':
    video_recording.release()

cv2.destroyAllWindows()
