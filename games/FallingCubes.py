import cv2
import random
import time
from core.CubesHandlingModule import CubesHandling


class FallingCubes(CubesHandling):
    """Игра 'Падающие кубики'"""

    def __init__(self, window_width, window_height, difficulty=3):
        super().__init__(window_width=window_width, window_height=window_height)
        self.points = 0
        self.cubes_falling = []  # Список кубиков: {'x', 'y', 'w', 'h', 'color', 'speed'}
        self.last_time = time.time()
        self.difficulty = difficulty
        # Начальный интервал зависит от сложности: 1.5 (лёгкая) -> 0.7 (сложная)
        self.spawn_interval = 2.0 - (difficulty * 0.25)
        self.game_over = False

    def spawn_cube(self, colors):
        w = random.randint(40, 80)
        h = w
        x = random.randint(0, self.window_width - w)
        y = -h
        # Скорость зависит от сложности
        base_speed = 3 + (self.difficulty * 2)
        speed = random.randint(base_speed, base_speed + 5)
        color = self.get_random_color(colors)

        self.cubes_falling.append(
            {
                "x": x,
                "y": y,
                "w": w,
                "h": h,
                "color": color,
                "speed": speed,
                "type": "falling",
            }
        )

    def play(self, img, fingers_pos, colors):
        if self.game_over:
            cv2.putText(
                img,
                "GAME OVER! Ctrl+Z to Reset",
                (self.window_width // 4, self.window_height // 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                colors["red"],
                3,
            )
            return

        # Появление новых кубиков
        if time.time() - self.last_time > self.spawn_interval:
            self.spawn_cube(colors)
            self.last_time = time.time()
            # Постепенное ускорение спавна
            self.spawn_interval = max(0.4, self.spawn_interval * 0.98)

        # Обновление и отрисовка
        for cube in self.cubes_falling[:]:
            cube["y"] += cube["speed"]

            # Отрисовка
            cv2.rectangle(
                img,
                (cube["x"], cube["y"]),
                (cube["x"] + cube["w"], cube["y"] + cube["h"]),
                cube["color"],
                2,
            )

            # Проверка касания
            for finger_x, finger_y in fingers_pos:
                if (
                    cube["x"] < finger_x < cube["x"] + cube["w"]
                    and cube["y"] < finger_y < cube["y"] + cube["h"]
                ):
                    self.points += 1
                    if cube in self.cubes_falling:
                        self.cubes_falling.remove(cube)
                    break

            # Проверка выхода за границу (проигрыш)
            if cube["y"] > self.window_height:
                self.game_over = True
                # self.cubes_falling.clear() # Можно очистить, можно оставить

        # Отрисовка счета
        cv2.putText(
            img,
            f"Score: {self.points}",
            (50, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            colors["white"],
            2,
        )

    def reset(self):
        self.points = 0
        self.cubes_falling = []
        self.spawn_interval = 2.0 - (self.difficulty * 0.25)
        self.last_time = time.time()
        self.game_over = False
