# Script that checks the license of the dependencies of a package
# How to use me:
# Create a virtualenv (or find a way to make this script create one)
# python pip-freeeze-check.py invenio-packagename

import sys
import os
from subprocess import call

import pkg_resources


def install(package_name, create_virtualenv=False):
    if not (os.path.isdir("./" + package_name)):
        print("Cloning git repository")
        call(["git", "clone", "https://github.com/inveniosoftware/" + package_name])
    # Make sure we run the script in a virtualenv
    if not hasattr(sys, 'real_prefix'):
        raise Exception("Not working in a virtualenv, exiting!")
    call(["pip", "install", "-e", package_name + "[all]"])


def _get_pkg_license(pkg):
    # https://stackoverflow.com/questions/19086030/
    license = None

    try:
        lines = pkg.get_metadata_lines('METADATA')
    except:
        lines = pkg.get_metadata_lines('PKG-INFO')

    for line in lines:
        if line.startswith('License:'):
            license = line[9:]
    if not license or license == 'UNKNOWN':
        try:
            lines = pkg.get_metadata_lines('METADATA')
        except:
            lines = pkg.get_metadata_lines('PKG-INFO')
        # Let's try to read the license from Classifiers
        for line in lines:
            if line.startswith('Classifier: License'):
                license = line.split('::')[-1].strip()
    if license:
        return license
    else:
        return '(License not found)'

def check():
    licenses = []
    for pkg in sorted(pkg_resources.working_set, key=lambda x: str(x).lower()):
        licenses.append([str(pkg), _get_pkg_license(pkg)])
    # Sort by license name
    licenses.sort(key=lambda x: x[1])
    for license in licenses:
        if 'gpl' in license[1].lower():
            print('!!!!!!!!!!!!! GPL license detected!!!!!!!!!!!')
        print("{0}\t --> {1}".format(*license))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("You need to provide packages name as an argument")
    package_name = str(sys.argv[1])
    install(package_name)
    check()
