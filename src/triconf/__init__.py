'''Configuration module intended to work as a namespace holder for
what would normally be a modules global vars. Provides helper
functions for pulling in variables from another namespace (such as an
argparse namespace), as well as provides an overloaded
argparse.ArgumentParser that provides the ability to modify via the
cli options passed in via a conf file.

Conf precidents: conf.ini->initialize kargs->cli (argparse) args

'''

from conf import ConfException, initialize, ArgumentParser

__all__ = ['ConfException', 'initialize', 'ArgumentParser']
