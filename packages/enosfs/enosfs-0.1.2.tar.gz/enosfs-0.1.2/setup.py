from setuptools import setup, find_packages
setup(
    name="enosfs",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "google-cloud-bigtable",
    ],
    entry_points={
        'console_scripts': [
            'enosfs=enosfs.cli:main',
        ],
    },
    author="Mrinal Gosain",
    author_email="mrinal_gosain@intuit.com",
    description="A CLI tool for operating ENOS Online Store",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://git.rsglab.com/enosfs",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)