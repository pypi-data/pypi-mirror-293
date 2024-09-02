from setuptools import setup, find_packages

setup(
    name='existrike',
    version='0.1.3',
    author='RADNET64',
    author_email='radnet@tutamail.com',
    description='Framework for pentesting',
    packages=find_packages(),
    include_package_data=True,  # Inclui arquivos definidos em MANIFEST.in
    install_requires=[
        'requests',
        'aiohttp',
        'colorama',
        'tqdm'
    ],
    entry_points={
        'console_scripts': [
            'existrike = existrike.main:main'
        ]
    },
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
