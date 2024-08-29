# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csrspy']

package_data = \
{'': ['*']}

install_requires = \
['pyproj>=3.6,<4.0']

setup_kwargs = {
    'name': 'csrspy',
    'version': '0.6.0',
    'description': 'ITRF/NAD83CSRS coordinate transforms in Python',
    'long_description': 'None',
    'author': 'Taylor Denouden',
    'author_email': 'taylor.denouden@hakai.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
