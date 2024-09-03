import io
from typing import Any, Optional

import magic
from django.core.files import File
from django.core.files.base import ContentFile
from PIL import Image

SUPPORTED_MIME_TO_FORMAT = {
    "image/jpeg": "JPEG",
    "image/png": "PNG",
}


def resize_image(
    uploaded_image: File,
    max_height: Optional[int] = None,
    max_width: Optional[int] = None,
) -> Optional[ContentFile]:
    uploaded_image_bytes = io.BytesIO(uploaded_image.read())
    # Check image format
    mime_type = magic.from_buffer(uploaded_image_bytes.read(2048), mime=True)
    if mime_type not in SUPPORTED_MIME_TO_FORMAT:
        return None
    uploaded_image_format = SUPPORTED_MIME_TO_FORMAT[mime_type]

    # Read in image
    image_obj = Image.open(uploaded_image_bytes)
    width, height = image_obj.size

    # Get ratio for resizing
    if not max_height:
        resize_ratio = max_width / width
    elif not max_width:
        resize_ratio = max_height / height
    else:
        resize_ratio = min((max_width / width), (max_height / height))

    # Calc new sizes and round to nearest int
    new_width = round(resize_ratio * width)
    new_height = round(resize_ratio * height)

    # Resize image
    resized_image = image_obj.resize(
        size=(new_width, new_height), resample=Image.Resampling.LANCZOS
    )

    # Return a file that can be saved directly to db
    final_image_bytes = io.BytesIO()
    resized_image.save(final_image_bytes, format=uploaded_image_format, quality=95)
    final_image = ContentFile(final_image_bytes.getvalue(), name=uploaded_image.name)

    return final_image
