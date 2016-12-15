"""
Make a new project.
"""


import os
import os.path
from argparse import ArgumentParser


parser = ArgumentParser(description=__doc__)

parser.add_argument('name', help='The name of the new project')
parser.add_argument('-s', '--summary', help='A short description of the new project')
parser.add_argument('--skel-dir', default='skel', help='Template directory')

args = parser.parse_args()

if not args.summary:
    args.summary = input('Summary: ')

if os.path.isdir(args.name):
    print('Using output directory %s.' % args.name)
else:
    try:
        os.makedirs(args.name)
        print('Created output directory %s.' % args.name)
    except OSError as e:
        print(e)
        if not os.path.isdir(args.name):
            print('Directory not created. Quitting.')
            raise SystemExit


for dirpath, dirnames, filenames in os.walk(args.skel_dir):
    dirpath = dirpath[len(args.skel_dir) + 1:]
    output_dirpath = os.path.join(args.name, dirpath)
    if os.path.isdir(output_dirpath):
        print('Entering directory %s.' % output_dirpath)
    else:
        try:
            os.makedirs(output_dirpath)
            print('Created directory %s.' % output_dirpath)
        except OSError as e:
            print(e)
            if not os.path.isdir(output_dirpath):
                print('No such directory: %s. Quitting.' % dirpath)
                raise SystemExit
    for filename in filenames:
        with open(os.path.join(args.skel_dir, dirpath, filename), 'r') as original, open(os.path.join(output_dirpath, filename), 'w') as target:
            target.write(
                original.read().format(
                    name=args.name,
                    summary=args.summary
                )
            )
            print('Wrote file %s.' % target.name)

print('Done.')
