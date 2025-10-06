import subprocess
import setuptools
from setuptools.extension import Extension
from setuptools.command.build_ext import build_ext


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mjhand",
    use_scm_version={'local_scheme': 'no-local-version'},
    author="Shintaro Minami",
    description="Japanese Riichi Mahjong Win-Hand Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ShintaroMinami/MJHand",
    ext_modules=[Extension('', [])],
    packages=setuptools.find_packages(),
    include_package_data=True,
    setup_requires=['setuptools_scm'],
    install_requires=[
        'numpy',
        'tqdm',
        'mahjong',
        ],
    scripts=[],

)