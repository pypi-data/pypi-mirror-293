# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['odf']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.12.3,<0.13.0']

entry_points = \
{'console_scripts': ['odf = odf.__main__:main']}

setup_kwargs = {
    'name': 'odf',
    'version': '0.0.1',
    'description': 'Open Data Framework CLI',
    'long_description': '# Open Data Framework [CLI]\n',
    'author': 'mykytapavlov',
    'author_email': 'mykytapavlov@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/opendataframework/odf',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
