from typing import ClassVar

import PIL.Image


class BaseEngine:
    """BaseEngine - The core of a frametype."""

    screen_width: int
    EngineArguments: ClassVar[dict[str, str]]

    def __init__(self, screen_width) -> None:
        self.screen_width = screen_width

    def generate(self, arguments: dict[str, str]) -> PIL.Image.Image:
        """Generate the image based on the arguments provided."""
        pass

    def verify(self, arguments: dict[str, str]) -> bool:
        """Verify a frame is proper. Currently not yet implemented."""
        for key in arguments.keys():
            if key not in self.EngineArguments.keys():
                return False
        return True
