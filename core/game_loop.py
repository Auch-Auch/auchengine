from typing import Protocol, Callable
from collections import defaultdict
import pygame
from pygame.locals import *


class BaseGameLoop(Protocol):

    def register_display_function(self, func: Callable) -> None:
        pass

    def register_event_handler(
        self, func: Callable[[pygame.event.Event], None], event_type: int
    ) -> None:
        pass

    def quit(self) -> None:
        pass

    def is_running(self) -> bool:
        pass

    def run(self) -> None:
        pass


class GameLoop:

    def __init__(self, fps: int = 60) -> None:
        self._fps = fps
        self._display_functions = []
        self._event_handlers: dict[int, list[Callable[[pygame.event.Event], None]]] = (
            defaultdict(list)
        )
        self._is_running = False
        self._event_handlers[pygame.QUIT].append(self.quit)
        self._event_handlers[pygame.KEYDOWN].append(
            lambda event: self.quit() if event.key == pygame.K_ESCAPE else None
        )
        self.clock = pygame.time.Clock()

    def quit(self) -> None:
        self._is_running = False
        pygame.event.set_grab(False)
        pygame.mouse.set_visible(True)

    def is_running(self) -> bool:
        return self._is_running

    def register_display_function(
        self, func: Callable[[pygame.event.Event], None]
    ) -> None:
        self._display_functions.append(func)

    def register_event_handler(self, func: Callable, event_type: int) -> None:
        self._event_handlers[event_type].append(func)

    def run(self) -> None:
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        self._is_running = True
        while self._is_running:
            for event in pygame.event.get():
                if event.type in self._event_handlers:
                    for event_handler in self._event_handlers[event.type]:
                        event_handler(event)
            for display_function in self._display_functions:
                display_function()
            pygame.display.flip()
            self.clock.tick(self._fps)
        pygame.quit()
