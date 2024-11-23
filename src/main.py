from os import mkdir, path
from random import shuffle
from shutil import rmtree
from sys import argv, exit

import ffmpeg
from PIL import Image
from rich.console import Console

split_size = 50
total_splits = 0


def sv_get_image():
    if len(argv) < 2 or not path.exists(argv[1]):
        return None

    return Image.open(argv[1])


def sv_random(max_range):
    random_sequence = [i for i in range(max_range)]
    shuffle(random_sequence)

    return random_sequence


def sv_get_w_h_splits(width, height):
    return width // split_size, height // split_size


def sv_split(image):
    images = []

    width, height = image.size
    w_iter, h_iter = sv_get_w_h_splits(width, height)

    left = 0
    upper = 0
    right = split_size
    lower = split_size

    counter = 0

    for i in range(h_iter):
        for j in range(w_iter):
            temporary_image = image.crop((left, upper, right, lower))

            images.append(temporary_image)
            counter += 1

            left += split_size
            right += split_size

        upper += split_size
        lower += split_size

        left = 0
        right = split_size

    return images


def sv_merge(image, images, sequence, iteration):
    width, height = image.size
    w_iter, h_iter = sv_get_w_h_splits(width, height)

    left = 0
    upper = 0
    right = split_size
    lower = split_size

    merge_image = Image.new("RGB", (width, height))

    counter = 0

    for i in range(h_iter):
        for j in range(w_iter):
            merge_image.paste(images[sequence[counter]], (left, upper, right, lower))

            counter += 1

            left += split_size
            right += split_size

        upper += split_size
        lower += split_size

        left = 0
        right = split_size

    merge_image.save(f"merge/{iteration:06}.jpg")


def sv_bubble_sort(image, images, sequence):
    n = len(sequence)

    for i in range(n):
        for j in range(n - 1):
            if sequence[j] > sequence[j + 1]:
                sequence[j], sequence[j + 1] = sequence[j + 1], sequence[j]

        sv_merge(image, images, sequence, i)


def sv_create_video():
    ffmpeg.input("merge/*.jpg", pattern_type="glob", framerate=30).output(
        "sort-image.mp4", loglevel="quiet"
    ).run(overwrite_output=True)


def main():
    global total_splits, split_size

    if len(argv) > 2:
        split_size = int(argv[2])

    console = Console()

    image = sv_get_image()

    if image is None:
        exit(-1)

    width, height = image.size

    total_splits = (width // split_size) * (height // split_size)

    if not path.exists("merge"):
        mkdir("merge")
    else:
        rmtree("merge/", ignore_errors=True)
        mkdir("merge")

    with console.status("Splitting image into pieces...", spinner="dots9"):
        images = sv_split(image)

    with console.status("Sorting with bubble sort...", spinner="dots9"):
        sv_bubble_sort(image, images, sv_random(total_splits))

    with console.status("Creating video with ffmpeg...", spinner="dots9"):
        sv_create_video()

    rmtree("merge/", ignore_errors=True)


if __name__ == "__main__":
    main()
