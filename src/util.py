from argparse import ArgumentParser, Namespace
from os import mkdir, path
from random import shuffle
from shutil import rmtree
from sys import exit

import ffmpeg
from PIL import Image
from PIL.Image import Image as ImageType
from PIL.ImageFile import ImageFile as ImageFileType
from rich import print as r_print


def sv_parse_image(image: str) -> ImageFileType | None:
    if path.exists(image):
        return Image.open(image)
    else:
        return None


def sv_create_merge_dir():
    if not path.exists("sv"):
        mkdir("sv")
    else:
        rmtree("sv/", ignore_errors=True)
        mkdir("sv")


def sv_create_video(directory: str, output: str) -> None:
    glob = f"{directory}/*.jpg"

    try:
        ffmpeg.input(glob, pattern_type="glob", framerate=30).output(
            output, loglevel="quiet"
        ).run(overwrite_output=True)
    except Exception:
        r_print("[bold red]Error[/bold red]: FFMPEG Failed with error.")
        exit(1)


def sv_parse_args() -> Namespace:
    parser = ArgumentParser(
        prog="sort-image", description="Visualize sorting algorithms via images."
    )

    parser.add_argument("image")
    parser.add_argument("-s", "--split")

    args = parser.parse_args()

    return args


def sv_generate_array(size: int) -> list[int]:
    array = list(i for i in range(size))
    shuffle(array)

    return array


def sv_split_image(image: ImageFileType, split: int) -> list[ImageType]:
    split_images = []

    w, h = image.size
    w, h = w // split, h // split

    left = 0
    upper = 0
    right = split
    lower = split

    counter = 0

    for _ in range(h):
        for _ in range(w):
            img = image.crop((left, upper, right, lower))
            split_images.append(img)

            counter += 1

            left += split
            right += split

        left = 0
        upper += split
        right = split
        lower += split

    return split_images


def sv_merge_image(
    image: ImageFileType,
    images: list[ImageType],
    array: list[int],
    count: int,
    split: int,
):
    w, h = image.size
    w, h = w // split, h // split

    img = Image.new("RGB", image.size)

    left = 0
    upper = 0
    right = split
    lower = split

    counter = 0

    for _ in range(h):
        for _ in range(w):
            img.paste(images[array[counter]], (left, upper, right, lower))

            counter += 1

            left += split
            right += split

        left = 0
        upper += split
        right = split
        lower += split

    img.save(f"sv/{count:010}.jpg")
