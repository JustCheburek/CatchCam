import cv2


class GameCollectAllCubes:
    """Игра по собиранию всех кубов в кучу"""

    def __init__(self):
        self.x_for_display = 0
        self.y_for_display = 0

    @staticmethod
    def hide(cubes):
        cubes['ready_cubes']['visibility'] = False
        cubes['ready_cubes']['text'] = ''

    def play(self, cubes):
        # Проверка кубов на соответствие координат
        cubes_saved = {}

        all_cubes = 0
        cubes_in_1_place = 2

        for cube in cubes:
            if cubes[cube]['type'] == 'cube':
                all_cubes += 1
                cube_x = cubes[cube]['x']
                cube_y = cubes[cube]['y']
                for cube2 in cubes_saved.values():
                    if cube_x == cube2[0] and cube_y == cube2[1]:
                        cubes_in_1_place += 1
                        self.x_for_display = cube_x
                        self.y_for_display = cube_y
                        break
                cubes_saved[cube] = (cube_x, cube_y)

        # показ сколько кубов осталось
        if cubes_in_1_place == all_cubes:
            cubes['ready_cubes']['text'] = 'WIN(ctrl+z)'
        else:
            cubes['ready_cubes']['x'], cubes['ready_cubes']['y'] = (self.x_for_display, self.y_for_display)
            cubes['ready_cubes']['text'] = f'{cubes_in_1_place} of {all_cubes}'
            if cubes_in_1_place != 2:
                cubes['ready_cubes']['visibility'] = True
