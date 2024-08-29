import os
import numpy as np
import pytest
from PIL import Image
import requests
from image_enhancer.enhancer import ImageEnhancer

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'test_output')

@pytest.fixture(scope="module")
def enhancer():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    return ImageEnhancer(output_dir=OUTPUT_DIR)

# @pytest.fixture
# def sample_image():
#     img = Image.new('RGB', (100, 100), color='red')
#     img_path = os.path.join(OUTPUT_DIR, "sample_image.png")
#     img.save(img_path)
#     return img_path

@pytest.fixture
def url_image():
    return "https://cdn.pixabay.com/photo/2024/07/08/17/54/model-8881740_1280.jpg"

# class TestLocalImage:
#     def test_load_image_local(self, enhancer, sample_image):
#         loaded_image = enhancer.load_image(sample_image)
#         assert isinstance(loaded_image, Image.Image)
#         assert loaded_image.size == (100, 100)

#     def test_basic_enhancements(self, enhancer, sample_image):
#         params = {
#             "brightness": 1.2,
#             "contrast": 1.1,
#             "saturation": 1.2,
#             "sharpness": 1.5,
#             "denoise_strength": 5,
#             "gamma": 1.2,
#             "edge_enhance": 1.5,
#             "hue_shift": 10
#         }
#         enhanced_path = enhancer.enhance(sample_image, params, "test_basic_enhancements.png")
#         assert os.path.exists(enhanced_path)
#         enhanced_img = Image.open(enhanced_path)
#         assert isinstance(enhanced_img, Image.Image)

#     def test_resize(self, enhancer, sample_image):
#         params = {"width": 50, "height": 50}
#         enhanced_path = enhancer.enhance(sample_image, params, "test_resize.png")
#         enhanced_img = Image.open(enhanced_path)
#         assert enhanced_img.size == (50, 50)

#     def test_rotate(self, enhancer, sample_image):
#         params = {"rotation_angle": 90}
#         enhanced_path = enhancer.enhance(sample_image, params, "test_rotate.png")
#         enhanced_img = Image.open(enhanced_path)
#         assert enhanced_img.size == (100, 100)  # Size should remain the same for 90-degree rotation

#     def test_flip(self, enhancer, sample_image):
#         params = {"flip_direction": "horizontal"}
#         enhanced_path = enhancer.enhance(sample_image, params, "test_flip.png")
#         enhanced_img = Image.open(enhanced_path)
#         assert enhanced_img.size == (100, 100)

#     def test_crop(self, enhancer, sample_image):
#         params = {"crop_box": (25, 25, 75, 75)}
#         enhanced_path = enhancer.enhance(sample_image, params, "test_crop.png")
#         enhanced_img = Image.open(enhanced_path)
#         assert enhanced_img.size == (50, 50)

#     def test_watermark(self, enhancer, sample_image):
#         params = {
#             "watermark_text": "Test",
#             "watermark_position": (10, 10)
#         }
#         enhanced_path = enhancer.enhance(sample_image, params, "test_watermark.png")
#         enhanced_img = Image.open(enhanced_path)
#         # Check if any pixel is different from the original red color
#         assert any(enhanced_img.getpixel((x, y)) != (255, 0, 0) 
#                    for x in range(100) for y in range(100))

#     def test_filter(self, enhancer, sample_image):
#         params = {"filter": "emboss"}
#         enhanced_path = enhancer.enhance(sample_image, params, "test_filter.png")
#         enhanced_img = Image.open(enhanced_path)
#         assert isinstance(enhanced_img, Image.Image)

#     def test_hsl_adjustment(self, enhancer, sample_image):
#         params = {"hue": 1.1, "saturation": 1.2, "lightness": 0.9}
#         enhanced_path = enhancer.enhance(sample_image, params, "test_hsl_adjustment.png")
#         enhanced_img = Image.open(enhanced_path)
#         assert isinstance(enhanced_img, Image.Image)

class TestURLImage:
    def test_load_image_url(self, enhancer, url_image):
        loaded_image = enhancer.load_image(url_image)
        assert isinstance(loaded_image, Image.Image)
        assert loaded_image.size[0] > 0 and loaded_image.size[1] > 0

    def test_basic_enhancements(self, enhancer, url_image):
        params = {
            "brightness": 1.2,
            "contrast": 1.1,
            "saturation": 1.2,
            "sharpness": 1.5,
            "gamma": 1.2,
            "hue_shift": 10,
            "edge_enhance": 1.2
        }
        enhanced_path = enhancer.enhance(url_image, params, "test_url_basic_enhancements.jpg")
        assert os.path.exists(enhanced_path)
        enhanced_img = Image.open(enhanced_path)
        assert isinstance(enhanced_img, Image.Image)

    def test_resize(self, enhancer, url_image):
        params = {"width": 800, "height": 600}
        enhanced_path = enhancer.enhance(url_image, params, "test_url_resize.jpg")
        enhanced_img = Image.open(enhanced_path)
        assert enhanced_img.size == (800, 600)

    def test_rotate(self, enhancer, url_image):
        params = {"rotation_angle": 90}
        enhanced_path = enhancer.enhance(url_image, params, "test_url_rotate.jpg")
        enhanced_img = Image.open(enhanced_path)
        original_img = enhancer.load_image(url_image)
        assert enhanced_img.size == (original_img.size[1], original_img.size[0])  # Width and height should be swapped

    def test_flip(self, enhancer, url_image):
        params = {"flip_direction": "horizontal"}
        enhanced_path = enhancer.enhance(url_image, params, "test_url_flip.jpg")
        assert os.path.exists(enhanced_path)

    def test_crop(self, enhancer, url_image):
        original_img = enhancer.load_image(url_image)
        original_width, original_height = original_img.size
        params = {"crop_box": (0, 0, original_width // 2, original_height // 2)}
        enhanced_path = enhancer.enhance(url_image, params, "test_url_crop.jpg")
        enhanced_img = Image.open(enhanced_path)
        assert enhanced_img.size == (original_width // 2, original_height // 2)

    def test_watermark(self, enhancer, url_image):
        params = {
            "watermark_text": "Test",
            "watermark_position": (10, 10)
        }
        enhanced_path = enhancer.enhance(url_image, params, "test_url_watermark.jpg")
        assert os.path.exists(enhanced_path)

    def test_filter(self, enhancer, url_image):
        params = {"filter": "emboss"}
        enhanced_path = enhancer.enhance(url_image, params, "test_url_filter.jpg")
        assert os.path.exists(enhanced_path)

    def test_hsl_adjustment(self, enhancer, url_image):
        params = {"hue": 1.1, "saturation": 1.2, "lightness": 0.9}
        enhanced_path = enhancer.enhance(url_image, params, "test_url_hsl.jpg")
        assert os.path.exists(enhanced_path)

    def test_load_image_invalid_url(self, enhancer):
        invalid_url = "https://example.com/nonexistent_image.jpg"
        with pytest.raises(ValueError):
            enhancer.load_image(invalid_url)

def test_batch_process(enhancer, url_image):
    params = {"brightness": 1.2, "contrast": 1.1}
    batch_results = enhancer.batch_process([url_image, url_image], params, ["test_url_batch_1.jpg", "test_url_batch_2.jpg"])
    assert len(batch_results) == 2
    for result in batch_results:
        assert os.path.exists(result)

def test_compare_before_after(enhancer, url_image):
    params = {"brightness": 1.2, "contrast": 1.1}
    comparison_path = enhancer.compare_before_after(url_image, params, "test_url_compare.jpg")
    assert os.path.exists(comparison_path)
    comparison_img = Image.open(comparison_path)
    original_img = enhancer.load_image(url_image)
    assert comparison_img.size[0] == original_img.size[0] * 2  # Width should be doubled

def test_output_directory():
    assert os.path.exists(OUTPUT_DIR)
    files = os.listdir(OUTPUT_DIR)
    assert len(files) > 0
    print(f"\nTotal files in output directory: {len(files)}")
    for file in files:
        print(f" - {file}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
