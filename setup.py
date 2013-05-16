from setuptools import setup

version = '0.1dev'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
    ])

install_requires = [
    'Django',
    'django-extensions',
    'django-nose',
    'lizard-ui >= 4.0b5',
    ],

tests_require = [
    'nose',
    'coverage',
    'mock',
    ]

setup(name='dbtranslator',
      version=version,
      description="Seamlessly translate Django model fields with Transifex.",
      long_description=long_description,
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
         'Programming Language :: Python',
         'Programming Language :: Python :: 2.7',
         'Development Status :: 3 - Alpha',
         'License :: GPL',
         'Topic :: Software Development :: Internationalization',
         'Framework :: Django',
      ],
      keywords=['django', 'database', 'model', 'translation',
                'internationalization', 'i18n'],
      author='Sander Smits',
      author_email='sander.smits@nelen-schuurmans.nl',
      url='https://github.com/nens/dbtranslator',
      license='GPL',
      packages=['dbtranslator'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'test': tests_require},
      entry_points={
          'console_scripts': [
          ]},
      )
