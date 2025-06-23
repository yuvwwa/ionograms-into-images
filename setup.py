from setuptools import setup, find_packages

setup(
    name="ionograms_into_images",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'numpy>=2.3.1',
        'matplotlib>=3.10.3',
        'ionread_python'
    ],
    author="Yulia Kravtsova",
    author_email="yuvwwa@gmail.com",
    description="Library for ionogram visualization and processing",
    url="https://github.com/yuvwwa/ionograms-into-images.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={
        'ionograms_into_images': '.',
    },
    python_requires='>=3.7',
)