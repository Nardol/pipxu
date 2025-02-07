# Author: Mark Blakeney, Feb 2024.
'''
Install extra packages into an application.

Note the same --index-url is used as/if specified in the original install.
'''
from __future__ import annotations

from argparse import ArgumentParser, Namespace
from typing import Optional

from .. import utils

def init(parser: ArgumentParser) -> None:
    'Called to add command arguments to parser at init'
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='give more output')
    parser.add_argument('package',
                        help='installed application name')
    parser.add_argument('extras', nargs='+',
                        help='extra package name[s] to inject/install')

def main(args: Namespace) -> Optional[str]:
    'Called to action this command'
    pkgname, vdir = utils.get_package_from_arg(args.package, args)
    if not vdir:
        return f'Application {pkgname} is not installed.'

    data = utils.get_json(vdir, args) or {}
    url = data.get('url')
    pip_args = utils.make_args((args.verbose, '-v'), (url, f'-i "{url}"'))
    extras = ' '.join(f'"{a}"' for a in args.extras)
    if not utils.piprun(vdir, f'install{pip_args} --compile {extras}', args):
        return f'Error: failed to install "{extras}" to {pkgname}'

    return utils.add_or_remove_pkg(vdir, pkgname, args.extras, args,
                                   data=data, add=True)
