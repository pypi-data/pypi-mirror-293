from PIL import Image, ImageDraw

from komis.BaseEngine import BaseEngine

RAINBOW = [
    0xFF0000,
    0x888800,
    0x00FF00,
    0x008888,
    0x0000FF,
    0xFFFFFF,
]  # just randomly made shit up here, for the hell of it.
# TODO: google the colors of the rainbow.


class GayEngine(BaseEngine):
    """
    Make a pride flag.

    (I haven't took the time to actually google the correct colours.)
    """

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
        newimage = Image.new("RGB", (self.screen_width, 200), 0x000000)
        draw = ImageDraw.Draw(newimage)
        flag = RAINBOW
        if "FLAG" in arguments.keys():
            match arguments["FLAG"]:
                case "RAINBOW":
                    flag = RAINBOW
                case "RAINBOW-REVERSED":
                    flag = RAINBOW[::-1]
                case _:
                    flag = RAINBOW
        for i in range(0, len(flag)):
            draw.rectangle(
                (
                    (self.screen_width / len(flag)) * i,
                    0,
                    (self.screen_width / len(flag)) * (i + 1),
                    199,
                ),
                flag[i],
                0xFFFFFF,
            )
        return newimage
