from PIL import Image

from komis.BaseEngine import BaseEngine


class LogoEngine(BaseEngine):
    """Draw the logo of the comic."""

    EngineArguments = {}

    def generate(self, arguments: dict[str, str]) -> Image:
        """
        Generate the image.

        Args:
        ----
            arguments (dict[str, str]): the ARGUMENTs defined in the KOMIS-FILE

        Returns:
        -------
            Image: The image which will be placed in the comic

        """
        logo = Image.open("assets/logo.png")
        newimage = Image.new("RGB", (self.screen_width, logo.size[1] + 20), 0x000000)
        newimage.paste(logo, ((self.screen_width - logo.size[1]) // 2, 10))
        return newimage
