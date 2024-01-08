import math
import os
from tkinter import *
from PIL import Image, ImageTk
import pyautogui

num_key_frames = 8


def print_image(im):
    for y in range(im.size[0]):
        for x in range(im.size[1]):
            print(im.getpixel((x, y)), end=' ')
        print()


class RotatableAnimation:
    def __init__(self, path, size):
        self.path = path
        self.frames = {}
        self.angle = 0
        self.n_step = 0

        for angle in range(0, 360):
            self.frames[angle] = []
            with Image.open(path) as im:
                self.n_frames = im.n_frames
                for i in range(im.n_frames):
                    im.seek(i)
                    A = im.copy().convert("RGBA").resize(size)
                    self.frames[angle].append(ImageTk.PhotoImage(A.rotate(angle)))

    def rotate(self, angle):
        self.angle = angle

    def step(self):
        self.n_step += 1
        self.n_step %= self.n_frames

    def current_frame(self):
        return self.frames[self.angle][self.n_step]


class Goose:
    def __init__(self, window):
        window.overrideredirect(1)
        window.attributes('-topmost', 1)
        window.geometry("100x100+500+500")
        window.configure(bg='blue')
        if os.name == 'nt':
            window.wm_attributes("-transparentcolor", "blue")

        self.x = 0
        self.y = 0
        self.target_x = 0
        self.target_y = 0
        self.animation = RotatableAnimation("goose.gif", (100, 100))
        self.label = Label(window, image=self.animation.current_frame(), bg='blue')
        self.label.pack()
        self.window = window

    def setTarget(self, x, y):
        self.target_x = x
        self.target_y = y

    def move(self):
        if self.x < self.target_x - 5:
            self.x += 5
        elif self.x > self.target_x + 5:
            self.x -= 5
        if self.y < self.target_y - 5:
            self.y += 5
        elif self.y > self.target_y + 5:
            self.y -= 5

        self.animation.step()
        self.animation.rotate(self.__calculate_angle())
        self.window.geometry("+{}+{}".format(self.x, self.y))

    def update(self):
        mouse_x, mouse_y = self.window.winfo_pointerxy()
        self.setTarget(mouse_x, mouse_y)
        self.move()
        self.label.config(image=self.animation.current_frame())

    def __calculate_angle(self):
        A = -1 * int(math.degrees(math.atan2(self.target_y - (self.y + 50), self.target_x - (self.x + 50))))
        A = A + 180
        return A % 360


window = Tk()


def frame():
    goose.update()
    window.after(40, frame)


goose = Goose(window)

window.after(40, frame)
window.mainloop()
