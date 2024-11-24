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
        "pandas",
        "pathlib",
        "pyarrow",
        "python-dateutil",
    ),
    entry_points={
        "console_scripts": [
            "musiclists = src.scripts.musiclists:cli",
        ],
    },
)
