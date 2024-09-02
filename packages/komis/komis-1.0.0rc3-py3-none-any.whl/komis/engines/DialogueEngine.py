from PIL import Image, ImageDraw

from komis.BaseEngine import BaseEngine


class DialogueEngine(BaseEngine):
    """Generate a person and a speech bubble."""

    EngineArguments = {
        "SPEAKER": "",
        "FORMAT": "",
        "SAYS": "",
        "FONT-SIZE": "",
        "SPEAKER-STATE": "",
    }

    EngineArguments = {
        "SPEAKER": "",
        "FORMAT": "",
        "SAYS": "",
        "FONT-SIZE": "",
        "SPEAKER-STATE": "",
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
        a_speaker = arguments["SPEAKER"]
        a_state = (
            arguments["SPEAKER-STATE"]
            if "SPEAKER-STATE" in arguments.keys()
            else "Default"
        )
        a_format = arguments["FORMAT"] if "FORMAT" in arguments.keys() else "jpg"
        a_says = arguments["SAYS"]
        a_font_size = (
            int(arguments["FONT-SIZE"]) if "FONT-SIZE" in arguments.keys() else 50
        )
        im = Image.open(f"assets/characters/{a_speaker}/{a_state}.{a_format}")
        im = im.resize(
            (
                (self.screen_width // 2) - 50,
                int((im.size[1] / im.size[0]) * ((self.screen_width // 2) - 50)),
            )
        )
        newimage = Image.new("RGB", (self.screen_width, im.size[1] + 60), 0x000000)
        newimage.paste(im, (50, 30))
        draw = ImageDraw.Draw(newimage)
        draw.text(
            ((self.screen_width // 2) + 50, (im.size[1] // 2)),
            a_says.replace("\\n", "\n"),
            anchor="lm",
            font_size=a_font_size,
        )
        return newimage
