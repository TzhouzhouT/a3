import tkinter as tk
from tkinter import filedialog  # For masters task
from typing import Callable, Union, Optional
from a3_support import *
from model import *
from constants import *


# Implement your classes here
class ItemView(tk.Frame):

    def __init__(self, master: tk.Frame, item_name: str, amount: int,
                 select_command: Optional[Callable[[str], None]] = None,
                 sell_command: Optional[Callable[[str], None]] = None,
                 buy_command: Optional[Callable[[str], None]] = None) -> None:
        super().__init__(master)
        # self.pack(side=tk.BOTTOM)
        canvas = tk.Canvas(master, width=INVENTORY_WIDTH, height=FARM_WIDTH // 6, bg=INVENTORY_COLOUR, borderwidth=2)
        canvas.pack(fill=tk.BOTH)
        # INVENTORY_COLOUR = '#fdc074'
        # INVENTORY_OUTLINE_COLOUR = '#d68f54'
        # INVENTORY_SELECTED_COLOUR = '#d68f54'
        # INVENTORY_EMPTY_COLOUR = 'grey'
        bg_color = INVENTORY_EMPTY_COLOUR if amount == 0 else INVENTORY_COLOUR
        amount = tk.Label(canvas, text=item_name + " :" + str(amount), bg=bg_color)
        sell_price = tk.Label(canvas, text="Sell price : $" + str(SELL_PRICES[item_name]), bg=bg_color)
        buy_price = tk.Label(canvas, text="Buy price : $" + str(BUY_PRICES.get(item_name, 'N/A')), bg=bg_color)
        amount.pack(fill=tk.BOTH)
        sell_price.pack(fill=tk.BOTH)
        buy_price.pack(fill=tk.BOTH)
    pass

    def update(self, amount: int, selected: bool = False) -> None:
        pass


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
        super().__init__(master, dimensions, size, **kwargs)

    def redraw(self, ground: list[str], plants: dict[tuple[int, int], Plant], player_position: tuple[int, int],
               player_direction: str) -> None:
        # 定义每个图像大小22
        image_width = 50
        image_height = 50
        images = {}
        relation = {}
        for c in set([item for line in ground for item in line]):
            image_file = 'images/' + IMAGES[c]
            get_image(image_file, (image_width, image_height), images)
            relation[c] = image_file
        i = 0
        for line in ground:
            for j, c in enumerate(line):
                self.create_image(j * image_width, i * image_height, anchor='nw', image=images[relation[c]])
            i += 1
        # 加载角色图像，并设置初始位置
        image_d = Image.open('images/player_d.png')
        image_d = image_d.resize((image_width, image_height), Image.LANCZOS)
        play_img = ImageTk.PhotoImage(image_d)
        self.create_image(0, self._size[1] // 2, anchor='nw', image=play_img)
        self.pack()


def play_game(root: tk.Tk, map_file: str) -> None:
    pass  # Implement your play_game function here


def main() -> None:
    pass


def turn_new_day(farm_model: FarmModel) -> None:
    return farm_model.new_day()


if __name__ == '__main__':
    main()
    # 创建画布并展示图像
    farm_model = FarmModel('maps/map1.txt')
    root = tk.Tk()
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.BOTTOM)
    button = tk.Button(button_frame, text='Next day', command=lambda: turn_new_day(farm_model))
    button.pack()

    info_frame = tk.Frame(root)
    info_frame.pack(side=tk.BOTTOM)
    info_bar = InfoBar(info_frame)

    farm_frame = tk.Frame(root, width=FARM_WIDTH, height=FARM_WIDTH, bg='blue')
    farm_view = FarmView(farm_frame, farm_model.get_dimensions(), (FARM_WIDTH, FARM_WIDTH))
    # farm_view.redraw(farm_model.get_map(), farm_model.get_plants(), (0, 0), DOWN)
    # 定义每个图像大小22
    image_width = 50
    image_height = 50
    ground = farm_model.get_map()
    images = {}
    relation = {}
    for c in set([item for line in ground for item in line]):
        image_file = 'images/' + IMAGES[c]
        get_image(image_file, (image_width, image_height), images)
        relation[c] = image_file
    i = 0
    for line in ground:
        for j, c in enumerate(line):
            farm_view.create_image(j * image_width, i * image_height, anchor='nw', image=images[relation[c]])
        i += 1
    # 加载角色图像，并设置初始位置
    image_d = Image.open('images/player_d.png')
    image_d = image_d.resize((image_width, image_height), Image.LANCZOS)
    play_img = ImageTk.PhotoImage(image_d)
    farm_view.create_image(0, farm_view._size[1] // 2, anchor='nw', image=play_img)
    farm_view.pack()
    farm_frame.pack(side=tk.LEFT)

    all_item_frame = tk.Frame(root, width=INVENTORY_WIDTH, height=FARM_WIDTH, bg='green', borderwidth=1)
    all_item_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
    for i in range(len(ITEMS)):
        item_frame = tk.Frame(all_item_frame, width=INVENTORY_WIDTH, height=FARM_WIDTH // 6, bg='green', borderwidth=1)
        item_frame.pack(side=tk.TOP, fill=tk.BOTH)
        item_view = ItemView(item_frame, ITEMS[i], farm_model.get_player().get_inventory().get(ITEMS[i], 0))

    # item_frame = tk.Frame(root, width=INVENTORY_WIDTH, height=FARM_WIDTH // 6, bg='red')
    # item_frame.pack(side=tk.BOTTOM)
    # amount = tk.Label(root, text="item_name" + " :" + str(0), bg='red')
    # amount.pack()
    # # 运行主循环
    root.mainloop()
