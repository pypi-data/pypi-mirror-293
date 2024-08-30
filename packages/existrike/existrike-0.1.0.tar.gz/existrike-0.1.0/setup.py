from setuptools import setup, find_packages

setup(
    name="existrike",
    version="0.1.0",
    packages=find_packages(),  # Inclui todos os pacotes e subpacotes
    install_requires=[
        'aiohttp',
        'colorama',
        'requests',
        'tqdm',
    ],
    entry_points={
        'console_scripts': [
            'existrike=ExiStrike.existrike:main',  # Atualize o módulo e função
        ],
    },
    author="RADNET64",
    author_email="radnet@tutamail.com",
    description="Beta version of the ExiStrike framework, this is not the final version, remembering that we are not responsible for your actions!",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RADNET64/Exploiter-alphatest",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
