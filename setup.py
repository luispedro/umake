from setuptools import setup

exec(compile(open('umake/umake_version.py').read(),
             'umake/umake_version.py', 'exec'))

long_description = open('README.md', encoding='utf-8').read()

setup(name='umake',
      version=__version__,
      description='Universal Make',
      long_description = long_description,
      long_description_content_type = 'text/markdown',
      classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
      ],
      url='https://github.com/luispedro/umake',
      author='Luis Pedro Coelho',
      author_email='luis@luispedro.org',
      license='MIT',
      packages = ['umake'],
      entry_points={
            'console_scripts': ['umake=umake.main:main'],
      }
)

