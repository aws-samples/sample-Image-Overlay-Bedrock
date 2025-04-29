from PIL import Image

def overlay_image(background_path, overlay_path, output_path, position, scale_factor=1.0):
    """
    Places the overlay image on top of the background image at the desired position.
    Optionally enlarges the overlay image based on the scale factor.
    
    :param background_path: Path to the background image
    :param overlay_path: Path to the image with a transparent background (PNG)
    :param output_path: Path where the output image will be saved
    :param position: Tuple (x, y) coordinates where the overlay image will be placed on the background
    :param scale_factor: A multiplier to enlarge or shrink the overlay image. Default is 1.0 (no change).
    """
    # Open the background image
    background = Image.open(background_path).convert("RGBA")

    # Open the overlay image
    overlay = Image.open(overlay_path).convert("RGBA")

    # Get dimensions of the overlay image
    overlay_width, overlay_height = overlay.size

    # Calculate new size for the overlay based on the scale factor
    new_overlay_width = int(overlay_width * scale_factor)
    new_overlay_height = int(overlay_height * scale_factor)

    # Resize the overlay image based on the scale factor
    overlay = overlay.resize((new_overlay_width, new_overlay_height), Image.Resampling.LANCZOS)
    print(f"Overlay resized to: {new_overlay_width}x{new_overlay_height}")

    # Get dimensions of the background image
    background_width, background_height = background.size

    # Ensure the overlay fits within the background's boundaries
    available_width = background_width - position[0]
    available_height = background_height - position[1]

    # Check if the overlay fits within the available space
    if new_overlay_width > available_width or new_overlay_height > available_height:
        print("Warning: The overlay image exceeds the background size at the given position and will be cropped.")

    # Paste the overlay onto the background (with mask to handle transparency)
    background.paste(overlay, position, mask=overlay)

    # Save the combined image
    background.save(output_path, format="PNG")

    print(f"Image saved as {output_path}")


# Example usage
background_image = "images/dogfood.jpg"
overlay_image_path = "images/dog_edit.png"  # This should have transparency
output_image = "images/overlay_output.png"
coordinates = (100, 0)  # x, y position where overlay is placed on the background
scale_factor = 1.2  # Example: 1.5 means increasing the size by 50%

overlay_image(background_image, overlay_image_path, output_image, coordinates, scale_factor)
