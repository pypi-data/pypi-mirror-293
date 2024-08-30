from setuptools import setup, find_packages


setup(
    name="folumo",
    version='0.1.9.4',
    author="Folumo (Ominox_)",
    author_email="<ominox_@folumo.com>",
    description='Multipurpose lib',
    long_description_content_type="text/markdown",
    long_description='',
    packages=find_packages(),
    install_requires=['pillow', 'pygame', 'requests'],
    keywords=['python', 'gui', 'app', 'game'],
    classifiers=[
        #"Development Status :: 2 - Developing",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)


"""

TODO:
  add functions that help with repetitive things such as buttons and fonts to canvases ...
  canter X, center Y, both, offsets
  make it so that its able to go on other screen sizes
  make it recalculate mouse position based on scale factor
  make function that displays newest updates
  make canvases scalable, + other filters
"""