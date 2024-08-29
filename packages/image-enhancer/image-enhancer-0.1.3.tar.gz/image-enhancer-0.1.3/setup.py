from setuptools import setup, find_packages

setup(
    name="image-enhancer",
    version="0.1.3",  # publish.sh에서 자동으로 업데이트됩니다
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "numpy",
        "Pillow",
        "requests",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A package for enhancing images with various filters and adjustments",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/image-enhancer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_data={
        'image_enhancer': ['*'],
    },
    exclude_package_data={
        '': ['publish.sh']
    },
)