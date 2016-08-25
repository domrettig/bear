from setuptools import setup, find_packages

entry_points = {
  'console_scripts': [
    'bear = bear.main:main'
  ]
}

setup(name='bear',
      version='0.1',
      packages=find_packages(),
      entry_points=entry_points)