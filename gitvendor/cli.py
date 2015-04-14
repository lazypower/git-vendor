import argparse
import importlib
import logging
import sys


def global_args(parser):
    parser.add_argument('--debug', action='store_true',
                        help='display debug output')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='squash all output')


def basic_args(parser):
    parser.add_argument('-r', '--repo', help='Repository to vendor')


def setup_parser():
    p = argparse.ArgumentParser(prog='git-vendor',
                                description='Vendor git repositories easily')
    sp = p.add_subparsers(dest='action', metavar='actions')

    init = sp.add_parser('init', help='Create sync configuration')
    sync = sp.add_parser('sync', help='Vendor code')
    sp.add_parser('version', help='print version')

    # add subcommand options
    global_args(init)
    global_args(sync)
    basic_args(init)
    basic_args(sync)
    sync.add_argument('-t', '--tag', help='Tag to vendor')
    sync.add_argument('-d', '--directory',
                      default='.', help='Output Directory')
    sync.add_argument('--allow-dirty', action='store_true',
                      help='Allow operations on a dirty repository')

    return p


def setup_logging(debug=None):
    logger = logging.getLogger('git-vendor')
    logger.setLevel(logging.INFO)
    if debug:
        logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    if debug:
        f = '%(asctime)s %(levelname)s %(name)s: %(message)s'
    else:
        f = '%(levelname)s: %(message)s'

    formatter = logging.Formatter(f)
    ch.setFormatter(formatter)

    if debug is None:
        ch = logging.NullHandler()

    logger.addHandler(ch)
    return logger


def main(args=None):
    parser = setup_parser()
    known, unknown = parser.parse_known_args(args)
    exit = 0
    if known.action == 'version':
        import pkg_resources
        print pkg_resources.require('git-vendor')[0].version
        sys.exit(0)

    log = setup_logging(known.debug)

    try:
        action = importlib.import_module("..%s" % known.action,
                                         'gitvendor.%s' % known.action)
        exit = action.main(known, unknown)
    except Exception as e:
        if known.debug:
            log.exception(e.message)
            sys.exit(exit)
        else:
            print(e)
            log.critical(e.message)
            sys.exit(exit)

if __name__ == "__main__":
    main()
