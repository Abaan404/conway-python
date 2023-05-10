import pygame

from config import config
from conway import Board
from sprite import Sprite
from typing import Iterable


class Painter:
    def __init__(self, screen: pygame.Surface) -> None:
        """The painter object to draw sprites on the screen.

        Args:
            screen (pygame.Surface): The screen surface from pygame.
        """
        self.screen = screen
        self.sprites = Sprite.render_sprites()
        self.grid_size = config.display.grid_size
        self.__font = pygame.font.Font(config.font.path, config.font.size)
        self.__scale = 1.0
        self.__cache = {}

    @property
    def scale(self) -> float:
        """Getter for the scale class variable.

        Returns:
            float: The scale of the painter.
        """
        return self.__scale

    @scale.setter
    def scale(self, value: float) -> None:
        """Setter for the scale class variable. Clamped between a maximum and minimum value from config.

        Args:
            value (float): The scale of the painter.
        """
        self.__scale = round(max(min(value, config.zoom.max), config.zoom.min), 2)
        self.__cache = {}

    def reload(self) -> None:
        """Redraws and reloads the sprites.
        """
        self.sprites = Sprite.render_sprites()
        self.__cache = {}

    def cells_debug(self, board: Board) -> None:
        """Draws every cell by looping the board rather than its cache. Also draws the neighbours of cached cells.

        Args:
            board (Board): The current board instance from the Conway class.
        """
        for position in board.alive_positions:
            for position in board.neighbours(position):
                position = [ax * self.grid_size for ax in position]
                self.__draw("cell_debug_neighbour", position)

        for position, cell in board:
            position = [ax * self.grid_size for ax in position]
            if cell.alive:
                self.__draw("cell_debug", position)

    def cells_highlight(self, positions: Iterable[tuple[int, int]]) -> None:
        """Highlights the cells from the user onto the screen.

        Args:
            positions (Iterable[tuple[int, int]]): The px positions to render the highlight at.
        """
        for position in positions:
            position = [ax // self.grid_size * self.grid_size for ax in position]
            self.__draw("cell_highlighted", position)

    def cells_alive(self, board: Board) -> None:
        """Draws evey cell present in the board's position cache onto the screen.

        Args:
            board (Board): The current board instance from the Conway class.
        """
        for position in board.alive_positions:
            position = [ax * self.grid_size for ax in position]
            self.__draw("cell", position)

    def background(self) -> None:
        """Renders the background of the game. Also draws a void behind the background (which can be commented out for a cool effect).
        """
        self.screen.fill(pygame.Color(config.sprite.background.void))
        self.__draw("background", (0, 0))

    def label(self, *labels: str, position: tuple[int, int], colour: str = config.font.colour) -> None:
        """Renders labels onto the screen. If multiple lables, A multiline left-justified label is drawn.

        Args:
            labels (str): labels to render.
            position (tuple[int, int]): The px position to render the label(s) at.
            colour (str, optional): Colour of the label. Defaults to config.font.colour.
        """
        for (offset, label) in enumerate(labels):
            self.screen.blit(self.__font.render(label, True, colour), (position[0], position[1] + self.__font.get_height() * offset))

    def __draw(self, identifier: str, position: tuple[int, int]) -> None:
        """Internal renderer/drawer function to blit sprites onto the screen. Also handles scaling and caching of each surface.

        Args:
            identifier (str): Unique string identifer of the sprite.
            position (tuple[int, int]): The px position to render the surface at.
        """
        if not (surface := self.__cache.get(identifier)):
            surface = self.sprites[identifier]
            # transform the width and height of the surface
            surface = pygame.transform.scale(surface, (surface.get_width() * self.scale, surface.get_height() * self.scale))
            self.__cache[identifier] = surface

        anchor = pygame.mouse.get_pos()
        # translate the position by scaling the distance from the surface to the anchor's position, then adding the anchor's position back
        position = [(ax - anch) * self.scale + anch for ax, anch in zip(position, anchor)]

        self.screen.blit(surface, position)
