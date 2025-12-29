from CubesHandlingModule import CubesHandling
import cv2
import random


class GameTouchCubes(CubesHandling):
    """Игра без смысла"""

    def play(self, cubes, main_cube, img, colors):
        """Начало"""
        self.contact_controller_cubes(cubes, main_cube)
        self.screen_limits_controller_cubes(cubes, main_cube)
        self.draw_face(main_cube, img, colors)

    @staticmethod
    def contact_controller_cubes(cubes, main_cube, power_push=4):  # чем больше power_push, тем слабее пинок
        """Функция по проверке касания главного куба с второстепенным"""
        for cube in cubes.values():
            if cube != main_cube and cube['type'] == 'cube' and cube.get('moving') and \
                    main_cube['type'] == 'cube' and main_cube.get('moving'):
                '''
                Толкашки
                помогалка - https://cdn.discordapp.com/attachments/726314300502835241/975339515076026378/unknown.png
                '''
                if cube['y'] + cube['h'] / 3 < main_cube['y'] + main_cube['h'] / 2 < cube['y'] + cube['h'] * (3 / 4):
                    # 6 ЧАСТЬ (с начала x до половины w) восток
                    if cube['x'] <= main_cube['x'] + main_cube['w'] <= cube['x'] + cube['w'] / 2:
                        cube['x'] += main_cube['w'] // power_push

                    # 5 ЧАСТЬ (c половины w до конца w) запад
                    elif cube['x'] + cube['w'] / 2 <= main_cube['x'] <= cube['x'] + cube['w']:
                        cube['x'] -= main_cube['w'] // power_push

                if cube['x'] + cube['w'] / 3 < main_cube['x'] + main_cube['w'] / 2 < cube['x'] + cube['w'] * (3 / 4):
                    # 7 ЧАСТЬ (с начала y до половины h) север
                    if cube['y'] <= main_cube['y'] + main_cube['h'] <= cube['y'] + cube['h'] / 2:
                        cube['y'] += main_cube['h'] // power_push

                    # 8 ЧАСТЬ (c половины h до конца h) юг
                    elif cube['y'] + cube['h'] / 2 <= main_cube['y'] <= cube['y'] + cube['h']:
                        cube['y'] -= main_cube['h'] // power_push

                # 1 ЧАСТЬ (с половины w до конца w, с начала y до половины h)
                if cube['x'] + cube['w'] / 2 <= main_cube['x'] <= cube['x'] + cube['w'] and \
                        cube['y'] <= main_cube['y'] + main_cube['h'] <= cube['y'] + cube['h'] / 2:
                    cube['y'] += main_cube['h'] // power_push
                    cube['x'] -= main_cube['w'] // power_push

                # 2 ЧАСТЬ (с половины w до конца w, с половины h до конца h)
                if cube['x'] + cube['w'] / 2 <= main_cube['x'] <= cube['x'] + cube['w'] and \
                        cube['y'] + cube['h'] / 2 <= main_cube['y'] <= cube['y'] + cube['h']:
                    cube['y'] -= main_cube['h'] // power_push
                    cube['x'] -= main_cube['w'] // power_push

                # 3 ЧАСТЬ (с начала x до половины w, с половины h до конца h)
                if cube['x'] <= main_cube['x'] + main_cube['w'] <= cube['x'] + cube['w'] / 2 and \
                        cube['y'] + cube['h'] / 2 <= main_cube['y'] <= cube['y'] + cube['h']:
                    cube['y'] -= main_cube['h'] // power_push
                    cube['x'] += main_cube['w'] // power_push

                # 4 ЧАСТЬ (с начала x до половины w, с начала y до половины h)
                if cube['x'] <= main_cube['x'] + main_cube['w'] <= cube['x'] + cube['w'] / 2 and \
                        cube['y'] <= main_cube['y'] + main_cube['h'] <= cube['y'] + cube['h'] / 2:
                    cube['y'] += main_cube['h'] // power_push
                    cube['x'] += main_cube['w'] // power_push

    def screen_limits_controller_cubes(self, cubes, main_cube):
        """Проверка на выход за границы экрана"""
        for cube in cubes.values():
            if cube != main_cube and cube['type'] == 'cube' and cube.get('moving') and \
                    main_cube['type'] == 'cube' and main_cube.get('moving'):
                # обычный куб
                chances_for_cube = {
                    'рандомный телепорт': 50,
                    'противоположная сторона': 30,
                    'случайное передвижение по стороне': 30,
                    'толстота': 10
                }
                if cube['x'] < 0 or cube['x'] + cube['w'] > self.window_width or \
                        cube['y'] < 0 or cube['y'] + cube['h'] > self.window_height:
                    event = \
                        random.choices(tuple(chances_for_cube.keys()), weights=tuple(chances_for_cube.values()), k=1)[0]

                    if event == 'рандомный телепорт':
                        cube['x'] = random.randint(0, self.window_width - cube['w'])
                        cube['y'] = random.randint(0, self.window_height - cube['h'])

                    elif event == 'противоположная сторона':
                        if cube['x'] < 0:
                            cube['x'] = self.window_width - cube['w']
                        elif cube['x'] + cube['w'] > self.window_width:
                            cube['x'] = 0
                        if cube['y'] < 0:
                            cube['y'] = self.window_height - cube['h']
                        elif cube['y'] + cube['h'] > self.window_height:
                            cube['y'] = 0

                    elif event == 'случайное передвижение по стороне':
                        if cube['x'] < 0:
                            cube['x'] = 0
                            cube['y'] = random.randint(0, self.window_height - cube['h'])

                        elif cube['x'] + cube['w'] > self.window_width:
                            cube['x'] = self.window_width - cube['w']
                            cube['y'] = random.randint(0, self.window_height - cube['h'])

                        if cube['y'] < 0:
                            cube['y'] = 0
                            cube['x'] = random.randint(0, self.window_width - cube['w'])

                        elif cube['y'] + cube['h'] > self.window_height:
                            cube['y'] = self.window_height - cube['h']
                            cube['x'] = random.randint(0, self.window_width - cube['w'])

                    elif event == 'толстота':
                        flattening = 1.7
                        if cube['x'] < 0:
                            cube['x'] = 0
                            cube['h'] = int(self.h * flattening)
                            cube['w'] = int(self.w // flattening)

                        elif cube['x'] + cube['w'] > self.window_width:
                            cube['x'] = self.window_width - cube['w']
                            cube['h'] = int(self.h * flattening)
                            cube['w'] = int(self.w // flattening)

                        if cube['y'] < 0:
                            cube['y'] = 0
                            cube['w'] = int(self.h * flattening)
                            cube['h'] = int(self.w // flattening)

                        elif cube['y'] + cube['h'] > self.window_height:
                            cube['y'] = self.window_height - cube['h']
                            cube['w'] = int(self.h * flattening)
                            cube['h'] = int(self.w // flattening)

                # главный куб
                if main_cube['x'] < 0:
                    main_cube['x'] = 0

                elif main_cube['x'] + main_cube['w'] > self.window_width:
                    main_cube['x'] = self.window_width - main_cube['w']

                if main_cube['y'] < 0:
                    main_cube['y'] = 0

                elif main_cube['y'] + main_cube['h'] > self.window_height:
                    main_cube['y'] = self.window_height - main_cube['h']

    @staticmethod
    def draw_face(main_cube, img, colors):
        cv2.line(img, (main_cube['x'] + main_cube['w'] // 4, main_cube['y'] + main_cube['w'] * 4 // 5),
                 (main_cube['x'] + main_cube['w'] * 3 // 4, main_cube['y'] + main_cube['w'] * 4 // 5),
                 colors['green'], 15)
        cv2.circle(img, (main_cube['x'] + main_cube['w'] // 5, main_cube['y'] + main_cube['h'] // 5),
                   10, colors['green'], cv2.FILLED)
        cv2.circle(img, (main_cube['x'] + main_cube['w'] * 4 // 5, main_cube['y'] + main_cube['h'] // 5),
                   10, colors['green'], cv2.FILLED)
