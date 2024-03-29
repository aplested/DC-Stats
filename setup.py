from setuptools import setup

setup(name='dcstats',
      version='0.3.2',
      description="DC's lab statistical tools",
      url='https://github.com/aplested/DC-Stats',
      keywords='randomisation hedges fieller',
      author='Andrew Plested',
      author_email='',
      license='MIT',
      packages=['dcstats'],
      install_requires=[
          'numpy',
          'pandas',
          'matplotlib',
          'PyQt5',
          'openpyxl'
      ],
      zip_safe=False)
