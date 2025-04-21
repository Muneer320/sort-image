# 📶 Sort Image

![Sort Image (Bubble Sort) - Preview](out/sort-image.gif)

Inspiration for this project is the following post from [Reddit](https://www.reddit.com/r/ProgrammerHumor/comments/cyrlvp/learn_sorting_algorithm_with_kronk/).

## 👷 Architecture

The flow of data is as follows: `PIL` is used for image manipulation, and either
`FFMPEG` or `OPENCV` can be used to combine the generated images into a video.

!["Architecture"](./docs/images/architecture.jpg)

## ⚙️ Usage

Install either `FFMPEG` or `OPENCV`.

```sh
sudo apt install ffmpeg
```

```sh
git clone https://github.com/surajkareppagol/sort-image
cd sort-image
```

```sh
python3 -m venv .venv
source .venv/bin/activate
```

```sh
pip install -r requirements.txt
```

```sh
python3 src/main.py [image]
```

## ➡️ Available Options

| Option | Description      | Arguments            |
| ------ | ---------------- | -------------------- |
| -      | Image            | None                 |
| s      | Image split size | Number (default: 50) |
| a      | Algorithm        | Index number (0 - 6) |
| b      | Builder          | "ff" or "cv"         |

## 📶 Sorting Algorithms

The following algorithms are available:

1. `Bubble Sort`
2. `Selection Sort`
3. `Insertion Sort`
4. `Merge Sort`
5. `Quick Sort`
6. `Heap Sort`

Each algorithm creates a visually unique sorting video, making it easier to
understand the sorting process.
