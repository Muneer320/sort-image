import argparse
from argparse import ArgumentParser, Namespace
from os import listdir, mkdir, path
from random import shuffle
from shutil import rmtree
from sys import exit

from PIL import Image
from PIL.Image import Image as ImageType
from PIL.ImageFile import ImageFile as ImageFileType

from term import r_print

# *************************************************#
#              SV_PARSE_IMAGE                      #
# *************************************************#


def sv_parse_image(image: str) -> ImageFileType | None:
    if path.exists(image):
        return Image.open(image)
    else:
        return None


# *************************************************#
#              SV_CREATE_MERGE_DIR                 #
# *************************************************#


def sv_create_merge_dir() -> None:
    if not path.exists("sv"):
        mkdir("sv")
    else:
        rmtree("sv/", ignore_errors=True)
        mkdir("sv")


# *************************************************#
#              SV_CREATE_VIDEO_FFMEPG              #
# *************************************************#


def sv_create_video_ffmpeg(
    directory: str, output: str, dimensions: tuple[int, int]
) -> None:
    import ffmpeg

    glob = f"{directory}/*.jpg"

    try:
        ffmpeg.input(glob, pattern_type="glob", framerate=30).output(
            output, loglevel="quiet"
        ).run(overwrite_output=True)
    except Exception:
        r_print("[bold red]Error[/bold red]: FFMPEG Failed with error.")
        exit(1)


# *************************************************#
#              SV_CREATE_VIDEO_OPENCV              #
# *************************************************#


def sv_create_video_opencv(
    directory: str, output: str, dimensions: tuple[int, int]
) -> None:
    import cv2

    try:
        width, height = dimensions

        video = cv2.VideoWriter(
            output, cv2.VideoWriter_fourcc(*"mp4v"), 30, (width, height)
        )

        for image in listdir(directory):
            img = cv2.imread(path.join(directory, image))
            video.write(img)

        cv2.destroyAllWindows()
        video.release()
    except Exception:
        r_print("[bold red]Error[/bold red]: OpenCV Failed with error.")
        exit(1)


# *************************************************#
#              SV_PARSE_ARGS                       #
# *************************************************#


def sv_parse_args() -> Namespace:
    parser = ArgumentParser(
        prog="sort-image", description="Visualize sorting algorithms via images."
    )

    parser.add_argument("image", type=str, help="Path to the image")
    parser.add_argument(
        "-s", "--split", type=int, help="Size of splits (Default is 50)", required=False
    )
    parser.add_argument(
        "-a",
        "--algorithm",
        type=int,
        help="Sorting algorithm to use",
        required=False,
    )
    parser.add_argument(
        "-b",
        "--builder",
        type=str,
        choices=["ff", "cv"],
        required=False,
        help="Video build tool: ff (FFMEPG) or cv (OPENCV)",
    )

    args = parser.parse_args()

    return args


# *************************************************#
#              SV_GENERATE_ARRAY                   #
# *************************************************#


def sv_generate_array(size: int) -> list[int]:
    array = list(i for i in range(size))
    shuffle(array)

    return array


# *************************************************#
#              SV_SPLIT_IMAGE                      #
# *************************************************#


def sv_split_image(image: ImageFileType, split: int) -> list[ImageType]:
    split_images: list[ImageType] = []

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


# *************************************************#
#              SV_MERGE_IMAGE                      #
# *************************************************#


def sv_merge_image(
    image: ImageFileType,
    images: list[ImageType],
    array: list[int],
    count: int,
    split: int,
) -> None:
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
