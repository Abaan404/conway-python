import numpy as np

from config import config
from typing import Generator, Iterable


class Cell:
    def __init__(self) -> None:
        """An object to represent a cell.
        """
        self.updated = False
        self.alive = False

    def __repr__(self) -> str:
        """Dunder method to represent the cell object.

        Returns:
            str: The representation of the cell object.
        """
        return f'conway.Cell alive={self.alive} updated={self.updated}'


class Board:
    def __init__(self) -> None:
        """An object to represent and interact with a board.
        """
        self.grid_size = config.display.grid_size
        self.shape = tuple(ax // self.grid_size for ax in config.display.window_size)
        self.alive_positions = set()

        # bypass creating references
        self._board = np.empty(shape=self.shape, dtype=object)
        for position in np.ndindex(self.shape):
            self._board[position] = Cell()

    def toggle(self, positions: Iterable[tuple[int, int]]) -> None:
        """Toggles the alive state of the cell on the board.

        Args:
            positions (Iterable[tuple[int, int]]): The positions at which to toggle each cell.
        """
        positions = self.validate_position(positions)
        for position in positions:
            alive = self[position].alive = not self[position].alive
            if alive:
                self.alive_positions.add(position)
            else:
                self.alive_positions.remove(position)

    def __iter__(self) -> Generator[tuple[tuple[int, int], Cell], None, None]:
        """Dunder method to enumerate the board class variable.

        Yields:
            Generator[tuple[tuple[int, int], Cell], None, None]: The position and its respective cell on the board.
        """
        for position in np.ndindex(self._board.shape):
            yield position, self._board[position]

    def __getitem__(self, position: tuple[int, int]) -> Cell:
        """Dunder method to fetch the cell at the position.

        Args:
            position (tuple[int, int]): Position of the cell.

        Returns:
            Cell: The cell at the specified position.
        """
        return self._board[position]

    def __setitem__(self, position: tuple[int, int], value: bool) -> None:
        """Dunder method to set the value and update cache at the position.

        Args:
            position (tuple[int, int]): Position of the cell.
            value (Cell): The cell object to set at position.
        """
        self._board[position].alive = value
        self._board[position].updated = False

    def validate_position(self, positions: Iterable[tuple[int, int]]) -> Generator[tuple[int, int], None, None]:
        """Validates the position (or Out-of-Bounds check) for each position passed to the method.

        Args:
            positions (Iterable[tuple[int, int]]): An iterable of all positions to be checked.

        Yields:
            Generator[tuple[int, int], None, None]: The filtered positions from the iterable.
        """
        for position in positions:
            i, j = position
            if not (i >= self.shape[0] or j >= self.shape[1] or i < 0 or j < 0):
                yield position

    def neighbours(self, position: tuple[int, int]) -> dict[tuple[int, int], Cell]:
        """Fetch the position and values in a 3x3 grid surrounding the cell on the board.

        Args:
            position (tuple[int, int]): The position of the cell.

        Returns:
            dict[tuple[int, int], Cell]: The dictionary mapping each cells position to its value.
        """
        i, j = position
        offsets = ((i-1, j+1), (i, j+1), (i+1, j+1),
                   (i-1, j),   (i, j),   (i+1, j),
                   (i-1, j-1), (i, j-1), (i+1, j-1))

        offsets = self.validate_position(offsets)
        return {offset: self[offset] for offset in offsets}

    def count_neighbours(self, position: tuple[int, int]) -> int:
        """Counts the alive neighbours around the cells.

        Args:
            position (tuple[int, int]): Position of the cell.

        Returns:
            int: The number of alive neighbours around the cell.
        """
        neighbours = (cell.alive for cell in self.neighbours(position).values())
        if self._board[position].alive:
            return sum(neighbours) - 1
        return sum(neighbours)

    def resize(self) -> None:
        """Resize the board and update class variables accordingly.
        """
        self.shape = tuple(ax // self.grid_size for ax in config.display.window_size)
        self._board = np.empty(shape=self.shape, dtype=object)
        for position in self.validate_position(np.ndindex(self.shape)):
            self._board[position] = Cell()
        for position in self.validate_position(self.alive_positions):
            self._board[position].alive = True

class Conway:
    def __init__(self) -> None:
        """The gameplay representation of the Conways Game of Life.
        """
        self.board = Board()
        self.generation = 0

    def __read_cache(self) -> Generator[tuple[tuple[int, int], Cell], None, None]:
        """Read values of only alive cells cached from the board. Also sets the cell's updated state to True.

        Yields:
            Generator[tuple[tuple[int, int], Cell], None, None]: The position and cell to be read.
        """
        for position in self.board.alive_positions:
            for position, cell in self.board.neighbours(position).items():
                if not cell.updated:
                    cell.updated = True
                    yield position, cell

    def update(self) -> None:
        """Update the board according to the rules of Conway's Game of Life (See: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)
        """
        self.generation += 1
        alive = set()
        dead = set()

        for position, cell in self.__read_cache():
            count = self.board.count_neighbours(position)
            if (cell.alive and count in {2, 3}) or (count == 3): # See: rules in README.md
                alive.add(position)
            else:
                dead.add(position)

        for position in alive:
            self.board[position] = True
        for position in dead:
            self.board[position] = False
        self.board.alive_positions = alive
