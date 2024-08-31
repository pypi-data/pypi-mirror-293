from setuptools import setup, find_packages

setup(
    name="custom_image_search",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "pandas",
    ],
    entry_points={
        'console_scripts': [
            'custom-image-search=custom_image_search.custom_image_search:custom_image_search',
        ],
    },
    author="Negin Babaiha, Philipp Münker",
    author_email="neginbabaiha@gmail.com",
    description="A package to search custom Images and extract image URLs.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
