# ConvertImagesToPDF

A Python command-line tool that converts multiple image files—including HEIC photos (e.g., from iPhone)—into a single, organized PDF document.

## Features

- **Batch Conversion:** Convert multiple images at once using wildcard search patterns.
  - Example: `main.py <target size> <image_path>/IMG_*`

- **Automatic Orientation Handling:** Supports both landscape and portrait orientations automatically.  
  - Example: `main.py 2016x1512 <image_path>/IMG_*`  
    Portrait images will resize to `1512x2016`, while landscape images resize to `2016x1512`.

- **HEIC Support:** Accepts and converts HEIC images (such as those from iPhones).

- **PDF Output:** Merges all resized images into a single PDF file, saved in the same directory as your input images.

## Usage Example

```bash
python3 main.py 3024x4032 /my/image/folder/IMG_751*
