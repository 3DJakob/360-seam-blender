# 360 Seam Blender

This project blends the left and right edges of 360-degree panorama images so the wraparound seam is less visible.

It is especially useful after editing 360 photos. Many photo edits and filters change pixels based on nearby pixels, so the left and right edges of an equirectangular image may no longer line up perfectly after export. That can create a visible seam when the image is viewed as a sphere. This script softens that mismatch by adjusting the edge regions before you publish or view the panorama.

The script looks for image files in the project root, applies a horizontal edge blend, and writes processed JPG files to the `output/` folder. If a `nadir.png` file exists in the root, it is pasted on top of each generated image.

## Supported Images

The script processes files in the project root with these extensions:

- `.jpg`
- `.jpeg`
- `.png`
- `.bmp`
- `.gif`
- `.tiff`

It skips `nadir.png`, because that file is reserved as an optional overlay.

## Quick Use

1. Put your panorama images in this project folder.
2. Double-click `Generate Images.command`.
3. Wait for Terminal to finish.
4. Find the generated images in `output/`.

The shortcut creates `.venv` if it is missing, installs `Pillow` if needed, and runs `app.py`.

## Terminal Use

You can also skip the shortcut and run the Python script yourself.

From the project folder:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install Pillow
.venv/bin/python app.py
```

Generated files are saved to:

```text
output/
```

## Files

- `app.py`: Main Python script that opens images, blends the edge seam, and saves outputs.
- `Generate Images.command`: Double-clickable macOS Terminal shortcut.
- `output/`: Generated images.
- `nadir.png`: Optional overlay image. Add this file to the root if you want it pasted onto each result.

## Notes

- Existing files in `output/` with the same names will be overwritten.
- The default blend ramp is `500` pixels wide.
- The script processes all supported image files in the root folder, including test images.
