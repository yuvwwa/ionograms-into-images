from setuptools import setup, find_packages

setup(
    name="ionimage",
    version="0.0.1",
    author="Yulia Kravtsova",
    packages=find_packages(),
    install_requires=[
        'ionarray>=0.0.18',
        'ionread_python>=0.0.16',
        'numpy>=2.3.1',
        'matplotlib>=3.10.3'
    ],
    package_dir={
        'ionimage': '.',
    },
)
