## ⚙️ Features and Improvements
### Sorting Algorithms
This fork has added multiple sorting algorithms. The available algorithms are:
- `Bubble Sort`
- `Selection Sort`
- `Insertion Sort`
- `Merge Sort`
- `Quick Sort`
- `Heap Sort`

### Video Formatter
Users can now choose between `ffmpeg` and `opencv` for video creation using the `-v` or `--video-formatter` argument. The default remains `ffmpeg`.

### Output File Name
The output video file is now named after the sorting algorithm used, e.g., `bubble_sort.mp4`, instead of the default `sort-image.mp4`.

### Improved Argument Handling
Arguments are better validated, including:
- Restricting sorting algorithm selection to valid indices.
- Ensuring proper types and ranges for inputs.
- Optional arguments for split size, algorithm, and video formatter.

### Updated Dependencies
The dependency file `requirements.txt` has been split:
- Use `requirements_ffmpeg.txt` if you plan to use `ffmpeg`.
- Use `requirements_opencv.txt` if you prefer `opencv`.

---

