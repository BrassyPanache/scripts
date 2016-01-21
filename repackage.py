import fileinput
import os
import argparse
import re
import shutil

parser = argparse.ArgumentParser(description='Refactor a package.')
parser.add_argument('--old', dest='old', help='the package to refactor', required=True)
parser.add_argument('--new', dest='new', help='the new package', required=True)
parser.add_argument('-d', dest='directory', default=".", help='the directory (default: .)')

arguments = parser.parse_args()
old = re.split('\.', arguments.old)
new = re.split('\.', arguments.new)

print('Moving package {0} to {1}'.format('.'.join(old), '.'.join(new)))

flagged = []
walk = []

for current, children, files in os.walk(arguments.directory):
    split = current.split(os.path.sep)

    if len(split) >= len(old):
        if split[len(old) * -1:] == old:
            flagged.append(split[:len(old) * -1])

    for file in files:
        refactor = os.path.join(current, file)

        for line in fileinput.input([refactor], inplace=True):
            print(line.replace(arguments.old, arguments.new), end='')

for flag in flagged:
    print('Found {0}'.format(os.path.sep.join(flag)))

    if len(new) > 0 and len(old) > 0:
        create = os.path.sep.join(flag + new[:-1])
        destination = os.path.sep.join(flag + new)
        source = os.path.sep.join(flag + old)
        delete = os.path.sep.join(flag + old[:-1])

        print('Moving {0} to {1}'.format(source, destination))

        if not os.path.exists(create):
            os.makedirs(create)

        shutil.move(source, destination)

        if os.path.exists(delete):
            shutil.rmtree(delete)
