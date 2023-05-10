import pygame

from config import config
from conway import Conway, Board
from painter import Painter
from file import FileHandler
from typing import Callable


class Event:
    def __init__(self) -> None:
        """The event object to interface with the EventHandler class.
        """
        self.registered = {}
        self.storage = {}

    def register(self, identifier: str, func: Callable, *args) -> None:
        """Register a callable object into the event handler.

        Args:
            identifier (str): The unique string identifier of the event.
            func (Callable): The callable object.
            args (tuple, optional): arguments to be passed as func(*args), can be callable.
        """
        self.registered[identifier] = (func, args)

    def release(self, identifier: str, persist: bool = False) -> None:
        """Release the callable object from the event handler.

        Args:
            identifier (str): The unique string identifier of the event.
            persist (bool, optional): Should the object retain its storage. Defaults to False.
        """
        if not persist:
            self.storage.pop(identifier, None)
        self.registered.pop(identifier, None)

    def toggle(self, identifier: str, func: Callable, *args) -> None:
        """Toggle the callable object from the event handler.

        Args:
            identifier (str): The unique string identifier of the event.
            func (Callable): The function to be registered.
            args (tuple, optional): arguments to be passed as func(*args), can be callable.
        """
        if self.registered.get(identifier):
            self.release(identifier)
        else:
            self.register(identifier, func, *args)

    def __getitem__(self, identifier: str) -> dict:
        """Fetch an event's storage.

        Args:
            identifier (str): The unique string identifier of the event.

        Returns:
            dict: The storage of the event.
        """
        return self.storage.get(identifier)

    def __delitem__(self, identifier: str) -> None:
        """Remove an event's storage.

        Args:
            identifier (str): The unique string identifier of the event.
        """
        self.storage.pop(identifier, None)

    def __setitem__(self, identifier: str, value: dict) -> None:
        """Update an event's storage.

        Args:
            identifier (str): The unique string identifier of the event.
            value (dict): The value to be updated into the event's storage.
        """
        try:
            self.storage[identifier].update(value)
        except KeyError:
            self.storage[identifier] = value


class EventHandler:
    def __init__(self, painter: Painter, clock: pygame.time.Clock, conway: Conway) -> None:
        """Initialize the game's event handler. Can be used as a setup to register events.

        Args:
            painter (Painter): The painter object of the game.
            clock (pygame.time.Clock): The pygame clock handler.
            conway (Conway): The gameplay object (Conway).
        """
        self.painter = painter
        self.clock = clock
        self.conway = conway
        self.file_handler = FileHandler()
        self.keybinds = config.keybinds

        self.event = Event()

        self.event.register("background", self.painter.background)
        self.event.register("highlight", self.painter.cells_highlight, lambda: self.file_handler.offset_px_position(*pygame.mouse.get_pos(), self.conway.board.grid_size))
        self.event.register("board", self.painter.cells_alive, lambda: self.conway.board)
        self.event.register("info", self.__info)

    def execute(self) -> None:
        """The event executor of the EventHandler that calls all registered events each frame.
        """
        for func, args in self.event.registered.values():
            if args:
                func(*(arg() if callable(arg) else arg for arg in args)) # handle callable args
            else:
                func()

    def video_resize_event(self, event: pygame.event) -> None:
        """The handler for pygame.VIDEORESIZE event.

        Args:
            event (pygame.event): the pygame event object.
        """
        config.display.window_size = (event.w, event.h)
        self.painter.reload()
        self.conway.board.resize()

    def mouse_down_event(self, event: pygame.event) -> None:
        """The handler for pygame.MOUSEBUTTONDOWN event.

        Args:
            event (pygame.event): the pygame event object.
        """
        if event.button == pygame.BUTTON_LEFT:
            self.__apply_grace("draw", self.__toggle_cell_event, step_seconds=-1)

    def mouse_up_event(self, event: pygame.event) -> None:
        """The handler for pygame.MOUSEBUTTONUP event.

        Args:
            event (pygame.event): the pygame event object.
        """
        if event.button == pygame.BUTTON_LEFT:
            self.event.release("draw")

    def mouse_scroll_event(self, event: pygame.event) -> None:
        """The handler for pygame.MOUSEWHEEL event.

        Args:
            event (pygame.event): the pygame event object.
        """
        if event.y > 0:
            self.painter.scale += config.zoom.step
        elif event.y < 0:
            self.painter.scale -= config.zoom.step

    def mouse_motion_event(self, event: pygame.event) -> None:
        """The handler for pygame.MOUSEMOTION event.

        Args:
            event (pygame.event): the pygame event object.
        """
        self.event["highlight"] = {"position": event.pos}

    def keyboard_keydown_event(self, event: pygame.event) -> None:
        """The handler for pygame.KEYDOWN event.

        Args:
            event (pygame.event): the pygame event object.
        """
        if event.key == self.keybinds.debug:
            # toggle between info and debug events
            if self.event.registered.get("info"):
                self.event.release("info")
                self.event.register("debug", self.__debug)
            else:
                self.event.release("debug")
                self.event.register("info", self.__info)

        elif event.key == self.keybinds.pause:
            self.event.toggle("game", self.conway.update)

        elif event.key == self.keybinds.reset:
            self.conway.board = Board()
            self.conway.generation = 0

        elif event.key == self.keybinds.step:
            self.__apply_grace("step_grace", self.conway.update)

        elif event.key == self.keybinds.highlight_up:
            self.__apply_grace("highlight_grace", self.__highlight_keyboard_event, lambda position: (position[0], position[1] - self.conway.board.grid_size))

        elif event.key == self.keybinds.highlight_down:
            self.__apply_grace("highlight_grace", self.__highlight_keyboard_event, lambda position: (position[0], position[1] + self.conway.board.grid_size))

        elif event.key == self.keybinds.highlight_left:
            self.__apply_grace("highlight_grace", self.__highlight_keyboard_event, lambda position: (position[0] - self.conway.board.grid_size, position[1]))

        elif event.key == self.keybinds.highlight_right:
            self.__apply_grace("highlight_grace", self.__highlight_keyboard_event, lambda position: (position[0] + self.conway.board.grid_size, position[1]))

        elif event.key == self.keybinds.toggle:
            self.__toggle_cell_event()

        elif event.key == self.keybinds.cycle_next:
            self.file_handler.rotate(+1)

        elif event.key == self.keybinds.cycle_prev:
            self.file_handler.rotate(-1)

    def keyboard_keyup_event(self, event: pygame.event) -> None:
        """The handler for pygame.KEYUP event.

        Args:
            event (pygame.event): the pygame event object.
        """
        if event.key == self.keybinds.step:
            self.event.release("step_grace")

        if event.key in [self.keybinds.highlight_up, self.keybinds.highlight_down, self.keybinds.highlight_left, self.keybinds.highlight_right]:
            self.event.release("highlight_grace")
            self.__highlight_keyboard_event(lambda position: position)  # reset highlight to mouse, position remains unchanged

    def __apply_grace(self, identifier: str, event: Callable, *args, grace_seconds: float = config.event.grace_seconds, step_seconds: float = config.event.step_seconds) -> None:
        """Internal helper function to provide grace to held events.

        Args:
            identifier (str): The unique string identifier of the event.
            event (Callable): The callable object to wrap grace onto.
            grace_seconds (int, optional): How many seconds to wait before the event is called every gametick. Defaults to config.event.grace_seconds (-1 for None).
            step_seconds (int, optional): How many seconds between each gametick to call the event. Defaults to config.event.step_seconds (-1 for None).
        """
        def grace_event(args):  # grace event wrapper
            grace = self.event[identifier]["grace"]
            step = self.event[identifier]["step"]
            if grace < 0:
                if step < 0:
                    event(*args)
                    self.event[identifier] = {"step": self.clock.get_fps() * step_seconds}
                    return
                self.event[identifier] = {"step": step - 1}
                return
            self.event[identifier] = {"grace": grace - 1}

        event(*args)
        self.event[identifier] = {
            "grace": self.clock.get_fps() * grace_seconds,
            "step": self.clock.get_fps() * step_seconds
        }
        self.event.register(identifier, grace_event, args)

    def __highlight_keyboard_event(self, move: Callable[[tuple[int, int]], tuple[int, int]]) -> None:
        """Internal helper function to allow arbitrary cell highlight movement through translation.

        Args:
            move (Callable[[tuple[int, int]], tuple[int, int]]): A callable object that dictates by how much current highlighted cell must move.
        """
        position = move(self.event["highlight"]["position"] if self.event["highlight"] else pygame.mouse.get_pos())
        self.event["highlight"] = {"position": position}

        if not self.event["highlight_grace"]:  # setup condition
            self.event.register("highlight", self.painter.cells_highlight, lambda: self.file_handler.offset_px_position(*self.event["highlight"]["position"], self.conway.board.grid_size))

    def __toggle_cell_event(self) -> None:
        """Internal helper function to interface with the internal Conway.Board.toggle function on user input.
        """
        if data := self.event["highlight"]:
            x, y = data["position"]
        else:
            x, y = pygame.mouse.get_pos()


        # scale px position to board indices
        x, y = x // self.conway.board.grid_size, y // self.conway.board.grid_size
        # offset indices for selected file before toggle
        positions = ((i+x, j+y) for i, j in self.file_handler.parse_position())
        self.conway.board.toggle(positions)

    def __debug(self) -> None:
        """Internal helper function to draw debug sprites onto the screen and display additional game info using labels.
        """
        # before the screen is initialized
        if (fps := self.clock.get_fps()) == 0:
            return
        self.painter.cells_debug(self.conway.board)
        self.painter.label(
            f"FPS   | {fps:.0f} ({1000/fps:.2f}ms)",
            f"Alive | {len(self.conway.board.alive_positions)} (Gen #{self.conway.generation})",
            f"File  | {self.file_handler.selected}",
            f"Grid  | {self.conway.board.shape[0]} x {self.conway.board.shape[1]}",
            *(f'{identifier} -> {self.event.storage.get(identifier, {})}' for identifier in self.event.registered.keys()),
            position=(10, 10)
        )

    def __info(self) -> None:
        """Internal helper function to display useful game info using labels.
        """
        # before the screen is initialized
        if (fps := self.clock.get_fps()) == 0:
            return
        self.painter.label(
            f"FPS   | {fps:.0f} ({1000/fps:.2f}ms)",
            f"Alive | {len(self.conway.board.alive_positions)} (Gen #{self.conway.generation})",
            f"File  | {self.file_handler.selected}",
            f" >>> {'Running' if self.event.registered.get('game') else 'Paused'}",
            position=(10, 10)
        )
