# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bluebuttonpy',
 'bluebuttonpy.core',
 'bluebuttonpy.documents',
 'bluebuttonpy.parsers',
 'bluebuttonpy.parsers.ccda']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bluebuttonpy',
    'version': '0.2.0',
    'description': '',
    'long_description': '',
    'author': 'Srikanth Srungarapu',
    'author_email': 'srikanth235@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
