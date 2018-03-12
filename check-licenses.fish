#!/usr/bin/env bash

# Run it like:
# ./check-licenses.sh invenio-packagename

set PACKAGE $argv[1]
if test -z "$PACKAGE"
    echo "No package specified!"
    exit
end

# Check if inside virtualenv
set IN_VENV (python -c 'import sys; print ("1" if hasattr(sys, "real_prefix") else "0")')

# Create the virtualenv and install the package
if [ $IN_VENV = "0" ]
    echo "Creating the virtualenv"
    mkvirtualenv "pip-freeze-test-$PACKAGE"
    echo "Cloning git repository"
    git clone "https://github.com/inveniosoftware/$PACKAGE"
    pip install -e $PACKAGE"[all]"
end

python ./pip-freeze-check.py

# Only delete the virtualenv if we just created one
if [ $IN_VENV = "0" ]
    echo "Deleting the virtualenv"
    deactivate
    rmvirtualenv "pip-freeze-test-$PACKAGE"
end
