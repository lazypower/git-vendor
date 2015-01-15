import argparse
import importlib
import logging
import sys


def basic_args(parser):
    parser.add_argument('-d', '--directory', help='Directory for vendoring')
    parser.add_argument('-t', '--tag', help='Tag to vendor')
    parser.add_argument('--debug', action='store_true',
                        help='display debug output')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='squash all output')


def setup_parser():
    p = argparse.ArgumentParser(prog='git-vendor',
                                description='Vendor git repositories easily')
    sp = p.add_subparsers(dest='action', metavar='actions')

    sp.add_parser('init', help='Create sync configuration')
    sync = sp.add_parser('sync', help='Vendor code')
    basic_args(sync)
    sp.add_parser('version', help='print version')
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
        f = '%(levelname)s %(name)s: %(message)s'

    formatter = logging.Formatter(f)
    ch.setFormatter(formatter)

    if debug is None:
        ch = logging.NullHandler()

    logger.addHandler(ch)
    return logger


def main(args=None):
    parser = setup_parser()
    known, unknown = parser.parse_known_args(args)

    if known.action == 'version':
        import pkg_resources
        print pkg_resources.require('git-vendor')[0].version
        sys.exit(0)

    log = setup_logging(debug=known.debug)

    try:
        action = importlib.import_module("..%s" % known.action,
                                         'gitvendor.%s' % known.action)
        exit = action.main(known, unknown)
    except Exception as e:
        if known.debug:
            log.exception(e.message)
        else:
            log.critical(e.message)
            exit = 1

    sys.exit(exit)

if __name__ == "__main__":
    main()
