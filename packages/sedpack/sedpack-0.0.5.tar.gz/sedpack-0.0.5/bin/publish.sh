#!/bin/bash -e
# Uploads the latest version of the library to Pypi.
# Make sure that the version number has been incremented.

# Install requirements.
if ! which pipx; then
  echo "Missing pipx, attempting install"
  sudo apt-get install pipx
  if !which pipx; then
    exit 1;
  fi
fi

# Go to the root of the repository.
cd $(dirname $(dirname "$0"))

# Delete old python wheels.
rm dist/*
# Build the python wheel.
pipx run build


# Upload to Pypi
pipx run twine upload dist/*
