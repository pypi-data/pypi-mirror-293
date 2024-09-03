import os
import pathlib
from distutils.core import setup
from setuptools import find_packages
from pinecore.utils.pkg import version


def get_readme_description(path: str = os.path.join(os.getcwd(), 'README.md')):
    """
    Get long description from readme file.
    """
    path = pathlib.Path(path).expanduser().resolve()
    with open(path, encoding='utf-8') as file:
        description = file.read()
    return description


setup(
    name='pyrefactoring',
    version=version.from_git(),
    packages=find_packages(),
    license='Copyright (c) 2024 Hieu Pham.',
    zip_safe=True,
    description='Restructuring existing Python source from a mess into clean code and flexible design.',
    long_description=get_readme_description(),
    long_description_content_type='text/markdown',
    author='Hieu Pham',
    author_email='64821726+hieupth@users.noreply.github.com',
    url='https://github.com/hieupth/pyrefactor',
    keywords=[],
    install_requires=['pydantic', 'networkx', 'pandas', 'rawpy', 'pillow_heif'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3'
    ],
)
