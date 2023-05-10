import pygame

from types import SimpleNamespace


class ConfigNamespace(SimpleNamespace):
    def __init__(self, config: dict, **kwargs):
        """Translates the config dict to dot-notation using a namespace.

        Args:
            config (dict): The config as a dict.
        """
        super().__init__(**kwargs)
        for key, value in config.items():
            if isinstance(value, dict):
                self.__setattr__(key, ConfigNamespace(value))
            else:
                self.__setattr__(key, value)


config = ConfigNamespace({
    "display": {
        # tuple[int, int]: The window size on launch.
        "window_size": (1282, 722),
        # int: The px grid width of each cell.
        "grid_size": 5,
        # False | int: The framerate at which to run the game at.
        "framerate": False
    },
    "zoom": {
        # float: Controls for the scale levels in zoom. Rounded to 2 decimal places.
        "max": 2.0,
        "min": 0.5,
        "step": 0.1
    },
    "sprite": {
        # str: Config for sprites rendered on screen ("#RGBA" or "#RGB").
        "background": {
            "colour": "#5B6FA4FF",
            "line_colour": "#5B94A4FF",
            "void": "#000000"
        },
        "cell": {
            "colour": "#5BA490FF",
            "highlighted_colour": "#5BA490AA",
            "debug_neighbour_colour": "#FF0000",
            "debug_colour": "#00FF00"
        },
        "icon": {
            "colours": ["#FF0000", "#00FF00", "#0000FF"],
            "squares": 4
        }
    },
    "font": {
        # str: Path to a font (.ttf).
        "path": "./fonts/JetBrainsMono-Bold.ttf",
        # str: Default colour of the font ("#RGBA" or "#RGB").
        "colour": "#FFFFFF",
        # int: the font size
        "size": 18
    },
    "keybinds": {
        # Keybinds to interact with the game, see: https://www.pygame.org/docs/ref/key.html for an exhaustive list.
        "highlight_up": pygame.K_w,
        "highlight_down": pygame.K_s,
        "highlight_left": pygame.K_a,
        "highlight_right": pygame.K_d,
        "toggle": pygame.K_RETURN,

        "pause": pygame.K_r,
        "step": pygame.K_e,
        "reset": pygame.K_q,

        "cycle_next": pygame.K_RIGHT,
        "cycle_prev": pygame.K_LEFT,

        "debug": pygame.K_F3
    },
    "event": {
        # float: values to control the delay between held events.
        "grace_seconds": 0.25,
        "step_seconds": 0.1
    },
    "patterns": {
        # str: Path to the user pattern directory.
        "folder": "./patterns"
    }
})
