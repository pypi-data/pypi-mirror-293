from PIL import Image, ImageDraw

from komis.BaseEngine import BaseEngine


class SimpleTextEngine(BaseEngine):
    """Just put some text on the screen."""

    EngineArguments = {
        "TEXT": "",
        "P-X": "",
        "FONT-SIZE": "",
        "BOX-WIDTH": "",
        "BOX-HEIGHT": "",
        "BOX-LINE-WIDTH": "",
    }

    EngineArguments = {
        "TEXT": "",
        "P-X": "",
        "FONT-SIZE": "",
        "BOX-WIDTH": "",
        "BOX-HEIGHT": "",
        "BOX-LINE-WIDTH": "",
    }

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
        newimage = Image.new(
            "RGB", (self.screen_width, self.screen_width // 4), 0x000000
        )
        sw = newimage.size[0]
        sh = newimage.size[1]
        px = float(arguments["P-X"]) if "P-X" in arguments.keys() else 0.5
        pw = int(sw * px)
        draw = ImageDraw.Draw(newimage)
        draw.text(
            (pw, newimage.size[1] // 2),
            arguments["TEXT"].replace("\\n", "\n"),
            anchor="mm",
            font_size=(
                int(arguments["FONT-SIZE"]) if "FONT-SIZE" in arguments.keys() else 80
            ),
        )
        if "BOX-WIDTH" in arguments.keys() and "BOX-HEIGHT" in arguments.keys():
            draw.rectangle(
                (
                    (pw) - (int(arguments["BOX-WIDTH"]) // 2),
                    (sh // 2) - (int(arguments["BOX-HEIGHT"]) // 2),
                    (pw) + (int(arguments["BOX-WIDTH"]) // 2),
                    (sh // 2) + (int(arguments["BOX-HEIGHT"]) // 2),
                ),
                width=int(arguments["BOX-LINE-WIDTH"])
                if "BOX-LINE-WIDTH" in arguments.keys()
                else 1,
            )
        return newimage
