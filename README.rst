======================
 Triconf
======================

Conf precidents: cli args (argparse) > conf.ini (configObj) > init args / function args

Subprocessors need map to subsections in config file and vice versa such that::

   setting1 = value1
   [subsection1]
     setting1 = value1

nests equally with::

   parser.add_argument('setting1', default=config.setting1)
   subparser = parser.add_subparsers(dest='subsection1') # should be dest='subsection1' by default
   parser2 = subsection1.add_parser('name_of_command_to_collect_for_subsection1')
   parser2.add_argument('setting1', default=config.subsection1.setting1)
