from typing import List, Callable

import cv2 as cv
import numpy as np

import math

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()


def camera_read():
    global cap
    ret, frame = cap.read()
    if not ret:
        return np.zeros(shape=(1, 1, 3), dtype=np.uint8)

    return frame


def camera_read_hsv():
    global cap

    ret, frame = cap.read()
    if not ret:
        return np.zeros(shape=(1, 1, 3), dtype=np.uint8)

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    return hsv


class GUI:
    def __init__(self):
        self.to_render = []

        self.joystick1 = Joystick(self)
        self.joystick2 = Joystick(self)

        self.display = Display(self)
        self.display.add_imshow(camera_read)
        self.display.add_imshow(camera_read_hsv)

        cv.createButton('autopilot', self.on_check, 1)

    def render(self):
        for elem in self.to_render:
            elem.render()

    @staticmethod
    def on_check(*args):
        print('checkbox', args[1])


class Joystick:
    __joysticks_count = 0

    def __init__(self, gui: GUI, window_name='Joystick'):
        Joystick.__joysticks_count += 1
        self.__window_name = f'{window_name}{Joystick.__joysticks_count}'

        self.angle: float = 0.0
        self.length: float = 0.0

        self.__image = np.zeros(shape=[400, 400, 3], dtype=np.uint8)

        cv.namedWindow(self.__window_name)
        cv.setMouseCallback(self.__window_name, self.__update_joystick)

        gui.to_render.append(self)

    def render(self, x=199, y=199):
        center = np.array([199, 199])

        cv.rectangle(self.__image, (x - 500, y - 500), (x + 500, y + 500), (0, 0, 0), -1)
        cv.circle(self.__image, center, 170, (102, 0, 0), -1)
        cv.rectangle(self.__image, (49, 179), (349, 219), (100, 100, 100), -1)
        cv.rectangle(self.__image, (179, 49), (219, 349), (100, 100, 100), -1)
        cv.line(self.__image, center,
                (int(self.length * np.cos(self.angle)), int(self.length * np.sin(self.angle))) + center,
                (200, 200, 200), lineType=16)
        cv.circle(self.__image,
                  (int(self.length * np.cos(self.angle)), int(self.length * np.sin(self.angle))) + center, 30,
                  (0, 0, 255), -1)

        cv.imshow(self.__window_name, self.__image)

    def __update_joystick(self, event, x, y, flags, param):
        # left button is pressed +
        # mouse moves
        if flags == cv.EVENT_FLAG_LBUTTON:
            r = 170
            screen_c = 199

            line_length = min(math.hypot(x - screen_c, y - screen_c), r)

            deg = -np.arctan2(x - screen_c, y - screen_c) + np.pi / 2
            # print(deg)

            self.length = line_length
            self.angle = deg

        else:
            self.length = 0
            self.angle = 0

        self.render(x, y)


class Display:
    __displays_count: int = 0

    def __init__(self, gui: GUI, window_name='Display'):
        Display.__displays_count += 1

        self.__window_name = f'{window_name}{Display.__displays_count}'
        self.__window_size = (640, 480)
        self.__current_index: int = 0

        self.__image_returners: List[Callable] = list()

        cv.namedWindow(self.__window_name)

        cv.createButton('<-', self.__on_previous, 'go back')
        cv.createButton('->', self.__on_next, 'go next')

        gui.to_render.append(self)

    def add_imshow(self, image_returner):
        self.__image_returners.append(image_returner)

    def render(self):
        if len(self.__image_returners) <= 0:
            return

        cv.imshow(self.__window_name, self.__image_returners[self.__current_index]())

    def __on_previous(self, *args):
        self.__current_index = (self.__current_index - 1) % max(1, len(self.__image_returners))

    def __on_next(self, *args):
        self.__current_index = (self.__current_index + 1) % max(1, len(self.__image_returners))


gui = GUI()

while True:
    gui.render()
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
