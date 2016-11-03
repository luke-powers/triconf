'''Configuration namespace very similar to argument_parser.Namespace

configurations are referenced as:

param.param.param

If represented as a dict it would be:
param['param']['param']['param']

A dict representation of the configuration namespace can be obtained
from a Namespace object with:
namespace.__dict__()

'''

from collections import namedtuple
import configobj

RENDERED_CONF_FILES = namedtuple('conf_files', 'filename rendering')

class Namespace(object):
    '''Conf namespace class, similar to argparse.Namespace class

    '''

    __hash__ = None

    def __init__(self, **kwargs):
        self.__rendered__ = []
        for name in kwargs:
            setattr(self, name, kwargs[name])

    def __contains__(self, key):
        return key in self.__dict__

    def __eq__(self, other):
        return vars(self) == vars(other)

    def __ne__(self, other):
        return not (self == other)

    def __repr__(self):
        type_name = type(self).__name__
        arg_strings = []
        for name, value in self._get_items():
            arg_strings.append('%s=%r' % (name, value))
        return '%s(%s)' % (type_name, ', '.join(arg_strings))

    def _get_items(self):
        '''Return a tuple list of all the attribute/values on the namespace.

        '''
        return sorted([x for x in self.__dict__.items() if not x[0].startswith('__')])

    def _render_conf_files(self, conf_file_names):
        if not hasattr(conf_file_names, 'append'):
            open(conf_file_names)
            conf_rendered = configobj.ConfigObj(conf_file_names)
            self(conf_rendered)
            self.__rendered__.append(RENDERED_CONF_FILES(conf_file_names, conf_rendered))
        else:
            for filename in conf_file_names:
                open(filename)
                conf_rendered = configobj.ConfigObj(filename)
                self(conf_rendered)
                self.__rendered__.append(RENDERED_CONF_FILES(filename, conf_rendered))

    def __call__(self, ns_obj, subspace_name=None):
        '''Turn object into a functor which if called, updates it's values
        with the object provided.

        '''
        if subspace_name and not ns_obj.has_key(subspace_name):
            ns_obj = {subspace_name: ns_obj}
        if not hasattr(ns_obj, 'items'):
            if hasattr(ns_obj, '__dict__'):
                ns_obj = ns_obj.__dict__
            else:
                raise ConfException('Unable to update configurations with given object: %s.' % ns_obj)
        for key, value in ns_obj.iteritems():
            if not key.startswith('__'):
                if hasattr(value, 'items') or hasattr(value, '__dict__'):
                    ns = Namespace()
                    ns(value)
                    self.__dict__[key] = ns
                else:
                    self.__dict__.update({key: value})
        # If we've been given new conf_file_names, load the conf
        # file in conf_File_names.
        if ns_obj.get('conf_file_names', False):
            self._render_conf_files(ns_obj['conf_file_names'])

    def __iter__(self):
        '''Make namespace iterable with generator.

        '''
        keys = self.__names__()
        i = 0
        while i < len(keys):
            yield self.__dict__[keys[i]]
            i+=1

    def __names__(self):
        '''Return the names of the attributes of the namespace.

        '''
        return sorted([x for x in self.__dict__.keys() if not x.startswith('__')])

