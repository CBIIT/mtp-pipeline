import os, sys, errno
import csv
import configargparse
import logging

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

"""
This will create a singleton argument parser that is appropriately configured
with the various command line, environment, and ini/yaml file options.

"""


def setup_parser():
    p = configargparse.get_argument_parser(config_file_parser_class=configargparse.YAMLConfigFileParser)
    p.description = 'PPDC data pipleline'

    # argument to read config file
    p.add('-c', '--config', is_config_file=True,
        env_var="PIS_CONFIG", help='path to config file (YAML)')
    return p


def get_args():
    p = configargparse.get_argument_parser()
    #dont use parse_args because that will error
    #if there are extra arguments e.g. for plugins
    args = p.parse_known_args()[0]

    #output all configuration values, useful for debugging
    #p.print_values()

    return args


def get_input_file(input_filename, default_name_file):
    if input_filename is None:
        return default_name_file

    # check the file exists
    if not os.path.isfile(input_filename):
        raise IOError(
            errno.ENOENT, os.strerror(errno.ENOENT), ' The input file does not exists: %s' % input_filename)
    else:
        return input_filename

def setBasicConfigLog():
    logFilename = os.path.join(BASE_DIR, 'log/output.log')
    logging.basicConfig(level=logging.INFO, filename=logFilename, format= '%(name)-12s: %(levelname)-8s %(message)s',
     datefmt='%H:%M:%S')

    # set up logging to console
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

    logger = logging.getLogger(__name__)
    return logger
