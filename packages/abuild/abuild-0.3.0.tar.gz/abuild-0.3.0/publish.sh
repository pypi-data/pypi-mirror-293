#!/bin/bash

set -xe

function cleanup() {
  git reset --hard HEAD~1
  git tag -d ${VERSION}
}


VERSION=$(semv)
PYVERSION="$(echo $VERSION | sed s/v//)"

SOURCEDIST=abuild-${PYVERSION}.tar.gz
BINDIST=abuild-${PYVERSION}-py3-none-any.whl

# Make sure the examples in the readme work
cram README.md

# Update README
echo "### ${VERSION}" >> README.md
echo "$(semv --changelog)" >> README.md

git add README.md
git commit -m "New Version"
git tag $VERSION

# If wthe release doesn't work somehow, we want to revert the automatic commit
trap cleanup ERR

python -m build

twine check dist/$SOURCEDIST dist/$BINDIST
twine upload --verbose dist/$SOURCEDIST dist/$BINDIST

# If release was successful, push the corresponding data
git push
