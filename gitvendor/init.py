from helpers import is_repository_clean, is_path_sane
from helpers import is_repository_initialized
import logging
from jinja2 import Template
import os

log = logging.getLogger('git-vendor.init')
base_omissions = ['.git', '.gitignore', '.gitmodules', 'revision']


def render_template(directory):
    filepath = os.path.dirname(os.path.abspath(__file__))
    template_path = "{}/template/vendor-rc".format(filepath)
    with open(template_path, 'r') as f:
        raw = f.read()
    template = Template(raw)
    content = template.render(omit=base_omissions)
    cfgpath = os.path.join(os.path.realpath(directory), '.vendor-rc')
    with open("{}".format(cfgpath), 'w+') as f:
        f.write(content)
    log.info("Initialized repository {}. You can modify the omitted files"
             " by editing {}.vendor-rc".format(directory, directory))


def main(args, debug):
    if not args.repo:
        args.repo = '.'
    path = is_path_sane(args.repo)
    dirty = is_repository_clean(args.repo, args.force)
    initialized = is_repository_initialized(args.repo)

    if not path and not dirty:
        return

    if initialized:
        log.warn('Repository: {} already initialized.'
                 ' Doing nothing'.format(args.repo))
        return

    render_template(args.repo)
