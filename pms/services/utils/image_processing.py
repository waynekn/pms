from io import BytesIO
from PIL import Image, ImageOps


def process_profile_pic(uploaded_file) -> BytesIO:

    image = Image.open(uploaded_file)

    # Convert to RGBA to handle transparency
    image = image.convert("RGBA")

    # Resize and compress
    image.thumbnail((300, 300))

    # Create circular mask
    mask = Image.new("L", (300, 300), 0)
    mask_draw = Image.new("L", (300, 300), 255)
    mask.paste(mask_draw, (0, 0), mask_draw)

    # Apply mask
    rounded = ImageOps.fit(image, (300, 300), centering=(0.5, 0.5))
    rounded.putalpha(mask)

    buffer = BytesIO()
    rounded.save(buffer, format="PNG", quality=85)
    buffer.seek(0)

    return buffer
