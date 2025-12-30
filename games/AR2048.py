import random
import numpy as np
import time


class Logic2048:
    def __init__(self, width=4, height=4):
        self.mat = []
        self.width = width
        self.height = height

        for i in range(height):
            self.mat.append([0] * width)

        self.add_new_2()

    def add_new_2(self):
        line = random.randint(0, self.height - 1)
        element = random.randint(0, self.width - 1)

        while self.mat[line][element] != 0:
            line = random.randint(0, self.height - 1)
            element = random.randint(0, self.width - 1)

        self.mat[line][element] = 2

    def get_current_state(self):
        for line in self.mat:
            if 2048 in line:
                return "Выигрыш \n1) ctrl + z, чтобы вернуться \n2) Можете продолжить играть, при этом 2048 пропадёт"

            if 0 in line:
                self.add_new_2()
                return

        for line in range(self.height - 1):
            for element_index in range(self.width - 1):
                main_element = self.mat[line][element_index]

                right_element = self.mat[line][element_index + 1]
                down_element = self.mat[line + 1][element_index]

                if main_element == down_element or main_element == right_element:
                    self.add_new_2()
                    return

            up_element = self.mat[line + 1][self.width - 1]
            if self.mat[line][3] == up_element:
                return

            left_element = self.mat[self.height - 1][line + 1]  # line = element_index
            if self.mat[3][line] == left_element:
                return

        return "Проигрыш \nctrl + z, чтобы вернуться"

    def print_mat(self, text=None):
        for line in self.mat:
            print(*line)
        if text is not None:
            print(text)

    # ДВИЖЕНИЯ
    def move_left(self):
        self.compress()
        self.merge()
        self.compress()
        return self.mat

    def move_right(self):
        self.reverse()
        self.move_left()
        self.reverse()
        return self.mat

    def move_up(self):
        self.transpose()
        self.move_left()
        self.transpose()
        return self.mat

    def move_down(self):
        self.transpose()
        self.move_right()
        self.transpose()
        return self.mat

    # ТРАНСФОРМАЦИЯ
    def compress(self):
        """Сдвижение влево"""
        new_mat = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        # self.print_mat('Compress:')
        for line in range(self.height):
            pos = 0
            for element in range(self.width):
                if self.mat[line][element] != 0:
                    new_mat[line][pos] = self.mat[line][element]
                    pos += 1

        self.mat = new_mat

    def merge(self):
        """Соединение"""
        # self.print_mat('Merge:')
        for line in range(self.height):
            for element in range(self.width - 1):
                main_element = self.mat[line][element]
                right_element = self.mat[line][element + 1]
                if main_element == right_element and main_element != 0:
                    self.mat[line][element] *= 2
                    self.mat[line][element + 1] = 0

    def reverse(self):
        """Переворот"""
        # self.print_mat('Reverse:')
        self.mat = np.fliplr(self.mat)

    def transpose(self):
        """Отражение одновременно и по горизонтали и по вертикали"""
        new_mat = [[], [], [], []]
        # self.print_mat('Transpose:')
        for i in range(self.height):
            for j in range(self.width):
                new_mat[i].append(self.mat[j][i])

        self.mat = new_mat


class AR2048(Logic2048):
    """Игра 2048"""

    def __init__(self):
        super().__init__()
        self.last_time = time.perf_counter()
        self.time_move = 0

    def reset(self):
        self.last_time = time.perf_counter()
        self.time_move = 0

    @staticmethod
    def near_coord(p1: int, p2: int, proximity: int = 100) -> True or False:
        if p2 + proximity >= p1 >= p2 - proximity:
            return True
        else:
            return False

    def play(self, cubes, colors, gesture):
        self.time_move = time.perf_counter() - self.last_time

        if self.time_move < 3:
            return

        move_made = False
        if gesture == "RIGHT_2":
            print("Вправо")
            self.move_right()
            move_made = True
        elif gesture == "LEFT_2":
            print("Влево")
            self.move_left()
            move_made = True
        elif gesture == "UP_2":
            print("Вверх")
            self.move_up()
            move_made = True
        elif gesture == "DOWN_2":
            print("Вниз")
            self.move_down()
            move_made = True

        if move_made:
            self.print_mat(self.get_current_state())

            for cube in cubes:
                if cubes[cube]["type"] == "text_2048":
                    if cubes[cube]["text"] == "WIN(ctrl+z)":
                        self.mat[int(cube) // 4][int(cube) % 4] = cubes[cube][
                            "text"
                        ] = 0

                    cubes[cube]["text"] = str(self.mat[int(cube) // 4][int(cube) % 4])

                    if 2 <= int(cubes[cube]["text"]) <= 16:
                        cubes[cube]["color_text"] = colors["green"]
                    elif 16 < int(cubes[cube]["text"]) <= 256:
                        cubes[cube]["color_text"] = colors["yellow"]
                    elif 256 < int(cubes[cube]["text"]):
                        cubes[cube]["color_text"] = colors["red"]
                    else:
                        cubes[cube]["color_text"] = colors["black"]
                    if int(cubes[cube]["text"]) == 2048:
                        cubes[cube]["text"] = "WIN(ctrl+z)"

            self.last_time = time.perf_counter()
