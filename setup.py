import setuptools

setuptools.setup(
    name="musiclists",
    version="0.1",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=(
        "click",
        "click_help_colors",
        "pathlib",
        "python-dateutil",
        "pypi-json",
    ),
    entry_points={
        "console_scripts": [
            "musiclists = src.scripts.musiclists:cli",
        ],
    },
)
