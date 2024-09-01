from setuptools import setup, find_packages

install_requires = \
['pydantic>=0.32.2']



# setup(
# name='nace',
# version='0.0.6',
# author='ucabdv1',
# author_email='ucabdv1@ucl.ac.uk',
# description='A test to see how pypi packages work',
# packages=find_packages(),
# classifiers=[
# 'Programming Language :: Python :: 3',
# 'License :: OSI Approved :: MIT License',
# 'Operating System :: OS Independent',
# ],
# python_requires='>=3.10',
# )

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README_pypi.md").read_text()


setup_kwargs = {
    'name': 'nace',
    'version': '0.0.7',
    'description': 'A re-implementation of NACE without global variables etc.',
    'long_description': long_description,
    'long_description_content_type':'text/markdown',
    'author': 'ucabdv1',
    'author_email': 'ucabdv1@ucl.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': find_packages(),
    # 'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10',
    'classifiers':[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            ]
}


setup(**setup_kwargs)