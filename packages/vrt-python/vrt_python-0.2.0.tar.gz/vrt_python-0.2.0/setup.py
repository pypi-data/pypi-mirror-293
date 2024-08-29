from setuptools import setup, find_packages

setup(
    name="vrt_python",  # This will be the package name used in pip
    version="0.2.0",
    author="Vladimir Shkodin",
    author_email="v.s.shkodin@gmail.com",
    description="A CLI tool for visual regression testing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vshkodin/vrt-python",
    packages=find_packages(),
    install_requires=[
        "Pillow==10.3.0",
        "numpy==1.26.4"
    ],
    entry_points={
        'console_scripts': [
            'vrt=vrt_python.cli:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
