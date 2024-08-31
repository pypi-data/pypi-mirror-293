from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="image-scraper-tool",  # Unique name for the package
    version="0.1.4",  # Version number
    packages=find_packages(),  # Automatically find package directories
    install_requires=[
        "selenium",
        "pandas",
    ],
    entry_points={
        'console_scripts': [
            'image-scraper=image_scraper_tool.custom_image_extractor:google_image_search',
        ],
    },
    author="Negin Babaiha, Philipp Münker",
    author_email="negin.babaiha@scai.fraunhofer.de",
    description="A package to search Google Images and extract image URLs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NeginBabaiha/image-url-extraction",  # Replace with your repo URL
    project_urls={
        "Bug Tracker": "https://github.com/NeginBabaiha/image-url-extraction/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
