from setuptools import setup, find_packages

setup(
    name="trackdir",
    version="1.0.0",
    description="A package to track file changes in a directory",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="MrFidal",
    author_email="mrfidal@proton.me",
    url="https://github.com/bytebreach/trackdir",
    packages=find_packages(),
    install_requires=[
        "watchdog"
    ],
    entry_points={
        'console_scripts': [
            'trackpath = trackdir.tracker:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
