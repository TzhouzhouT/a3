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
            size=(FARM_WIDTH + INVENTORY_WIDTH, INFO_BAR_HEIGHT))

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
        super().__init__(
            master,
            dimensions=dimensions,
            size=(FARM_WIDTH, FARM_WIDTH)
        )
        self.cache = {}
        for values in IMAGES.values():
            picture_path = f"images/{values}"
            get_image(picture_path, self.get_cell_size(), self.cache)

    def redraw(self, ground: list[str], plants: dict[tuple[int, int], 'Plant'],
               player_position: tuple[int, int], player_direction: str) -> None:
        """
        """
        self.clear()
        # Draw the ground.
        for i, row in enumerate(ground):
            for j, col in enumerate(row):
                image_path = ''
                if col == 'S':
                    image_path = 'images/soil.png'
                elif col == "U":
                    image_path = 'images/untilled_soil.png'
                elif col == "G":
                    image_path = 'images/grass.png'
                image = get_image(image_path, self.get_cell_size(), self.cache)
                midpoint = self.get_midpoint((i, j))
                self.create_image(midpoint, image=image)
                # Draw the plants.
        for key, value in plants.items():
            midpoint = self.get_midpoint(key)
            plant_image_name = f'images/' + get_plant_image_name(value)
            plant = get_image(plant_image_name, self.get_cell_size(), self.cache)
            self.create_image(midpoint, image=plant)
        # Draw the player.
        player_image_path = f"images/player_{player_direction}.png"
        player_image = get_image(player_image_path, self.get_cell_size(), self.cache)
        midpoint = self.get_midpoint(player_position)
        self.create_image(midpoint, image=player_image)


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
        # Determine the background colour
        if amount > 0:
            bg_colour = INVENTORY_COLOUR
        else:
            bg_colour = INVENTORY_EMPTY_COLOUR
        # Build a label frame.
        self.configure(bg=bg_colour, highlightbackground=INVENTORY_OUTLINE_COLOUR, highlightthickness=0.5)
        self.label_container = tk.Frame(self, bg=bg_colour, highlightbackground=INVENTORY_OUTLINE_COLOUR)
        self.label_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.amount_label = tk.Label(self.label_container, text=item_name + ": " + str(amount), bg=bg_colour,
                                     highlightbackground=INVENTORY_OUTLINE_COLOUR)
        self.amount_label.pack(side=tk.TOP)
        self.label2 = tk.Label(self.label_container, text="Sell price: $" + str(SELL_PRICES[item_name]), bg=bg_colour,
                               highlightbackground=INVENTORY_OUTLINE_COLOUR)
        self.label2.pack(side=tk.TOP)
        self.label3 = tk.Label(self.label_container, text="Buy price: $" + str(BUY_PRICES.get(item_name, 'N/A')),
                               bg=bg_colour, highlightbackground=INVENTORY_OUTLINE_COLOUR)
        self.label3.pack(side=tk.TOP)
        if str(BUY_PRICES.get(item_name, 'N/A')) != 'N/A':
            button1 = tk.Button(self, text="Buy", command=lambda: buy_command(item_name), bg="white")
            button1.pack(side=tk.LEFT, expand=1)
        button2 = tk.Button(self, text="Sell", command=lambda: sell_command(item_name), bg="white")
        button2.pack(side=tk.LEFT, expand=1)
        # Bind.
        self.bind("<Button-1>", lambda event: select_command(item_name))
        self.label_container.bind("<Button-1>", lambda event: select_command(item_name))
        self.amount_label.bind("<Button-1>", lambda event: select_command(item_name))
        self.label2.bind("<Button-1>", lambda event: select_command(item_name))
        self.label3.bind("<Button-1>", lambda event: select_command(item_name))

    def update(self, amount: int, selected: bool = False) -> None:
        """
        """
        if amount > 0:
            colour = INVENTORY_COLOUR
            if selected:
                colour = INVENTORY_SELECTED_COLOUR
        else:
            colour = INVENTORY_EMPTY_COLOUR
        self.configure(bg=colour, highlightbackground=INVENTORY_OUTLINE_COLOUR)
        self.label2.configure(bg=colour, highlightbackground=INVENTORY_OUTLINE_COLOUR)
        self.label_container.configure(bg=colour, highlightbackground=INVENTORY_OUTLINE_COLOUR)
        self.label3.configure(bg=colour, highlightbackground=INVENTORY_OUTLINE_COLOUR)
        self.amount_label.configure(text=self.item_name + ": " + str(amount), bg=colour,
                                    highlightbackground=INVENTORY_OUTLINE_COLOUR)


class FarmGame(object):
    """
    """
    def __init__(self, master: tk.Tk, map_file: str) -> None:
        """
        """
        # Set the title of the window.
        self.item_list = {}
        master.title("Farm Game")
        self.farm_model = FarmModel(map_file)
        # Create the main GUI window.
        # Create the title banner.
        self.banner_image = get_image('images/header.png', size=(FARM_WIDTH + INVENTORY_WIDTH, BANNER_HEIGHT))
        banner_label = tk.Label(master, image=self.banner_image)
        banner_label.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        # Create a button to enable users to increment the day.
        button_frame = tk.Frame(master)
        button_frame.pack(side=tk.BOTTOM)
        button = tk.Button(button_frame, text='Next day', command=lambda: (
            self.farm_model.new_day(), self.redraw()))
        button.pack()

        # Create an instance.
        self.info_bar = InfoBar(master)
        self.info_bar.pack(side=tk.BOTTOM)
        # self.info_bar.redraw(1, 0, 100)

        # Create a farm_view.
        self.farm_view = FarmView(master, dimensions=self.farm_model.get_dimensions(), size=(FARM_WIDTH, FARM_WIDTH))
        self.farm_view.pack(side=tk.LEFT)

        item_list_frame = tk.Frame(master, width=INVENTORY_WIDTH, height=FARM_WIDTH)
        item_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        for i in range(len(ITEMS)):
            # Create the Item list.
            item_view = ItemView(item_list_frame, ITEMS[i],
                                 self.farm_model.get_player().get_inventory().get(ITEMS[i], 0),
                                 self.select_item, self.sell_item, self.buy_item)
            item_view.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
            self.item_list[ITEMS[i]] = item_view

        # Bind the handle_keypress method.
        master.bind('<KeyPress>', self.handle_keypress)
        # Call the redraw method to ensure the view draws according to the current model state.
        self.redraw()

    def redraw(self) -> None:
        """
        """
        self.info_bar.redraw(
            day=self.farm_model.get_days_elapsed(),
            money=self.farm_model.get_player().get_money(),
            energy=self.farm_model.get_player().get_energy()
        )
        self.farm_view.redraw(
            self.farm_model.get_map(), self.farm_model.get_plants(),
            self.farm_model.get_player().get_position(),
            self.farm_model.get_player().get_direction()
        )

    def handle_keypress(self, event: tk.Event) -> None:
        """
        """
        keypress = event.char
        selected_item = self.farm_model.get_player().get_selected_item()
        player_position = self.farm_model.get_player_position()
        ground = self.farm_model.get_map()[player_position[0]][player_position[1]]
        # Player attempts to move.
        if keypress == UP or keypress == DOWN or keypress == LEFT or keypress == RIGHT:
            self.farm_model.move_player(keypress)
        # Attempt to plant the seed at the player's current position.
        # If the position does not contain soil, a plant already exists in that spot,
        # or a seed is not currently selected, do nothing
        elif keypress == 'p':
            if selected_item is not None and selected_item in SEEDS:
                item_view = self.item_list[selected_item]
                seed_inv = self.farm_model.get_player().get_inventory().get(selected_item, 0)
                if ground == SOIL and seed_inv > 0:
                    if selected_item == 'Potato Seed':
                        plant = PotatoPlant()
                    elif selected_item == 'Kale Seed':
                        plant = KalePlant()
                    elif selected_item == 'Berry Seed':
                        plant = BerryPlant()
                    else:
                        return
                    if self.farm_model.add_plant(player_position, plant):
                        self.farm_model.get_player().remove_item((selected_item, 1))
                        item_view.update(self.farm_model.get_player().get_inventory().get(selected_item, 0), True)
        # Attempt to harvest the plant from the player's current position.
        # If no plant exists at the player’s current location, or the plant is not ready for harvest, do nothing.
        # If the harvest is successful, add the harvested item/s to the player’s inventory,
        # and if the plant should be removed on harvest, remove the plant from the farm.
        elif keypress == 'h':
            target_plant = self.farm_model.get_plants().get(player_position)
            if target_plant is not None and target_plant.can_harvest():
                # plant3 = self.plant.get(player_position)
                harvest_result = self.farm_model.harvest_plant(player_position)
                if harvest_result is not None:
                    self.farm_model.get_player().add_item(harvest_result)
                    item_name = harvest_result[0]
                    item_view = self.item_list[item_name]
                    item_view.update(self.farm_model.get_player().get_inventory().get(item_name, 0), False)
        # Attempt to remove the plant from the player's current position
        elif keypress == 'r':
            self.farm_model.remove_plant(player_position)
        # Attempt to till the soil from the player’s current position.
        elif keypress == 't':
            # ground = self.farm_model.get_map()[player_position[0]][player_position[1]]
            if ground == UNTILLED:
                self.farm_model.till_soil(player_position)
        # Attempt to untill the soil from the player’s current position.
        elif keypress == 'u':
            plants = self.farm_model.get_plants()
            if plants.get(player_position) is None or ground == 'SOIL':
                self.farm_model.untill_soil(player_position)
        if keypress in ['w', 'a', 's', 'd', 'p', 'h', 'r', 't', 'u']:
            self.redraw()

    def select_item(self, item_name: str) -> None:
        """
        """
        for item_key, item_view in self.item_list.items():
            amount = self.farm_model.get_player().get_inventory().get(item_key, 0)
            if item_name == item_key:
                item_view.update(amount, True)
                if amount > 0:
                    self.farm_model.get_player().select_item(item_name)
                else:
                    self.farm_model.get_player()._selected_item = None
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


def play_game(root: tk.Tk, map_file: str) -> None:
    """Create the window.

    Parameters:
    root:

    map_file:
    """
    game = FarmGame(root, map_file)
    # Start the main event loop
    root.mainloop()


def main() -> None:
    """
    Create the window, ensure it displays when the program is run and set its
    title.
    """
    # Create the main GUI window.
    root = tk.Tk()
    map_file = 'maps/map2.txt'
    play_game(root, map_file)


if __name__ == '__main__':
    main()
