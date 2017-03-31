======================
 Triconf
======================

Configuration module intended to deal with config files, config
command line parameters, and parameters set within a module via an
`initialize()` function.

Conf precidents: conf.ini < initialize kargs < cli (argparse) args

=============
 Quick Usage
=============

::

   import triconf
   CONFIGS = triconf.initialize('my_module', conf_file_names=['conf1.ini', 'conf2.ini'],
                                 override_param1=1, override_param2=2)
   parser = triconf.ArgumentParser(CONFIGS)
   parser.add_argument('argument')
   CONFIGS(parser.parse_args())

   print CONFIGS.argument
   print CONFIGS.file_param1.sub_param_1

====================
 triconf.initialize
====================

Takes a namespace name (whatever your module name is) and an optional
argument 'conf_file_names' which defaults to conf.ini, that allows you
to specify multiple config files that will be parsed and added to the
config namespace. Any duplicated values between the conf files will be
resolved by simply last conf wins, with the right most config file
passed in overwriting any duplicate metrics from the previous conf
file.

=======================
 Conf Namespace Object
=======================

The Conf Namespace Object is heavily based on the
ArgumentParser.Namespace object, but also has __iter__ implemented in
order to iterate over attributes in the conf namespace object.

========================
 triconf.ArgumentParser
========================

ArgumentParser.__init__ call has been overridden such that parameters
picked up from any conf file can also be overwritten via commandline
parameters. The config files can also be overridden with
--conf_file_names on the command line allowing different config files
to be loaded other than what was specified in the code.
