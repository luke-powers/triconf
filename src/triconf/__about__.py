__all__ = [
    '__author__', '__author_email__', '__classifiers__', '__desc__', '__license__',
    '__package_name__', '__scripts__', '__team__', '__url__', '__version__',
]

__author__ = 'Luke Powers'
__author_email__ = 'luke.powers@openx.com'
__classifiers__ = ['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: Apache Software License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities',
                   'Private :: Do Not Upload' # Do not allow this package to be uploaded to pypi.python.org
]
__desc__ = '''Configuration module intended to work as a namespace holder for configuration values.'''
__license__ = 'Apache Software License 2.0'
__package_exclude__ = ['tests']
__package_name__ = 'triconf'
__requires__ = [
    'argparse>=1.1',
    'configobj>=5.0.6'
    ]
__scripts__ = []
__team__ = 'autoeng'
__url__ = 'http://github.op.dc.openx.org/%s/%s' % ('autoeng', 'openx_python_triconf')
__version__ = '1.0.1'
