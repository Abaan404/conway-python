import random
import pygame

from PIL import Image, ImageDraw
from config import config

# assets folder? gimp or photoshop? whats that?

class Sprite:
    def __init__(self, size: tuple[int, int], fill: str = "#FFFFFF") -> None:
        """The base sprite class.

        Args:
            size (tuple[int, int]): The px size of the sprite.
            fill (str, optional): The colour to fill the sprite with.. Defaults to "#FFFFFF".
        """

        self.image = Image.new(mode="RGBA", size=size, color=fill)
        self.draw = ImageDraw.Draw(self.image)

    def render(self) -> pygame.Surface:
        """Renders the sprite as a pygame.Surface object.

        Returns:
            pygame.Surface: The pygame.Surface object of the drawn sprite.
        """
        return pygame.image.fromstring(self.image.tobytes(), self.image.size, self.image.mode).convert_alpha()

    @staticmethod
    def render_sprites() -> dict[str, pygame.Surface]:
        """Returns a dict mapping the sprites to a unique string identifier for each sprite.

        Returns:
            dict[str, pygame.Surface]: The rendered sprites each mapped to a unique identifier.
        """
        return {
            "background": Background(
                size=config.display.window_size,
                bg_fill=config.sprite.background.colour,
                lin_fill=config.sprite.background.line_colour,
                grid_size=config.display.grid_size).render(),
            "cell": Cell(
                length=config.display.grid_size,
                cell_fill=config.sprite.cell.colour).render(),
            "cell_highlighted": Cell(
                length=config.display.grid_size,
                cell_fill=config.sprite.cell.highlighted_colour).render(),
            "cell_debug": Cell(
                length=config.display.grid_size,
                cell_fill=config.sprite.cell.debug_colour).render(),
            "cell_debug_neighbour": Cell(
                length=config.display.grid_size,
                cell_fill=config.sprite.cell.debug_neighbour_colour).render(),
            "icon": Icon(
                width=256, # maximum allowed width for icons by Win32 apps.
                sq_fill=config.sprite.icon.colours,
                squares=config.sprite.icon.squares).render()
        }


class Background(Sprite):
    def __init__(self, size: tuple[int, int], bg_fill: str, lin_fill: str, grid_size: int) -> None:
        """The background sprite for the game. Draws an image with square grids.

        Args:
            size (tuple[int, int]): The px size of the background sprite.
            bg_fill (str): The fill colour of the sprite.
            lin_fill (str): The gridline fill colour of the sprite.
            grid_size (int): The grid size of the background sprite.
        """
        super().__init__(size=size, fill=bg_fill)
        self.lin_fill = lin_fill

        for i in range(0, self.image.width, grid_size):
            self.__draw_line(i, "vertical")
        for j in range(0, self.image.height, grid_size):
            self.__draw_line(j, "horizontal")

    def __draw_line(self, offset: int, orientation: str) -> None:
        """helper function to draw a line onto the background.

        Args:
            offset (int): px offset for the line from origin.
            orientation (str): if the line should be vertical or horizontal.
        """
        if orientation == "horizontal":
            x, y = 0, offset
            x_end, y_end = self.image.width, offset
        elif orientation == "vertical":
            x, y = offset, 0
            x_end, y_end = offset, self.image.height

        line = ((x, y), (x_end, y_end))
        self.draw.line(line, width=1, fill=self.lin_fill)


class Cell(Sprite):
    def __init__(self, length: int, cell_fill: str) -> None:
        """The cell sprite for the game. Draws a square image.

        Args:
            length (int): The px length of the square
            cell_fill (str): The fill colour of the sprite.
        """
        super().__init__(size=(length, length), fill=cell_fill)


class Icon(Sprite):
    def __init__(self, width: tuple[int, int], sq_fill: list[str], squares: int) -> None:
        """The icon sprite for the game. Draws an icon for the game.

        Args:
            width (tuple[int, int]): The px width of the icon.
            sq_fill (list[str]): A list of randomly selected fill colour for each drawn square.
            squares (int): The length of the number of squares to be drawn.
        """
        super().__init__((width, width), fill="#00000000")
        padding = width // (squares * 4)
        sq_width = (width - padding * (squares + 1)) // squares

        for i in range(padding, width - padding, sq_width + padding):
            for j in range(padding, width - padding, sq_width + padding):
                self.draw.rounded_rectangle(xy=(i, j, i + sq_width, j + sq_width), radius=sq_width * 0.3, fill=random.choice(sq_fill))
