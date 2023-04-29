#!/usr/bin/python3

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = '1'

import pygame

from config import config
from conway import Conway
from painter import Painter
from events import EventHandler


class Game:
    def __init__(self) -> None:
        """The Game object of the program. Entrypoint for setup functions.
        """
        pygame.init()

        self.running = True
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(config.display.window_size, pygame.RESIZABLE)

        self.conway = Conway()
        self.painter = Painter(screen=self.screen)
        self.event_handler = EventHandler(
            painter=self.painter,
            clock=self.clock,
            conway=self.conway
        )

        pygame.display.set_caption("Conway's Game of Life")
        pygame.display.set_icon(self.painter.sprites["icon"])

    def game_loop(self) -> None:
        """The game loop of the Game object. See events.py to register functions to the loop.
        """
        while self.running:
            # flip is called first to ensure quiet shutdown on quit.
            pygame.display.flip()
            self.clock.tick(config.display.framerate)
            self.event_loop()

    def event_loop(self) -> None:
        """The event loop of the Game object. The execute method of the EventHandler is called here and also redirects pygame specific events to the EventHandler.
        """
        self.event_handler.execute()
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = not self.running
                    pygame.quit()

                case pygame.KEYDOWN:
                    self.event_handler.keyboard_keydown_event(event)

                case pygame.KEYUP:
                    self.event_handler.keyboard_keyup_event(event)

                case pygame.MOUSEBUTTONDOWN:
                    self.event_handler.mouse_down_event(event)

                case pygame.MOUSEBUTTONUP:
                    self.event_handler.mouse_up_event(event)

                case pygame.MOUSEWHEEL:
                    self.event_handler.mouse_scroll_event(event)

                case pygame.MOUSEMOTION:
                    self.event_handler.mouse_motion_event(event)

                case pygame.VIDEORESIZE:
                    self.event_handler.video_resize_event(event)


if __name__ == "__main__":
    game = Game()
    game.game_loop()
