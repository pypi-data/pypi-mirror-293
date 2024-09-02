from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "simple-video-to-skeletal-animation",
    version = "0.1",
    description = "This package will allow you to provide a video and get an animated skeleton",
    # py_modules = [ "skelly" ],
    # package_dir = { '' : "simple-video-to-skeletal-animation" },
    packages=["skelly"],
    classifiers = [
        # "Development Status :: 5 - Production/Stable",
        # "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        # "Operating System :: OS Independent",
        # "Programming Language :: Python",
        # "Programming Language :: Python :: 3"
    ],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    install_requires = [ 
        # "numba ",
        # "numpy ",
        # "pandas"
    ],
    url = "https://github.com/professorcode1/simple-video-to-skeletal-animation",
    author = "Raghav Kumar",
    author_email = "raghkum2000@gmail.com"

)