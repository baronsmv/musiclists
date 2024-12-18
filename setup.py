#!/usr/bin/env python3

import setuptools

setuptools.setup(
    name="musiclists",
    version="0.1",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=(
        "bs4",
        "click",
        "click_help_colors",
        "m3u8",
        "mutagen",
        "polars",
    ),
    entry_points={
        "console_scripts": [
            "musiclists = src.scripts.musiclists:cli",
        ],
    },
)
