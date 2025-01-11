from shutil import rmtree

from rich.progress import Progress

import util
from sort import SVSort
from term import r_print, status

# *************************************************#
#              SV_MAIN                             #
# *************************************************#


def sv_main() -> None:
    args = util.sv_parse_args()
    directory = "sv"

    image = util.sv_parse_image(args.image)

    if image is None:
        r_print("[bold red]Error[/bold red]: Invalid image file.")
        exit(1)

    split = int(args.split) if args.split else 50
    builder = args.builder if args.builder else "ff"

    w, h = image.size
    splits = (w // split) * (h // split)

    util.sv_create_merge_dir()

    with status("Splitting image into pieces...", spinner="dots9"):
        images = util.sv_split_image(image, split)

    with Progress() as progress:
        task = progress.add_task(f"Generating {splits} images...", total=splits)

        array = util.sv_generate_array(splits)
        sv_sort = SVSort(array)

        # Generator
        algorithm = (
            int(args.algorithm)
            if (args.algorithm and int(args.algorithm) < sv_sort.total_algorithms)
            else 0
        )

        sort = sv_sort.sort(algorithm)

        for index, iteration in enumerate(sort()):
            util.sv_merge_image(image, images, iteration, index, split)
            progress.update(task, advance=1)

    video = f"{sv_sort.algorithms[algorithm].__name__}.mp4"

    # Defaults to FFMEPG
    if builder == "ff":
        with status("Creating video with ffmpeg...", spinner="dots9"):
            util.sv_create_video_ffmpeg(directory, video, image.size)
    elif builder == "cv":
        with status("Creating video with OpenCV...", spinner="dots9"):
            util.sv_create_video_opencv(directory, video, image.size)

    rmtree(directory, ignore_errors=True)

    r_print("🚀 Video generated.")


if __name__ == "__main__":
    try:
        sv_main()
    except KeyboardInterrupt as interrupt:
        rmtree("sv/", ignore_errors=True)
        r_print("[bold red]Error[/bold red]: Interrupted.")
        r_print(interrupt)
        exit(1)
    except Exception as exception:
        rmtree("sv/", ignore_errors=True)
        r_print("[bold red]Error[/bold red]: Exception occurred.")
        r_print(exception)
        exit(1)
