from setuptools import setup, find_packages

setup(
    name="drawscape-factorio",
    version="0.11",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            'drawscape-factorio=drawscape_factorio.main:main',
        ],
    },
)