# ImageEnhancer

ImageEnhancer는 다양한 이미지 처리 기능을 제공하는 Python 패키지입니다. 로컬 이미지 파일과 URL의 이미지를 모두 처리할 수 있으며, 노이즈 제거, 밝기/대비 조정, 색상 강화, 선명도 증가, 크기 조정, 회전 등 다양한 기능을 제공합니다.

## 설치

pip를 사용하여 ImageEnhancer를 설치할 수 있습니다:

```bash
pip install image-enhancer
```

## 사용법

기본적인 사용법은 다음과 같습니다:

```python
from image_enhancer import ImageEnhancer

enhancer = ImageEnhancer(output_dir="enhanced_images")

# 로컬 이미지 파일 처리
enhanced_path = enhancer.enhance("path/to/local/image.jpg", {
    "brightness": 1.2,
    "contrast": 1.1,
    "sharpness": 1.5
}, "enhanced_local_image.jpg")

# URL의 이미지 처리
url = "https://example.com/image.jpg"
enhanced_path = enhancer.enhance(url, {
    "denoise_strength": 10,
    "saturation": 1.2,
    "gamma": 1.1
}, "enhanced_url_image.jpg")

print(f"Enhanced image saved at: {enhanced_path}")
```

## 주요 기능

ImageEnhancer는 다음과 같은 주요 기능을 제공합니다:

- 노이즈 제거 (`denoise_strength`)
- 밝기 조정 (`brightness`)
- 대비 조정 (`contrast`)
- 색상 강화 (`color`)
- 채도 조정 (`saturation`)
- 색조 이동 (`hue_shift`)
- 선명도 증가 (`sharpness`)
- 엣지 강화 (`edge_enhance`)
- 감마 보정 (`gamma`)
- 크기 조정 (`width`, `height`)
- 회전 (`rotation_angle`)
- 뒤집기 (`flip_direction`)
- 자르기 (`crop_box`)
- 워터마크 추가 (`watermark_text`, `watermark_position`)
- 필터 적용 (`filter`)
- HSL 조정 (`hue`, `saturation`, `lightness`)

각 기능은 `enhance` 메서드에 전달되는 파라미터 딕셔너리를 통해 조절할 수 있습니다.

## 고급 기능

### 배치 처리

여러 이미지를 동시에 처리할 수 있습니다:

```python
enhancer = ImageEnhancer()
params = {"brightness": 1.2, "contrast": 1.1}
image_paths = ["image1.jpg", "image2.jpg", "image3.jpg"]
output_names = ["enhanced1.jpg", "enhanced2.jpg", "enhanced3.jpg"]
results = enhancer.batch_process(image_paths, params, output_names)
```

### 처리 전후 비교

원본 이미지와 처리된 이미지를 나란히 비교할 수 있습니다:

```python
comparison_path = enhancer.compare_before_after("original.jpg", params, "comparison.jpg")
```

## 예제

```python
enhancer = ImageEnhancer()

params = {
    "denoise_strength": 5,
    "brightness": 1.2,
    "contrast": 1.1,
    "color": 1.1,
    "saturation": 1.2,
    "hue_shift": 10,
    "sharpness": 1.5,
    "edge_enhance": 1.2,
    "gamma": 1.1,
    "width": 800,
    "height": 600,
    "rotation_angle": 45,
    "flip_direction": "horizontal",
    "crop_box": (100, 100, 700, 500),
    "watermark_text": "Copyright 2024",
    "watermark_position": (50, 50),
    "filter": "emboss"
}

enhanced_path = enhancer.enhance("https://example.com/image.jpg", params, "enhanced_image.jpg")
print(f"Enhanced image saved at: {enhanced_path}")
```

## 프로젝트 구조

```
image-enhancer/
├── image_enhancer/
│   ├── __init__.py
│   └── enhancer.py
├── tests/
│   └── test_enhancer.py
├── README.md
├── setup.py
└── requirements.txt
```

## 기여하기

버그 리포트, 기능 제안, 풀 리퀘스트 등 모든 기여를 환영합니다. 기여하기 전에 프로젝트의 이슈 트래커를 확인해 주세요.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.
