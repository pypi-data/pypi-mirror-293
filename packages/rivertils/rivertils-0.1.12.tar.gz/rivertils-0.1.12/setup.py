# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rivertils']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-translate==3.9.0']

setup_kwargs = {
    'name': 'rivertils',
    'version': '0.1.12',
    'description': 'utilities commonly used by rivers cuomo',
    'long_description': "# Rivertils\n\nScripts that are imported by packages you've deployed to pypi\n\n## To publish to PyPi \n\n- increment the version number in pyproject.toml\n- poetry build\n- poetry publish --username __token__ --password (use the token in the pypi account) [text](https://pypi.org/manage/account/token/)\nSet your username to __token__\nSet your password to the token value, including the pypi- prefix\n- git commit and push",
    'author': 'Rivers Cuomo',
    'author_email': 'riverscuomo@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
