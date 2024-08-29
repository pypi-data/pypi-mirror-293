import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageDraw, ImageFont
import requests
from io import BytesIO
import os
from typing import Dict, Any, Union, List, Tuple

class ImageEnhancer:
    def __init__(self, output_dir: str = "enhanced_images"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def load_image(self, image_path: str) -> Image.Image:
        """Load an image from a file path or URL."""
        try:
            if image_path.startswith(('http://', 'https://')):
                response = requests.get(image_path)
                response.raise_for_status()
                return Image.open(BytesIO(response.content))
            else:
                return Image.open(image_path)
        except (requests.RequestException, IOError) as e:
            raise ValueError(f"Failed to load image from {image_path}: {str(e)}")

    def save_image(self, img: Image.Image, filename: str) -> str:
        """Save the image to the output directory."""
        filepath = os.path.join(self.output_dir, filename)
        img.save(filepath, quality=95)
        return filepath

    def process_rgba(self, img: Image.Image, process_func: callable, *args, **kwargs) -> Image.Image: # type: ignore
        """Process RGBA images while preserving the alpha channel."""
        if img.mode == 'RGBA':
            rgb, alpha = img.convert('RGB'), img.split()[3]
            processed_rgb = process_func(rgb, *args, **kwargs)
            r, g, b = processed_rgb.split()
            return Image.merge('RGBA', (r, g, b, alpha))
        else:
            return process_func(img, *args, **kwargs)

    def enhance(self, image_path: str, params: Dict[str, Any], output_filename: str) -> str:
        """Apply various enhancements to the image based on the provided parameters."""
        img = self.load_image(image_path)

        enhancement_functions = [
            (self.denoise, 'denoise_strength'),
            (self.adjust_brightness_contrast, 'brightness', 'contrast'),
            (self.enhance_color, 'color', 'saturation'),
            (self.shift_hue, 'hue_shift'),
            (self.sharpen, 'sharpness'),
            (self.edge_enhance, 'edge_enhance'),
            (self.gamma_correction, 'gamma'),
            (self.resize, 'width', 'height'),
            (self.rotate, 'rotation_angle'),
            (self.flip, 'flip_direction'),
            (self.crop, 'crop_box'),
            (self.add_watermark, 'watermark_text', 'watermark_position'),
            (self.apply_filter, 'filter'),
            (self.adjust_hsl, 'hue', 'saturation', 'lightness')
        ]

        for func, *param_names in enhancement_functions:
            if all(params.get(name) is not None for name in param_names):
                img = self.process_rgba(img, func, *[params.get(name) for name in param_names])

        return self.save_image(img, output_filename)

    def denoise(self, img: Image.Image, strength: float) -> Image.Image:
        """Apply denoising to the image."""
        img_array = np.array(img)
        denoised = cv2.fastNlMeansDenoisingColored(img_array, None, strength, strength, 7, 21)
        return Image.fromarray(denoised)

    def adjust_brightness_contrast(self, img: Image.Image, brightness: float, contrast: float) -> Image.Image:
        """Adjust the brightness and contrast of the image."""
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(brightness)
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(contrast)

    def enhance_color(self, img: Image.Image, color: float, saturation: float) -> Image.Image:
        """Enhance the color and saturation of the image."""
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(color)
        enhancer = ImageEnhance.Color(img)
        return enhancer.enhance(saturation)

    def shift_hue(self, img: Image.Image, hue_shift: int) -> Image.Image:
        """Shift the hue of the image."""
        img_hsv = img.convert('HSV')
        h, s, v = img_hsv.split()
        h = h.point(lambda x: (x + hue_shift) % 256)
        img_hsv = Image.merge('HSV', (h, s, v))
        return img_hsv.convert('RGB')

    def sharpen(self, img: Image.Image, sharpness: float) -> Image.Image:
        """Sharpen the image."""
        enhancer = ImageEnhance.Sharpness(img)
        return enhancer.enhance(sharpness)

    def edge_enhance(self, img: Image.Image, strength: float) -> Image.Image:
        """Enhance the edges in the image."""
        enhanced = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
        return Image.blend(img, enhanced, strength - 1.0)

    def gamma_correction(self, img: Image.Image, gamma: float) -> Image.Image:
        """Apply gamma correction to the image."""
        img_array = np.array(img)
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        return Image.fromarray(cv2.LUT(img_array, table))

    def resize(self, img: Image.Image, width: int, height: int) -> Image.Image:
        """Resize the image to the specified dimensions."""
        return img.resize((width, height), Image.Resampling.LANCZOS)

    def rotate(self, img: Image.Image, angle: float) -> Image.Image:
        """Rotate the image by the specified angle."""
        return img.rotate(angle, expand=True)

    def flip(self, img: Image.Image, direction: str) -> Image.Image:
        """Flip the image horizontally or vertically."""
        if direction == 'horizontal':
            return ImageOps.mirror(img)
        elif direction == 'vertical':
            return ImageOps.flip(img)
        else:
            raise ValueError("Direction must be 'horizontal' or 'vertical'")

    def crop(self, img: Image.Image, crop_box: Tuple[int, int, int, int]) -> Image.Image:
        """Crop the image to the specified box (left, top, right, bottom)."""
        return img.crop(crop_box)

    def add_watermark(self, img: Image.Image, text: str, position: Tuple[int, int]) -> Image.Image:
        """Add a text watermark to the image."""
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        draw.text(position, text, font=font, fill=(255, 255, 255, 128))
        return img

    def apply_filter(self, img: Image.Image, filter_name: str) -> Image.Image:
        """Apply a predefined filter to the image."""
        filters = {
            'blur': ImageFilter.BLUR,
            'contour': ImageFilter.CONTOUR,
            'emboss': ImageFilter.EMBOSS,
            'find_edges': ImageFilter.FIND_EDGES,
            'smooth': ImageFilter.SMOOTH,
            'sharpen': ImageFilter.SHARPEN,
        }
        if filter_name in filters:
            return img.filter(filters[filter_name])
        else:
            raise ValueError(f"Unknown filter: {filter_name}")

    def adjust_hsl(self, img: Image.Image, hue: float, saturation: float, lightness: float) -> Image.Image:
        """Adjust the HSL values of the image."""
        img_hls = img.convert('HSV')
        h, l, s = img_hls.split()
        h = h.point(lambda x: int(x * hue) % 256)
        s = s.point(lambda x: int(x * saturation))
        l = l.point(lambda x: int(x * lightness))
        return Image.merge('HSV', (h, l, s)).convert(img.mode)

    def batch_process(self, image_paths: List[str], params: Dict[str, Any], output_filenames: List[str]) -> List[str]:
        """Process multiple images with the same parameters."""
        return [self.enhance(path, params, output_name) for path, output_name in zip(image_paths, output_filenames)]

    def compare_before_after(self, image_path: str, params: Dict[str, Any], output_filename: str) -> str:
        """Create a side-by-side comparison of the original and enhanced images."""
        original = self.load_image(image_path)
        enhanced_path = self.enhance(image_path, params, f"temp_{output_filename}")
        enhanced = self.load_image(enhanced_path)

        # Create a new image with both original and enhanced side by side
        total_width = original.width + enhanced.width
        max_height = max(original.height, enhanced.height)
        comparison = Image.new('RGB', (total_width, max_height))
        comparison.paste(original, (0, 0))
        comparison.paste(enhanced, (original.width, 0))

        return self.save_image(comparison, output_filename)

    def get_output_dir(self) -> str:
        """Return the output directory path."""
        return self.output_dir
