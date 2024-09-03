from setuptools import setup, find_packages

setup(
    name="chiga",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "chiga=chiga.cli:main",
        ],
    },
    install_requires=[
        # List any package dependencies here
    ],
    author="AHMED FAHIM",
    author_email="amhex01@gmail.com",
    description="A custom package installer that manages requirements.txt",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/CHiigaw/chiga",
)
