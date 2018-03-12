# Script that checks the license of the dependencies of a package
# How to use me:
# Create a virtualenv (or find a way to make this script create one)
# python pip-freeze-check.py

from subprocess import call

import pkg_resources


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
    check()
