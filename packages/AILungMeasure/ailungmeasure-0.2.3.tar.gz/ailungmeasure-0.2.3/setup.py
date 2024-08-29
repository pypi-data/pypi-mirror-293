# setup.py
from setuptools import setup, find_packages
import os

# Read the contents of the README file
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="AILungMeasure",
    version="0.2.3",  # Update this version number
    packages=find_packages(include=["AILungMeasure", "AILungMeasure.*"]),
    install_requires=[
        "torch",
        "Pillow",
        "torchvision",
        "matplotlib",
        "opencv-python",
        "numpy",
        "imutils",
        "gdown",
        "pydicom",
    ],
    author="Mostafa Ismail",
    author_email="mostafa.ismail.k@gmail.com",
    description="Automated lung size measurements using deep learning and computer vision on portable chest radiographs.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    # url="https://github.com/MostafaI/AILungMeasure",  # Update with your project URL
    
    url="https://doi.org/10.1016/j.ajt.2024.08.015", # Direct DOI link 
    project_urls={"DOI": "https://doi.org/10.1016/j.ajt.2024.08.015"}, # Adding DOI under project_urls },
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    package_data={
        '': ['Images/*.png', 'README.md'],
    },
    license="Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International",
)
