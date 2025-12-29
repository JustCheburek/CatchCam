import cv2
import random


class CubesHandling:
    """Работа с кубами"""

    def __init__(self, size_cube=(130, 130), size_bumpers=2, window_width=1920,
                 window_height=1080):
        """Объявление переменных"""
        self.w, self.h = size_cube  # ширина, высота
        self.size = size_bumpers  # бортики куба
        self.prediction_move_cubes = 5  # передвижение кубов
        self.range_prediction_cubes = 7  # кол-во передвижения
        self.window_width = window_width
        self.window_height = window_height

    @staticmethod
    def check_cursor_in_cube(cursor, cube, name_cube, colors, game, reducing_size_cube=5) -> True or False:
        """Функция по проверке нажатия курсором на куб"""
        if cube.get('visibility'):
            cursor_x1, cursor_y1 = cursor
            if cube['type'] == 'cube':
                if cube['x'] + cube['w'] / reducing_size_cube < cursor_x1 < cube['x'] + cube['w'] - cube['w'] \
                        / reducing_size_cube and cube['y'] + cube['w'] / reducing_size_cube < cursor_y1 < cube['y'] + \
                        cube['h'] - cube['h'] / reducing_size_cube:
                    if game != '2048':
                        colors[name_cube] = cube.get('color_pressed')
                    return True
                else:
                    if game != '2048':
                        colors[name_cube] = cube.get('color_unpressed')
                    return False
            else:
                if cube['x'] < cursor_x1 < cube['x'] + cube['w'] and cube['y'] < cursor_y1 < cube['y'] + cube['h']:
                    colors[name_cube] = cube.get('color_pressed')
                    return True
                else:
                    colors[name_cube] = cube.get('color_unpressed')
                    return False

    def prediction_cubes(self, cube, cubes, cursor):
        """Предсказания кубов"""
        cursor_x, cursor_y = cursor

        last_cursor_cube = cubes['last_cursor']

        if last_cursor_cube.get('x') is not None or last_cursor_cube.get('y') is not None:
            if last_cursor_cube['x'] > cursor_x:
                for _ in range(self.range_prediction_cubes):
                    cube['x'] -= self.prediction_move_cubes

            elif last_cursor_cube['x'] + last_cursor_cube['w'] < cursor_x:
                for _ in range(self.range_prediction_cubes):
                    cube['x'] += self.prediction_move_cubes

            if last_cursor_cube['y'] > cursor_y:
                for _ in range(self.range_prediction_cubes):
                    cube['y'] -= self.prediction_move_cubes

            elif last_cursor_cube['y'] + last_cursor_cube['h'] < cursor_y:
                for _ in range(self.range_prediction_cubes):
                    cube['y'] += self.prediction_move_cubes

    def move_cube(self, cubes, cursor, cube, with_prediction: bool = True) -> 'cube':
        """Функция по передвижению кубов и по их предсказаниям"""
        if cube.get('moving') is True:
            # Движение
            cursor_x, cursor_y = cursor
            cube['x'], cube['y'] = cursor_x - cube['w'] // 2, cursor_y - cube['h'] // 2

            if with_prediction:
                self.prediction_cubes(cube, cubes, cursor)


class TransformatorCubes(CubesHandling):
    def change_cube_stats_to_game_stats(self, cubes, game, colors):
        """Готовит кубы к игре"""
        for cube in cubes.values():
            if cube['type'] == 'cube':
                cube['visibility'], cube['moving'] = True, True
                cube['w'], cube['h'] = self.w, self.h
                if game == '2048':
                    cube['type'] = 'text_2048'
                    cube['text'] = '0'
                    cube['color_text'] = colors['black']
            elif cube['type'] == 'text':
                cube['visibility'] = False

    @staticmethod
    def change_cube_stats_to_menu_stats(cube):
        """Готовит кубы к меню"""
        if cube['type'] == 'text_2048':
            cube['type'] = 'cube'
            cube['text'] = ''
        if cube['type'] == 'cube':
            cube['visibility'], cube['moving'] = False, False
            cube['x'] = cube['orig_x']
            cube['y'] = cube['orig_y']
        elif cube['type'] == 'text':
            cube['visibility'] = True

    @staticmethod
    def cube_fix(cube, name_cube, colors):
        """Добавление недостающих атрибутов кубов"""
        if cube['type'] == 'text':
            textSize = cv2.getTextSize(text=cube['text'], thickness=2,
                                       fontScale=1, fontFace=cv2.FONT_HERSHEY_SIMPLEX)[0]
            cube['w'] = textSize[0] + 20
            cube['h'] = textSize[1] + 40

        elif cube['type'] == 'cube':
            cube['x'] = cube['orig_x']
            cube['y'] = cube['orig_y']

        if cube.get('color_unpressed') is None:
            cube['color_unpressed'] = colors['black']
        if cube.get('color_pressed') is None:
            cube['color_pressed'] = colors['red']
        colors[name_cube] = cube['color_unpressed']

        if cube['type'] == 'text' and cube.get('color_text') is None:
            cube['color_text'] = colors['green']
        if cube.get('create_cube') is None:
            cube['create_cube'] = True


class StartMenu(TransformatorCubes):
    def show(self, cube, cubes, menu, colors):
        # суть игры
        essence = None

        if cube == menu['menus'][1]:  # проверка нажатия на текст
            menu['now'] = menu['menus'][1]  # смена игры
            essence = 'можно настроить всё под себя'

        elif cube == menu['menus'][2]:
            menu['now'] = menu['menus'][2]
            essence = 'её нет)'

        elif cube == menu['menus'][3]:
            menu['now'] = menu['menus'][3]
            essence = 'собрать все кубы в друг друга'

        elif cube == menu['menus'][4]:
            menu['now'] = menu['menus'][4]
            essence = 'собрать куб 2048'

        self.change_cube_stats_to_game_stats(cubes, menu['now'], colors)
        print(f'Режим - {menu["now"]}, суть проста - {essence}, чтобы вернуться жми - CTRL + Z')
