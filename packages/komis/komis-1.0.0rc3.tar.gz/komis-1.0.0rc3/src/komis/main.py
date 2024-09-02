import importlib
import importlib.metadata
import os
import shutil

from PIL import Image
from rich import print
from rich.panel import Panel

from .BaseEngine import BaseEngine

SCREEN_WIDTH = 800
PART_HEIGHT = 800

engines = {}


for frametype in importlib.metadata.entry_points(group="komis.frametype"):
    if issubclass(frametype.load(), BaseEngine):
        engines[frametype.name] = frametype.load()(SCREEN_WIDTH)
    else:
        print(
            f"What!? :confused: engine '{frametype.name}' is in group 'komis.frametype'\
                but does not inherit 'komis.BaseEngine.BaseEngine."
        )


def read_komis_file(filename: str):
    """Open a file and read it."""
    read_file_data = ""
    with open(filename) as f:
        read_file_data = f.read()
    return read_file_data


def parse_komis_file(file: str):
    """Parse the KOMIS-FILE."""
    has_started = False
    curr_frame = None
    for rule in file.split("\n"):
        rsplit = rule.split("\t")
        # print(rsplit)
        if not has_started:
            assert len(rsplit) in [2, 4]
            if len(rsplit) == 2:
                assert rsplit == ["KOMIS-FILE", "START"]
                has_started = True
                continue
            else:
                global SCREEN_WIDTH, PART_HEIGHT
                SCREEN_WIDTH = int(rsplit[2])
                PART_HEIGHT = int(rsplit[3])
                has_started = True
                for engine in engines:
                    engines[engine].screen_width = SCREEN_WIDTH
                continue
        if curr_frame is None:
            assert rsplit == ["BEGIN-FRAME"]
            curr_frame = {}
            continue
        if "type" not in curr_frame.keys():
            assert rsplit[0] == "TYPE"
            assert len(rsplit) == 2
            curr_frame["type"] = rsplit[1]
            continue
        match rsplit[0]:
            case "ARGUMENT":
                assert len(rsplit) >= 3
                if "args" in curr_frame.keys():
                    assert rsplit[1] not in curr_frame["args"].keys()
                    curr_frame["args"][rsplit[1]] = "\t".join(rsplit[2:])
                else:
                    curr_frame["args"] = {}
                    curr_frame["args"][rsplit[1]] = "\t".join(rsplit[2:])
                continue
            case "BEGIN-FRAME":
                assert len(rsplit) == 1
                yield curr_frame
                curr_frame = {}
                continue
            case "KOMIS-FILE":
                assert len(rsplit) == 2
                assert rsplit == ["KOMIS-FILE", "END"]
                yield curr_frame
                break


def check(filename: str) -> bool:
    """Check whether the KOMIS-FILE is readable."""
    print(
        "Oh-Kay! I'll be reading the file you've\
            given me and showing you it's contents."
    )
    try:
        d = read_komis_file(filename=filename)
        p = parse_komis_file(d)
        required_types = set()
        for frame in p:
            required_types.add(frame["type"])
            print(
                Panel(
                    str(
                        "\n".join(
                            [
                                f"[blue bold]{x}[/]: {frame['args'][x]}"
                                for x in frame["args"]
                            ]
                        )
                        if "args" in frame.keys()
                        else "[blue bold]No ARGUMENTs.[/]"
                    ),
                    title="[green]Frame[/]",
                    subtitle=f"Type [bold]{frame['type']}[/]",
                )
            )
            assert engines[frame["type"]].verify(
                frame["args"] if "args" in frame.keys() else {}
            )
        print(
            Panel(str("\n".join(required_types)), title="Required TYPEs for your file.")
        )
        print(Panel(str("\n".join(engines.keys())), title="Known TYPEs."))
        for required_type in required_types:
            assert required_type in engines.keys()
    except AssertionError:
        print(
            "[red]NOPE! An error occurred. An assertion failed.\
                This probably means that your file is corrupt.[/]"
        )
        return False
    except Exception:
        print("[red]NOPE! An [blink bold]UNKNOWN[/blink bold] error occurred.[/]")
        return False
    else:
        return True


def showtime(filename: str, out_dir_name: str):
    """Generate the comic."""
    images: list[Image.Image] = []
    assert check(filename=filename)
    d = read_komis_file(filename=filename)
    p = parse_komis_file(d)
    for frame in p:
        images.append(
            engines[frame["type"]].generate(
                arguments=frame["args"] if "args" in frame.keys() else {}
            )
        )
    full_height = 0
    for image in images:
        full_height += image.size[1]
    newImage = Image.new("RGB", (SCREEN_WIDTH, full_height), 0)
    y = 0
    for image in images:
        newImage.paste(image, (0, y))
        y += image.size[1]
    # newImage.show()
    h = newImage.size[1]
    last_part_height = h % PART_HEIGHT
    h = h - last_part_height
    if os.path.exists(out_dir_name):
        shutil.rmtree(out_dir_name)
    os.makedirs(out_dir_name)
    for i in range(h // PART_HEIGHT):
        im = Image.new("RGB", (SCREEN_WIDTH, PART_HEIGHT))
        im.paste(newImage, (0, PART_HEIGHT * -i))
        im.save(f"{out_dir_name}/{i}.png")
    if last_part_height != 0:
        im = Image.new("RGB", (SCREEN_WIDTH, last_part_height))
        im.paste(newImage, (0, PART_HEIGHT * -(h // PART_HEIGHT)))
        im.save(f"{out_dir_name}/{h//PART_HEIGHT}.png")
    newImage.save(f"{out_dir_name}/full.png")
