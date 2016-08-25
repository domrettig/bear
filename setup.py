from setuptools import setup, find_packages

entry_points = {
  'console_scripts': [
    'bear = main:main'
  ]
}

setup(name='bear',
      version='0.1.0',
      packages=find_packages(),
      entry_points=entry_points)