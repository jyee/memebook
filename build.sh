#!/bin/bash
# $1 is the version
# $2 is the prefix

if [ "$#" -ne 2 ]; then
  echo "Incorrect parameters"
  echo "Usage: build.sh <version> <prefix>"
  exit 1
fi

VERSION=$1
PREFIX=$2
SCRIPTDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

for DIR in "$SCRIPTDIR"/*; do
  if [ -d "$DIR" ] && [ -f "$DIR/Dockerfile" ]; then
    IMAGE=${DIR/$SCRIPTDIR\//}
    pushd $DIR
      #docker build -t "$PREFIX/$IMAGE:$VERSION" -t "$PREFIX/$IMAGE:latest" .
      docker build -t "$PREFIX/$IMAGE:$VERSION" .
    popd
  fi
done
