import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import requests
from io import BytesIO
import os

class ImageEnhancer:
    def __init__(self, output_dir="enhanced_images"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def load_image(self, image_path):
        if image_path.startswith(('http://', 'https://')):
            response = requests.get(image_path)
            return Image.open(BytesIO(response.content))
        else:
            return Image.open(image_path)

    def save_image(self, img, filename):
        filepath = os.path.join(self.output_dir, filename)
        img.save(filepath, quality=95)
        return filepath

    def process_rgba(self, img, process_func, *args, **kwargs):
        if img.mode == 'RGBA':
            rgb, alpha = img.convert('RGB'), img.split()[3]
            processed_rgb = process_func(rgb, *args, **kwargs)
            r, g, b = processed_rgb.split()
            return Image.merge('RGBA', (r, g, b, alpha))
        else:
            return process_func(img, *args, **kwargs)

    def enhance(self, image_path, params):
        img = self.load_image(image_path)

        if params.get('denoise_strength', 0) > 0:
            img = self.process_rgba(img, self.denoise, params['denoise_strength'])
        img = self.process_rgba(img, self.adjust_brightness_contrast, params.get('brightness', 1.0), params.get('contrast', 1.0))
        img = self.process_rgba(img, self.enhance_color, params.get('color', 1.0), params.get('saturation', 1.0))
        img = self.process_rgba(img, self.shift_hue, params.get('hue_shift', 0))
        img = self.process_rgba(img, self.sharpen, params.get('sharpness', 1.0))
        if params.get('edge_enhance', 1.0) > 1.0:
            img = self.process_rgba(img, self.edge_enhance, params['edge_enhance'])
        img = self.process_rgba(img, self.gamma_correction, params.get('gamma', 1.0))

        filename = f"enhanced_{os.path.basename(image_path)}"
        return self.save_image(img, filename)

    def denoise(self, img, strength):
        img_array = np.array(img)
        denoised = cv2.fastNlMeansDenoisingColored(img_array, None, strength, strength, 7, 21)
        return Image.fromarray(denoised)

    def adjust_brightness_contrast(self, img, brightness, contrast):
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(brightness)
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(contrast)

    def enhance_color(self, img, color, saturation):
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(color)
        enhancer = ImageEnhance.Color(img)
        return enhancer.enhance(saturation)

    def shift_hue(self, img, hue_shift):
        img_hsv = img.convert('HSV')
        h, s, v = img_hsv.split()
        h = h.point(lambda x: (x + int(hue_shift * 255 / 360)) % 256)
        img_hsv = Image.merge('HSV', (h, s, v))
        return img_hsv.convert('RGB')

    def sharpen(self, img, sharpness):
        enhancer = ImageEnhance.Sharpness(img)
        return enhancer.enhance(sharpness)

    def edge_enhance(self, img, strength):
        enhanced = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
        return Image.blend(img, enhanced, strength - 1.0)

    def gamma_correction(self, img, gamma):
        img_array = np.array(img)
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        return Image.fromarray(cv2.LUT(img_array, table))