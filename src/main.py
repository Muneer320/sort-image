from shutil import rmtree

from rich import print as r_print
from rich.console import Console

import util
from sort import SVSort


def main():
    console = Console()
    args = util.sv_parse_args()

    directory = "sv"
    video = "sort-image.mp4"

    # Get image
    image = util.sv_parse_image(args.image)

    if image is None:
        console.print("[bold red]Error[/bold red]: Invalid image file.")
        exit(1)

    # Get split size
    split = int(args.split) if args.split else 50

    w, h = image.size
    splits = (w // split) * (h // split)

    util.sv_create_merge_dir()

    # Process
    status = console.status

    with status("Splitting image into pieces...", spinner="dots9"):
        images = util.sv_split_image(image, split)

    with status("Sorting with bubble sort...", spinner="dots9"):
        array = util.sv_generate_array(splits)
        sort = SVSort(array)

        for index, iteration in enumerate(sort.bubble_sort()):
            util.sv_merge_image(image, images, iteration, index, split)

    with status("Creating video with ffmpeg...", spinner="dots9"):
        util.sv_create_video(directory, video)

    rmtree(directory, ignore_errors=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        rmtree("sv/", ignore_errors=True)
        r_print("[bold red]Error[/bold red]: Exception occured.")
        exit(1)
