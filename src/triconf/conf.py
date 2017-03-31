import argparse
from conf_namespace import Namespace

class ConfException(Exception):
    def __init__(self, msg=''):
        super(ConfException, self).__init__(msg)

def initialize(namespace_name, **kargs):
    '''Initializer for configuration data for the given
    namespace_name. Also takes keyword conf_file_names which defaults
    to conf.ini to specify the configuration files. Note that
    conf_file_names can take a list of conf filenames as well, with
    the last filename in the list taking precedents over the other
    files.

    '''
    conf_file_names = kargs.pop('conf_file_names', 'conf.ini')
    namespace = Namespace()
    try:
        namespace._render_conf_files(conf_file_names)
    except IOError:
        from pipes import quote
        file_d = open(quote(conf_file_names), 'a')
        file_d.close()
        namespace._render_conf_files(conf_file_names)
    namespace(kargs)
    return namespace

class ArgumentParser(argparse.ArgumentParser):
    '''Overloads argparse.ArgumentParser to automatically add the
    parameters gathered from the given config namespace as turning on
    ArgumentDefaultsHelpFormatter. Hiding the help output of the conf
    file parameters can be achieved by passing in
    suppress_conf_file_help = True

    '''
    def __init__(self, namespace, *args, **kargs):
        suppress_conf_file_help = kargs.pop('suppress_conf_file_help', False)
        super(ArgumentParser, self).__init__(*args, **kargs)
        self.formatter_class = kargs['formatter_class'] if kargs.has_key('formatter_class') \
                               else argparse.ArgumentDefaultsHelpFormatter
        # default_help_char is to work around an issue in argparse.
        default_help_char = ' ' if self.formatter_class == argparse.ArgumentDefaultsHelpFormatter else ''
        conf_file_help \
            = arparse.SUPPRESS if suppress_conf_file_help else 'Load conf file along with/instead of %s' \
            % ','.join([x.filename for x in namespace.__rendered__])
        self.add_argument('--conf_file_names', nargs='*', help=conf_file_help)
        for rendered in [x.rendering for x in namespace.__rendered__]:
            for conf_key in rendered.keys():
                if hasattr(rendered[conf_key], 'keys'):
                    # No ability to change dict objects as we don't
                    # render any json that would be put on the cli.
                    continue
                if suppress_conf_file_help:
                    help_string = argparse.SUPPRESS
                else:
                    # Need at least a space in help text in order for default
                    # to display in help if no help text/comments given.
                    help_string = rendered.inline_comments.get(conf_key, default_help_char)
                    help_string = help_string.strip('#') if help_string else default_help_char
                param_kargs = {'default': rendered.get(conf_key, ''), 'help': help_string}
                if hasattr(rendered[conf_key], 'append'):
                    param_kargs['nargs'] = '+'
                self.add_argument('--%s' % conf_key, **param_kargs)

