#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'ascii-animator',
        version = '0.2.1',
        description = 'A simple ASCII art animator',
        long_description = '# ascii-animator\n[![build+test](https://github.com/soda480/ascii-animator/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/soda480/ascii-animator/actions/workflows/main.yml)\n[![complexity](https://img.shields.io/badge/complexity-A-brightgreen)](https://radon.readthedocs.io/en/latest/api.html#module-radon.complexity)\n[![vulnerabilities](https://img.shields.io/badge/vulnerabilities-None-brightgreen)](https://pypi.org/project/bandit/)\n[![PyPI version](https://badge.fury.io/py/ascii-animator.svg)](https://badge.fury.io/py/ascii-animator)\n[![python](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-teal)](https://www.python.org/downloads/)\n\nA simple ASCII text animator.\n\nThe `ascii-art-animator` CLI will take as input a GIF image, extract all the frames from it, convert each frame to ASCII art using [ascii-magic](https://pypi.org/project/ascii-magic/), then display each frame to the terminal using [list2term](https://pypi.org/project/list2term/).\n\n### Installation\n```bash\npip install ascii_animator\n```\n\n### Usage\n```\nusage: ascii-art-animator [-h] [-s SPEED] [-f FILE] [-d] [-a] [-m MAX_LOOPS] [-c COLUMNS]\n\nAscii Art Animator from GIF\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -s SPEED, --speed SPEED\n                        speed of the animation: very_slow, slow, normal, fast (default normal)\n  -f FILE, --file FILE  the path to a gif file\n  -d, --debug           display debug messages to stdout\n  -a, --show_axis       display the grid axis\n  -m MAX_LOOPS, --max_loops MAX_LOOPS\n                        maximum number of loops, set to 0 to loop through image until keyboard interrupt (default 1)\n  -c COLUMNS, --columns COLUMNS\n                        the number of characters per row (default 150)\n```\n\n### Examples\n\n#### ASCII Art Animator\n\nUse `ascii-art-animator` to convert the following GIF image to an ascii animation and demonstrate the use of the optional arguments.\n* show x and y axis\n* loop through the image 3 times \n* set columns to 100 characters\n\n```bash\nascii-art-animator -f docs/images/marcovich.gif -a -m 3 -c 100\n```\n**input**\n\n![example](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/marcovich.gif)\n\n**output**\n\n![example](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/marcovich-exec.gif)\n\n### `Animation` class\n\nUse the Animation class to create your own animations.\n\n#### [Binary Search Animation](https://github.com/soda480/ascii-animator/blob/main/examples/example5.py)\n\nA binary search is a search algorithm that finds a specific value in a sorted array by repeatedly dividing the search interval in half.\n\n![example](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/example5.gif)\n\n#### [Selection Sort Animation](https://github.com/soda480/ascii-animator/blob/main/examples/example4.py)\n\nA selection sort search is a simple and efficient sorting algorithm that works by repeatedly selecting the smallest (or largest) element from the unsorted portion of the list and moving it to the sorted portion of the list.\n\n![example](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/example4.gif)\n\nHere is another [example](https://github.com/soda480/ascii-animator/blob/main/examples/example6.py) of a selection sort animation this time using vertical bars.\n\n![example](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/example6.gif)\n\n#### [Equalizer Bars Animation](https://github.com/soda480/ascii-animator/blob/main/examples/example2.py)\n\nAn animation for symmetrical equalizer bars.\n\n![example](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/example2.gif)\n\n#### [Matrix Animation](https://github.com/soda480/ascii-animator/blob/main/examples/example3.py)\n\nA Matrix animation.\n\n![example](https://raw.githubusercontent.com/soda480/ascii-animator/main/docs/images/example3.gif)\n\n#### [Game-Of-Life](https://github.com/soda480/game-of-life)\n\nA Conway Game-Of-Life implementation that uses `ascii_animator` to display the game to the terminal.\n\n### Development\n\nClone the repository and ensure the latest version of Docker is installed on your development server.\n\nBuild the Docker image:\n```bash\ndocker image build \\\n-t ascii-animator:latest .\n```\n\nRun the Docker container:\n```bash\ndocker container run \\\n--rm \\\n-it \\\n-v $PWD:/code \\\nascii-animator:latest \\\nbash\n```\n\nExecute the build:\n```sh\npyb -X\n```\n',
        long_description_content_type = 'text/markdown',
        classifiers = [
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.12'
        ],
        keywords = '',

        author = 'Emilio Reyes',
        author_email = 'soda480@gmail.com',
        maintainer = '',
        maintainer_email = '',

        license = 'Apache License, Version 2.0',

        url = 'https://github.com/soda480/ascii-animator',
        project_urls = {},

        scripts = [],
        packages = ['ascii_animator'],
        namespace_packages = [],
        py_modules = [],
        entry_points = {
            'console_scripts': ['ascii-art-animator = ascii_animator.cli:main']
        },
        data_files = [],
        package_data = {},
        install_requires = [
            'list2term~=0.1.0',
            'ascii-magic~=1.6'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
