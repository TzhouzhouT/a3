import tkinter as tk
from tkinter import filedialog  # For masters task
from typing import Callable, Union, Optional
from a3_support import *
from model import *
from constants import *


# Implement your classes here
class InfoBar(AbstractGrid):
    """
    """

    def __init__(self, master: tk.Tk | tk.Frame) -> None:
        """Sets up the InfoBar.

        Parameters:
        master:
        """
        super().__init__(
            master,
            dimensions=(2, 3),
            size=(FARM_WIDTH + INVENTORY_WIDTH, INFO_BAR_HEIGHT)
        )

    def redraw(self, day: int, money: int, energy: int) -> None:
        """Clears the InfoBar and redraws it to display the provided day,
        money, and energy.

        Parameters:
        day:

        money:

        energy:
        """
        self.clear()
        self.annotate_position((0, 0), "Day:", HEADING_FONT)
        self.annotate_position((1, 0), str(day), HEADING_FONT)
        self.annotate_position((0, 1), "Money:", HEADING_FONT)
        self.annotate_position((1, 1), "$" + str(money), HEADING_FONT)
        self.annotate_position((0, 2), "Energy:", HEADING_FONT)
        self.annotate_position((1, 2), str(energy), HEADING_FONT)


class FarmView(AbstractGrid):
    """
    """

    def __init__(self, master: tk.Tk | tk.Frame, dimensions: tuple[int, int],
                 size: tuple[int, int], **kwargs) -> None:
        """
        """
        super().__init__(master, dimensions=dimensions, size=size)
        self.cache = {}
        for value in IMAGES.values():
            picture_path = f"images/{value}"
            get_image(picture_path, self.get_cell_size(), self.cache)

    def redraw(self, ground: list[str], plants: dict[tuple[int, int], 'Plant'],
               player_position: tuple[int, int], player_direction: str) -> None:
        """
        """
        self.clear()
        # Draw the ground.
        for i, row in enumerate(ground):
            for j, col in enumerate(row):
                p = (i, j)
                pixel_x, pixel_y = self.get_midpoint(p)
                if col in ['S', "U", "G"]:
                    # Get the picture name based on the col value.
                    picture_name = IMAGES[col]
                    # Get the picture path using the picture_name.
                    picture_path = f"images/{picture_name}"
                    image0 = self.cache.get(picture_path)
                    self.create_image(pixel_x, pixel_y, image=image0)
        # Draw the plants.
        for key, value in plants.items():
            pixel_x1, pixel_y1 = self.get_midpoint(key)
            picture_name1 = get_plant_image_name(value)
            get_image(picture_name1, self.get_cell_size(), self.cache)
            image1 = self.cache.get(picture_name1)
            self.create_image(pixel_x1, pixel_y1, image1)
        # Draw the player.
        player = self.cache.get("images/player")
        player = f"images/player_{player_direction}.png"
        image2 = self.cache.get(player)
        pixel_x2, pixel_y2 = self.get_midpoint(player_position)
        self.create_image(pixel_x2, pixel_y2, image=image2)


class ItemView(tk.Frame):
    """A frame displaying relevant information and buttons for a single item."""

    def __init__(self, master: tk.Frame, item_name: str, amount: int,
                 select_command: Optional[Callable[[str], None]] = None,
                 sell_command: Optional[Callable[[str], None]] = None,
                 buy_command: Optional[Callable[[str], None]] = None) -> None:
        """
        """
        super().__init__(master)
        self.item_name = item_name
        self.amount = amount
        if amount > 0:
            bg_color = INVENTORY_COLOUR
        else:
            bg_color = INVENTORY_EMPTY_COLOUR
        self.configure(bg=bg_color)
        # Build a label frame.
        self.label_frame = tk.Frame(self, width=INVENTORY_WIDTH, height=FARM_WIDTH // 6, bg=bg_color)
        self.label_frame.pack_propagate(False)
        self.label_frame.pack(side=tk.LEFT)
        self.label_container = tk.Frame(self.label_frame, bg=bg_color)
        self.label_container.pack(side=tk.LEFT, fill=tk.Y)
        self.amount_label = tk.Label(self.label_container, text=item_name + ": " + str(amount), bg=bg_color)
        self.amount_label.pack(side=tk.TOP, anchor=tk.W)
        self.sell_label = tk.Label(self.label_container, text="Sell price: $" + str(SELL_PRICES[item_name]),
                                   bg=bg_color)
        self.sell_label.pack(side=tk.TOP, anchor=tk.W)
        self.buy_label = tk.Label(self.label_container, text="Buy price: $" + str(BUY_PRICES.get(item_name, 'N/A')),
                                  bg=bg_color)
        self.buy_label.pack(side=tk.TOP, anchor=tk.W)
        if str(BUY_PRICES.get(item_name, 'N/A')) != 'N/A':
            button1 = tk.Button(self.label_frame, text="Buy", command=lambda: buy_command(item_name))
            button1.pack(side=tk.LEFT, expand=1)
        button2 = tk.Button(self.label_frame, text="Sell", command=lambda: sell_command(item_name))
        button2.pack(side=tk.LEFT, expand=1)
        # 因这些组件将 master 覆盖了 所以无法点击到 master 故都bind 上select_command  可以看看是否有更好的处理方式
        master.bind("<Button-1>", lambda event: select_command(item_name))
        self.label_frame.bind("<Button-1>", lambda event: select_command(item_name))
        self.label_container.bind("<Button-1>", lambda event: select_command(item_name))
        self.amount_label.bind("<Button-1>", lambda event: select_command(item_name))
        self.sell_label.bind("<Button-1>", lambda event: select_command(item_name))
        self.buy_label.bind("<Button-1>", lambda event: select_command(item_name))

    def update(self, amount: int, selected: bool = False) -> None:
        """
        """
        if amount > 0:
            color = INVENTORY_COLOUR
            if selected:
                color = INVENTORY_SELECTED_COLOUR
        else:
            color = INVENTORY_EMPTY_COLOUR
        self.amount_label.configure(bg=color)
        self.sell_label.configure(bg=color)
        self.buy_label.configure(bg=color)
        self.label_frame.configure(bg=color)
        self.label_container.configure(bg=color)
        self.amount_label.configure(text=self.item_name + ": " + str(amount))


class FarmGame(object):
    """
    """
    farm_model: FarmModel = None
    info_bar: InfoBar = None
    item_list: {str: ItemView} = {}

    def __init__(self, master: tk.Tk, map_file: str) -> None:
        """
        """
        # Set the title of the window.
        master.title("Farm Game")
        self.farm_model = FarmModel(map_file)
        # Create the main GUI window.
        # Create the title banner.
        self.cache = {}
        self.banner_image = get_image('images/header.png', size=(FARM_WIDTH + INVENTORY_WIDTH, BANNER_HEIGHT))
        banner_label = tk.Label(master, image=self.banner_image)
        banner_label.pack(side=tk.TOP)

        # Create a button to enable users to increment the day.
        button_frame = tk.Frame(master)
        button_frame.pack(side=tk.BOTTOM)
        button = tk.Button(button_frame, text='Next day', command=lambda: (
            self.farm_model.new_day(), self.info_bar.redraw(self.farm_model.get_days_elapsed(),
                                                            self.farm_model.get_player().get_money(),
                                                            self.farm_model.get_player().get_energy())))
        button.pack()

        # Create an instance.
        self.info_bar = InfoBar(master)
        self.info_bar.pack(side=tk.BOTTOM)
        self.info_bar.redraw(1, 0, 100)

        # Create a farmview.
        farm_view = FarmView(master, dimensions=self.farm_model.get_dimensions(), size=(FARM_WIDTH, FARM_WIDTH))
        farm_view.pack(side=tk.LEFT)
        farm_view.redraw(self.farm_model.get_map(), self.farm_model.get_plants(),
                         self.farm_model.get_player().get_position(),
                         self.farm_model.get_player().get_direction())

        item_list_frame = tk.Frame(master, width=INVENTORY_WIDTH, height=FARM_WIDTH)
        item_list_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        for i in range(len(ITEMS)):
            # Create the Item list.
            item_view = ItemView(item_list_frame, ITEMS[i],
                                 self.farm_model.get_player().get_inventory().get(ITEMS[i], 0),
                                 self.select_item, self.sell_item, self.buy_item)
            # item_view.update(self.farm_model.get_player().get_inventory().get(ITEMS[i], 0), False)
            item_view.pack(side=tk.TOP)
            self.item_list[ITEMS[i]] = item_view

        # Bind the handle_keypress method.
        master.bind('<KeyPress>', self.handle_keypress)
        master.mainloop()

    def redraw(self) -> None:
        """
        """
        pass

    def select_item(self, item_name: str) -> None:
        """
        """
        for item_key, item_view in self.item_list.items():
            amount = self.farm_model.get_player().get_inventory().get(item_key, 0)
            if item_name == item_key:
                item_view.update(amount, True)
            else:
                item_view.update(amount, False)

    def buy_item(self, item_name: str) -> None:
        """
        """
        buy_price = BUY_PRICES.get(item_name)
        self.farm_model.get_player().buy(item_name, buy_price)
        day = self.farm_model.get_days_elapsed()
        energy = self.farm_model.get_player().get_energy()
        money = self.farm_model.get_player().get_money()
        self.info_bar.redraw(day, money, energy)
        item_view = self.item_list[item_name]
        item_view.update(self.farm_model.get_player().get_inventory().get(item_name, 0), True)

    def sell_item(self, item_name: str) -> None:
        """
        """
        sell_price = SELL_PRICES.get(item_name)
        self.farm_model.get_player().sell(item_name, sell_price)
        day = self.farm_model.get_days_elapsed()
        energy = self.farm_model.get_player().get_energy()
        money = self.farm_model.get_player().get_money()
        self.info_bar.redraw(day, money, energy)
        item_view = self.item_list[item_name]
        item_view.update(self.farm_model.get_player().get_inventory().get(item_name, 0), True)

    def handle_keypress(self, event: tk.Event) -> None:
        """
        """
        self.farm_model.move_player(event.keysym)
        self.farm_model.get_player().set_direction(event.keysym)
        print(event)
        pass


def play_game(root: tk.Tk, map_file: str) -> None:
    """Create the window.

    Parameters:
    root:

    map_file:
    """
    game = FarmGame(root, map_file)


def main() -> None:
    """
    Create the window, ensure it displays when the program is run and set its
    title.
    """
    # Create the main GUI window.
    root = tk.Tk()
    map_file = 'maps/map1.txt'
    FarmGame(root, map_file)

    # Start the main event loop
    root.mainloop()


if __name__ == '__main__':
    main()
