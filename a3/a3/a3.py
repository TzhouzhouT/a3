import tkinter as tk
from tkinter import filedialog  # For masters task
from typing import Callable, Union, Optional
from a3_support import *
from model import *
from constants import *


# Implement your classes here
class InfoBar(AbstractGrid):
    day = 0
    money = 0
    energy = 0

    def __init__(self, master: tk.Tk | tk.Frame) -> None:
        super().__init__(master, (2, 3), (FARM_WIDTH, INFO_BAR_HEIGHT))
        self.redraw(1, 0, 100)

    def redraw(self, day: int, money: int, energy: int) -> None:
        self.day = day
        self.money = money
        self.energy = energy
        self.create_text(100, 45, text="Day:\n\n" + str(self.day), font=HEADING_FONT)
        self.create_text(200, 45, text="Money:\n\n$" + str(self.money), font=HEADING_FONT)
        self.create_text(300, 45, text="Energy:\n\n" + str(self.energy), font=HEADING_FONT)
        self.pack()


class FarmView(AbstractGrid):

    def __init__(self, master: tk.Tk | tk.Frame, dimensions: tuple[int, int], size: tuple[int, int], **kwargs) -> None:
        super().__init__(master, dimensions, size)

    def redraw(self, ground: list[str], plants: dict[tuple[int, int], Plant], player_position: tuple[int, int],
               player_direction: str) -> None:
        # 加载每张图像并存储到字典中
        # 定义每个图像大小
        image_width = 50
        image_height = 50
        images = {}
        for c in set([item for line in ground for item in line]):
            image_file = ''
            if c == GRASS:
                image_file = 'images/grass.png'
            elif c == SOIL:
                image_file = 'images/soil.png'
            elif c == UNTILLED:
                image_file = 'images/untilled_soil.png'
            get_image(image_file, (image_width, image_height), images)
            self.create_image(image_width, image_height, anchor='nw', image=images[image_file])
        self.pack()
        pass


def play_game(root: tk.Tk, map_file: str) -> None:
    pass  # Implement your play_game function here


def main() -> None:
    pass


if __name__ == '__main__':
    main()
    # 创建画布并展示图像
    farm_model = FarmModel('maps/map2.txt')
    # print(farm_model.get_dimensions())
    # print(farm_model.get_map())

    root = tk.Tk()
    root.geometry("700x700")
    info_frame = tk.Frame(root)
    info_frame.pack(side=tk.BOTTOM)
    farm_frame = tk.Frame(root)
    farm_frame.pack(side=tk.BOTTOM)
    #
    # # 创建四个Canvas
    # canvas1 = tk.Canvas(frame)
    # image_banner = Image.open('images/header.png')
    # img_banner = ImageTk.PhotoImage(image_banner)
    # banner_id = canvas1.create_image(0, 0, image=img_banner)
    # # canvas1.grid(row=0, column=0)
    # canvas1.pack(side=tk.TOP)
    farm_view = FarmView(farm_frame, farm_model.get_dimensions(), (FARM_WIDTH, FARM_WIDTH))
    farm_view.redraw(farm_model.get_map(), None, (0, 0), DOWN)
    farm_view.pack(side=tk.BOTTOM)
    info_bar = InfoBar(info_frame)
    # info_bar.create_text(100, 45, text="Day:\n\n" + str(info_bar.day), font=HEADING_FONT)
    # info_bar.create_text(200, 45, text="Money:\n\n$" + str(info_bar.money), font=HEADING_FONT)
    # info_bar.create_text(300, 45, text="Energy:\n\n" + str(info_bar.energy), font=HEADING_FONT)
    # # info_bar.grid(row=2, column=0)
    # info_bar.pack(side=tk.BOTTOM)
    # # 运行主循环
    root.mainloop()

