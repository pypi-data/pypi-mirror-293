from setuptools import setup, find_packages

setup(
  name='ledoc-ui-bundle',
  version='0.1.0',
  packages=find_packages(),
  package_data={'dist': ['*']},
  zip_safe=False
)
