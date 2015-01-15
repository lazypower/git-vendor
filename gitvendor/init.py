from helpers import repository_sanity, is_path_sane
import logging
from jinja2 import Template
import os

log = logging.getLogger('git-vendor.init')
base_omissions = ['.git', '.gitignore', '.gitmodules', 'revision']


def render_template(directory):
    template_path = "{}/templates/vendor-rc".format(os.path.abspath(__file__))
    with open(template_path, 'r') as f:
        raw = f.read()
    template = Template(raw)
    print template.render(omit=base_omissions)


def main(args, debug):
    path = is_path_sane(args.directory)
    dirty = repository_sanity(args.directory)

    if path or dirty:
        return

    render_template(args.directory)
