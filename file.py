import os
import collections

from config import config
from typing import Generator


class FileHandler:
    def __init__(self) -> None:
        """The FileHandler class to interface with patterns loaded in the user's directory. Initial setup will create a path as defined by the config.
        """

        if not os.path.exists(config.patterns.folder):
            os.mkdir(config.patterns.folder)

        if "singular.cells" not in os.listdir(config.patterns.folder):
            with open("./patterns/singular.cells", "w") as f:
                f.write("! singular.cell\nO")

        self.selected = "singular.cells"
        self.__files = collections.deque((filename for filename in os.listdir(config.patterns.folder) if filename.endswith(".cells") or filename.endswith(".rle")))
        self.__cache = {}

    def rotate(self, direction: int) -> None:
        """Rotates between selected files.

        Args:
            direction (int): +1 for next file, -1 for previous file.
        """
        self.__files.rotate(direction)
        self.selected = self.__files[0]

    def __decode_rle(self) -> Generator[tuple[int, int], None, None]:
        """Decode a Life file encoded using RLE. Spec provided by https://conwaylife.com/wiki/Run_Length_Encoded.

        Yields:
            Generator[tuple[int, int]]: The positions at which the pattern is be created at.
        """
        with open(f'{config.patterns.folder}/{self.selected}') as f:
            stream = list(filter(lambda line: not line.startswith("#"), f.readlines()))
            meta = stream.pop(0).split(", ")
            # potential for load efficiency using width and height. TODO (perhaps unnecessary since positions are cached on load)
            width, height, rule = int(meta[0][4:]), int(meta[1][4:]), str(meta[2][7:-1])
            stream = ''.join(stream).replace('\n', "")

        # ensure Life file is of the correct format
        if rule.lower() != "b3/s23":
            yield ()

        i, j = 0, 0
        run_count = "0"
        for char in stream:
            if char.isdigit():
                run_count += char

            elif char.isalpha():
                if char == "o":
                    for run in range(0, max(int(run_count), 1)):
                        yield i + run, j
                i += max(int(run_count), 1)
                run_count = "0"

            else:
                j += max(int(run_count), 1)
                i = 0
                run_count = "0"

    def __decode_cells(self) -> Generator[tuple[int, int], None, None]:
        """Decode a Life file encoded using plaintext. Spec provided by https://conwaylife.com/wiki/Plaintext.

        Yields:
            Generator[tuple[int, int]]: The positions at which the pattern is be created at.
        """
        with open(f'{config.patterns.folder}/{self.selected}') as f:
            lines = filter(lambda line: not line.startswith("!"), f.readlines())
        for j, line in enumerate(lines):
            for i, char in enumerate(line):
                if char == "O":
                    yield i, j

    def parse_position(self) -> list[tuple[int, int]]:
        """Parses the Life files and returns the positions at which the pattern is be created at.

        Returns:
            list[tuple[int, int]]: A list of positions where the cells are alive.
        """

        if positions := self.__cache.get(self.selected, []): # if already cached
            return positions

        if self.selected.endswith(".cells"):
            pattern = list(self.__decode_cells())

        elif self.selected.endswith(".rle"):
            pattern = list(self.__decode_rle())

        self.__cache[self.selected] = pattern
        return positions

    def offset_px_position(self, offset_x: int, offset_y: int, grid_size: int) -> Generator[tuple[int, int], None, None]:
        """A helper function to translate position indices of selected files to px coordinates with appropriate offsets applied to them.

        Args:
            offset_x (int): px offset on the x-axis.
            offset_y (int): px offset on the y-axis.
            grid_size (int): the grid size of the rendered screen.

        Yields:
            Generator[tuple[int, int]]: the px coordinates of the alive cells to be drawn.
        """
        positions = self.parse_position()
        for i, j in positions:
            yield offset_x + grid_size * i, offset_y + grid_size * j
