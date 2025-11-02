from setuptools import setup, find_packages

setup(
    name="ionimage",
    version="0.0.1",
    author="Yulia Kravtsova",
    packages=find_packages(),
    install_requires=[
        'ionarray>=0.0.18',
        'ionread_python>=0.0.16',
        'numpy>=1.26.4',
        'matplotlib>=3.4.1'
    ],
    package_dir={
        'ionimage': '.',
    },
)
