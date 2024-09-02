# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rechip8', 'rechip8.core']

package_data = \
{'': ['*'], 'rechip8': ['bin/*', 'static/*']}

install_requires = \
['pygame>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'rechip8',
    'version': '1.4.1',
    'description': 'A CHIP-8 Emulator written in Python.',
    'long_description': '<p align="center"> <img src="https://raw.githubusercontent.com/mooncell07/reChip8/master/docs/img/invader.png" height=100> </p>\n\n<h1 align="center"> <a href="https://mooncell07.github.io/reChip8/">re:Chip8</a> </h1>\n<h2 align="center">\n<img alt="Stargazers" src="https://img.shields.io/github/stars/mooncell07/reChip8?style=for-the-badge&logo=starship&color=C9CBFF&logoColor=D9E0EE&labelColor=302D41">\n<img alt="Issues" src="https://img.shields.io/github/issues/mooncell07/reChip8?style=for-the-badge&logo=gitbook&color=B5E8E0&logoColor=D9E0EE&labelColor=302D41">\n<img alt="Releases" src="https://img.shields.io/github/license/mooncell07/reChip8?style=for-the-badge&logo=github&color=F2CDCD&logoColor=D9E0EE&labelColor=302D41"/>\n</h2>\n\nre:Chip8 (Formerly: Lemon.pie) is a **[CHIP-8](https://en.wikipedia.org/wiki/CHIP-8)** Emulator written in Python using Pygame.\nThis project aims at implementing the classic variant of CHIP-8 Virtual Machine. Currently a Work in Progress.\n\n## Demo\n\n![CHIP-8 Logo](https://raw.githubusercontent.com/mooncell07/reChip8/master/docs/img/chip8-logo.png)\n\n![PONG](https://raw.githubusercontent.com/mooncell07/reChip8/master/docs/img/gameplay-pong.png)\n\n![Animal Race](https://raw.githubusercontent.com/mooncell07/reChip8/master/docs/img/gameplay-animal-race.png)\n\nUsage and more info is available on [re:Chip8](https://mooncell07.github.io/reChip8/).\n',
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
