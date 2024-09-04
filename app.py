from PIL import Image
import os
import colorsys

def clamp(value, min_value=0.0, max_value=1.0):
    """Clamp a value to ensure it stays within the provided range."""
    return max(min_value, min(value, max_value))

def blend(image, original_filename, ramp_width):
    # Get image dimensions
    width, height = image.size

    # Convert image to RGB mode if not already in RGB
    image = image.convert("RGB")

    # Create a new image to store blended results
    blended_image = image.copy()
    pixels = blended_image.load()

    # Loop through each horizontal pixel line
    for y in range(height):
        # Get the leftmost and rightmost pixel colors
        left_pixel = image.getpixel((0, y))
        right_pixel = image.getpixel((width - 1, y))

        # Convert RGB values to HLS (Hue, Lightness, Saturation)
        left_hls = colorsys.rgb_to_hls(*[c / 255.0 for c in left_pixel])
        right_hls = colorsys.rgb_to_hls(*[c / 255.0 for c in right_pixel])

        # if left is pure black or pure white set the h and s values to the right pixel
        if left_hls[1] == 0 or left_hls[1] == 1:
            left_hls = (right_hls[0], left_hls[1], right_hls[2])
        if right_hls[1] == 0 or right_hls[1] == 1:
            right_hls = (left_hls[0], right_hls[1], left_hls[2])

        # Calculate the difference in HLS values
        h_diff = (left_hls[0] - right_hls[0]) / 2
        l_diff = (left_hls[1] - right_hls[1]) / 2
        s_diff = (left_hls[2] - right_hls[2]) / 2

        # Apply blending for the left ramp
        for x in range(min(ramp_width, width // 2)):
            # Calculate the blend factor: 1 at the edge, 0 at the end of the ramp
            blend_factor = 1 - (x / ramp_width)

            # # Get the current pixel color
            current_pixel = image.getpixel((x, y))

            current_hls = colorsys.rgb_to_hls(*[c / 255.0 for c in current_pixel])
            # if black or white pixel set the h and s values to the left pixel
            if current_hls[1] == 0 or current_hls[1] == 1:
                current_hls = (left_hls[0], current_hls[1], left_hls[2])


            # # Apply HLS differences scaled by the blend factor
            new_hls = (
                clamp(current_hls[0] - h_diff * blend_factor),  # Hue
                clamp(current_hls[1] - l_diff * blend_factor),  # Lightness
                clamp(current_hls[2] - s_diff * blend_factor),  # Saturation
            )

            # # Convert back to RGB and apply to the pixel
            new_rgb = colorsys.hls_to_rgb(*new_hls)
            pixels[x, y] = tuple(int(c * 255) for c in new_rgb)

        # Apply blending for the right ramp
        for x in range(max(width - ramp_width, width // 2), width):
            # Calculate the blend factor: 1 at the edge, 0 at the end of the ramp
            blend_factor = 1 - ((width - x) / ramp_width)

            # Get the current pixel color
            current_pixel = image.getpixel((x, y))
            current_hls = colorsys.rgb_to_hls(*[c / 255.0 for c in current_pixel])
            # if black or white pixel set the h and s values to the right pixel
            if current_hls[1] == 0 or current_hls[1] == 1:
                current_hls = (right_hls[0], current_hls[1], right_hls[2])

            # Apply HLS differences scaled by the blend factor
            new_hls = (
                clamp(current_hls[0] + h_diff * blend_factor),  # Hue
                clamp(current_hls[1] + l_diff * blend_factor),  # Lightness
                clamp(current_hls[2] + s_diff * blend_factor),  # Saturation
            )

            # Convert back to RGB and apply to the pixel
            new_rgb = colorsys.hls_to_rgb(*new_hls)
            pixels[x, y] = tuple(int(c * 255) for c in new_rgb)




    # Save the blended image as a new JPEG file
    save_image_as_jpeg(blended_image, original_filename)

def save_image_as_jpeg(image, original_filename):
    # Generate a new filename by appending '_blended' to the original name
    base_name = os.path.splitext(os.path.basename(original_filename))[0]
    new_filename = f"{base_name}_blended.jpg"
    # save in /output folder
    image.save(f"output/{new_filename}", "JPEG")
    print(f"Saved blended image as {new_filename}")

def open_images_and_apply_blend():
    # Get the list of files in the current directory
    current_directory = os.getcwd()
    files = os.listdir(current_directory)

    # Iterate through the files and open images
    for file in files:
        # Check if the file is an image by looking at its extension
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
            try:
                # Open the image
                image = Image.open(file)
                print(f"Opened image: {file}")

                # Call the blend function with the opened image and the filename
                blend(image, file, ramp_width=500)
            except Exception as e:
                print(f"Failed to open image {file}: {e}")

if __name__ == "__main__":
    open_images_and_apply_blend()
