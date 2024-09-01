# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lemon8', 'lemon8.components']

package_data = \
{'': ['*'], 'lemon8': ['bin/*', 'static/*']}

install_requires = \
['pygame>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'lemon8',
    'version': '1.3.12',
    'description': 'A CHIP-8 emulator written in Python.',
    'long_description': '<p align="center"> <img src="https://raw.githubusercontent.com/mooncell07/lemon.pie/master/docs/img/lemon.png" height=100> </p>\n\n<h1 align="center"> <a href="https://mooncell07.github.io/lemon.pie/">Lemon.pie</a> </h1>\n<h2 align="center">\n<img alt="Stargazers" src="https://img.shields.io/github/stars/mooncell07/lemon.pie?style=for-the-badge&logo=starship&color=C9CBFF&logoColor=D9E0EE&labelColor=302D41">\n<img alt="Issues" src="https://img.shields.io/github/issues/mooncell07/lemon.pie?style=for-the-badge&logo=gitbook&color=B5E8E0&logoColor=D9E0EE&labelColor=302D41">\n<img alt="Releases" src="https://img.shields.io/github/license/mooncell07/lemon.pie?style=for-the-badge&logo=github&color=F2CDCD&logoColor=D9E0EE&labelColor=302D41"/>\n</h2>\n\nLemon is a **[CHIP-8](https://en.wikipedia.org/wiki/CHIP-8)** Emulator written in Python using Pygame.\nThis library aims at implementing the original and classic varient of CHIP-8 Virtual Machine. Currently a Work in Progress.\n\nThis project is the successor of my very first implementation of the VM (Now archived) Trace-Fractal.\n\n## Screencaps\n\n![CHIP-8 Logo](https://raw.githubusercontent.com/mooncell07/lemon.pie/master/docs/img/chip8-logo.png)\n\n![PONG](https://raw.githubusercontent.com/mooncell07/lemon.pie/master/docs/img/gameplay-pong.png)\n\n![Animal Race](https://raw.githubusercontent.com/mooncell07/lemon.pie/master/docs/img/gameplay-animal-race.png)\n\nUsage and more info can be found on [Lemon.pie](https://mooncell07.github.io/lemon.pie/).\n',
    'author': 'mooncell07',
    'author_email': '80042274+mooncell07@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
