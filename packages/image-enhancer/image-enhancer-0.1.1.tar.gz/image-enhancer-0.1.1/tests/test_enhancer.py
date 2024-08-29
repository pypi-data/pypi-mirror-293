import os
import numpy as np
import pytest
from PIL import Image
import requests
from image_enhancer.enhancer import ImageEnhancer

# 고정된 출력 디렉토리 설정
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'test_output')

@pytest.fixture(scope="module")
def enhancer():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    return ImageEnhancer(output_dir=OUTPUT_DIR)

def test_enhance_url_image(enhancer):
    url = "https://cdn.pixabay.com/photo/2024/07/08/17/54/model-8881740_1280.jpg"
    params = {
        "brightness": 1.2,
        "contrast": 1.1,
        "sharpness": 1.5,
        "saturation": 1.2,
        "hue_shift": 10,
        "edge_enhance": 1.2
    }
    
    try:
        enhanced_path = enhancer.enhance(url, params)
        assert os.path.exists(enhanced_path)
        
        # 원본 이미지 저장
        original_img = Image.open(requests.get(url, stream=True).raw)
        original_path = os.path.join(OUTPUT_DIR, "original_url_image.jpg")
        original_img.save(original_path)
        
        print(f"\nOriginal image saved at: {original_path}")
        print(f"Enhanced image saved at: {enhanced_path}")
        
        # 이미지 비교 (옵션)
        original_img = Image.open(original_path)
        enhanced_img = Image.open(enhanced_path)
        assert enhanced_img.size == original_img.size
        
        # 출력 디렉토리의 모든 파일 리스트 출력
        print("\nFiles in output directory:")
        for file in os.listdir(OUTPUT_DIR):
            print(f" - {file}")
        
    except Exception as e:
        pytest.fail(f"Test failed with error: {str(e)}")

@pytest.fixture
def sample_image():
    img = Image.new('RGB', (100, 100), color='red')
    img_path = os.path.join(OUTPUT_DIR, "sample_image.png")
    img.save(img_path)
    return img_path

def test_load_image_local(enhancer, sample_image):
    loaded_image = enhancer.load_image(sample_image)
    assert isinstance(loaded_image, Image.Image)
    assert loaded_image.size == (100, 100)

def test_load_image_url(enhancer):
    url = "https://cdn.pixabay.com/photo/2024/07/08/17/54/model-8881740_1280.jpg"
    loaded_image = enhancer.load_image(url)
    assert isinstance(loaded_image, Image.Image)
    assert loaded_image.size[0] > 0 and loaded_image.size[1] > 0

def test_load_image_invalid_url(enhancer):
    invalid_url = "https://example.com/nonexistent_image.jpg"
    with pytest.raises(requests.exceptions.RequestException):
        enhancer.load_image(invalid_url)

def test_save_image(enhancer):
    img = Image.new('RGB', (100, 100), color='blue')
    saved_path = enhancer.save_image(img, "test.png")
    assert os.path.exists(saved_path)
    assert saved_path.endswith("test.png")

def test_process_rgba(enhancer):
    img = Image.new('RGBA', (100, 100), color=(255, 0, 0, 128))
    processed = enhancer.process_rgba(img, lambda x: x)
    assert processed.mode == 'RGBA'

def test_denoise(enhancer):
    img = Image.fromarray(np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8))
    denoised = enhancer.denoise(img, 10)
    assert isinstance(denoised, Image.Image)

def test_adjust_brightness_contrast(enhancer):
    img = Image.new('RGB', (100, 100), color='gray')
    adjusted = enhancer.adjust_brightness_contrast(img, 1.5, 1.2)
    assert isinstance(adjusted, Image.Image)

def test_enhance_color(enhancer):
    img = Image.new('RGB', (100, 100), color='blue')
    enhanced = enhancer.enhance_color(img, 1.5, 1.2)
    assert isinstance(enhanced, Image.Image)

def test_shift_hue(enhancer):
    img = Image.new('RGB', (100, 100), color='red')
    shifted = enhancer.shift_hue(img, 180)
    assert isinstance(shifted, Image.Image)
    assert shifted.getpixel((0, 0))[0] < 128  # Should be more cyan than red

def test_sharpen(enhancer):
    img = Image.new('RGB', (100, 100), color='gray')
    sharpened = enhancer.sharpen(img, 2.0)
    assert isinstance(sharpened, Image.Image)

def test_edge_enhance(enhancer):
    img = Image.new('RGB', (100, 100), color='gray')
    img.putpixel((50, 50), (255, 255, 255))
    enhanced = enhancer.edge_enhance(img, 2.0)
    assert isinstance(enhanced, Image.Image)

def test_gamma_correction(enhancer):
    img = Image.new('RGB', (100, 100), color='gray')
    corrected = enhancer.gamma_correction(img, 1.5)
    assert isinstance(corrected, Image.Image)

def test_enhance_integration(enhancer, sample_image):
    params = {
        "denoise_strength": 5,
        "brightness": 1.2,
        "contrast": 1.1,
        "color": 1.1,
        "sharpness": 1.5,
        "gamma": 1.2,
        "saturation": 1.2,
        "hue_shift": 10,
        "edge_enhance": 1.5
    }
    enhanced_path = enhancer.enhance(sample_image, params)
    assert os.path.exists(enhanced_path)
    enhanced_img = Image.open(enhanced_path)
    assert isinstance(enhanced_img, Image.Image)
    
    print(f"\nEnhanced image saved at: {enhanced_path}")
    
    # 출력 디렉토리의 모든 파일 리스트 출력
    print("\nFiles in output directory:")
    for file in os.listdir(OUTPUT_DIR):
        print(f" - {file}")

# 새로운 테스트 함수 추가: 출력 디렉토리 확인
def test_output_directory():
    assert os.path.exists(OUTPUT_DIR)
    files = os.listdir(OUTPUT_DIR)
    assert len(files) > 0
    print(f"\nTotal files in output directory: {len(files)}")
    for file in files:
        print(f" - {file}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
