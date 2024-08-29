# Image Enhancer

Image Enhancer is a Python package that allows you to easily apply various enhancements and filters to your images.

## Installation

You can install Image Enhancer using pip:

```
pip install image-enhancer
```

## Usage

Here's a simple example of how to use Image Enhancer:

```python
from image_enhancer import ImageEnhancer

enhancer = ImageEnhancer()

# Enhance an image from a local file
enhanced_image_path = enhancer.enhance("path/to/your/image.jpg", {
    "brightness": 1.2,
    "contrast": 1.1,
    "sharpness": 1.5,
    "saturation": 1.2
})

print(f"Enhanced image saved to: {enhanced_image_path}")

# Enhance an image from a URL
enhanced_image_path = enhancer.enhance("https://example.com/image.jpg", {
    "denoise_strength": 10,
    "gamma": 1.2,
    "hue_shift": 10
})

print(f"Enhanced image saved to: {enhanced_image_path}")
```

## Parameters

The `enhance` method accepts the following parameters:

- `denoise_strength`: Strength of denoising (0-20)
- `brightness`: Brightness adjustment (0.5-2.0)
- `contrast`: Contrast adjustment (0.5-2.0)
- `color`: Color enhancement (0.0-2.0)
- `sharpness`: Sharpness enhancement (0.0-2.0)
- `gamma`: Gamma correction (0.5-2.0)
- `saturation`: Saturation adjustment (0.0-2.0)
- `hue_shift`: Hue shift (-30 to 30)
- `edge_enhance`: Edge enhancement (1.0-3.0)

## License

This project is licensed under the MIT License.


